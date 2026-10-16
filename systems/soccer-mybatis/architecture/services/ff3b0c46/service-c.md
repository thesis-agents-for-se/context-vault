---
id: "service-c"
artifact_type: "service_boundary"
status: "draft"
system: "soccer-mybatis"
run_id: "ff3b0c462c284652bdc363b871bcc785"
proposal: true
written_by: "agents"
tags:
  - "service"
  - "agent"
---

# Service C

Written by the agents of the modernization flow while they worked. Every section is an unapproved proposal until a person reviews it.

## partition-reviewer - result - run ff3b0c46 (unapproved proposal)

### Entities and Fields
This service contains the following entities and their fields, as derived from the [[systems/soccer-mybatis/architecture/runs/ff3b0c46|run ff3b0c46]] and [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-c|Service C]] details:

- **[[systems/soccer-mybatis/code/entities/matches|matches]]**: `id`, `created_at`, `home_team_id`, `away_team_id`, `stadium`, `home_goals`, `away_goals`, `finished`
- **[[systems/soccer-mybatis/code/entities/goals|goals]]**: `id`, `created_at`, `match_id`, `player_id`, `minute`
- **[[systems/soccer-mybatis/code/entities/players|players]]**: `id`, `created_at`, `name`, `shirt_number`, `age`, `preferred_foot`, `position`, `goals`, `team_id`

### Use Cases
The service is responsible for the following use cases, based on the [[systems/soccer-mybatis/architecture/runs/ff3b0c46|run ff3b0c46]] and [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-c|Service C]] evidence:

- **[[systems/soccer-mybatis/business/use-cases/match-creation|match_creation]]**: Writes all fields of [[systems/soccer-mybatis/code/entities/matches|matches]].
- **[[systems/soccer-mybatis/business/use-cases/create-match|Create match]]**: Reads fields from [[systems/soccer-mybatis/code/entities/players|players]] and [[systems/soccer-mybatis/code/entities/teams|teams]] (though [[systems/soccer-mybatis/code/entities/teams|teams]] is not owned by this service).
- **[[systems/soccer-mybatis/business/use-cases/match-detail|match_detail]]**: Reads all fields of [[systems/soccer-mybatis/code/entities/matches|matches]].
- **[[systems/soccer-mybatis/business/use-cases/match-finish|match_finish]]**: Reads all fields of [[systems/soccer-mybatis/code/entities/matches|matches]] and writes to `matches.finished`.
- **[[systems/soccer-mybatis/business/use-cases/record-goal|record_goal]]**: Writes to all fields of [[systems/soccer-mybatis/code/entities/goals|goals]] and updates `matches.home_goals`, `matches.away_goals`, and `players.goals`. It also reads fields from [[systems/soccer-mybatis/code/entities/matches|matches]], [[systems/soccer-mybatis/code/entities/players|players]], and [[systems/soccer-mybatis/code/entities/teams|teams]].
- **[[systems/soccer-mybatis/business/use-cases/delete-team|delete_team]]**: Writes to all fields of [[systems/soccer-mybatis/code/entities/players|players]] and [[systems/soccer-mybatis/code/entities/teams|teams]] (though [[systems/soccer-mybatis/code/entities/teams|teams]] is not owned by this service). It also reads fields from [[systems/soccer-mybatis/code/entities/matches|matches]], [[systems/soccer-mybatis/code/entities/players|players]], and [[systems/soccer-mybatis/code/entities/teams|teams]].
- **[[systems/soccer-mybatis/business/use-cases/get-team-details|get_team_details]]**: Reads fields from [[systems/soccer-mybatis/code/entities/players|players]] and [[systems/soccer-mybatis/code/entities/teams|teams]].
- **[[systems/soccer-mybatis/business/use-cases/list-players|list_players]]**: Reads fields from [[systems/soccer-mybatis/code/entities/players|players]] and [[systems/soccer-mybatis/code/entities/teams|teams]].
- **[[systems/soccer-mybatis/business/use-cases/add-player|add_player]]**: Writes and reads all fields of [[systems/soccer-mybatis/code/entities/players|players]].
- **[[systems/soccer-mybatis/business/use-cases/remove-player|remove_player]]**: Writes and reads all fields of [[systems/soccer-mybatis/code/entities/players|players]].
- **[[systems/soccer-mybatis/business/use-cases/reset-player-goals|reset_player_goals]]**: Writes to `players.goals` and reads fields from [[systems/soccer-mybatis/code/entities/players|players]] and [[systems/soccer-mybatis/code/entities/teams|teams]].
- **[[systems/soccer-mybatis/business/use-cases/get-match|Get match]]**: Reads fields from [[systems/soccer-mybatis/code/entities/players|players]] and [[systems/soccer-mybatis/code/entities/teams|teams]].
- **[[systems/soccer-mybatis/business/use-cases/finish-match|Finish match]]**: Reads fields from [[systems/soccer-mybatis/code/entities/players|players]] and [[systems/soccer-mybatis/code/entities/teams|teams]].

### Relationships
- **Bidirectional Relationship with [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-a|Service A]]**: Shares multiple fields from [[systems/soccer-mybatis/code/entities/teams|teams]] and [[systems/soccer-mybatis/code/entities/players|players]], including `teams.id`, `teams.created_at`, `teams.name`, `teams.city`, `teams.country`, `teams.coach`, `players.id`, `players.created_at`, `players.name`, `players.shirt_number`, `players.age`, `players.preferred_foot`, `players.goals`, and `players.team_id`.

### Observations
- This service is the largest in the partition, containing **65% of the fields** and **87% of the use cases** (evidence from [[evaluacion]]).
- The grouping of [[systems/soccer-mybatis/code/entities/matches|matches]], [[systems/soccer-mybatis/code/entities/goals|goals]], and [[systems/soccer-mybatis/code/entities/players|players]] is justified by:
  - **Transactional affinity**: The [[systems/soccer-mybatis/business/use-cases/record-goal|record_goal]] and [[systems/soccer-mybatis/business/use-cases/delete-team|delete_team]] use cases write to multiple entities within this service, demonstrating a need for atomicity.
  - **Semantic Proximity**: The entities are closely related in the domain model, as evidenced by the [[acoplamiento]] queries.
  - **Consistency Criticality**: The [[systems/soccer-mybatis/code/entities/goals|goals]] entity has a **High** consistency criticality, requiring atomic updates with [[systems/soccer-mybatis/code/entities/matches|matches]] and [[systems/soccer-mybatis/code/entities/players|players]] (evidence from [[acoplamiento]]).
- The service exhibits high coupling with [[systems/soccer-mybatis/architecture/services/ff3b0c46/service-a|Service A]] due to shared fields from [[systems/soccer-mybatis/code/entities/teams|teams]] and [[systems/soccer-mybatis/code/entities/players|players]].
