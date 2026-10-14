---
id: event-driven-integration
name: Event-Driven Integration
type: pattern
solves: [chatty-communication, cyclic-dependency, shared-database, database-as-integration-point, distributed-transactions, esb-misuse, service-chain]
sources:
  - https://www.dataversity.net/articles/data-management-patterns-for-microservices-architecture/
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-data-persistence/enabling-patterns.md
  - https://medium.com/@amrelsayed.mohamed/catalog-of-microservice-anti-patterns-and-bad-smells-30ebe5a1214e
---

## Summary

Event-Driven Integration means services publish facts about what happened and
other services react to them, instead of calling each other directly. The
producer does not know who consumes its events. This breaks runtime coupling and
is the main tool for replacing direct database access between services.

## How it works

The owning service publishes a domain event, such as `OrderPlaced`, to a broker.
Consumers subscribe and do their own work: update a local copy of the data,
trigger the next step of a Saga, or send a notification.

Rules that make it work in practice:

- Publish the event in the same local transaction as the state change, using an
  outbox table. Otherwise the two can disagree.
- Make every consumer idempotent, since brokers deliver at least once.
- Version event schemas and only add fields inside a version.
- Keep events as facts about the domain, not as commands to a specific service.

Keep the pipes simple. Routing and transformation belong in the endpoints, not in
the broker, which is the difference between this pattern and `esb-misuse`.

## When to use it

Use it when the caller does not need an answer right away, when several
consumers care about the same fact, when you need to break a dependency cycle, or
when a consumer reads another service's data often enough that calling out every
time is too slow.

## Cost and risks

The system becomes eventually consistent, and users may see stale data for a
short time. Debugging is harder, because the flow is not visible in one place, so
tracing across the broker is required. Duplicate and out-of-order messages are
normal and must be handled. Unowned or badly named events spread quickly and are
hard to change later.

## Sources

- Data Management Patterns for Microservices Architecture, Dataversity.
- Enabling data persistence in microservices, AWS Prescriptive Guidance.
- Catalog of Microservice Anti-Patterns and Bad Smells, Medium.
