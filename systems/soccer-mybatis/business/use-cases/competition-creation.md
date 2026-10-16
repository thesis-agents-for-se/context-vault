---
id: "competition-creation"
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

# competition_creation

Written by the agents of the modernization flow while they worked. Every section is an unapproved proposal until a person reviews it.

## business-analyst - use-cases - run ff3b0c46 (unapproved proposal)

This use case handles the creation of a new [[systems/soccer-mybatis/code/entities/competition|competition]] in the system. It ensures the uniqueness of the competition name before inserting a new record.

**Reads:**
- `competitions.name` (to validate uniqueness). Evidence: [[soccer.mapper.CompetitionMapper.countByName]] in `src/main/resources/soccer/mapper/CompetitionMapper.xml` (line 5).

**Writes:**
- `competitions.created_at`
- `competitions.name`
- `competitions.season`

Evidence: [[soccer.mapper.CompetitionMapper.insert]] in `src/main/resources/soccer/mapper/CompetitionMapper.xml` (line 15).
