# Microservices Antipattern Knowledge Base

A catalog of microservice antipatterns, with a focus on service communication,
data persistence, and how services talk to databases. Each antipattern lives in
its own file so an agent can load only what it needs.

The goal is to keep the LLM context small. An agent should never read the whole
catalog. It should find the two or three files that match what it sees in the
code, and read only those.

## In this repository

The catalog lives inside the Obsidian vault as its shared shelf (`knowledge/patterns/`).
Agents reach it through the librarian, read-only: `search_knowledge` with
`brain: "patterns"` and `read_note` on `patterns/INDEX.md` or on an entry. Notes about a
monolith link to an entry by its id, for example `[[shared-database]]`. See
[docs/librarian.md](../../docs/librarian.md).

## Layout

```
antipatterns/
  boundaries/      service size, ownership, and where the lines are drawn
  communication/   how services call each other
  persistence/     data ownership, databases, transactions
  operations/      deployment, shared code, monitoring
patterns/          the fixes, one file per pattern
SCHEMA.md          the file format every entry follows
INDEX.md           flat list of every entry with its one-line summary (generated)
RETRIEVAL.md       how to index this catalog in a vector database
tools/             index builder and consistency checker
```

Rebuild the index and validate every cross reference:

```
python3 tools/build_index.py          # rebuild INDEX.md
python3 tools/build_index.py --check  # validate only, for CI
```

## How to use it

1. Read `INDEX.md` (small, cheap) to pick candidates.
2. Read the matching antipattern file. It tells you what to look for in a repo.
3. Read the pattern files listed under `solutions` only when you need to write
   the recommendation.

## Entry format

Every antipattern file has the same sections in the same order:

- **Summary** - what it is, in three sentences or less.
- **Why it hurts** - the real cost.
- **How to spot it** - concrete evidence found in code, config, or schemas.
- **Solutions** - up to three, each with what to do, when it fits, and the cost.
- **Related** - other entries that often show up together.
- **Sources** - where this comes from.

See `SCHEMA.md` for the full field list.

## Counts

- 20 antipatterns across 4 categories
- 15 corrective patterns
- every file is under 700 words, so one file fits easily in a prompt

## Scope note

This catalog targets teams moving a monolith to microservices. It leans toward
data and communication problems, because those are the ones that are hardest to
undo once the system is live.
