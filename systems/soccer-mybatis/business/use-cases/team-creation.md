---
id: "team-creation"
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

# team_creation

Written by the agents of the modernization flow while they worked. Every section is an unapproved proposal until a person reviews it.

## business-analyst - use-cases - run ff3b0c46 (unapproved proposal)

This use case handles the creation of a new [[systems/soccer-mybatis/code/entities/team|team]] in the system. It ensures the uniqueness of the team name before inserting a new record.

**Reads:**
- `teams.name` (to validate uniqueness).

Evidence: [[soccer.mapper.TeamMapper.countByName]] in `src/main/resources/soccer/mapper/TeamMapper.xml` (line 5).

**Writes:**
- `teams.name`
- `teams.city`
- `teams.coach`
- `teams.country`
- `teams.created_at`

Evidence: [[soccer.mapper.TeamMapper.insert]] in `src/main/resources/soccer/mapper/TeamMapper.xml` (line 15).
