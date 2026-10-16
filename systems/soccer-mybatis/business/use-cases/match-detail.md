---
id: "match-detail"
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

# match_detail

Written by the agents of the modernization flow while they worked. Every section is an unapproved proposal until a person reviews it.

## business-analyst - use-cases - run ff3b0c46 (unapproved proposal)

This use case retrieves the details of an existing [[systems/soccer-mybatis/code/entities/match|match]] in the system. It provides read-only access to match information such as teams, score, and stadium.

**Reads:**
- `matches.id`
- `matches.home_team_id`
- `matches.away_team_id`
- `matches.home_goals`
- `matches.away_goals`
- `matches.stadium`
- `matches.finished`
- `matches.created_at`

Evidence: [[soccer.mapper.MatchMapper.findById]] in `src/main/resources/soccer/mapper/MatchMapper.xml` (line 5).

**Writes:**
- None.
