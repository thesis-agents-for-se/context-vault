---
id: shared-libraries
name: Shared Libraries
category: operations
aliases: [Common Library Coupling, Shared Kernel Abuse]
severity: medium
detects_on: [code, config, repo-layout]
signals:
  - A library named common, core, or shared is imported by most services.
  - The shared library contains domain entities or business rules.
  - Services must upgrade the library at the same time.
  - The library has no version, or every service pins the same snapshot.
  - A change in the library triggers a rebuild of all services.
related: [distributed-monolith, nano-service, lack-of-communication-standards]
solutions: [service-granularity-refactoring, api-contract-standards]
sources:
  - https://arxiv.org/abs/1908.04101
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
  - https://medium.com/@amrelsayed.mohamed/catalog-of-microservice-anti-patterns-and-bad-smells-30ebe5a1214e
---

## Summary

Shared Libraries becomes an antipattern when services depend on common code that
holds business logic or domain models, and that code is not versioned properly.
Reuse looks like good practice, but here it rebuilds the coupling of a monolith
at the code level. A change in one place forces a release everywhere.

## Why it hurts

If all services must use the same library version, they must be released
together, which is a `distributed-monolith` in slow motion. Domain rules inside
a shared library also blur ownership: nobody knows which team decides when the
rule changes. Upgrades become risky, because a small fix for one service ships
to all the others at the same time. Teams then avoid upgrading, and the library
accumulates old versions in production.

## How to spot it

- List the dependencies of every service and find the ones that appear in almost
  all of them and are built in house.
- Open the shared library. Domain entities, validation rules, or workflow code
  inside it is the problem. Logging helpers are not.
- Check whether the library uses semantic versions, or whether services depend
  on `latest`, a snapshot, or a git branch.
- Look at the commit history. If library changes and service changes land in the
  same pull request, the coupling is real.
- Check whether more than one service is blocked from upgrading because of a
  breaking change.

## Solutions

### 1. Version the library strictly

- **Do:** Use semantic versioning, publish to a registry, let each service pick
  its own version, and support the last two major versions during a migration
  window.
- **Fits when:** The shared code is genuinely useful and stable.
- **Cost:** Maintaining several versions costs time, and the owning team must
  take that responsibility.

### 2. Keep shared code to cross-cutting concerns only

- **Do:** Allow shared libraries for logging, tracing, auth clients, and
  serialization helpers. Do not allow shared domain entities or business rules,
  even if that means duplicating a class.
- **Fits when:** The library is a mix of infrastructure and domain code.
- **Cost:** Some duplication between services, which teams often resist. The
  duplication is the price of independence.

### 3. Turn the shared logic into a service

- **Do:** If the shared logic really has one owner and one rule set, put it
  behind an API instead of inside every service.
- **Fits when:** The logic changes often and must be consistent everywhere at
  the same time, such as pricing or tax rules.
- **Cost:** A network call instead of a local one, plus a new runtime dependency
  that can fail or become a `bottleneck-service`.

## Related

Shared Libraries is a frequent cause of `distributed-monolith`. Moving logic
into libraries is also a valid fix for `nano-service`, so the two must be
balanced.

## Sources

- Taibi and Lenarduzzi, Microservices Anti-Patterns: A Taxonomy, 2019.
- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
- Catalog of Microservice Anti-Patterns and Bad Smells, Medium.
