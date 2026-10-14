---
id: database-per-service
name: Database per Service
type: pattern
solves: [shared-database, database-as-integration-point, distributed-transactions, distributed-monolith, mega-service]
sources:
  - https://microservices.io/patterns/data/database-per-service.html
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-data-persistence/enabling-patterns.md
  - https://docs.aws.amazon.com/pdfs/prescriptive-guidance/latest/modernization-data-persistence/modernization-data-persistence.pdf
---

## Summary

Database per Service means the data of a service is private. Only that service
reads and writes it. Any other service that needs the data asks through an API
or receives it through events. This is the base rule that most persistence
antipatterns break.

## How it works

Each service owns its tables and its migrations, and holds its own transactions.
No other service gets a connection to that store, and there are no foreign keys
crossing service lines.

There are three levels of separation, from weakest to strongest:

1. **Private tables** in a shared database, enforced with database users and
   grants. Cheapest to adopt, and easy to break if grants are loose.
2. **Schema per service** in the same database instance. Clear boundaries, still
   one instance to scale and back up.
3. **Database per service**, a separate instance or cluster per service. Full
   independence, including the freedom to choose a different engine.

Once data is private, you need replacements for what a single database gave you
for free:

- Writes across services: `saga`.
- Reads across services: `api-composition` or `cqrs`.
- Data that a consumer needs locally: `event-driven-integration`.
- Reports and analytics: `reporting-data-store`.

## When to use it

Use it whenever a service should be deployable and scalable on its own. Start at
the level the team can actually enforce, and move up. Enforce boundaries with
permissions, not with documents, because a rule that is not enforced is broken
within a few sprints.

## Cost and risks

You lose joins and single database transactions across services. Reports get
harder. Migrating existing shared data is slow and needs a plan for the period
when both the old and the new store are live. Splitting too early, before the
boundaries are understood, causes more damage than a shared database does,
because moving data back is expensive.

## Sources

- Pattern: Database per service, microservices.io.
- Enabling data persistence in microservices, AWS Prescriptive Guidance.
