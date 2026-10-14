---
id: mega-service
name: Mega Service
category: boundaries
aliases: [God Service, God Component, Fat Service]
severity: high
detects_on: [code, repo-layout, schema]
signals:
  - One service is much larger than the rest, by files, lines, or endpoints.
  - One service owns many unrelated tables.
  - Most commits in the repository land in the same service.
  - Most other services depend on this one.
  - The service handles several business capabilities that do not share data.
related: [bottleneck-service, distributed-monolith, wrong-cuts]
solutions: [domain-driven-decomposition, strangler-fig, database-per-service]
sources:
  - https://medium.com/@leela.kumili/10-microservice-anti-patterns-every-engineer-must-avoid-639f068a8249
  - https://arxiv.org/abs/1908.04101
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
---

## Summary

A Mega Service is one microservice that holds too many responsibilities. It
often keeps most of the old monolith while smaller services are carved out
around it. It breaks the single responsibility idea and becomes the slow part of
the system.

## Why it hurts

A Mega Service becomes a bottleneck for both runtime and people. You cannot
scale one feature without scaling everything inside it. Every team needs to
touch it, so merge conflicts and release queues appear. A failure in any part of
it takes down all of its capabilities at once. Over time it grows faster than
the rest, because adding code there is always the easy path.

## How to spot it

- Count lines of code, source files, and HTTP or gRPC endpoints per service.
  A service three or more times bigger than the median is a candidate.
- Count the tables each service owns. A service that owns tables from unrelated
  business areas, such as billing and shipping, is doing too much.
- Read the commit history. If one service receives most of the commits and most
  of the authors, it is the center of gravity.
- Build the call graph. A service that almost everything calls, and that also
  calls almost everything, is both a Mega Service and a `bottleneck-service`.
- Look at the package structure inside the service. Several top-level packages
  with no shared types is a natural split line.

## Solutions

### 1. Split by subdomain

- **Do:** Group the service internals by business subdomain, then extract each
  group into its own service with its own tables.
- **Fits when:** The internal packages or the tables already fall into clear
  groups.
- **Cost:** Data that used to be joined now lives apart. Some reads become API
  calls or need a read model.

### 2. Extract by risk, starting at the edges

- **Do:** Rank the capabilities inside the service by change rate and by number
  of incoming dependencies. Extract the ones that change often and are called
  least first.
- **Fits when:** The service is in production and a big split is too risky.
- **Cost:** Slow. The service stays large for a while, so the pain is not
  removed right away.

### 3. Use Strangler Fig with a routing layer

- **Do:** Put a router or gateway in front of the service, move one route group
  at a time to a new service, and keep the old path until traffic is cut over.
- **Fits when:** Clients cannot be changed quickly.
- **Cost:** The router becomes critical infrastructure and must be watched.

## Related

A Mega Service usually also acts as a `bottleneck-service`. If several small
services exist only to serve it, also check `wrong-cuts`.

## Sources

- 10 Microservice Anti-Patterns Every Engineer Must Avoid, Medium.
- Taibi and Lenarduzzi, Microservices Anti-Patterns: A Taxonomy, 2019.
- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
