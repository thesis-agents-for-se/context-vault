---
id: "team-detail"
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

# team_detail

Written by the agents of the modernization flow while they worked. Every section is an unapproved proposal until a person reviews it.

## business-analyst - use-cases - run ff3b0c46 (unapproved proposal)

This use case retrieves the details of an existing [[systems/soccer-mybatis/code/entities/team|team]] in the system, including its associated [[systems/soccer-mybatis/code/entities/player|player]] records. It provides read-only access to team and player information.

**Reads:**
- `teams.id`, `teams.name`, `teams.city`, `teams.coach`, `teams.country`, `teams.created_at`
- `players.id`, `players.team_id`

Evidence:
- [[soccer.mapper.TeamMapper.findById]] in `src/main/resources/soccer/mapper/TeamMapper.xml` (line 9).
- [[soccer.mapper.PlayerMapper.findByTeamId]] in `src/main/resources/soccer/mapper/PlayerMapper.xml` (line 19).

**Writes:**
- None.
