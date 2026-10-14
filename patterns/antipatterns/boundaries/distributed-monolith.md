---
id: distributed-monolith
name: Distributed Monolith
category: boundaries
aliases: [Distributed Big Ball of Mud, Monolith in Disguise]
severity: high
detects_on: [code, config, repo-layout, schema]
signals:
  - Services must be released together or in a fixed order.
  - A change to one service forces changes in two or more others in the same pull request.
  - Several services point at the same database or the same tables.
  - Shared DTO or model libraries are imported by most services.
  - The CI pipeline builds and deploys all services as one unit.
related: [shared-database, cyclic-dependency, shared-libraries, chatty-communication]
solutions: [domain-driven-decomposition, database-per-service, strangler-fig]
sources:
  - https://garnetgrid.com/insights/microservices-anti-patterns
  - https://www.macropatternsconsortium.com/blog/microservices-anti-patterns
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
---

## Summary

A Distributed Monolith is a system split into many deployable services that
still has to be deployed as one piece. The services are separate on paper, but
strong dependencies, a shared database, or rigid contracts tie them together.
The team pays the cost of distribution and keeps the constraints of a monolith.

## Why it hurts

The Distributed Monolith removes the one thing a monolith does well: a simple
release. Now a single feature needs a coordinated release across several teams,
plus network calls that can fail. Testing gets harder because no service can be
verified alone. Scaling one part is not possible when that part reads and writes
the same tables as everything else.

## How to spot it

Look for these in the repository and the pipeline:

- A release checklist or runbook that lists a deploy order for services.
- Version numbers that move together across all services.
- One database connection string, or one schema name, repeated in several
  service config files.
- A shared library such as `common-model` or `core-dto` that every service
  depends on, and that changes often in the commit history.
- Pull requests that touch three or more service directories at once. Count this
  over the last 100 commits. A high number is strong evidence.
- Integration tests that need the whole system running to pass.

## Solutions

### 1. Redraw boundaries with Domain-Driven Design

- **Do:** Map bounded contexts to the real business capabilities, then move code
  so each service owns one context end to end, including its data.
- **Fits when:** The service split followed technical layers or database tables
  instead of business processes.
- **Cost:** This is a large refactor. It needs domain knowledge from the
  business side, not just from developers.

### 2. Split the data with Database per Service

- **Do:** Give each service its own database or schema. Replace direct table
  reads with API calls or events. Use Saga for writes that cross services and
  CQRS for reads that cross services.
- **Fits when:** A shared database is the main reason services deploy together.
- **Cost:** You give up easy joins and ACID across services. You have to design
  for eventual consistency.

### 3. Migrate gradually with Strangler Fig

- **Do:** Pull one capability out at a time, put an anti-corruption layer in
  front of the old system, and route traffic to the new service when it is
  ready.
- **Fits when:** The system is in production and a rewrite is not an option.
- **Cost:** Two systems run side by side for a long time. Routing and data sync
  add temporary complexity.

## Related

The Distributed Monolith is usually the result of other antipatterns rather than
a root cause. Check `shared-database`, `cyclic-dependency`, `shared-libraries`,
and `chatty-communication` first. Fixing those often removes this one.

## Sources

- 12 Microservices Anti-Patterns, Garnet Grid.
- 10 Microservices Anti-Patterns That Will Ruin Your System, Macro Patterns.
- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
