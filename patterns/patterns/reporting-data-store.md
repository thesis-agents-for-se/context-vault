---
id: reporting-data-store
name: Reporting Data Store
type: pattern
solves: [reporting-database, database-as-integration-point, shared-database]
sources:
  - https://www.oreilly.com/content/microservices-antipatterns-and-pitfalls/
  - https://medium.com/@rizqimulkisrc/using-mysql-with-microservices-patterns-anti-patterns-da8e0d45a87c
  - https://www.dataversity.net/articles/data-management-patterns-for-microservices-architecture/
---

## Summary

A Reporting Data Store is a separate database for reporting and analytics, fed
from the services instead of queried inside them. Transactional stores keep
serving the application, and report users get a store built for wide queries.

## How it works

Data moves from each service to the reporting store through one of:

- **Change data capture,** reading the database log and streaming changes. Near
  real time, and it does not require service code changes, but it couples the
  pipeline to the internal schema unless the events are mapped.
- **Domain events,** where each service publishes what happened and the pipeline
  builds the reporting model from those. Cleaner contract, more work per service.
- **Scheduled export,** a periodic job that pushes an agreed extract. Simplest,
  with the largest delay.

The reporting store can be a warehouse, a columnar database, or a set of
materialised views, and it should hold a model built for reports, not a copy of
the service tables. Publish that model as the contract for report authors, so
services can still change their internal schema.

For reports that must stay inside one service, `cqrs` read models are the lighter
option. A read replica of the service database is a quick first step, but it
still exposes the internal schema, so treat it as temporary.

## When to use it

Use it when reports cross several services, need history, or are heavy enough to
affect user facing latency.

## Cost and risks

Another store and a pipeline to run, monitor, and back up. Reports show data that
is minutes or hours old, and report users have to accept that. If the pipeline
just copies raw tables, the coupling moves instead of disappearing, so invest in
the reporting model.

## Sources

- Richards, Microservices antipatterns and pitfalls, O'Reilly.
- Data Management Patterns for Microservices Architecture, Dataversity.
