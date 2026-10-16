---
id: "goal-scoring"
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

# goal_scoring

Written by the agents of the modernization flow while they worked. Every section is an unapproved proposal until a person reviews it.

## business-analyst - use-cases - run ff3b0c46 (unapproved proposal)

This use case records a goal in an existing [[systems/soccer-mybatis/code/entities/match|match]]. It updates the match score and the goal statistics of the [[systems/soccer-mybatis/code/entities/player|player]] who scored. It also creates a record in the `goals` table.

**Reads:**
- `matches.id`, `matches.home_goals`, `matches.away_goals`, `matches.home_team_id`, `matches.away_team_id`, `matches.stadium`, `matches.finished`, `matches.created_at` (to validate match existence).
- `players.id`, `players.team_id`, `players.shirt_number`, `players.goals` (to validate player existence and update statistics).

Evidence:
- [[soccer.mapper.MatchMapper.findById]] in `src/main/resources/soccer/mapper/MatchMapper.xml` (line 5).
- [[soccer.mapper.PlayerMapper.findByTeamIdAndNumber]] in `src/main/resources/soccer/mapper/PlayerMapper.xml` (line 13).

**Writes:**
- `goals.created_at`
- `goals.match_id`
- `goals.minute`
- `goals.player_id`
- `matches.home_goals` or `matches.away_goals` (depending on the team).
- `players.goals`

Evidence:
- [[soccer.mapper.GoalMapper.insert]] in `src/main/resources/soccer/mapper/GoalMapper.xml` (line 5).
- [[soccer.mapper.MatchMapper.updateScore]] in `src/main/resources/soccer/mapper/MatchMapper.xml` (line 20).
- [[soccer.mapper.PlayerMapper.addGoal]] in `src/main/resources/soccer/mapper/PlayerMapper.xml` (line 46).
