---
id: no-api-gateway
name: No API Gateway
category: communication
aliases: [Direct Client to Service, Missing Edge Layer]
severity: medium
detects_on: [config, code, docs]
signals:
  - Clients hold the address of several internal services.
  - Each service implements its own authentication and token checks.
  - Internal services are exposed to the public network.
  - CORS rules are repeated in every service.
  - Rate limiting exists in some services and not in others.
related: [hardcoded-endpoints, no-api-versioning, lack-of-communication-standards]
solutions: [api-gateway, api-composition, observability-stack]
sources:
  - https://www.politesi.polimi.it/retrieve/04fb6ce8-cc33-4207-a932-6e0701e8f932/2022_04_ESAS.pdf
  - https://assets.ptidej.net/Publications/Documents/EuroPLoP20.doc.pdf
  - https://arxiv.org/abs/1908.04101
---

## Summary

No API Gateway means external clients call internal microservices directly,
with no single entry point in front of them. Each service then has to solve
security, routing, and limits on its own. The internal service layout becomes
part of the public contract.

## Why it hurts

Without a gateway, every service repeats the same edge concerns, and each one
can get them wrong in a different way. Any change to the internal split breaks
clients, because clients know the internal addresses. Security review has to
cover many entry points instead of one. There is also no single place to collect
request metrics, so end to end visibility is missing.

## How to spot it

- Read the client code, including mobile and front end. If it builds requests to
  more than one service host, there is no gateway.
- Look for repeated auth middleware, JWT validation, or CORS config across
  service repositories.
- Check the ingress or load balancer rules. Many public routes that point
  straight at internal services confirm it.
- Look for rate limiting or request logging in only some services. Uneven
  coverage means no shared edge.

## Solutions

### 1. Put an API Gateway in front

- **Do:** Add one entry point that handles routing, authentication, TLS, rate
  limits, and request logging, and stop exposing services directly.
- **Fits when:** There are several client types and more than a handful of
  services.
- **Cost:** The gateway is a single point of failure and needs its own scaling
  and monitoring. Keep business logic out of it.

### 2. Add Backends for Frontends

- **Do:** Give each client type, such as web, mobile, and partner API, its own
  thin backend that shapes responses for that client.
- **Fits when:** Different clients need very different payload sizes and shapes.
- **Cost:** More components to run and keep in sync. Some logic gets duplicated
  across the backends.

### 3. Centralise observability at the edge

- **Do:** Generate a correlation id at the gateway, pass it downstream, and
  collect latency and error rates per route in one place.
- **Fits when:** You already have a gateway but are still blind to end to end
  behaviour.
- **Cost:** Services must accept and forward the correlation headers, which
  needs a small change in every one.

## Related

No API Gateway usually comes with `hardcoded-endpoints` and `no-api-versioning`,
because there is no layer where those could be handled.

## Sources

- Design Patterns and Anti-Patterns in Microservices Architecture, Politecnico di Milano, 2022.
- On the Study of Microservices Antipatterns: a Catalog Proposal, EuroPLoP 2020.
- Taibi and Lenarduzzi, Microservices Anti-Patterns: A Taxonomy, 2019.
