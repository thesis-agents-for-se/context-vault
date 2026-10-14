# Index

One line per entry. Read this first, then open only the files you need.

## Antipatterns

### Boundaries and granularity

| id | name | severity | summary |
|---|---|---|---|
| [`distributed-monolith`](antipatterns/boundaries/distributed-monolith.md) | Distributed Monolith | high | A Distributed Monolith is a system split into many deployable services that still has to be deployed as one piece. |
| [`mega-service`](antipatterns/boundaries/mega-service.md) | Mega Service | high | A Mega Service is one microservice that holds too many responsibilities. |
| [`nano-service`](antipatterns/boundaries/nano-service.md) | Nano Service | medium | Nano Service is the opposite of a Mega Service. |
| [`wrong-cuts`](antipatterns/boundaries/wrong-cuts.md) | Wrong Cuts | high | Wrong Cuts means the services were split along technical lines or along database tables, instead of along business capabilities. |

### Communication between services

| id | name | severity | summary |
|---|---|---|---|
| [`chatty-communication`](antipatterns/communication/chatty-communication.md) | Chatty Communication | high | Chatty Communication happens when one business operation needs many remote calls between services, often one after another. |
| [`cyclic-dependency`](antipatterns/communication/cyclic-dependency.md) | Cyclic Dependency | high | A Cyclic Dependency exists when two or more services call each other in a loop. |
| [`esb-misuse`](antipatterns/communication/esb-misuse.md) | ESB Misuse | medium | ESB Misuse means using a heavy Enterprise Service Bus as the central hub of a microservice system. |
| [`hardcoded-endpoints`](antipatterns/communication/hardcoded-endpoints.md) | Hardcoded Endpoints | medium | Hardcoded Endpoints means service addresses, IPs, or ports are written into the source code instead of resolved at runtime. |
| [`lack-of-communication-standards`](antipatterns/communication/lack-of-communication-standards.md) | Lack of Communication Standards | medium | Lack of Communication Standards means each team picks its own protocols, payload formats, error handling, and retry rules. |
| [`no-api-gateway`](antipatterns/communication/no-api-gateway.md) | No API Gateway | medium | No API Gateway means external clients call internal microservices directly, with no single entry point in front of them. |
| [`no-api-versioning`](antipatterns/communication/no-api-versioning.md) | No API Versioning | medium | No API Versioning means a service changes its public contract without offering a way for old clients to keep working. |
| [`service-chain`](antipatterns/communication/service-chain.md) | Service Chain | high | A Service Chain is a long line of services that must each call the next one to answer a single request. |

### Data, persistence and databases

| id | name | severity | summary |
|---|---|---|---|
| [`data-driven-migration`](antipatterns/persistence/data-driven-migration.md) | Data-Driven Migration | high | Data-Driven Migration means the move from monolith to microservices is planned around the existing database schema or around a new technology, instead of around business capabilities. |
| [`database-as-integration-point`](antipatterns/persistence/database-as-integration-point.md) | Database as Integration Point | high | Database as Integration Point means services integrate by reaching into each other's databases instead of calling APIs or consuming events. |
| [`distributed-transactions`](antipatterns/persistence/distributed-transactions.md) | Distributed Transactions | high | Distributed Transactions means using one ACID transaction that spans several services or several resources, usually through two-phase commit. |
| [`reporting-database`](antipatterns/persistence/reporting-database.md) | Reporting on the Transactional Database | medium | This antipattern is running heavy reporting and analytics queries against the production transactional database of a service, often from outside the service. |
| [`shared-database`](antipatterns/persistence/shared-database.md) | Shared Database | high | Shared Database means several microservices read and write the same schema, and often the same tables. |

### Deployment and operations

| id | name | severity | summary |
|---|---|---|---|
| [`bottleneck-service`](antipatterns/operations/bottleneck-service.md) | Bottleneck Service | high | A Bottleneck Service is a service that too many other services depend on. |
| [`insufficient-monitoring`](antipatterns/operations/insufficient-monitoring.md) | Insufficient Monitoring | high | Insufficient Monitoring means the system has no reliable way to see what happens across services: no distributed traces, no central logs, no useful metrics. |
| [`shared-libraries`](antipatterns/operations/shared-libraries.md) | Shared Libraries | medium | Shared Libraries becomes an antipattern when services depend on common code that holds business logic or domain models, and that code is not versioned properly. |

## Patterns

| id | name | solves |
|---|---|---|
| [`anti-corruption-layer`](patterns/anti-corruption-layer.md) | Anti-Corruption Layer | data-driven-migration, distributed-monolith, shared-database |
| [`api-composition`](patterns/api-composition.md) | API Composition | chatty-communication, wrong-cuts, nano-service, shared-database, reporting-database, no-api-gateway |
| [`api-contract-standards`](patterns/api-contract-standards.md) | API Contract Standards | lack-of-communication-standards, no-api-versioning, shared-libraries, insufficient-monitoring |
| [`api-gateway`](patterns/api-gateway.md) | API Gateway and Backends for Frontends | no-api-gateway, hardcoded-endpoints, no-api-versioning, esb-misuse |
| [`cqrs`](patterns/cqrs.md) | CQRS and Read Models | chatty-communication, reporting-database, shared-database |
| [`database-per-service`](patterns/database-per-service.md) | Database per Service | shared-database, database-as-integration-point, distributed-transactions, distributed-monolith, mega-service |
| [`domain-driven-decomposition`](patterns/domain-driven-decomposition.md) | Domain-Driven Decomposition | wrong-cuts, mega-service, nano-service, distributed-monolith, data-driven-migration, cyclic-dependency |
| [`event-driven-integration`](patterns/event-driven-integration.md) | Event-Driven Integration | chatty-communication, cyclic-dependency, shared-database, database-as-integration-point, distributed-transactions, esb-misuse, service-chain |
| [`observability-stack`](patterns/observability-stack.md) | Observability Stack | insufficient-monitoring, chatty-communication, service-chain, bottleneck-service, no-api-gateway |
| [`reporting-data-store`](patterns/reporting-data-store.md) | Reporting Data Store | reporting-database, database-as-integration-point, shared-database |
| [`resilience-patterns`](patterns/resilience-patterns.md) | Resilience Patterns | bottleneck-service, lack-of-communication-standards, chatty-communication, service-chain |
| [`saga`](patterns/saga.md) | Saga | distributed-transactions, service-chain, bottleneck-service |
| [`service-discovery`](patterns/service-discovery.md) | Service Discovery and External Configuration | hardcoded-endpoints, distributed-monolith |
| [`service-granularity-refactoring`](patterns/service-granularity-refactoring.md) | Service Granularity Refactoring | nano-service, mega-service, wrong-cuts, service-chain, shared-libraries, bottleneck-service, cyclic-dependency, esb-misuse |
| [`strangler-fig`](patterns/strangler-fig.md) | Strangler Fig | distributed-monolith, mega-service, data-driven-migration |
