---
id: "configuration"
artifact_type: "architecture_decision"
status: "draft"
system: "soccer-mybatis"
run_id: "ff3b0c462c284652bdc363b871bcc785"
proposal: true
written_by: "agents"
tags:
  - "decision"
  - "agent"
---

# configuration

Written by the agents of the modernization flow while they worked. Every section is an unapproved proposal until a person reviews it.

## configuration-analyst-business - configuration - run ff3b0c46 (unapproved proposal)

### Criteria Prioritization for Service Cutting in [[systems/soccer-mybatis/architecture/runs/ff3b0c46|run ff3b0c46]]

This section documents the prioritization of criteria used for service cutting, based on static analysis, inferred metrics, and estimated business rules. No expert validation or runtime telemetry was available.

---

#### **High Priority Criteria**

##### **1. Security Contextuality**
**Weight:** `8` (Very High)
**Rationale:**
- The `ROLE_ADMIN` role has exclusive access to critical operations like `TeamController.deleteTeam` and `TeamController.resetGoals`.
- Entities [[systems/soccer-mybatis/code/entities/teams|teams]] and [[systems/soccer-mybatis/code/entities/players|players]] contain sensitive data (e.g., `city`, `country`) classified as PII.
**Evidence:**
- `metric:security_contextuality` (E403, E404)
- `metric:security_criticality` (E381)

##### **2. Consistency Criticality**
**Weight:** `8` (Very High)
**Rationale:**
- Entities like [[systems/soccer-mybatis/code/entities/competitions|competitions]], [[systems/soccer-mybatis/code/entities/goals|goals]], [[systems/soccer-mybatis/code/entities/matches|matches]], [[systems/soccer-mybatis/code/entities/players|players]], and [[systems/soccer-mybatis/code/entities/teams|teams]] have non-confluent pairs identified in `metric:consistency_criticality`.
- Operations like `AUTO_INCREMENT` in `INSERT` statements and foreign keys without `ON DELETE CASCADE` require strict consistency.
**Evidence:**
- `metric:consistency_criticality` (E388, E389, E390, E391, E392)

##### **3. Semantic Proximity**
**Weight:** `5` (High)
**Rationale:**
- Strong semantic proximity between [[systems/soccer-mybatis/code/entities/teams|teams]] and [[systems/soccer-mybatis/code/entities/players|players]], as well as [[systems/soccer-mybatis/code/entities/matches|matches]] and [[systems/soccer-mybatis/code/entities/goals|goals]].
- Transactional operations like `TeamService.deleteTeam` and `MatchService.scoreGoal` group these entities.
**Evidence:**
- `metric:consistency_constraint` (E376, E377, E378, E379)

##### **4. Consistency Constraint**
**Weight:** `5` (High)
**Rationale:**
- Transactional affinity in code and critical invariants in the DDL suggest strong consistency constraints.
- Operations like `record_goal` ([[systems/soccer-mybatis/business/use-cases/record-goal|record_goal]]) and `delete_team` ([[systems/soccer-mybatis/business/use-cases/delete-team|delete_team]]) require atomicity.
**Evidence:**
- `metric:consistency_constraint` (E375, E376, E377, E378)

---

#### **Medium Priority Criteria**

##### **5. Security Criticality**
**Weight:** `5` (High)
**Rationale:**
- [[systems/soccer-mybatis/code/entities/teams|teams]] contains sensitive columns (`city`, `country`) classified as PII.
**Evidence:**
- `metric:security_criticality` (E381)

##### **6. Latency**
**Weight:** `3` (Medium)
**Rationale:**
- Latency is critical for operations like `record_goal` ([[systems/soccer-mybatis/business/use-cases/record-goal|record_goal]]) and `view_match_score` ([[systems/soccer-mybatis/business/use-cases/view-match-score|view_match_score]]).
**Evidence:**
- `doc:2:Soccer league - How the system is used.txt` (E352, E354)

##### **7. Availability Criticality**
**Weight:** `3` (Medium)
**Rationale:**
- Documentation emphasizes latency for operations like `record_goal` and `view_match_score`.
**Evidence:**
- `doc:2:Soccer league - How the system is used.txt` (E352, E354)

##### **8. Security Constraint**
**Weight:** `3` (Medium)
**Rationale:**
- Sensitive data in [[systems/soccer-mybatis/code/entities/teams|teams]] and restricted access to `ROLE_ADMIN` suggest security constraints.
**Evidence:**
- `metric:security_criticality` (E381)

---

#### **Low Priority Criteria**

##### **9. Identity & Lifecycle Commonality**
**Weight:** `1` (Low)
**Rationale:**
- Lifecycle affinity between entities is limited (e.g., [[systems/soccer-mybatis/code/entities/players|players]] and [[systems/soccer-mybatis/code/entities/teams|teams]] have low Jaccard affinity).
**Evidence:**
- `metric:identity_lifecycle` (E370, E371, E372, E373, E374)

##### **10. Storage Similarity**
**Weight:** `1` (Low)
**Rationale:**
- Tables have disparate storage footprints (e.g., [[systems/soccer-mybatis/code/entities/teams|teams]] at 1392 bytes vs. [[systems/soccer-mybatis/code/entities/goals|goals]] at 36 bytes).
**Evidence:**
- `metric:storage_similarity` (E407, E408, E409, E410, E411)

##### **11. Content Volatility**
**Weight:** `1` (Low)
**Rationale:**
- Data volatility is estimated to be low due to the domain nature (e.g., infrequent updates to teams, players, or matches).
**Evidence:**
- `doc:0:Soccer league - Business rules.txt` (E336, E337, E338)

---

#### **Very Low Priority Criteria**

##### **12. Shared Owner**
**Weight:** `0.5` (Very Low)
**Rationale:**
- No evidence of shared ownership between entities.
**Evidence:**
- `approved:erm` (E000, E001, E002, E003, E004)

##### **13. Structural Volatility**
**Weight:** `0.5` (Very Low)
**Rationale:**
- No evidence of frequent schema changes in the DDL or codebase.
**Evidence:**
- `approved:erm` (E000, E001, E002, E003, E004)

##### **14. Predefined Service Constraint**
**Weight:** `0.5` (Very Low)
**Rationale:**
- No explicit architectural requirements define predefined services.
**Evidence:**
- `metric:identity_lifecycle` (E371, E372)

## configuration-analyst-code - configuration - run ff3b0c46 (unapproved proposal)

### Criteria Prioritization for Service Cutting

This section documents the prioritization of criteria used for service cutting in the current [[systems/soccer-mybatis/architecture/runs/ff3b0c46|run ff3b0c46]], based on static analysis, inferred metrics, and documented requirements. The weights reflect the relevance of each criterion to the domain and technical constraints.

---

#### **1. Identity & Lifecycle Commonality**
**Weight:** `1` (Low)
**Rationale:**
Low affinity between entities (e.g., [[systems/soccer-mybatis/code/entities/players|players]] and [[systems/soccer-mybatis/code/entities/teams|teams]] with `0.25` Jaccard affinity). No shared primary keys or `CASCADE` operations in foreign keys.
**Evidence:**
- [[metric:identity_lifecycle]]: Affinity metrics and FK analysis.

---

#### **2. Semantic Proximity**
**Weight:** `5` (High)
**Rationale:**
Strong semantic relationships between entities (e.g., [[systems/soccer-mybatis/code/entities/players|players]] belong to [[systems/soccer-mybatis/code/entities/teams|teams]], [[systems/soccer-mybatis/code/entities/matches|matches]] involve [[systems/soccer-mybatis/code/entities/goals|goals]]). Coherence in domain rules and transactional operations.
**Evidence:**
- [[doc:0:Soccer league - Business rules.txt]]
- [[metric:consistency_constraint]]: Transactional affinity between [[systems/soccer-mybatis/code/entities/players|players]] and [[systems/soccer-mybatis/code/entities/teams|teams]].

---

#### **3. Shared Owner**
**Weight:** `0.5` (Very Low)
**Rationale:**
No evidence of shared ownership. Roles like `Administrators` interact with multiple entities but without explicit organizational boundaries.
**Evidence:**
- [[doc:1:Soccer league - How the system is used.txt]]: Role descriptions.

---

#### **4. Latency**
**Weight:** `3` (Moderate)
**Rationale:**
Critical for operations like [[systems/soccer-mybatis/business/use-cases/record-a-goal|Record a goal]] and [[systems/soccer-mybatis/business/use-cases/show-the-scoreboard-of-a-match|Show the scoreboard of a match]], but no SLOs or telemetry data available.
**Evidence:**
- [[doc:2:Soccer league - How the system is used.txt]]: Latency requirements.

---

#### **5. Security Contextuality**
**Weight:** `8` (Very High)
**Rationale:**
Differentiated security contexts for `ROLE_ADMIN` (e.g., access to [[systems/soccer-mybatis/code/entities/players|players]] and [[systems/soccer-mybatis/code/entities/teams|teams]]). [[systems/soccer-mybatis/code/entities/teams|teams]] contains PII columns (`city`, `country`).
**Evidence:**
- [[metric:security_contextuality]]: Role-based access.
- [[metric:security_criticality]]: Sensitivity classification.

---

#### **6. Structural Volatility**
**Weight:** `0.5` (Very Low)
**Rationale:**
No evidence of frequent structural changes. Core entities (e.g., [[systems/soccer-mybatis/code/entities/teams|teams]], [[systems/soccer-mybatis/code/entities/players|players]]) have stable fields.
**Evidence:**
- [[approved:erm]]: Data model stability.

---

#### **7. Consistency Criticality**
**Weight:** `8` (Very High)
**Rationale:**
Non-confluent pairs in entities like [[systems/soccer-mybatis/code/entities/competitions|competitions]], [[systems/soccer-mybatis/code/entities/goals|goals]], and [[systems/soccer-mybatis/code/entities/teams|teams]]. Critical transactional operations (e.g., [[systems/soccer-mybatis/architecture/services/ff3b0c46/matchservice-scoregoal|MatchService.scoreGoal]]).
**Evidence:**
- [[metric:consistency_criticality]]: DDL analysis and transactional risks.

---

#### **8. Availability Criticality**
**Weight:** `3` (Moderate)
**Rationale:**
Relevant for real-time operations (e.g., [[systems/soccer-mybatis/business/use-cases/record-a-goal|Record a goal]]), but no SLOs or telemetry data available.
**Evidence:**
- [[doc:2:Soccer league - How the system is used.txt]]: Availability requirements.

---

#### **9. Content Volatility**
**Weight:** `0.5` (Very Low)
**Rationale:**
No evidence of high data volatility. Git commits reflect code changes, not frequent data writes.
**Evidence:**
- [[approved:erm]]: Stable fields like `created_at`.

---

#### **10. Storage Similarity**
**Weight:** `1` (Low)
**Rationale:**
Significant differences in storage requirements (e.g., [[systems/soccer-mybatis/code/entities/teams|teams]] at 1392 bytes vs. [[systems/soccer-mybatis/code/entities/goals|goals]] at 36 bytes).
**Evidence:**
- [[metric:storage_similarity]]: Per-row storage estimates.

---

#### **11. Security Criticality**
**Weight:** `3` (Moderate)
**Rationale:**
[[systems/soccer-mybatis/code/entities/teams|teams]] contains PII columns (`city`, `country`). Other entities are classified as `Public`.
**Evidence:**
- [[metric:security_criticality]]: Sensitivity classification.

---

#### **12. Consistency Constraint**
**Weight:** `5` (High)
**Rationale:**
Transactional invariants (e.g., [[systems/soccer-mybatis/architecture/services/ff3b0c46/matchservice-scoregoal|MatchService.scoreGoal]] for [[systems/soccer-mybatis/code/entities/goals|goals]] and [[systems/soccer-mybatis/code/entities/matches|matches]]). Strong consistency requirements.
**Evidence:**
- [[metric:consistency_constraint]]: Transactional affinity metrics.

---

#### **13. Predefined Service Constraint**
**Weight:** `0.5` (Very Low)
**Rationale:**
Clustering suggestions (e.g., [[systems/soccer-mybatis/code/entities/teams|teams]]-[[systems/soccer-mybatis/code/entities/players|players]], [[systems/soccer-mybatis/code/entities/matches|matches]]-[[systems/soccer-mybatis/code/entities/goals|goals]]) are inferred, not documented.
**Evidence:**
- [[metric:identity_lifecycle]]: Affinity metrics.

---

#### **14. Security Constraint**
**Weight:** `3` (Moderate)
**Rationale:**
[[systems/soccer-mybatis/code/entities/teams|teams]] contains PII columns. `ROLE_ADMIN` has access to critical operations.
**Evidence:**
- [[metric:security_criticality]]: Sensitivity classification.
- [[metric:security_contextuality]]: Role-based access.

## configuration-analyst-risk - configuration - run ff3b0c46 (unapproved proposal)

### Risk Analyst Input: Criteria Weights for Service Cutting

This section outlines the proposed weights for each criterion in the service cutting process, based on the analysis of the current run [[systems/soccer-mybatis/architecture/runs/ff3b0c46|run ff3b0c46]]. The weights prioritize criteria that drive cohesive, secure, and consistent service boundaries.

---

#### **Proposed Weights**

| **Criterion**                     | **Weight** | **Basis**       | **Confidence** | **Key Rationale**                                                                                                                                                                                                 |
|--------------------------------------|------------|-----------------|----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [[systems/soccer-mybatis/code/entities/identity-lifecycle-commonality|Identity & Lifecycle Commonality]] | 1          | inferred        | medium         | Low affinity (e.g., 0.25 for [[systems/soccer-mybatis/code/entities/players|players]]-[[systems/soccer-mybatis/code/entities/teams|teams]]). No CASCADE in DDL, suggesting independent lifecycles.                                                                                         |
| [[systems/soccer-mybatis/code/entities/semantic-proximity|Semantic Proximity]]         | 5          | inferred        | high           | Strong semantic proximity in transactional operations (e.g., [[systems/soccer-mybatis/business/use-cases/delete-team|delete_team]] and [[systems/soccer-mybatis/business/use-cases/add-player|add_player]]). Domain cohesion in soccer league.                                                          |
| [[systems/soccer-mybatis/code/entities/shared-owner|Shared Owner]]               | 0.5        | estimated       | low            | No evidence of shared ownership. Documentation lacks organizational structure.                                                                                                                                    |
| [[systems/soccer-mybatis/code/entities/latency|Latency]]                    | 3          | estimated       | low            | Critical for [[systems/soccer-mybatis/business/use-cases/record-goal|record_goal]] and [[systems/soccer-mybatis/business/use-cases/match-detail|match_detail]], described as immediate in documentation. No SLOs defined.                                                                                     |
| [[systems/soccer-mybatis/code/entities/security-contextuality|Security Contextuality]]    | 8          | inferred        | medium         | Differentiated security context for [[role:ROLE_ADMIN]] (e.g., [[systems/soccer-mybatis/business/use-cases/delete-team|delete_team]]). Entities like [[systems/soccer-mybatis/code/entities/players|players]] and [[systems/soccer-mybatis/code/entities/teams|teams]] share this context.                                              |
| [[systems/soccer-mybatis/code/entities/structural-volatility|Structural Volatility]]     | 0.5        | estimated       | low            | No evidence of frequent schema changes. Entities like [[systems/soccer-mybatis/code/entities/teams|teams]] and [[systems/soccer-mybatis/code/entities/players|players]] have stable fields.                                                                                                |
| [[systems/soccer-mybatis/code/entities/consistency-criticality|Consistency Criticality]]    | 8          | inferred        | medium         | Non-confluent pairs in [[systems/soccer-mybatis/code/entities/teams|teams]], [[systems/soccer-mybatis/code/entities/competitions|competitions]], etc. Critical operations like `deleteById` require transactions to avoid inconsistencies.                                                      |
| [[systems/soccer-mybatis/code/entities/availability-criticality|Availability Criticality]]  | 3          | estimated       | low            | Low latency critical for [[systems/soccer-mybatis/business/use-cases/record-goal|record_goal]] and [[systems/soccer-mybatis/business/use-cases/match-detail|match_detail]], but no SLOs defined.                                                                                                             |
| [[systems/soccer-mybatis/code/entities/content-volatility|Content Volatility]]        | 1          | estimated       | low            | Data like [[systems/soccer-mybatis/code/entities/teams|teams]] and [[systems/soccer-mybatis/code/entities/players|players]] registered before the season and rarely change.                                                                                                                 |
| [[systems/soccer-mybatis/code/entities/storage-similarity|Storage Similarity]]        | 0.5        | inferred        | medium         | Disparate storage requirements (e.g., [[systems/soccer-mybatis/code/entities/teams|teams]] at 1392 bytes/row vs. [[systems/soccer-mybatis/code/entities/goals|goals]] at 36 bytes/row).                                                                                                    |
| [[systems/soccer-mybatis/code/entities/security-criticality|Security Criticality]]      | 5          | inferred        | medium         | [[systems/soccer-mybatis/code/entities/teams|teams]] contains PII (e.g., `city`, `country`). Administrative operations require strict access control.                                                                                                 |
| [[systems/soccer-mybatis/code/entities/consistency-constraint|Consistency Constraint]]    | 5          | inferred        | medium         | Transactional affinity in [[systems/soccer-mybatis/business/use-cases/score-goal|score_goal]] (writes to [[systems/soccer-mybatis/code/entities/goals|goals]] and [[systems/soccer-mybatis/code/entities/matches|matches]]). Invariants require atomicity.                                                                              |
| [[systems/soccer-mybatis/code/entities/predefined-service-constraint|Predefined Service Constraint]] | 1          | estimated       | low            | [[systems/soccer-mybatis/code/entities/competitions|competitions]] described as independent, but no predefined service boundaries.                                                                                                                           |
| [[systems/soccer-mybatis/code/entities/security-constraint|Security Constraint]]       | 3          | inferred        | medium         | [[systems/soccer-mybatis/code/entities/teams|teams]] contains PII, and operations like [[systems/soccer-mybatis/business/use-cases/delete-team|delete_team]] are restricted to [[role:ROLE_ADMIN]]. Shared security context with [[systems/soccer-mybatis/code/entities/players|players]].                                               |

---

#### **Key Evidence**

1. **Identity & Lifecycle Commonality**: 
   - `metric:identity_lifecycle` (affinity Jaccard, threshold 0.5).
   - Example: [[systems/soccer-mybatis/code/entities/players|players]]-[[systems/soccer-mybatis/code/entities/teams|teams]] affinity of 0.25 (no CASCADE in DDL).

2. **Semantic Proximity**:
   - `metric:consistency_constraint` (affinity 0.333 for [[systems/soccer-mybatis/code/entities/goals|goals]]-[[systems/soccer-mybatis/code/entities/matches|matches]]).
   - Documentation: `doc:0:Soccer league - Business rules.txt`.

3. **Security Contextuality**:
   - `metric:security_contextuality` (role [[role:ROLE_ADMIN]] for [[systems/soccer-mybatis/code/entities/players|players]] and [[systems/soccer-mybatis/code/entities/teams|teams]]).
   - Code: [[systems/soccer-mybatis/business/use-cases/teamcontroller-deleteteam|TeamController.deleteTeam]].

4. **Consistency Criticality**:
   - `metric:consistency_criticality` (non-confluent pairs in [[systems/soccer-mybatis/code/entities/teams|teams]], [[systems/soccer-mybatis/code/entities/competitions|competitions]], etc.).
   - Code: `deleteById` operation in [[systems/soccer-mybatis/code/entities/teams|teams]].

5. **Security Criticality**:
   - `metric:security_criticality` ([[systems/soccer-mybatis/code/entities/teams|teams]] classified as `Internal` for PII).

---

#### **Cluster Suggestion**

The analysis suggests **4 clusters** as a starting point, prioritizing:
- **Semantic proximity**: Grouping [[systems/soccer-mybatis/code/entities/matches|matches]] and [[systems/soccer-mybatis/code/entities/goals|goals]] for transactional consistency.
- **Security contextuality**: Isolating [[systems/soccer-mybatis/code/entities/teams|teams]] and [[systems/soccer-mybatis/code/entities/players|players]] for [[role:ROLE_ADMIN]].
- **Consistency constraints**: Ensuring atomicity in operations like [[systems/soccer-mybatis/business/use-cases/score-goal|score_goal]].

## configuration-judge - configuration - run ff3b0c46 (unapproved proposal)

### Selection of Proposal: **risk**

The **risk** proposal was selected as the most robust and evidence-backed configuration for the Service Cutter analysis in this [[systems/soccer-mybatis/architecture/runs/ff3b0c46|run ff3b0c46]]. The decision is based on the following key factors:

### Rationale for Selection
1. **Explicit Treatment of Uncertainty and Limitations**
   - The **risk** proposal acknowledges and documents the limitations of the available data, such as the absence of telemetry, SLOs, or commit history to validate hypotheses (e.g., structural volatility, availability). This is critical to avoid overinterpreting incomplete data.
   - For example, in **Structural Volatility** and **Content Volatility**, the proposal clarifies that estimates are based on the absence of evidence of frequent changes, rather than observed data. This reduces the risk of decisions based on unvalidated assumptions.
   - Evidence: [[metric:structural_volatility]] (E384-E387), [[metric:content_volatility]] (E398-E403).

2. **Alignment with Business Invariants and Transactional Consistency**
   - The proposal prioritizes **Consistency Criticality** (value 8) in alignment with the invariants identified in the DDL and critical transactions of the system. For instance:
     - The `delete_team` operation (E330, E331) requires cascading deletion of players to maintain the business invariant: *"A team can be deleted only if it has never played a match. Its players are deleted with it."*
     - The `MatchService.scoreGoal` transaction (E376, E377) links `matches` and `goals` to ensure a goal cannot exist without a valid match.
   - These decisions are supported by metrics such as [[metric:consistency_criticality]] (E388-E396), which identify non-confluent pairs in critical operations.

3. **Focus on Security Risks and Data Sensitivity**
   - The proposal assigns high weights to **Security Contextuality** (value 8) and **Security Criticality** (value 5) based on:
     - The classification of `teams` as **Internal** due to containing PII (city, country) according to PCI DSS and NIST SP 800-122 (E381).
     - Restricted access to the **ROLE_ADMIN** role for sensitive operations (E404), justifying the grouping of entities with similar security requirements.
   - This mitigates risks of exposing sensitive data by avoiding mixing it with public entities (e.g., `matches` or `competitions`).

4. **Consistency with Documentation and Business Rules**
   - The proposal faithfully reflects the rules described in the documentation, such as:
     - The semantic relationship between `teams` and `players` (E336, E337).
     - The criticality of latency in operations like `record_goal` (E352) and `match_detail` (E354), even without defined SLOs.
   - It also avoids contradictions with metrics like [[metric:identity_lifecycle]] (E374), which shows low affinity between unrelated entities.

5. **Rejection of Invalid or Confusing Arguments**
   - **Does not confuse complexity with volatility**: In **Structural Volatility**, the proposal clarifies that the absence of frequent schema changes does not imply low complexity, but rather stability.
   - **Does not treat 'undetermined' as a low value**: In **Consistency Criticality**, it recognizes that `competition_teams` has an **undetermined** level (E397) but does not assume it is low. Instead, it proposes a separate aggregate for this entity to avoid unvalidated assumptions.
   - **Does not assume optimality**: The proposal does not claim the design is optimal but is supported by available evidence and aligned with business requirements.

6. **Handling of Latency and Availability**
   - Although SLOs are not defined, the proposal prioritizes latency in critical operations like `record_goal` (value 3 in **Latency** and **Availability Criticality**) based on documentation (E352, E354). This avoids ignoring implicit business requirements.

7. **Evidence-Backed Classifications**
   - Classifications of entities (e.g., `goals` as **High** in **Consistency Criticality**) are supported by metrics like [[metric:consistency_criticality]] (E389) and transactional operations (E235, E236).


### Disagreements with Other Proposals
#### Proposal: **code**
- **Underestimation of Consistency Criticality**
  - The **code** proposal assigns a value of 5 to **Consistency Constraint**, despite metrics like [[metric:consistency_criticality]] (E388-E396) identifying non-confluent pairs in critical operations (e.g., `teams` and `players`). This ignores risks of inconsistency in key transactions.
  - Evidence: [[systems/soccer-mybatis/business/use-cases/delete-team|delete_team]] (E330, E331), [[systems/soccer-mybatis/business/use-cases/scoregoal|scoreGoal]] (E376, E377).

- **Inadequate Treatment of Uncertainty**
  - The proposal does not document the limitations of the absence of telemetry or commit history in criteria like **Structural Volatility** and **Content Volatility**, which could lead to decisions based on unvalidated assumptions.
  - Evidence: [[metric:structural_volatility]] (E384-E387), [[metric:content_volatility]] (E398-E403).

- **Security Risks**
  - While it prioritizes **Security Contextuality** (value 8), the proposal does not explain how it mitigates risks of exposing sensitive data in entities like `teams`.
  - Evidence: [[systems/soccer-mybatis/code/entities/teams|teams]] (E381).


#### Proposal: **business**
- **Overvaluation of Security**
  - The **business** proposal assigns a value of 8 to **Security Constraint**, but there is no evidence of compliance requirements (e.g., GDPR) or security audits. The classification of `teams` as **Internal** (E381) alone does not justify such a high weight.
  - Evidence: [[systems/soccer-mybatis/code/entities/teams|teams]] (E381).

- **Ignoring Consistency Criticality Metrics**
  - Although it prioritizes **Consistency Criticality** (value 8), the proposal does not explain how it mitigates risks identified in [[metric:consistency_criticality]] (E392-E396), such as foreign keys without `ON DELETE CASCADE`.
  - Evidence: [[metric:consistency_criticality]] (E392-E396).

- **Confusion Between Transactional Affinity and Invariants**
  - In **Consistency Constraint**, the proposal assumes that write affinity (E376, E377) proves business invariants, but the metric [[metric:consistency_constraint]] (E375) clarifies that affinity does not prove consistency constraints.
  - Evidence: [[metric:consistency_constraint]] (E375).


### Limitations of the Selected Proposal
- **Lack of Telemetry and SLOs**: There is no historical data on latency, availability, or volatility in production, which limits confidence in criteria like **Latency** and **Availability Criticality**.
- **Uncertainty in Undeclared Invariants**: Metrics like [[metric:consistency_criticality]] (E397) identify signs of uniqueness in `competition_teams`, but these cannot be statically distinguished. This may require additional validations in the code.
- **Dependence on Naming Rules for Security**: The classification of sensitive columns (E381) is based on PCI DSS and NIST SP 800-122, but there is no contextual analysis of the actual data.
