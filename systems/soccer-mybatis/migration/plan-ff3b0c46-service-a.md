---
id: "plan-ff3b0c46-service-a"
artifact_type: migration_step
status: draft
source_repository: ""
source_commit: ""
confidence: estimated
reviewer: ""
updated_at: "2026-10-14"
tags:
  - migration-step
  - planner
---

# Migration of Service A (plan soccer-mybatis-ff3b0c46-plan)

Written by the planner from the plan approved by Juan David. Draft: review before relying on it.

## What is extracted

Service [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-a|Service A]], from [[systems/soccer-mybatis/architecture/runs/ff3b0c46|run ff3b0c46]].

Owns competitions and teams entities and their use cases (create_competition, create_team, register_team_to_competition). Exposes REST APIs for these use cases. Reads and writes foreign entities (competition_teams, players) only through negotiated APIs.

## Order and dependencies

Wave 2. Relies on: no other service.

## Patterns applied

- [[patterns/patterns/database-per-service]]: Competitions and teams are owned exclusively by Service A, justifying a dedicated schema.
- [[patterns/patterns/strangler-fig]]: Traffic for Service A's use cases can be gradually routed to the new service without disrupting the monolith.
- [[patterns/patterns/api-contract-standards]]: Service A interacts with foreign entities (competition_teams, players) via APIs, requiring contract tests to ensure compatibility.

## Data of other services

- competition_teams (owned by [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-b|Service B]]) through api
- players (owned by [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-c|Service C]]) through api

## Steps

| Step | Operation | Verification | Rollback |
| --- | --- | --- | --- |
| S-service-a-01 | create_service_schema | Service A starts and connects to the new schema without errors. | Revert datasource configuration to point to the monolith schema. |
| S-service-a-02 | create_api_client | API client compiles and passes contract tests for competition_teams API. | Revert to direct SQL queries for competition_teams. |
| S-service-a-03 | create_api_client | API client compiles and passes contract tests for players API. | Revert to direct SQL queries for players. |
| S-service-a-04 | create_api_endpoint | Contract tests for POST /api/competitions, POST /api/teams, and POST /api/competitions/{id}/teams pass. | Remove the endpoints; the monolith path still works. |
| S-service-a-05 | create_contract_test | Contract tests for competition_teams and players APIs pass. | Remove the contract tests. |
| S-service-a-06 | add_gateway_route | Requests to /api/competitions, /api/teams, and /api/competitions/{id}/teams reach Service A. | Route traffic back to the monolith. |

## Risks and mitigations

- Data consistency during cross-service operations (e.g., register_team_to_competition) may fail if Service B or Service C are unavailable. (high): Implement retry policies and circuit breakers for API calls. Use contract tests to verify API compatibility.
- Service A's API calls to Service B and Service C may introduce latency for use cases requiring foreign data (e.g., players). (medium): Optimize API calls with caching for read-heavy foreign data (e.g., players). Monitor performance and adjust as needed.
- The proposal departs from decision seq 7 (Service C uses sagas for cross-service transactions) by not assigning sagas to Service C. (medium): Clarify with stakeholders whether sagas should be implemented in Service A or Service C for register_team_to_competition.

## Open questions

- Are there existing contract tests for Service B and Service C APIs that Service A can reuse?
- What is the expected latency for API calls to Service B and Service C, and is caching required?
- Should sagas for register_team_to_competition be implemented in Service A or Service C?
