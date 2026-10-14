# Entry format

Every antipattern file is a Markdown file with YAML frontmatter. The frontmatter
is metadata for search and filtering. The body is the text that gets embedded.

## Frontmatter fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes | kebab-case, unique, same as the file name |
| `name` | string | yes | human name |
| `category` | enum | yes | `boundaries`, `communication`, `persistence`, `operations` |
| `aliases` | list | no | other names used in the literature |
| `severity` | enum | yes | `low`, `medium`, `high` |
| `detects_on` | list | yes | what an agent must inspect: `code`, `config`, `schema`, `traces`, `repo-layout`, `docs` |
| `signals` | list | yes | short, checkable statements. One line each. |
| `related` | list | no | ids of other antipatterns |
| `solutions` | list | yes | ids of files under `patterns/` |
| `sources` | list | yes | URLs or book titles |

## Body sections

Fixed order, fixed headings. Do not add or rename headings.

```markdown
## Summary
## Why it hurts
## How to spot it
## Solutions
### 1. <pattern name>
### 2. <pattern name>
### 3. <pattern name>
## Related
## Sources
```

Each numbered solution has three lines:

- **Do:** the change.
- **Fits when:** the condition where it is the right call.
- **Cost:** what you give up.

## Writing rules

- Plain English. Short sentences. No filler.
- Every section must make sense on its own, without the rest of the file. A
  chunker may split the file at the headings.
- Repeat the antipattern name inside each section. Do not write "this problem"
  or "it" at the start of a section, because the chunk may be read alone.
- Keep each file under about 700 words.
- Under **How to spot it**, write evidence, not theory. "Two services share a
  connection string" is useful. "Coupling is high" is not.

## Pattern files

Files under `patterns/` use a smaller frontmatter: `id`, `name`, `type`
(`pattern`), `solves` (list of antipattern ids), `sources`. Body sections:

```markdown
## Summary
## How it works
## When to use it
## Cost and risks
## Sources
```
