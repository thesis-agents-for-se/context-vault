---
id: "match-creation"
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

# match_creation

Written by the agents of the modernization flow while they worked. Every section is an unapproved proposal until a person reviews it.

## business-analyst - use-cases - run ff3b0c46 (unapproved proposal)

This use case handles the creation of a new [[systems/soccer-mybatis/code/entities/match|match]] in the system. It initializes the match with basic details such as teams, stadium, and initial score.

**Reads:**
- None (direct insertion).

**Writes:**
- `matches.away_goals`
- `matches.away_team_id`
- `matches.created_at`
- `matches.finished`
- `matches.home_goals`
- `matches.home_team_id`
- `matches.stadium`

Evidence: [[soccer.mapper.MatchMapper.insert]] in `src/main/resources/soccer/mapper/MatchMapper.xml` (line 15).
