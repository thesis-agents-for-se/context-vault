---
id: esb-misuse
name: ESB Misuse
category: communication
aliases: [ESB Usage, Heavy Middleware, Smart Pipes]
severity: medium
detects_on: [config, code, docs]
signals:
  - A central bus holds routing rules, transformations, and business logic.
  - Adding a new service requires a change in the bus configuration.
  - Message formats are translated inside the middleware, not at the endpoints.
  - One team owns the bus and becomes a queue for every other team.
  - The bus is a single point of failure for all service traffic.
related: [bottleneck-service, distributed-monolith, lack-of-communication-standards]
solutions: [event-driven-integration, api-gateway, service-granularity-refactoring]
sources:
  - https://medium.com/@amrelsayed.mohamed/catalog-of-microservice-anti-patterns-and-bad-smells-30ebe5a1214e
  - https://arxiv.org/abs/1908.04101
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
---

## Summary

ESB Misuse means using a heavy Enterprise Service Bus as the central hub of a
microservice system. The bus ends up holding routing, data mapping, and business
rules. Microservices are supposed to use simple pipes and keep the logic in the
endpoints, so this reverses the idea.

## Why it hurts

A central bus is a single point of failure for all traffic. It also becomes a
shared bottleneck for delivery, because every new integration needs a change
inside it, made by the team that owns it. Business rules hidden in bus
configuration are hard to test, hard to version, and hard to find. Services stop
being independent, since their behaviour depends on config they do not own.

## How to spot it

- Look for transformation or mapping files in the middleware, such as XSLT,
  mapping flows, or routing DSL files that encode business decisions.
- Check whether the onboarding guide for a new service includes a bus change.
- Look for message enrichment done in the bus, where it calls a service to fill
  in fields.
- Check whether a single middleware component sits on the path of most calls.
- Look for one repository owned by an integration team that changes every time
  any service changes.

## Solutions

### 1. Replace the bus with light messaging

- **Do:** Move to a plain broker or event bus that only moves messages, and put
  routing and mapping inside the services that own the data.
- **Fits when:** The bus is mostly used for point to point delivery that a queue
  or topic can do.
- **Cost:** Each service takes on work the bus used to do, so shared conventions
  become more important.

### 2. Pull business rules out of the bus

- **Do:** Identify every rule encoded in bus configuration and move it into a
  service that owns that part of the domain.
- **Fits when:** You cannot remove the bus yet, but you want to stop it growing.
- **Cost:** A period where logic exists in both places. Track the migration list
  so nothing is left behind.

### 3. Move flows out one at a time

- **Do:** Route new integrations through an API gateway or direct events, and
  migrate existing flows off the bus one by one until it can be turned off.
- **Fits when:** The bus carries many flows and cannot be replaced at once.
- **Cost:** Two integration styles run in parallel, so operations must watch
  both.

## Related

ESB Misuse creates a `bottleneck-service` at the infrastructure level. Systems
that depend on bus config for every change also show `distributed-monolith`
behaviour.

## Sources

- Catalog of Microservice Anti-Patterns and Bad Smells, Medium.
- Taibi and Lenarduzzi, Microservices Anti-Patterns: A Taxonomy, 2019.
- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
