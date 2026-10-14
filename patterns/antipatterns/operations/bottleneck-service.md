---
id: bottleneck-service
name: Bottleneck Service
category: operations
aliases: [Hub-like Dependency, Central Orchestrator, Single Point of Failure Service]
severity: high
detects_on: [code, traces, config]
signals:
  - One service has many incoming and outgoing dependencies compared to the rest.
  - Most requests pass through the same service.
  - When that service is down, almost nothing works.
  - The service is the first to run out of CPU, memory, or connections.
  - It coordinates business flows that belong to other services.
related: [mega-service, cyclic-dependency, service-chain, esb-misuse]
solutions: [service-granularity-refactoring, resilience-patterns, saga]
sources:
  - https://arxiv.org/abs/1908.04101
  - https://garnetgrid.com/insights/microservices-anti-patterns
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
---

## Summary

A Bottleneck Service is a service that too many other services depend on. It
usually appears when one service is made the orchestrator of every flow, or when
it owns data that everyone needs. It limits both throughput and availability for
the whole system.

## Why it hurts

If this service is slow, every flow is slow. If it is down, the system is down,
which removes the fault isolation that microservices are supposed to give. It
also becomes a release bottleneck, since most features need a change in it.
Capacity planning gets harder because its load is the sum of everyone else's
traffic, and it grows in ways its own team cannot predict.

## How to spot it

- Build the dependency graph and compute in-degree and out-degree per service.
  The service with a much higher count than the rest is the candidate.
- In traces, count how many distinct request types include this service. A high
  share means it sits on the critical path of everything.
- Look at incident history. A service named in most incidents is a bottleneck in
  practice.
- Read its code for orchestration of flows that belong to other domains, such as
  a user service that also drives the order workflow.
- Check connection pool and thread pool metrics. Saturation here first is a
  practical confirmation.

## Solutions

### 1. Move orchestration out

- **Do:** Give each business flow an owner. Move the coordination for a flow to
  the service that owns its outcome, or to a dedicated workflow, instead of
  keeping it all in one place.
- **Fits when:** The service became central because it coordinates, not because
  it holds data.
- **Cost:** More services take on coordination work, and the flow becomes harder
  to see in one place. Good tracing is needed.

### 2. Scale it properly while it stays central

- **Do:** Run several replicas behind a load balancer, add autoscaling, and
  separate read traffic from write traffic if the load is uneven.
- **Fits when:** The service must stay central for now, such as an auth service.
- **Cost:** Cost of running more instances. Scaling hides the design problem, so
  it should be paired with a longer term plan.

### 3. Protect callers with resilience patterns

- **Do:** Add circuit breakers, timeouts, bounded retries with backoff, and a
  fallback behaviour in every caller, so the bottleneck failing does not take
  everything with it.
- **Fits when:** You cannot change the topology soon, but you must limit the
  blast radius.
- **Cost:** Fallback behaviour must be defined per caller, which is real product
  work, not just config.

## Related

A Bottleneck Service is often also a `mega-service`. When the bottleneck is
middleware rather than a service, see `esb-misuse`.

## Sources

- Taibi and Lenarduzzi, Microservices Anti-Patterns: A Taxonomy, 2019.
- 12 Microservices Anti-Patterns, Garnet Grid.
- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
