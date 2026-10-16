---
id: "plan-ff3b0c46-data-decisions"
artifact_type: architecture_decision
status: draft
source_repository: ""
source_commit: ""
confidence: estimated
reviewer: ""
updated_at: "2026-10-14"
tags:
  - architecture-decision
  - planner
---

# Data ownership and access (plan soccer-mybatis-ff3b0c46-plan)

Written by the planner from the plan approved by Juan David, for [[systems/soccer-mybatis/architecture/runs/ff3b0c46|run ff3b0c46]]. Draft: review before relying on it.

## Decision

| Entity | Owner | Consumers and how they reach it | Owner decided by |
| --- | --- | --- | --- |
| competition_teams | [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-b\|Service B]] | [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-a\|Service A]] (api) | partition |
| players | [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-c\|Service C]] | [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-a\|Service A]] (api) | partition |
| teams | [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-a\|Service A]] | [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-c\|Service C]] (api) | partition |

## Waves

- Wave 1: [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-b|Service B]]
- Wave 2: [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-c|Service C]], [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-a|Service A]]

## Open questions

None.
