---
id: cyclic-dependency
name: Cyclic Dependency
category: communication
aliases: [Circular Dependency, Service Cycle]
severity: high
detects_on: [code, config, traces]
signals:
  - Service A calls service B and service B calls service A.
  - A longer loop exists, such as A calls B, B calls C, C calls A.
  - Two services list each other in their client configuration or service discovery usage.
  - Startup fails or hangs when services boot in the wrong order.
  - A retry storm between two services appears in the logs.
related: [distributed-monolith, bottleneck-service, chatty-communication]
solutions: [event-driven-integration, domain-driven-decomposition, service-granularity-refactoring]
sources:
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
  - https://arxiv.org/abs/1908.04101
  - https://assets.ptidej.net/Publications/Documents/EuroPLoP20.doc.pdf
---

## Summary

A Cyclic Dependency exists when two or more services call each other in a loop.
The cycle can be direct, between two services, or indirect through a third. It
makes the dependency graph impossible to order, so no service can be released,
started, or reasoned about on its own.

## Why it hurts

A cycle blocks independent deployment, because a breaking change in either
direction needs both sides updated at once. It also makes failures spread in
both directions, and retries on both sides can amplify load until both services
fall over. Cold starts become fragile, since each service waits for the other.
Tracing a bug is harder because the call path loops back on itself.

## How to spot it

- Build the service call graph from the code. Collect the base URLs, client
  classes, or generated stubs each service uses, then look for cycles.
- Check service discovery config and environment variables. If A has `B_URL` and
  B has `A_URL`, that is a direct cycle.
- Read the deployment docs for a required boot order. That order usually exists
  because of a cycle.
- In traces, look for a service id appearing twice in the same trace path.
- Look for timeouts and retries between the same pair of services in the logs.

## Solutions

### 1. Break the cycle with events

- **Do:** Turn one direction of the call into an event. The service that used to
  call back now publishes a fact, and the other side reacts to it.
- **Fits when:** The call back does not need an immediate answer, for example a
  status update or a notification.
- **Cost:** You need a broker, plus handling for duplicate and out-of-order
  messages.

### 2. Give the graph a direction

- **Do:** Declare which service is upstream and which is downstream, then let
  calls flow one way only. Move the data the downstream service needs into its
  own request, or pass it as a parameter.
- **Fits when:** One of the two services is clearly closer to the client or
  closer to the core domain.
- **Cost:** Some request payloads grow, and one side may need a small amount of
  duplicated data.

### 3. Pull the shared part out

- **Do:** Find the logic or data that both services keep asking each other for,
  and move it into a third service that both depend on, or into a shared
  library if it is stateless.
- **Fits when:** The cycle exists because one concept was split across both
  services.
- **Cost:** A new service is a new deployment unit. A library can bring
  `shared-libraries` problems.

## Related

Cyclic Dependency is a strong sign of `distributed-monolith`. Cycles that form
around one central service also point at `bottleneck-service`.

## Sources

- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
- Taibi and Lenarduzzi, Microservices Anti-Patterns: A Taxonomy, 2019.
- On the Study of Microservices Antipatterns: a Catalog Proposal, EuroPLoP 2020.
