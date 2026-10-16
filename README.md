# Knowledge vault

This folder is an Obsidian vault. It keeps the knowledge of the project under version control.
Notes, templates and the shared Obsidian settings in `.obsidian/` are saved in Git as plain
Markdown and JSON.

## Connect it to app-modernization

This repository is the live vault of
[app-modernization](https://github.com/thesis-agents-for-se/app-modernization). In that
repository, the `knowledge/` folder only holds the seed: the patterns catalog, the templates
and the Obsidian settings. What the agents and the people write lives here. The app does not
clone or push this repository. It reads and writes a folder on disk, and that folder must be
a clone of this repository.

**1. Clone the vault** to an absolute path outside app-modernization:

```bash
git clone <url of this repository> /absolute/path/context-vault
```

**2a. With Docker Compose** (option A of the app-modernization deployment guide), add this
to the `.env` file of app-modernization:

```
VAULT_DIR=/absolute/path/context-vault
HOST_UID=1000        # id -u of the folder's owner
HOST_GID=1000        # id -g
```

Then, from app-modernization, run `docker compose up -d --build --wait`. Compose mounts the
folder as `/data/knowledge` in the orchestrator and in the stages. The vault already has
content, so the `init` service does not seed it and does not change its owner. If the services
cannot write to it, `init` stops and asks you to set `HOST_UID` and `HOST_GID`.

**2b. Without containers** (option B), add this to the same `.env` file. The orchestrator, the
decomposer and the planner all read it:

```
KNOWLEDGE_DIR=/absolute/path/context-vault
```

The path must be absolute, and the same for all three. If it is missing, the decomposer warns
at startup that it would write to `knowledge/` inside the code repository.

**3. Check it.** At startup the decomposer prints `vault: <path>`. A project of the
orchestrator writes to `systems/<slug>/`. The project page shows the slug.

**4. Commit what they write.** The agents' draft notes and the business documents uploaded
through the orchestrator arrive uncommitted. The planner reads the knowledge version from this
Git repository. While there are uncommitted files, it stops at its `knowledge` gate. To go on
with a reproducible version:

```bash
cd /absolute/path/context-vault
git add -A && git commit -m "Notes of run <id>" && git push
```

On a server, do this in the server's clone. Nothing does it for you.

**The catalog does not sync by itself.** If `patterns/` or `templates/` change in the
`knowledge/` folder of app-modernization, copy them here and commit them.

## What to keep in Git

- Keep the notes: systems, use cases, entities, architecture, migrations, decisions, and
  `templates/`.
- Keep the shared vault settings, such as `app.json`, `core-plugins.json` and
  `templates.json`.
- Do not keep `workspace.json`, `workspace-mobile.json` or caches. They are Obsidian's local
  state, and this repository's `.gitignore` leaves them out.
- The facts store and the search index live in `runs/_knowledge/` of app-modernization, not
  here. `runs/` is not in Git there. The Markdown sources stay in this repository.
- Agents do not touch these files directly. Everything they read or write goes through the
  librarian (`librarian/`, see
  [docs/librarian.md](https://github.com/thesis-agents-for-se/app-modernization/blob/main/docs/librarian.md)).

Do not keep LangGraph checkpoints or experiment results here. The workflow state and the
structured facts have their own stores.

## What is in the vault

| Folder | Content | Who writes it |
|---|---|---|
| `systems/<monolith>/` | The knowledge of each monolith, split into four brains | Agents (drafts) and people |
| `patterns/` | Shared catalog of microservice patterns and antipatterns | Only people; agents read it |
| `templates/` | Obsidian note templates | People |

The catalog has its own [README](patterns/README.md), format and validator. A monolith's notes
link to a catalog entry by its name, for example `[[shared-database]]`.

## One system per monolith, split into brains

Each monolith has its own folder, `systems/<monolith>/`. The name is the same one used in
`runs/<monolith>/` in app-modernization. It comes from the code's folder name, in lowercase and
with dashes (`JPetStore 6` → `jpetstore-6`). Inside, the knowledge is split into four brains:

| Brain | Content | Templates |
|---|---|---|
| `business/` | Problem, solution, benefits, stakeholders, requirements, constraints, use cases and business rules. `business/references/` keeps the source documents, each PDF with its `.txt` | `business-overview`, `business-stakeholder`, `business-requirement`, `business-constraint`, `business-use-case` |
| `code/` | What the system looks like today: components, entities and data, data access, dependencies | `code-component`, `code-entity` |
| `architecture/` | Where it is going: service boundaries, decisions, antipatterns found | `architecture-service`, `architecture-decision` |
| `migration/` | How to get there: steps, order, risks, data migration | `migration-step` |

A note belongs to the brain and the system of its folder; templates do not set them. If a note
has `system:` in its frontmatter, that value wins. Agents can only write inside a brain of
their own monolith, and facts from approved notes are only given to that monolith's agents.

The use case agent, the configuration table and the search index read from
`business/references/`.

## Notes the agents write

No note is generated by fixed code. When a decomposer agent finishes its work, it gets one more
turn in its own conversation with a single tool, `write_vault_note`, and writes what it found.
Agents that work in parallel (the ERM generators, the three analysts of the configuration
table) write at the same time; the librarian's write queue puts the writes in order. Notes are
in English, like the catalog and the templates. They are always `status: draft` with
`proposal: true`: they are proposals until a person reviews them.

| Agent | What it writes | Folder |
|---|---|---|
| ERM explorer (`erm-explorer`) | One note per entity and a summary in the run's index | `code/entities/`, `architecture/runs/` |
| Use case explorer (`use-case-explorer`) or business analyst (`business-analyst`) | One note per use case | `business/use-cases/` |
| Cluster advisor (`cluster-advisor`) | The suggested number of services | `architecture/decisions/cluster-count-<run>.md` |
| Configuration analysts and judge (`configuration-analyst-<role>`, `configuration-judge`) | Their priority proposal, the judge's decision and the evidence they cite | `architecture/decisions/configuration-<run>.md` |
| Partition reviewer (`partition-reviewer`) | One note per service and its reading of the partition | `architecture/services/<run>/`, `architecture/decisions/partition-review-<run>.md` |
| Planner (when the plan is approved) | Migration per service and data decisions | `migration/plan-<run>-<service>.md`, `architecture/plan-<run>-data-decisions.md` |

`<run>` is the first eight characters of the run's id. Entities and use cases are system notes,
one per name; everything else is per run.

**One section per agent.** The first write creates the note with its frontmatter. Then each
agent adds its own section, `## <agent> - <stage> - run <run> (unapproved proposal)`, without
deleting what other agents wrote. If an agent writes a level 1 or 2 heading, it becomes level 3
so the structure stays intact. A `reviewed` or `approved` note is never touched.

**Links.** Agents use a short form and the librarian turns it into the full path with an alias:
`[[entity:orders]]` → `[[systems/jpetstore/code/entities/orders|orders]]`. Short forms:
`[[entity:…]]`, `[[use_case:…]]`, `[[service:…]]`, `[[decision:…]]`, `[[run:]]`,
`[[pattern:<id>]]` and `[[antipattern:<id>]]`. A pattern that is not in the catalog stays as
plain text. An entity or service that has no note yet stays as a link: Obsidian shows it as an
empty node until another agent writes it.

**It never blocks.** If the model does not support tools, the vault is not available or the
write fails, the agent still gives its answer. The failure is saved in its evidence
(`vault_notes`) and as a `vault` event. What an agent writes here never counts as grounding
evidence.

**The graph.** `.obsidian/graph.json` gives each kind of note its own color (entities, use
cases, services, run indexes, decisions, migration, patterns and antipatterns), shows the
direction of the links, and hides `business/references/` and `templates/`.

## Separate databases

These files live in app-modernization, not in this repository.

| File | Content | Can be rebuilt |
|---|---|---|
| `workspace.sqlite3` | LangGraph checkpoints, cycle state and operational approvals | No: it is execution state |
| `runs/_knowledge/knowledge-store.sqlite3` | The write queue; approved snapshots of the ERM, use cases and configuration with their full origin; single facts that point to their snapshot (`artifact_id`); note proposals and locks | No: durable store |
| `runs/_knowledge/rag-index/<corpus>.sqlite3` | FTS5, manifest, chunks and dense vectors of one corpus (the vault plus one legacy codebase) | Yes: it is rebuilt from the sources |

There is one index per corpus, next to the store, named by a hash of the vault and legacy
paths. This way a search on another system (or a test) does not rebuild or delete this
system's index. The old `knowledge-index.sqlite3` is only read once to move its locks and
proposals; you can delete it.

At startup, the workflow copies the current approvals from the checkpoint to the knowledge
store. Running this twice is safe. Each artifact keeps, as its origin, the candidates that were
compared, the merge plan and the source commit.

## Reading, search and agent writes

- `search_knowledge` uses SQLite FTS5/BM25 and, if configured, dense embeddings. It always
  adds sparse vector similarity as an extra signal. It returns the citation, path, line range,
  system, artifact type, case, commit, status and confidence, and it can filter by them. By
  default it leaves out `draft` notes. Without credentials or a configured model, it uses
  BM25 plus sparse vectors.
- To turn on dense embeddings (optional), set one of these providers before starting the
  server:

  ```bash
  # In .env or exported. Remote: needs OPENROUTER_API_KEY and sends chunks and queries to the provider.
  RAG_EMBEDDING_PROVIDER=openrouter
  RAG_EMBEDDING_MODEL=<embedding model from the catalog>

  # Local option for the embeddings (not for the agents); needs Ollama running.
  RAG_EMBEDDING_PROVIDER=ollama
  RAG_EMBEDDING_MODEL=<downloaded embedding model>
  ```

  The dense index keeps up to 5,000 vectors per corpus; `RAG_EMBEDDING_MAX_CHUNKS` changes the
  limit. Changing the provider, the model or the sources rebuilds the vectors. If embeddings
  fail, search falls back to BM25 and sparse similarity and tells the agent which mode it used
  and why.
- The index is built from `systems/` (including the documents in
  `systems/<monolith>/business/references/`) and chunks of the legacy code. It leaves out
  `.obsidian`, `templates/`, tests, temporary files, recovery copies and build output.
- The index includes the vault's Markdown notes and the `.java`, `.xml`, `.sql`, `.md` and
  `.txt` files of the legacy code and its documents. Each PDF needs a `.txt` file next to it
  with its text; the indexer does not read PDF files.
- `read_note` returns the SHA-256 it saw. `propose_note_update` saves a proposal in SQLite
  without touching the Markdown; `apply_note_update` puts it in the **write queue**. All writes
  from all agents go through that one queue and are applied one at a time, in order of arrival,
  through a temporary file and `os.replace`. A write based on an old hash gets a conflict and
  writes nothing. Readers see either the full old version or the full new one.
- `append_note_section` adds a section to an existing draft without a hash. Because the queue
  is sequential, the sections of all agents are kept.
- An agent can only create or update Markdown notes under `systems/<monolith>/<brain>/`, with
  `status: draft`. Agents cannot change `reviewed` or `approved` notes, and they cannot approve
  a note. A person reviews a note by editing it, changing its status and committing it to Git.
- The queue lock expires after three minutes if its process dies. Edits made by people in
  Obsidian do not use the queue: avoid editing a note while an agent is updating it. The hash
  check detects an earlier human edit.

Tools available to the agents in the LangGraph tool loops: `search_knowledge`, `read_note`,
`propose_note_update`, `apply_note_update`, `append_note_section`, `write_queue_status` and
`read_approved_facts`. Approved facts come from the workflow's structured snapshot, together
with approved notes that have a valid `facts_json`. Search results are treated as cited
evidence, never as instructions. For physical data access, the code and the DDL of the commit
are the authority.

What these tools return is context: **it does not count as grounding evidence**. The checks
that a column, entity or reference "was read" only accept what the authoritative tools
returned (legacy code, approved model, Engine result). An agent could save a draft and read it
back; if that counted, it could back up columns it made up.

The legacy file list is reused for 60 seconds (it is tied to one commit). The vault is scanned
again on every search, so a new note shows up right away. Unknown tool arguments are ignored.
