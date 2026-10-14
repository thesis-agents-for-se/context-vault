---
id: no-api-versioning
name: No API Versioning
category: communication
aliases: [Breaking API Changes, Unversioned Contracts]
severity: medium
detects_on: [code, config, docs]
signals:
  - API routes have no version segment and no version header.
  - Fields are removed or renamed in place in the commit history.
  - Required fields are added to existing request bodies.
  - Consumers are asked to deploy at the same time as the provider.
  - Event payloads change shape with no schema version and no registry.
related: [lack-of-communication-standards, distributed-monolith, no-api-gateway]
solutions: [api-contract-standards, api-gateway, event-driven-integration]
sources:
  - https://arxiv.org/abs/1908.04101
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
  - https://assets.ptidej.net/Publications/Documents/EuroPLoP20.doc.pdf
---

## Summary

No API Versioning means a service changes its public contract without offering
a way for old clients to keep working. Routes have no version, payload changes
land in place, and consumers break on the next deploy. It also applies to events
whose payload shape changes without a schema version.

## Why it hurts

Without versioning, provider and consumer must ship at the same moment, which is
exactly the coupling microservices try to remove. Teams then batch releases and
the system drifts toward a `distributed-monolith`. Rollbacks get risky too,
because going back to an older provider can break clients already updated. In
event systems, old messages still in the queue can no longer be read.

## How to spot it

- Read the route definitions. Look for `/v1/` or a version header. If neither
  exists, there is no versioning.
- Search the commit history of DTO or schema files for renamed and deleted
  fields. Each one is a past breaking change.
- Look for new fields marked as required in request models.
- Check whether events carry a `version` or `schemaVersion` field, and whether a
  schema registry is in use.
- Look in release notes or chat for phrases about deploying services together.

## Solutions

### 1. Version the contract and keep old versions alive

- **Do:** Add a version to routes or headers, keep the previous version running
  during a defined support window, and only make additive changes inside a
  version.
- **Fits when:** The API has external or slow moving consumers.
- **Cost:** Two versions must be maintained and tested at once, which doubles
  some work for the support window.

### 2. Route versions at the gateway

- **Do:** Let the gateway map version paths to the right service instance, so
  clients see a stable address while the backend moves.
- **Fits when:** A gateway is already in place and you want a controlled
  cutover.
- **Cost:** Routing rules grow and must be cleaned up when old versions retire.

### 3. Version event schemas

- **Do:** Add a version field to every event, register schemas, and require that
  consumers ignore unknown fields. Never change the meaning of an existing
  field.
- **Fits when:** Services talk through a broker.
- **Cost:** A schema registry to run, plus rules in CI that block incompatible
  changes.

## Related

No API Versioning is part of the wider `lack-of-communication-standards`
problem, and it is one of the fastest ways to end up in `distributed-monolith`.

## Sources

- Taibi and Lenarduzzi, Microservices Anti-Patterns: A Taxonomy, 2019.
- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
- On the Study of Microservices Antipatterns: a Catalog Proposal, EuroPLoP 2020.
