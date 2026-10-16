---
id: "player-addition"
artifact_type: "use_case"
status: "draft"
system: "soccer-mybatis"
run_id: "ff3b0c462c284652bdc363b871bcc785"
proposal: true
written_by: "agents"
tags:
  - "use-case"
  - "agent"
---

# player_addition

Written by the agents of the modernization flow while they worked. Every section is an unapproved proposal until a person reviews it.

## business-analyst - use-cases - run ff3b0c46 (unapproved proposal)

This use case handles the addition of a new [[systems/soccer-mybatis/code/entities/player|player]] to an existing [[systems/soccer-mybatis/code/entities/team|team]]. It validates the uniqueness of the player's shirt number within the team before insertion.

**Reads:**
- `teams.id`, `teams.name`, `teams.city`, `teams.coach`, `teams.country`, `teams.created_at` (to validate team existence).
- `players.team_id`, `players.shirt_number` (to validate shirt number uniqueness).

Evidence:
- [[soccer.mapper.TeamMapper.findById]] in `src/main/resources/soccer/mapper/TeamMapper.xml` (line 9).
- [[soccer.mapper.PlayerMapper.countByTeamIdAndNumber]] in `src/main/resources/soccer/mapper/PlayerMapper.xml` (line 9).

**Writes:**
- `players.name`
- `players.age`
- `players.position`
- `players.preferred_foot`
- `players.shirt_number`
- `players.team_id`
- `players.goals`
- `players.created_at`

Evidence: [[soccer.mapper.PlayerMapper.insert]] in `src/main/resources/soccer/mapper/PlayerMapper.xml` (line 33).
