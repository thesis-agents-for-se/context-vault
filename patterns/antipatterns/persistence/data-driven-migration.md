---
id: data-driven-migration
name: Data-Driven Migration
category: persistence
aliases: [Schema First Migration, Technology Driven Split]
severity: high
detects_on: [repo-layout, schema, docs]
signals:
  - Services map one to one to tables from the old monolith database.
  - The migration plan starts by splitting the database, not by splitting behaviour.
  - Service names copy table names.
  - The stated reason for the migration is a new database or framework.
  - The old data model survives untouched inside the new services.
related: [wrong-cuts, shared-database, distributed-monolith, nano-service]
solutions: [domain-driven-decomposition, strangler-fig, anti-corruption-layer]
sources:
  - https://www.oreilly.com/content/microservices-antipatterns-and-pitfalls/
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
  - https://assets.ptidej.net/Publications/Documents/EuroPLoP20.doc.pdf
---

## Summary

Data-Driven Migration means the move from monolith to microservices is planned
around the existing database schema or around a new technology, instead of
around business capabilities. Teams split tables first and hope services will
follow. The result keeps the old model's problems in a more expensive shape.

## Why it hurts

The old schema reflects how data was stored, not how the business works, so
services built on it get the wrong boundaries. Migrating data first also means
migrating twice: once for the technical split, then again when the domain
boundaries are finally understood. Because the model did not change, services
still need each other's tables to do anything useful, which brings back
`shared-database` and `distributed-transactions`. Teams then report the
migration as done while none of the promised benefits arrive.

## How to spot it

- Read the migration plan or the project board. If the first milestones are
  about databases and frameworks and not about capabilities, that is the signal.
- Compare the service list with the old table list. A near one to one match is
  direct evidence.
- Check whether the new services still use the monolith's entity classes or
  generated models.
- Look for a migration goal stated as "move to technology X". A tool is not a
  target state.
- Check whether any business process was actually redesigned, or only moved.

## Solutions

### 1. Plan the migration by subdomain

- **Do:** List business capabilities and pick the order to extract them. Move
  behaviour first, and treat data restructuring as a step inside each capability
  extraction, not as the first phase.
- **Fits when:** The migration is starting, or only a few services have shipped.
- **Cost:** Needs domain input and slows the first visible delivery. Early
  services may still read from the old database for a while.

### 2. Use Strangler Fig, one capability at a time

- **Do:** Extract one capability, route its traffic to the new service, verify
  it in production, then extract the next. Validate the boundary before moving
  its data.
- **Fits when:** The monolith is live and cannot be paused.
- **Cost:** Long transition with two systems running, plus routing and data sync
  work.

### 3. Protect the new model with an anti-corruption layer

- **Do:** Put a translation layer between the new service and the legacy model,
  so the new design is not shaped by old tables and old field names.
- **Fits when:** The new service still needs legacy data during the transition.
- **Cost:** Extra code to write and maintain. It should be deleted once the
  legacy source is gone, and often is not.

## Related

Data-Driven Migration is the usual cause of `wrong-cuts` and of a lasting
`shared-database`. If the split produced one service per table, also check
`nano-service`.

## Sources

- Richards, Microservices antipatterns and pitfalls, O'Reilly.
- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
- On the Study of Microservices Antipatterns: a Catalog Proposal, EuroPLoP 2020.
