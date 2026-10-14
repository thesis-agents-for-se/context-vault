---
id: chatty-communication
name: Chatty Communication
category: communication
aliases: [Chatty Services, Too Many Remote Calls, N+1 Service Calls]
severity: high
detects_on: [code, traces]
signals:
  - One business operation makes many synchronous calls to other services.
  - A remote call sits inside a loop.
  - A service calls another service once per item in a list.
  - A handler awaits several remote calls in sequence that could run in parallel or not at all.
  - Traces show long chains of short calls for one request.
related: [service-chain, nano-service, wrong-cuts, bottleneck-service]
solutions: [api-composition, cqrs, event-driven-integration]
sources:
  - https://www.designgurus.io/blog/10-common-microservices-anti-patterns
  - https://www.geeksforgeeks.org/blogs/microservice-anti-patterns/
  - https://stackandsystem.com/series/microservices/microservices-antipatterns
---

## Summary

Chatty Communication happens when one business operation needs many remote calls
between services, often one after another. Each call adds network time and one
more thing that can fail. It is the network version of the N+1 query problem.

## Why it hurts

Latency adds up. Ten calls of 20 ms each become 200 ms before any work is done.
Availability drops as well: if each service is up 99.9 percent of the time, a
chain of ten gives about 99 percent. Load grows in a non-obvious way, since one
client request becomes many internal requests. Under traffic spikes the inner
services get hit hardest and fail first.

## How to spot it

- Search the code for HTTP or gRPC client calls inside `for`, `foreach`, `map`,
  or stream operations. This is the clearest case.
- Count remote calls per request handler. More than three synchronous calls in
  one handler deserves a look.
- Look for sequential `await` calls that do not depend on each other. These are
  chatty and also needlessly serial.
- In traces, sort requests by span count. Requests with many short spans to
  different services are the ones to fix.
- Look for a service that calls another just to enrich each row of a list. That
  is the N+1 shape.

## Solutions

### 1. Add API Composition

- **Do:** Create an aggregating endpoint or a composition service that fans out
  once, in parallel, and returns one coarse response to the client.
- **Fits when:** The chattiness is between the client and the services, or the
  calls are independent.
- **Cost:** The aggregator becomes a new dependency and can turn into a
  `bottleneck-service` if it takes on business logic.

### 2. Replicate the data the caller needs with a read model

- **Do:** Publish domain events from the owning service and keep a local read
  model in the consumer, so the lookup becomes a local query.
- **Fits when:** The data is read often, changes rarely, and can be slightly
  stale.
- **Cost:** Eventual consistency, duplicated storage, and the need to handle
  out-of-order or repeated events.

### 3. Batch the API and move work to async

- **Do:** Replace `GET /item/{id}` loops with `POST /items:batch`, and move work
  that does not need an immediate answer to a queue.
- **Fits when:** The caller already has all the ids, or the caller does not need
  the result now.
- **Cost:** Batch endpoints are harder to cache and to authorize per item. Async
  work needs status tracking.

## Related

Chatty Communication is often a symptom of `nano-service` or `wrong-cuts`. If
the calls form a straight line of hops, see `service-chain`.

## Sources

- 10 Common Microservices Anti-Patterns, Design Gurus.
- Microservice Anti-Patterns, GeeksforGeeks.
- Microservices Anti-Patterns series, Stack and System.
