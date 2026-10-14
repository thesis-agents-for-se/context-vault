---
id: reporting-database
name: Reporting on the Transactional Database
category: persistence
aliases: [Reporting Database Anti-Pattern, Analytics on OLTP]
severity: medium
detects_on: [code, schema, config]
signals:
  - Reports and dashboards query the live transactional database.
  - Long analytical queries with many joins and group by run against service tables.
  - A BI tool has credentials for a service database.
  - Indexes exist only to serve reports, not the service itself.
  - Slow query logs are dominated by report queries during business hours.
related: [database-as-integration-point, shared-database, mega-service]
solutions: [reporting-data-store, cqrs, api-composition]
sources:
  - https://www.oreilly.com/content/microservices-antipatterns-and-pitfalls/
  - https://medium.com/@rizqimulkisrc/using-mysql-with-microservices-patterns-anti-patterns-da8e0d45a87c
  - https://www.dataversity.net/articles/data-management-patterns-for-microservices-architecture/
---

## Summary

This antipattern is running heavy reporting and analytics queries against the
production transactional database of a service, often from outside the service.
Reports need wide scans and many joins, while transactional workloads need short
and fast access. Putting both on the same store makes each one worse.

## Why it hurts

Report queries take locks and use cache and CPU that the service needs, so user
facing latency rises at the worst times, usually at month end. Report authors
also depend on the internal schema, so the owning team can no longer change it
freely. To make reports fast, teams add indexes that slow down writes. Over time
the transactional model gets shaped by reporting needs instead of by the domain.

## How to spot it

- Check which users and tools connect to the service database. A BI or reporting
  account is the direct finding.
- Read the slow query log and look for queries with several joins, aggregates,
  and wide date ranges.
- Look for indexes whose columns match report filters and not service queries.
- Look for scheduled jobs that run large SELECT statements at fixed times.
- Look for report endpoints inside a service that build large aggregations at
  request time.

## Solutions

### 1. Move reporting to its own store

- **Do:** Create a dedicated reporting database or warehouse, fed by replication,
  change data capture, or a scheduled export from each service, and point all
  reporting tools there.
- **Fits when:** Reports cross several services or need history.
- **Cost:** Another store to run, plus a delay between the source and the
  report. Report authors must accept data that is not real time.

### 2. Apply CQRS with read models

- **Do:** Separate the write model from the read model. Build read models shaped
  for the questions being asked, updated from events.
- **Fits when:** The same service serves both heavy reads and frequent writes.
- **Cost:** More code and more storage. Read models can fall behind or get out
  of sync and need a rebuild path.

### 3. Expose reporting through APIs with limits

- **Do:** Offer explicit endpoints for the reports that are actually needed, with
  paging, fixed filters, and a query timeout, and block free form access to the
  database.
- **Fits when:** There are only a few known reports.
- **Cost:** Every new report needs work from the owning team, which can become a
  bottleneck.

## Related

When the reporting queries come from another service or from a data team with
direct credentials, this is also `database-as-integration-point`.

## Sources

- Richards, Microservices antipatterns and pitfalls, O'Reilly.
- Using MySQL with Microservices: Patterns and Anti-Patterns, Medium.
- Data Management Patterns for Microservices Architecture, Dataversity.
