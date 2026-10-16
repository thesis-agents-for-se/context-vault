---
id: "player-listing"
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

# player_listing

Written by the agents of the modernization flow while they worked. Every section is an unapproved proposal until a person reviews it.

## business-analyst - use-cases - run ff3b0c46 (unapproved proposal)

This use case retrieves the list of [[systems/soccer-mybatis/code/entities/player|player]] records associated with a specific [[systems/soccer-mybatis/code/entities/team|team]]. It supports optional filtering by player position.

**Reads:**
- `teams.id`, `teams.name`, `teams.city`, `teams.coach`, `teams.country`, `teams.created_at` (to validate team existence).
- `players.id`, `players.team_id`, `players.position` (to list players, optionally filtered by position).

Evidence:
- [[soccer.mapper.TeamMapper.findById]] in `src/main/resources/soccer/mapper/TeamMapper.xml` (line 9).
- [[soccer.mapper.PlayerMapper.findByTeamId]] in `src/main/resources/soccer/mapper/PlayerMapper.xml` (line 19).
- [[soccer.mapper.PlayerMapper.findByTeamIdAndPosition]] in `src/main/resources/soccer/mapper/PlayerMapper.xml` (line 26).

**Writes:**
- None.
