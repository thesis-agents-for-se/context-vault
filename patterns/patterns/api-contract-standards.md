---
id: api-contract-standards
name: API Contract Standards
type: pattern
solves: [lack-of-communication-standards, no-api-versioning, shared-libraries, insufficient-monitoring]
sources:
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
  - https://medium.com/@amrelsayed.mohamed/catalog-of-microservice-anti-patterns-and-bad-smells-30ebe5a1214e
  - https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design
---

## Summary

API Contract Standards means one written and enforced agreement on how services
expose and change their APIs: protocols, payload shape, errors, versioning, and
documentation. It replaces per team habits with one predictable style.

## How it works

The standard should cover at least:

- **Protocol choice.** For example REST with JSON at the edge, gRPC for internal
  high traffic calls, events for asynchronous work. State when each is used.
- **Naming and formats.** One case style, ISO dates in UTC, money as an amount
  plus a currency code, and stable field names.
- **Errors.** One response shape with a machine readable code, a message, and
  the correlation id. A clear list of which status codes callers may retry.
- **Versioning.** A version in the path or header, additive changes only inside
  a version, and a support window for the previous one.
- **Documentation.** An OpenAPI or protobuf file per service, generated from
  code, published in one catalog.
- **Correlation.** Every service reads and forwards the trace header.

Enforce it in CI with a linter for the API spec and a contract test between
provider and consumer, so a breaking change fails the build instead of failing
in production.

## When to use it

Set it up early, before the number of services grows. Adding it later means
migrating existing services, which is slow but still worth doing, starting with
the most used APIs.

## Cost and risks

Writing the standard is the easy part. Keeping it alive needs review and CI
checks, or it becomes a document nobody reads. Shipping it as a shared client
library helps adoption but brings `shared-libraries` risk, so version that
library properly and keep business logic out of it.

## Sources

- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
- Catalog of Microservice Anti-Patterns and Bad Smells, Medium.
