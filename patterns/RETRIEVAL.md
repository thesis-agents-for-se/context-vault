# Indexing this catalog in a vector database

This file explains how to load the catalog into a vector store, and when a
vector store is not the right tool. The format of the files was chosen with this
use in mind.

## Short answer

Yes, it is easy. The whole catalog is 35 small Markdown files with fixed
headings and structured frontmatter, which is close to the ideal input for a
retrieval pipeline. A first working version is a few dozen lines of code.

The more important point: at this size, vector search is not the only thing you
need, and it should not be the first thing the agent uses.

## Is a vector database even needed here?

The catalog is about 17,000 words in total. `INDEX.md` alone is around 1,500
tokens and lists every entry with a one-line summary.

So there are two workable designs:

**Design A, index in context.** Put `INDEX.md` in the agent prompt. The agent
picks the ids it wants and reads those files from disk. No embeddings, no
database, and the selection is explainable and repeatable.

**Design B, vector search.** Embed the chunks and retrieve by similarity from
what the agent observed in the code.

Design A is enough while the catalog is this size, and it is the better baseline
for a thesis, because you can compare against it. Design B earns its place when
the catalog grows past a few hundred entries, when you add project specific
notes and past audit findings, or when queries are free text observations rather
than names.

The recommended setup is both: vector search proposes candidates, and the agent
then loads the full file by id. Similarity picks the candidate; the file, not the
retrieved fragment, is what the agent reasons over.

## Chunking

Do not split by a fixed number of characters. The files already have meaning
based boundaries. Use two levels:

**Level 1, one chunk per file.** Each file is 400 to 700 words, which is a good
chunk size, and it is self-contained. This is the unit the agent reads.

**Level 2, one chunk per `signals` line.** This is the part that matters for an
agent looking at code. Each signal is a short, concrete statement such as "A
remote call sits inside a loop" or "Two services run migrations against the same
schema". Embedded on its own, it matches closely what a code analysis step would
report. Every signal chunk carries the parent `id` in its metadata, so a hit
resolves to the full file.

Optionally add a level for the `## How to spot it` and `## Solutions` sections,
prefixed with the antipattern name so the chunk still makes sense alone. The
schema requires that each section repeats the name for exactly this reason.

## What to store

For every chunk, store the text plus this metadata:

```json
{
  "id": "shared-database",
  "name": "Shared Database",
  "kind": "antipattern",
  "category": "persistence",
  "severity": "high",
  "chunk_type": "document | signal | section",
  "detects_on": ["config", "code", "schema"],
  "path": "antipatterns/persistence/shared-database.md"
}
```

Metadata is what makes retrieval precise. If the agent is currently reading
database configuration, filter on `category = persistence` or
`detects_on contains config` before the similarity search. That removes most
false matches at no cost.

Prepend the name and aliases to the embedded text of each chunk. It helps when a
query uses a different term for the same idea, for example "shared persistence"
for `shared-database`.

## Search

Use hybrid search: dense vectors plus BM25 keyword matching, combined with
reciprocal rank fusion. Pure dense search is weak on exact technical terms such
as `@Transactional`, `XA`, or `traceparent`, which are the tokens that carry the
most signal here. Most stores support hybrid search directly: Qdrant, Weaviate,
Milvus, and pgvector with a tsvector column.

For the embedding model, any current general purpose model is fine at this size.
The catalog is English and the vocabulary is standard, so the model is not the
bottleneck. If the agent will ever ask in Spanish, use a multilingual model, or
translate the query before searching, since the corpus is English.

Retrieve 5 candidates, keep the top 3 after filtering, and load those full files.
More than that wastes the context you are trying to protect.

## Suggested agent flow

This is the part that actually controls context growth:

1. A code analysis step produces observations as short factual statements, for
   example "service `billing` and service `orders` use the same JDBC URL".
2. Each observation is used as a query, filtered by `detects_on`.
3. Retrieval returns candidate ids from signal chunks.
4. The agent loads at most three full antipattern files by id.
5. It confirms or rejects each candidate against the `## How to spot it`
   checklist, which is the step that reduces hallucination, because the claim
   has to match named evidence.
6. Only for confirmed findings does it load the pattern files listed in
   `solutions`.

Two properties of this flow matter for your context limit. Retrieval is driven
by small observations instead of by the whole repository, and pattern files are
loaded only after a finding is confirmed, so the expensive text never enters the
prompt for antipatterns that were rejected.

## Keeping the index in sync

Run `python3 tools/build_index.py --check` in CI. It validates the schema and
every cross reference, so a broken `solutions` id cannot reach the index.

Store a content hash per file and re-embed only the files whose hash changed.
Embedding the whole catalog takes seconds today, but the hash also gives you a
version to record with each agent run, which you will want when reporting
results.

## Pitfalls

- **Retrieval is not evidence.** A similarity hit only says a file looks
  related. The agent must still find the signal in the code before reporting a
  finding. Without that rule, a vector store makes hallucination faster.
- **Antipatterns overlap.** `shared-database`, `database-as-integration-point`,
  and `distributed-monolith` describe related situations, so queries about one
  will return the others. That is correct behaviour, and it is why `related` is
  in the frontmatter. Report the root cause and mention the rest.
- **Do not embed source code into the same index.** Keep the knowledge base and
  the repository index separate. They answer different questions and mixing them
  makes both worse.
- **Measure it.** Build a small set of query and expected id pairs, at least
  five per antipattern, and track recall at 3 and precision at 3. Without that
  set you cannot tell whether a change to chunking helped.

## Minimal example

```python
# pip install chromadb pyyaml
import pathlib, re, yaml, chromadb

client = chromadb.PersistentClient(path=".chroma")
col = client.get_or_create_collection("antipatterns")

for path in pathlib.Path(".").rglob("antipatterns/**/*.md"):
    raw, body = re.match(r"^---\n(.*?)\n---\n(.*)$", path.read_text(), re.S).groups()
    meta = yaml.safe_load(raw)
    base = {"id": meta["id"], "name": meta["name"], "kind": "antipattern",
            "category": meta["category"], "severity": meta["severity"],
            "path": str(path)}

    # level 1: the whole document
    col.add(ids=[meta["id"]],
            documents=["%s. %s" % (meta["name"], body)],
            metadatas=[dict(base, chunk_type="document")])

    # level 2: one chunk per signal
    for i, signal in enumerate(meta["signals"]):
        col.add(ids=["%s::signal::%d" % (meta["id"], i)],
                documents=["%s: %s" % (meta["name"], signal)],
                metadatas=[dict(base, chunk_type="signal")])

hits = col.query(query_texts=["two services connect to the same database"],
                 where={"category": "persistence"}, n_results=5)
print({m["id"] for m in hits["metadatas"][0]})
```

Chroma is used here because it is the shortest example. For the final system
prefer Qdrant or pgvector, because both support hybrid search and metadata
filters well, and pgvector avoids running one more service if you already have
PostgreSQL.
