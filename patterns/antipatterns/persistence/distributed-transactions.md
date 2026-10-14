---
id: distributed-transactions
name: Distributed Transactions
category: persistence
aliases: [Transactional Integration, Two-Phase Commit Across Services, XA Transactions]
severity: high
detects_on: [code, config]
signals:
  - XA or two-phase commit is configured across services or across resources.
  - A transaction annotation wraps a block that contains remote calls.
  - A transaction manager coordinates a database and a message broker together.
  - A rollback in one service is expected to undo work already done in another.
  - Long running database transactions appear while waiting on a network call.
related: [shared-database, database-as-integration-point, chatty-communication]
solutions: [saga, event-driven-integration, database-per-service]
sources:
  - https://medium.com/@rizqimulkisrc/using-mysql-with-microservices-patterns-anti-patterns-da8e0d45a87c
  - https://medium.com/@amrelsayed.mohamed/catalog-of-microservice-anti-patterns-and-bad-smells-30ebe5a1214e
  - https://microservices.io/patterns/data/database-per-service.html
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-data-persistence/enabling-patterns.md
---

## Summary

Distributed Transactions means using one ACID transaction that spans several
services or several resources, usually through two-phase commit. The goal is to
keep strong consistency across the whole operation. In a distributed system it
costs availability and adds coordination that is hard to operate.

## Why it hurts

A two-phase commit holds locks while it waits for every participant to answer.
One slow or unreachable participant blocks the others, so a partial failure
becomes a full stall. Throughput drops because locks are held across the network.
The failure modes are also hard to recover from: if the coordinator dies after
prepare, rows stay locked until someone intervenes. On top of that, it ties
services together at runtime, which removes independent availability.

## How to spot it

- Grep for XA settings, `javax.transaction`, JTA transaction managers, or
  distributed transaction coordinators in config.
- Look for transaction annotations, such as `@Transactional`, around code that
  makes an HTTP, gRPC, or broker call inside the same block.
- Look for a transaction that covers both a database write and a message publish
  without an outbox table.
- Check for database metrics showing long transaction durations that match
  network call times.
- Look in the code for comments or handlers that try to "undo" a call to another
  service after a failure. That is a hand rolled compensation, and it shows the
  boundary is wrong.

## Solutions

### 1. Use the Saga pattern

- **Do:** Split the operation into local transactions, one per service, linked
  by events or by an orchestrator. For each step, define a compensating action
  that reverses its business effect.
- **Fits when:** A business process really spans several services and must be
  reliable.
- **Cost:** More moving parts. Compensations are business decisions, not
  rollbacks, and intermediate states are visible to users.

### 2. Design for eventual consistency

- **Do:** Accept that data converges after a short delay. Use asynchronous
  messages, retries, and idempotent handlers, and show the user a pending state
  where needed.
- **Fits when:** The business can accept a short window of inconsistency, which
  is most cases outside payments and ledgers.
- **Cost:** The team must design for duplicates, retries, and states that do not
  exist in a single database model.

### 3. Keep ACID inside one service

- **Do:** Draw the boundary so that data that must change together lives in one
  service, and use a normal local transaction there. Use the outbox pattern to
  publish events reliably from the same transaction.
- **Fits when:** The need for atomicity points at data that was split for the
  wrong reason.
- **Cost:** The service holds more data and may grow. It may mean redoing a
  boundary you already shipped.

## Related

Distributed Transactions often appear after a `shared-database` split, or when
`wrong-cuts` separated data that changes together.

## Sources

- Using MySQL with Microservices: Patterns and Anti-Patterns, Medium.
- Catalog of Microservice Anti-Patterns and Bad Smells, Medium.
- Pattern: Database per service, microservices.io.
- Enabling data persistence in microservices, AWS Prescriptive Guidance.
