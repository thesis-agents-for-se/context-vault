---
id: nano-service
name: Nano Service
category: boundaries
aliases: [Over-Microservices, Too Fine Grained, Micro Microservices]
severity: medium
detects_on: [repo-layout, code, traces]
signals:
  - Services expose only one or two endpoints and hold no data of their own.
  - The overhead code, such as config and boilerplate, is larger than the business code.
  - Several services are always deployed and changed together.
  - A single request fans out to many tiny services.
  - A service is a thin wrapper over a library call or a single query.
related: [chatty-communication, service-chain, wrong-cuts]
solutions: [service-granularity-refactoring, api-composition, domain-driven-decomposition]
sources:
  - https://algomaster.io/learn/microservices/anti-patterns-reference
  - https://stackandsystem.com/series/microservices/microservices-antipatterns
  - https://arxiv.org/abs/1908.04101
---

## Summary

Nano Service is the opposite of a Mega Service. The system has too many very
small services, each doing almost nothing on its own. The split was driven by
the wish to be "micro" instead of by a real need for separate deployment or
scaling.

## Why it hurts

Every Nano Service carries a fixed cost: a pipeline, a container, config,
monitoring, and a network hop. When the business logic inside is a few lines,
that cost is larger than the value. Requests take longer because they cross many
boundaries. Debugging gets hard because one simple flow spreads over many logs.
Teams end up deploying groups of services together, which brings back the
coordination problem.

## How to spot it

- Compare the size of business code to the size of infrastructure code per
  service. A service whose Dockerfile, config, and wiring are bigger than its
  domain code is a candidate.
- List services with fewer than three endpoints and no database.
- Check which services always appear in the same release. Services that never
  ship alone do not need to be apart.
- Read a distributed trace for one common request. Many hops that each do one
  small step point at this antipattern.
- Look for services whose whole job is to call one other service and reshape the
  response.

## Solutions

### 1. Merge services that change together

- **Do:** Group services by how often they change in the same commit or release,
  and merge each group into one service with clear internal modules.
- **Fits when:** Release history shows repeated joint deployment.
- **Cost:** The merged service is larger. Keep internal module boundaries so it
  does not turn into a `mega-service`.

### 2. Draw boundaries around deployment and business flow

- **Do:** Keep a service separate only when it needs its own release cycle, its
  own scaling, its own data, or its own team. Otherwise merge it.
- **Fits when:** You are planning the split and can still change it cheaply.
- **Cost:** Needs a clear rule the team agrees on, or the debate repeats for
  every new service.

### 3. Turn logic into a library instead of a service

- **Do:** Move stateless helper logic that does not need its own deployment into
  a versioned library.
- **Fits when:** The service holds no state and every caller uses the same
  version of the logic.
- **Cost:** Libraries create their own coupling. Version them properly, or you
  trade this antipattern for `shared-libraries`.

## Related

Nano Service is a common cause of `chatty-communication` and `service-chain`.
When the tiny services map to single tables, also check `wrong-cuts`.

## Sources

- Microservices Anti-Patterns: Complete Reference, AlgoMaster.
- Microservices Anti-Patterns series, Stack and System.
- Taibi and Lenarduzzi, Microservices Anti-Patterns: A Taxonomy, 2019.
