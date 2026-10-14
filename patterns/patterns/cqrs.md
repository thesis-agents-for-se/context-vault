---
id: cqrs
name: CQRS and Read Models
type: pattern
solves: [chatty-communication, reporting-database, shared-database]
sources:
  - https://www.dataversity.net/articles/data-management-patterns-for-microservices-architecture/
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-data-persistence/enabling-patterns.md
  - https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design
---

## Summary

CQRS means separating the write model from the read model. Writes go through the
domain model and keep the rules. Reads go to a separate model shaped for the
questions being asked. It removes the need to make one schema good at both jobs.

## How it works

The write side stores the source of truth and publishes events when state
changes. The read side listens to those events and keeps one or more read models,
each built for a specific screen or query. A read model can live in another
table, another database, or a search engine, and it can hold data that came from
several services.

Because the read model is updated after the write, it lags by a short time. The
system must handle repeated and out-of-order events, and there must be a way to
rebuild a read model from scratch when it drifts or when the shape changes.

Event sourcing is a related but separate choice: storing the events themselves as
the source of truth. CQRS does not require it.

## When to use it

Use it when a service has very different read and write loads, when a query needs
data from several services, or when reporting queries are hurting transactional
performance. It is also a good way to remove chatty per-row lookups: the consumer
keeps a local read model instead of calling out for each item.

## Cost and risks

More code, more storage, and a second path that can break. Users may see stale
data right after a write, so the UI has to account for that. Do not apply CQRS to
a whole system by default. Use it for the specific reads that need it, and leave
simple CRUD services alone.

## Sources

- Data Management Patterns for Microservices Architecture, Dataversity.
- Enabling data persistence in microservices, AWS Prescriptive Guidance.
- Designing the infrastructure persistence layer, Microsoft .NET docs.
