---
id: shared-database
name: Shared Database
category: persistence
aliases: [Shared Persistence, I Was Taught to Share, Common Database]
severity: high
detects_on: [config, code, schema]
signals:
  - Two or more services use the same connection string, host, and database name.
  - The same table is mapped by entity classes in more than one service.
  - Two services run migrations against the same schema.
  - A table has columns that only one service writes and another only reads.
  - Foreign keys link tables that belong to different services.
related: [database-as-integration-point, distributed-monolith, distributed-transactions, reporting-database]
solutions: [database-per-service, api-composition, event-driven-integration]
sources:
  - https://medium.com/@subham11/the-shared-database-anti-pattern-c87013d2dcb2
  - https://www.oreilly.com/library/view/microservices-antipatterns-and/9781492042716/ch03.html
  - https://microservices.io/patterns/data/database-per-service.html
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-data-persistence/enabling-patterns.md
---

## Summary

Shared Database means several microservices read and write the same schema, and
often the same tables. Each service can change data that another service depends
on. It is the most common reason a microservice migration stays stuck halfway.

## Why it hurts

The database schema becomes a shared contract that nobody owns. A column rename
can break services that the owning team does not know about, so every schema
change turns into a coordination meeting. Services cannot be deployed or rolled
back alone, because migrations are shared. Data rules get duplicated and drift,
since each service validates in its own way before writing. Scaling is limited
too, as one database instance carries the load of every service.

## How to spot it

- Compare connection settings across services. Same host plus same database
  name is direct evidence.
- List the tables mapped by each service's ORM entities or repositories, then
  look for tables that appear in more than one list.
- Check the migration folders. Two services with migrations touching the same
  table is a strong signal.
- Look for foreign keys that cross what should be service boundaries.
- Look at database grants. One shared user with full rights, used by all
  services, means the boundary does not exist at the database level.

## Solutions

### 1. Database per service

- **Do:** Give every service its own database. The service owns its tables and
  is the only one that reads or writes them. Others go through its API or
  through events.
- **Fits when:** You want real independence and can accept eventual consistency
  between services.
- **Cost:** No cross service joins and no single ACID transaction. You need
  Saga, CQRS, or API Composition to replace them. Data migration is real work.

### 2. Private tables inside one shared database

- **Do:** Keep one database instance, but assign each table a single owner
  service. Only the owner writes. Other services read through the owner's API.
  Enforce it with database users and grants, not just with a rule in a document.
- **Fits when:** You cannot split infrastructure yet, but you can fix ownership
  now.
- **Cost:** The instance is still a shared failure point and a shared scaling
  limit. The boundary holds only if grants are enforced.

### 3. Schema per service in the same instance

- **Do:** Give each service its own schema in the same database server, with no
  cross schema queries and no cross schema foreign keys.
- **Fits when:** The team is not ready to run many database instances, but wants
  a clear path to split later.
- **Cost:** Still one instance to scale and back up. The temptation to do a
  cross schema join stays, so it must be blocked by permissions.

## Related

Shared Database is the base for `database-as-integration-point`,
`distributed-transactions`, and `reporting-database`. It is also the most common
cause of `distributed-monolith`.

## Sources

- The Shared Database Anti-Pattern, Medium.
- Richards, Microservices AntiPatterns and Pitfalls, chapter 3, O'Reilly.
- Pattern: Database per service, microservices.io.
- Enabling data persistence in microservices, AWS Prescriptive Guidance.
