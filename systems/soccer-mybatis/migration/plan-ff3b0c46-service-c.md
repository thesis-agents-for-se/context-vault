---
id: "plan-ff3b0c46-service-c"
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

# Migration of Service C (plan soccer-mybatis-ff3b0c46-plan)

Written by the planner from the plan approved by Juan David. Draft: review before relying on it.

## What is extracted

Service [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-c|Service C]], from [[systems/soccer-mybatis/architecture/runs/ff3b0c46|run ff3b0c46]].

Service C owns matches, goals, and players entities; exposes APIs for all use cases; reads teams data only through Service A's API. No direct writes to teams.

## Order and dependencies

Wave 2. Relies on: no other service.

## Patterns applied

- [[patterns/patterns/database-per-service]]: Service C owns matches, goals, and players, requiring isolated schema.
- [[patterns/patterns/strangler-fig]]: Traffic can move gradually behind routes to avoid big-bang migration.
- [[patterns/patterns/anti-corruption-layer]]: Isolates Service C from Service A's domain model for teams.
- [[patterns/patterns/saga]]: Handles distributed transactions for cross-service operations like delete_team.

## Data of other services

- teams (owned by [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-a|Service A]]) through api

## Steps

| Step | Operation | Verification | Rollback |
| --- | --- | --- | --- |
| S-service-c-01 | create_service_schema | Service C starts against the new schema. | Revert datasource config to monolith schema. |
| S-service-c-02 | create_api_client | Contract test for GET /teams/{id} passes. | Revert to monolith data access for teams. |
| S-service-c-03 | create_anti_corruption_layer | Anti-corruption layer maps teams data to Service C's domain model. | Revert to direct API calls without mapping. |
| S-service-c-04 | migrate_data | Data migration script completes without errors.; Sample records match in monolith and Service C. | Revert to monolith schema and restore data from backup. |
| S-service-c-05 | create_api_endpoint | Contract tests for POST /api/matches, GET /api/matches/{id}, PATCH /api/matches/{id}/finish pass. | Remove endpoints; monolith path remains active. |
| S-service-c-06 | create_api_endpoint | Contract tests for POST /api/players, DELETE /api/players/{id}, GET /api/players pass. | Remove endpoints; monolith path remains active. |
| S-service-c-07 | replace_transaction_with_saga | Saga completes for delete_team use case.; Compensating transactions trigger on failure. | Revert to monolith transaction for delete_team. |
| S-service-c-08 | add_gateway_route | Requests to /api/matches and /api/players reach Service C. | Route /api/matches and /api/players back to monolith. |

## Risks and mitigations

- Data inconsistency during delete_team saga if Service A or C fails. (high): Implement compensating transactions and retry logic for sagas.
- Performance overhead from anti-corruption layer during high traffic. (medium): Cache teams data for read-heavy use cases (e.g., match_detail).

## Open questions

- What is the expected latency for teams API calls during peak traffic?
- Are there existing tests for saga rollback scenarios?
