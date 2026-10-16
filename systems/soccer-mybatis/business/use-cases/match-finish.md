---
id: "match-finish"
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

# match_finish

Written by the agents of the modernization flow while they worked. Every section is an unapproved proposal until a person reviews it.

## business-analyst - use-cases - run ff3b0c46 (unapproved proposal)

This use case marks an existing [[systems/soccer-mybatis/code/entities/match|match]] as finished. It updates the match status to reflect its completion.

**Reads:**
- `matches.id`
- `matches.finished`
- `matches.home_goals`
- `matches.away_goals`
- `matches.home_team_id`
- `matches.away_team_id`
- `matches.stadium`
- `matches.created_at` (to validate match existence).

Evidence: [[soccer.mapper.MatchMapper.findById]] in `src/main/resources/soccer/mapper/MatchMapper.xml` (line 5).

**Writes:**
- `matches.finished`

Evidence: [[soccer.mapper.MatchMapper.finish]] in `src/main/resources/soccer/mapper/MatchMapper.xml` (line 24).
