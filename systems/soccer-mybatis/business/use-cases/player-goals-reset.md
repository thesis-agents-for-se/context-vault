---
id: "player-goals-reset"
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

# player_goals_reset

Written by the agents of the modernization flow while they worked. Every section is an unapproved proposal until a person reviews it.

## business-analyst - use-cases - run ff3b0c46 (unapproved proposal)

This use case resets the goal count for all [[systems/soccer-mybatis/code/entities/player|player]] records associated with a specific [[systems/soccer-mybatis/code/entities/team|team]]. It validates the team's existence before performing the update.

**Reads:**
- `teams.id`, `teams.name`, `teams.city`, `teams.coach`, `teams.country`, `teams.created_at` (to validate team existence).
- `players.id`, `players.team_id`, `players.goals` (to reset goals).

Evidence:
- [[soccer.mapper.TeamMapper.findById]] in `src/main/resources/soccer/mapper/TeamMapper.xml` (line 9).
- [[soccer.mapper.PlayerMapper.findByTeamId]] in `src/main/resources/soccer/mapper/PlayerMapper.xml` (line 19).

**Writes:**
- `players.goals`

Evidence: [[soccer.mapper.PlayerMapper.resetGoals]] in `src/main/resources/soccer/mapper/PlayerMapper.xml` (line 50).
