---
id: api-composition
name: API Composition
type: pattern
solves: [chatty-communication, wrong-cuts, nano-service, shared-database, reporting-database, no-api-gateway]
sources:
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-data-persistence/enabling-patterns.md
  - https://stackandsystem.com/series/microservices/microservices-antipatterns
  - https://microservices.io/patterns/data/database-per-service.html
---

## Summary

API Composition answers a query that needs data from several services by calling
each owner and joining the results in memory. One component does the fan-out, so
the client makes a single call. It is the simplest replacement for a cross
service join.

## How it works

A composer, which can be an endpoint in an existing service, a dedicated
aggregation service, or the API gateway, receives one request. It calls the
services it needs in parallel, waits for the answers, and assembles the response.

To keep it safe:

- Call in parallel, not in sequence, when the calls are independent.
- Set a timeout per call and decide what a partial answer looks like.
- Keep the composer free of business rules. It shapes data, it does not decide.
- Use batch endpoints on the downstream services instead of one call per row.

## When to use it

Use it for read queries that join a small number of services and a small result
set, and where the data must be fresh. It is also the fastest way to give clients
a coarse API while deeper boundary problems are fixed underneath.

## Cost and risks

The composer depends on every service it calls, so its availability is the
product of theirs, and it can become a `bottleneck-service`. Joining large
result sets in memory does not scale, and paging or sorting across services is
hard to do correctly. When the query is large, repeated, or analytical, use
`cqrs` or `reporting-data-store` instead.

## Sources

- Enabling data persistence in microservices, AWS Prescriptive Guidance.
- Pattern: Database per service, microservices.io.
- Microservices Anti-Patterns series, Stack and System.
