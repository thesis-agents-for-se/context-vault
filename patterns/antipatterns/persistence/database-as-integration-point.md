---
id: database-as-integration-point
name: Database as Integration Point
category: persistence
aliases: [Database Integration, Direct Database Access, Integration Database]
severity: high
detects_on: [code, config, schema]
signals:
  - A service connects to another service's database to read or write data.
  - A service runs SQL against tables it does not own.
  - Data is exchanged by writing rows into a table that another service polls.
  - A batch job writes directly into a service's tables at night.
  - A view or synonym in one database points at another service's tables.
related: [shared-database, reporting-database, distributed-monolith]
solutions: [database-per-service, event-driven-integration, reporting-data-store]
sources:
  - https://www.oreilly.com/content/microservices-antipatterns-and-pitfalls/
  - https://medium.com/@rizqimulkisrc/using-mysql-with-microservices-patterns-anti-patterns-da8e0d45a87c
  - https://microservices.io/patterns/data/database-per-service.html
---

## Summary

Database as Integration Point means services integrate by reaching into each
other's databases instead of calling APIs or consuming events. The database
becomes the integration channel. It looks convenient because the data is right
there, and it removes the owning service's ability to change anything.

## Why it hurts

The internal schema turns into a public API that was never designed as one. The
owning team cannot rename a column, change a type, or move to a different store
without breaking unknown consumers. Business rules are bypassed as well: a
direct write skips validation, so invalid data enters through the side door.
Locking and load from foreign queries hit the owning service's performance, and
nobody can tell where the load comes from.

## How to spot it

- Compare each service's connection settings with the list of databases owned by
  other services. A mismatch is the finding.
- Grep for raw SQL, table names, or ORM entities that do not belong to the
  service you are reading.
- Look for a service with more than one datasource configured, where the second
  one belongs elsewhere.
- Look for tables used as queues, with columns like `status`, `processed_at`,
  and a poller on the other side.
- Check ETL and batch job scripts. They often write directly into service
  tables.
- In the database itself, check grants: a user named for service A with rights
  on service B's tables confirms it.

## Solutions

### 1. Allow access only through the owner's API

- **Do:** Remove the foreign connection and expose the needed data as an
  endpoint on the owning service. Revoke the database grants so the old path
  cannot come back.
- **Fits when:** The consumer needs small amounts of fresh data.
- **Cost:** More network calls and a runtime dependency on the owner. Watch for
  `chatty-communication` if the calls are per row.

### 2. Replicate data with domain events

- **Do:** Have the owner publish events when data changes, and let consumers
  keep their own local copy in the shape they need.
- **Fits when:** The consumer reads the data often and can tolerate a short
  delay.
- **Cost:** Eventual consistency, extra storage, and consumers must handle
  duplicate and out-of-order events.

### 3. Give heavy readers a separate store

- **Do:** For reporting or analytics consumers, feed a replica or a dedicated
  reporting database through replication or a scheduled export, and point them
  there.
- **Fits when:** The consumer is a report, a dashboard, or a data team.
- **Cost:** Another store to run and keep in sync. The exported shape still
  needs a contract, or the coupling just moves.

## Related

Database as Integration Point is the active form of `shared-database`. When the
foreign reader is a report, see `reporting-database`.

## Sources

- Richards, Microservices antipatterns and pitfalls, O'Reilly.
- Using MySQL with Microservices: Patterns and Anti-Patterns, Medium.
- Pattern: Database per service, microservices.io.
