---
id: wrong-cuts
name: Wrong Cuts
category: boundaries
aliases: [Wrong Service Boundaries, Layered Services, Entity Services]
severity: high
detects_on: [repo-layout, code, schema]
signals:
  - Service names match technical layers, such as ui-service, logic-service, data-service.
  - Service names match single database tables, such as user-service, address-service, order-item-service.
  - A service only exposes create, read, update, and delete endpoints with no business rules.
  - One business use case always touches the same group of services.
  - Business rules live in the caller instead of the service that owns the data.
related: [nano-service, chatty-communication, mega-service, data-driven-migration]
solutions: [domain-driven-decomposition, service-granularity-refactoring, api-composition]
sources:
  - https://assets.ptidej.net/Publications/Documents/EuroPLoP20.doc.pdf
  - https://arxiv.org/abs/1908.04101
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
---

## Summary

Wrong Cuts means the services were split along technical lines or along database
tables, instead of along business capabilities. A common shape is one service
for the front end, one for business logic, and one for data access. Another
common shape is one service per table, each exposing plain CRUD.

## Why it hurts

With Wrong Cuts, one business change spreads across many services, because no
single service owns a complete capability. Cohesion inside each service is low
and coupling between them is high. Teams cannot work in parallel, since every
feature needs all of them. The system also becomes chatty, because a use case
must call several services to assemble one answer.

## How to spot it

- Read the service list. Names like `api-layer`, `business-layer`, or
  `persistence-service` are direct evidence of a layer split.
- Names that copy table names one to one suggest an entity split.
- Open the controllers. If a service has only `POST /x`, `GET /x/{id}`,
  `PUT /x/{id}`, `DELETE /x/{id}` and no rule or validation beyond field checks,
  it is a data wrapper, not a service.
- Trace one real use case, such as "place an order", through the code. Count how
  many services it touches. Four or more for a single simple flow is a warning.
- Look for business logic in an orchestrator or in the gateway. That means the
  logic had no home.

## Solutions

### 1. Decompose by business capability or subdomain

- **Do:** List the business capabilities first. Assign each capability one owner
  service, and move the data and rules for that capability into it.
- **Fits when:** The domain is understood and stakeholders can describe the
  processes.
- **Cost:** Requires moving code and data between services. Expect a period with
  duplicated code.

### 2. Measure cohesion and coupling, then merge or split

- **Do:** Compute how often services change together and how often they call
  each other. Merge services that always change together. Split services that
  hold two unrelated groups of operations.
- **Fits when:** You need evidence before a big refactor, or the domain is
  unclear.
- **Cost:** Metrics point at symptoms, not at the correct boundary. Use them to
  start the discussion, not to end it.

### 3. Hide the mess behind API Composition while you fix it

- **Do:** Add one aggregating service or endpoint per use case, so clients see a
  single coarse API while the wrong cuts are corrected underneath.
- **Fits when:** Clients are already suffering and a full redesign will take
  months.
- **Cost:** This hides the problem. It must be a step in a plan, not the plan.

## Related

Wrong Cuts often creates `chatty-communication` and `nano-service`. When the
split follows the old database schema, check `data-driven-migration`.

## Sources

- On the Study of Microservices Antipatterns: a Catalog Proposal, EuroPLoP 2020.
- Taibi and Lenarduzzi, Microservices Anti-Patterns: A Taxonomy, 2019.
- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
