---
id: "competition-team-registration"
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

# competition_team_registration

Written by the agents of the modernization flow while they worked. Every section is an unapproved proposal until a person reviews it.

## business-analyst - use-cases - run ff3b0c46 (unapproved proposal)

This use case manages the registration of a [[systems/soccer-mybatis/code/entities/team|team]] in an existing [[systems/soccer-mybatis/code/entities/competition|competition]]. It validates the existence of both the competition and the team before creating the association in the `competition_teams` table.

**Reads:**
- `competitions.id`, `competitions.name`, `competitions.season`, `competitions.created_at` (to validate competition existence).
- `teams.id`, `teams.name`, `teams.city`, `teams.coach`, `teams.country`, `teams.created_at` (to validate team existence).
- `competition_teams.competition_id`, `competition_teams.team_id` (to validate existing registrations).

Evidence: 
- [[soccer.mapper.CompetitionMapper.findById]] in `src/main/resources/soccer/mapper/CompetitionMapper.xml` (line 9).
- [[soccer.mapper.CompetitionMapper.findTeams]] in `src/main/resources/soccer/mapper/CompetitionMapper.xml` (line 20).
- [[soccer.mapper.CompetitionMapper.countRegistration]] in `src/main/resources/soccer/mapper/CompetitionMapper.xml` (line 27).

**Writes:**
- `competition_teams.competition_id`
- `competition_teams.team_id`

Evidence: [[soccer.mapper.CompetitionMapper.registerTeam]] in `src/main/resources/soccer/mapper/CompetitionMapper.xml` (line 31).
