---
id: api-gateway
name: API Gateway and Backends for Frontends
type: pattern
solves: [no-api-gateway, hardcoded-endpoints, no-api-versioning, esb-misuse]
sources:
  - https://www.politesi.polimi.it/retrieve/04fb6ce8-cc33-4207-a932-6e0701e8f932/2022_04_ESAS.pdf
  - https://garnetgrid.com/insights/microservices-anti-patterns
  - https://assets.ptidej.net/Publications/Documents/EuroPLoP20.doc.pdf
---

## Summary

An API Gateway is a single entry point between clients and internal services. It
handles routing, authentication, TLS, rate limits, and request logging in one
place. Backends for Frontends is a variation where each client type gets its own
thin gateway.

## How it works

Clients call the gateway, not the services. The gateway maps a public route to
an internal service, checks the caller's token, applies limits, generates a
correlation id, and forwards the request. The internal layout stays private, so
services can be split or merged without changing client code.

Backends for Frontends adds one backend per client type, such as web, mobile,
and partner API. Each one shapes responses for its client, for example a small
payload for mobile.

Keep the gateway thin. Routing, security, and shaping belong there. Business
rules do not: a gateway full of business logic turns into `esb-misuse`.

## When to use it

Use it as soon as there is more than one client type or more than a handful of
services. Use Backends for Frontends when client needs differ enough that one
API forces every client to accept a bad fit.

## Cost and risks

The gateway is on the path of every request, so it must be highly available and
scaled properly. It can become a `bottleneck-service` for delivery too, if one
team must approve every route change. Several gateways in the Backends for
Frontends style mean more components and some duplicated logic.

## Sources

- Design Patterns and Anti-Patterns in Microservices Architecture, Politecnico di Milano, 2022.
- 12 Microservices Anti-Patterns, Garnet Grid.
