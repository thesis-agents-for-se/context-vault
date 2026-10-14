---
id: domain-driven-decomposition
name: Domain-Driven Decomposition
type: pattern
solves: [wrong-cuts, mega-service, nano-service, distributed-monolith, data-driven-migration, cyclic-dependency]
sources:
  - https://assets.ptidej.net/Publications/Documents/EuroPLoP20.doc.pdf
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
  - https://medium.com/@leela.kumili/10-microservice-anti-patterns-every-engineer-must-avoid-639f068a8249
---

## Summary

Domain-Driven Decomposition means drawing service boundaries around business
capabilities and bounded contexts, not around technical layers or database
tables. A service owns one capability end to end: its rules, its data, and its
API. It is the main fix for boundary antipatterns.

## How it works

Start from the business, not the code:

1. List the business capabilities, such as ordering, billing, shipping, and
   identity. Use the language the business uses.
2. Group them into bounded contexts. A context has one consistent meaning for
   each term. If "customer" means two different things, that is two contexts.
3. Map the relationships between contexts, and mark where one depends on
   another and in which direction.
4. Assign one owner service per context, and move the data for that context
   into it.
5. Where a context must talk to a legacy model, put an `anti-corruption-layer`
   between them.

Two practical checks on a proposed boundary: can this service be deployed
without the others, and does a typical change in this area touch only this
service.

## When to use it

Use it at the start of a migration, and again whenever boundaries are clearly
wrong. Use metrics such as change coupling and call frequency as input, but not
as the decision, since they describe the current design rather than the right
one.

## Cost and risks

It needs time from people who know the business, and they are usually busy.
Results are slow to show, which makes it hard to defend against pressure to just
split by table. Getting a boundary wrong is expensive to undo, so extract the
first services carefully and verify them in production before continuing.

## Sources

- On the Study of Microservices Antipatterns: a Catalog Proposal, EuroPLoP 2020.
- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
