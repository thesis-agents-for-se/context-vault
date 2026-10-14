---
id: lack-of-communication-standards
name: Lack of Communication Standards
category: communication
aliases: [No Shared Contracts, Inconsistent APIs]
severity: medium
detects_on: [code, docs, config]
signals:
  - Services use different protocols and formats with no rule about when to use each.
  - Error responses have a different shape in every service.
  - Field naming styles differ, such as snake_case in one service and camelCase in another.
  - Date and money formats are not consistent across APIs.
  - Some services have API documentation and others have none.
  - Timeout and retry values are picked per service with no shared policy.
related: [no-api-versioning, no-api-gateway, esb-misuse, insufficient-monitoring]
solutions: [api-contract-standards, resilience-patterns]
sources:
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
  - https://medium.com/@amrelsayed.mohamed/catalog-of-microservice-anti-patterns-and-bad-smells-30ebe5a1214e
  - https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design
---

## Summary

Lack of Communication Standards means each team picks its own protocols,
payload formats, error handling, and retry rules. Nothing is technically wrong
in any single service, but together they do not fit. Every new integration then
starts with a negotiation.

## Why it hurts

Integration cost grows with each service, because callers must learn a new style
every time. Error handling becomes unreliable: a caller cannot tell a retryable
failure from a permanent one if every service reports errors differently.
Monitoring suffers too, since there is no common field to correlate requests.
Mistakes repeat, because no shared rule captures what the last team learned.

## How to spot it

- Compare error payloads across services. Different field names for the error
  code or message is direct evidence.
- Compare field naming and date formats in two or three API responses.
- Count how many services publish an OpenAPI or protobuf contract. Partial
  coverage is the signal.
- Grep for timeout and retry settings. Values that differ by an order of
  magnitude with no explanation mean there is no policy.
- Check if there is a written API guideline in the repository or wiki. If not,
  assume the standard does not exist.

## Solutions

### 1. Define shared API contracts

- **Do:** Pick the default style, for example REST with JSON for external calls
  and gRPC for internal high traffic calls, and write down naming, versioning,
  and pagination rules.
- **Fits when:** The number of services is growing and new ones appear often.
- **Cost:** Existing services need to be aligned over time, which is slow work
  with no visible feature value.

### 2. Standardise errors, timeouts, and retries

- **Do:** Agree on one error response shape, one set of retryable status codes,
  and default timeout and backoff values. Ship them in a small client library or
  a service template.
- **Fits when:** Failures spread between services or retries cause load spikes.
- **Cost:** A shared client library must be versioned carefully, or it becomes a
  `shared-libraries` problem.

### 3. Document every API in the same way

- **Do:** Require an OpenAPI or protobuf file per service, generated from code
  where possible, and publish them in one catalog.
- **Fits when:** Teams waste time asking each other how an API works.
- **Cost:** Documentation drifts unless it is generated and checked in CI.

## Related

Lack of Communication Standards makes `no-api-versioning` and
`insufficient-monitoring` worse, because there is no shared contract or shared
correlation field to build on.

## Sources

- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
- Catalog of Microservice Anti-Patterns and Bad Smells, Medium.
- Designing the infrastructure persistence layer, Microsoft .NET docs.
