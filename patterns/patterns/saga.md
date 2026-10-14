---
id: saga
name: Saga
type: pattern
solves: [distributed-transactions, service-chain, bottleneck-service]
sources:
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-data-persistence/enabling-patterns.md
  - https://microservices.io/patterns/data/database-per-service.html
  - https://www.dataversity.net/articles/data-management-patterns-for-microservices-architecture/
---

## Summary

A Saga replaces one transaction that crosses services with a sequence of local
transactions, one per service. If a step fails, earlier steps are undone by
compensating actions instead of by a database rollback. It gives reliability
without locking resources across the network.

## How it works

Each step commits locally and then triggers the next step. Every step that
changes state needs a matching compensation, such as "cancel reservation" for
"reserve stock". Compensations are business actions, not rollbacks, so they must
be designed with the business.

There are two styles:

- **Choreography.** Each service publishes an event and the next one reacts.
  There is no central coordinator. Good for short flows of two or three steps.
  In longer flows the logic gets scattered and nobody can see the whole process.
- **Orchestration.** One orchestrator holds the flow and calls each step. The
  process is visible in one place and easier to retry and monitor. The risk is
  that the orchestrator grows into a `bottleneck-service`.

Every handler must be idempotent, because messages get delivered more than once.
Use the outbox pattern so the local commit and the published event cannot get out
of step.

## When to use it

Use it for business processes that span services and must complete reliably, such
as order placement, booking, or payment plus fulfilment. Use it when the answer
to "we need a distributed transaction" is really "we need the whole process to
finish or be undone".

## Cost and risks

Intermediate states are visible to users, so the product must show them, for
example "payment pending". Compensations can fail too and need a manual path.
Testing is harder, because failures at any step have to be simulated. Do not use
a Saga to cover a boundary mistake: if the steps always run together and never
alone, the data may belong in one service.

## Sources

- Enabling data persistence in microservices, AWS Prescriptive Guidance.
- Data Management Patterns for Microservices Architecture, Dataversity.
