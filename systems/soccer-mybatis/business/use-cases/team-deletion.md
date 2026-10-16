---
id: "team-deletion"
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

# team_deletion

Written by the agents of the modernization flow while they worked. Every section is an unapproved proposal until a person reviews it.

## business-analyst - use-cases - run ff3b0c46 (unapproved proposal)

This use case handles the deletion of an existing [[systems/soccer-mybatis/code/entities/team|team]] from the system. It validates dependencies such as active matches and deletes associated [[systems/soccer-mybatis/code/entities/player|player]] records in a cascading manner.

**Reads:**
- `teams.id`, `teams.name`, `teams.city`, `teams.coach`, `teams.country`, `teams.created_at` (to validate team existence).
- `matches.home_team_id`, `matches.away_team_id` (to validate active matches).
- `players.id`, `players.team_id` (to validate and delete associated players).

Evidence:
- [[soccer.mapper.TeamMapper.findById]] in `src/main/resources/soccer/mapper/TeamMapper.xml` (line 9).
- [[soccer.mapper.MatchMapper.countByTeamId]] in `src/main/resources/soccer/mapper/MatchMapper.xml` (line 11).
- [[soccer.mapper.PlayerMapper.findByTeamId]] in `src/main/resources/soccer/mapper/PlayerMapper.xml` (line 19).

**Writes:**
- Deletes records from `players` table (all fields).
- Deletes records from `teams` table (all fields).

Evidence:
- [[soccer.mapper.PlayerMapper.deleteByTeamId]] in `src/main/resources/soccer/mapper/PlayerMapper.xml` (line 42).
- [[soccer.mapper.TeamMapper.deleteById]] in `src/main/resources/soccer/mapper/TeamMapper.xml` (line 20).
