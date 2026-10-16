---
id: "player-removal"
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

# player_removal

Written by the agents of the modernization flow while they worked. Every section is an unapproved proposal until a person reviews it.

## business-analyst - use-cases - run ff3b0c46 (unapproved proposal)

This use case handles the removal of an existing [[systems/soccer-mybatis/code/entities/player|player]] from the system. It validates the player's existence before deletion.

**Reads:**
- `players.id`, `players.team_id`, `players.shirt_number` (to validate player existence).

Evidence: [[soccer.mapper.PlayerMapper.findByTeamIdAndNumber]] in `src/main/resources/soccer/mapper/PlayerMapper.xml` (line 13).

**Writes:**
- Deletes records from `players` table (all fields).

Evidence: [[soccer.mapper.PlayerMapper.deleteById]] in `src/main/resources/soccer/mapper/PlayerMapper.xml` (line 38).
