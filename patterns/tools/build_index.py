#!/usr/bin/env python3
"""Build INDEX.md and check that the catalog is consistent.

Run from the repository root:

    python3 tools/build_index.py          # rebuild INDEX.md
    python3 tools/build_index.py --check  # only validate, do not write

Checks:
  - every required frontmatter field is present
  - id matches the file name
  - every id in `related` points at an existing antipattern
  - every id in `solutions` points at an existing pattern file
  - every id in `solves` points at an existing antipattern
  - the body has the required headings in the required order
"""

import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

AP_FIELDS = ["id", "name", "category", "severity", "detects_on", "signals",
             "solutions", "sources"]
PT_FIELDS = ["id", "name", "type", "solves", "sources"]

AP_HEADINGS = ["## Summary", "## Why it hurts", "## How to spot it",
               "## Solutions", "## Related", "## Sources"]
PT_HEADINGS = ["## Summary", "## How it works", "## When to use it",
               "## Cost and risks", "## Sources"]

CATEGORY_TITLE = {
    "boundaries": "Boundaries and granularity",
    "communication": "Communication between services",
    "persistence": "Data, persistence and databases",
    "operations": "Deployment and operations",
}


def parse(path):
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise SystemExit("%s: missing frontmatter" % path)
    raw, body = m.group(1), m.group(2)

    data, key = {}, None
    for line in raw.split("\n"):
        if line.startswith("  - "):
            data.setdefault(key, []).append(line[4:].strip())
        elif ":" in line:
            key, value = line.split(":", 1)
            key, value = key.strip(), value.strip()
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                data[key] = [v.strip() for v in inner.split(",")] if inner else []
            elif value:
                data[key] = value
            else:
                data[key] = []
    return data, body


def first_sentence(body):
    summary = body.split("## Summary", 1)[1].split("##", 1)[0].strip()
    one_line = " ".join(summary.split())
    return one_line.split(". ")[0].rstrip(".") + "."


def main():
    check_only = "--check" in sys.argv
    errors = []

    antipatterns, patterns = {}, {}

    for path in sorted((ROOT / "antipatterns").rglob("*.md")):
        data, body = parse(path)
        antipatterns[data.get("id")] = (path, data, body)
        for field in AP_FIELDS:
            if not data.get(field):
                errors.append("%s: missing field '%s'" % (path.name, field))
        if data.get("id") != path.stem:
            errors.append("%s: id does not match file name" % path.name)
        if data.get("category") != path.parent.name:
            errors.append("%s: category does not match folder" % path.name)
        found = [h for h in AP_HEADINGS if h in body]
        if found != AP_HEADINGS:
            errors.append("%s: headings wrong or missing: %s" % (path.name, found))

    for path in sorted((ROOT / "patterns").glob("*.md")):
        data, body = parse(path)
        patterns[data.get("id")] = (path, data, body)
        for field in PT_FIELDS:
            if not data.get(field):
                errors.append("%s: missing field '%s'" % (path.name, field))
        if data.get("id") != path.stem:
            errors.append("%s: id does not match file name" % path.name)
        found = [h for h in PT_HEADINGS if h in body]
        if found != PT_HEADINGS:
            errors.append("%s: headings wrong or missing: %s" % (path.name, found))

    for pid, (path, data, _) in antipatterns.items():
        for ref in data.get("related", []):
            if ref not in antipatterns:
                errors.append("%s: related '%s' does not exist" % (path.name, ref))
        for ref in data.get("solutions", []):
            if ref not in patterns:
                errors.append("%s: solution '%s' has no pattern file" % (path.name, ref))

    for pid, (path, data, _) in patterns.items():
        for ref in data.get("solves", []):
            if ref not in antipatterns:
                errors.append("%s: solves '%s' does not exist" % (path.name, ref))

    if errors:
        print("FAILED")
        for e in errors:
            print("  -", e)
        return 1

    print("ok: %d antipatterns, %d patterns, all references resolve"
          % (len(antipatterns), len(patterns)))

    if check_only:
        return 0

    out = ["# Index", "",
           "One line per entry. Read this first, then open only the files you need.",
           "", "## Antipatterns", ""]

    by_category = {}
    for pid, (path, data, body) in antipatterns.items():
        by_category.setdefault(data["category"], []).append((pid, path, data, body))

    for category in ["boundaries", "communication", "persistence", "operations"]:
        if category not in by_category:
            continue
        out.append("### %s" % CATEGORY_TITLE[category])
        out.append("")
        out.append("| id | name | severity | summary |")
        out.append("|---|---|---|---|")
        for pid, path, data, body in sorted(by_category[category]):
            rel = path.relative_to(ROOT)
            out.append("| [`%s`](%s) | %s | %s | %s |"
                       % (pid, rel, data["name"], data["severity"], first_sentence(body)))
        out.append("")

    out += ["## Patterns", "", "| id | name | solves |", "|---|---|---|"]
    for pid, (path, data, body) in sorted(patterns.items()):
        rel = path.relative_to(ROOT)
        out.append("| [`%s`](%s) | %s | %s |"
                   % (pid, rel, data["name"], ", ".join(data["solves"])))
    out.append("")

    (ROOT / "INDEX.md").write_text("\n".join(out))
    print("wrote INDEX.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
