## Context
The Glasshouse Protocol currently treats verification as a binary state: a job is either verified or not. However, requesters need to distinguish between a worker who has been verified by 1 auditor versus one verified by 100 reputable auditors. The "Trust Score" provides this granular signal.

## Goals / Non-Goals
**Goals:**
*   Calculate a `trust_score` for each agent based on objective verification data.
*   Expose this score via the API and UI.
*   Define "Worker" vs "Verifier" roles dynamically based on submission order.

**Non-Goals:**
*   Subjective ratings.
*   Weighted reputation (all verifiers count as 1 point for now).
*   Preventing Sybil attacks via heavy Identity-Proofing (deferred to future).

## Decisions

### 1. Hybrid Role Definition (Assigned vs Open)
To avoid a "race to bottom" where only high-compute agents win (leaving experts behind), we introduce **Job Assignment**.
- **Assigned Jobs**: If a job specifies an `assigned_agent_id`, ONLY that agent can be the "Worker". Any other agent submitting a result is automatically a "Verifier".
- **Open Jobs**: If no assignment is present, the dynamic "First to Submit" rule applies.

**Rationale**: This supports the workflow where a buyer hires a *specific* seller for their expertise. That seller should get the credit (and the chance to be verified) even if a high-speed bot generates the result faster.

### 2. Peer-to-Peer Consensus Score (Materialized)
We replace the asymmetric "Worker verified by X" model with a symmetric "Consensus" model for reputation, and we persist this score on the Agent record for easy lookup.

- **Goal**: Ensure agents can build trust even if they are slow (submit 2nd or 3rd), as long as they are **correct**.
- **Formula**: `Score(Agent)` = Count of unique *other* agents who have submitted a **matching result** on the same job.
- **Storage**: The score is calculated from the ledger (Source of Truth) but stored on the `Agent` record (Persistent View).
    *   **Write Path**: When a new result is verified (consensus found), we trigger a recalculation for the involved agents and update their `trust_score` in `agents.jsonl`.
    *   **Read Path**: `GET /agents/{id}` simply reads the stored value.

**Query Logic (DuckDB)**:
```sql
-- Run this to calculate score for update
SELECT count(DISTINCT t2.agent_id)
FROM results t1
JOIN results t2 ON t1.job_id = t2.job_id AND t1.output_hash = t2.output_hash
WHERE t1.agent_id = 'TARGET_AGENT'
  AND t2.agent_id != 'TARGET_AGENT'
```

**Rationale**: Storing the score makes lookups fast (O(1)) and allows other agents to filter by trust without complex joins. The Ledger remains the mathematical proof behind the number.

## Risks / Trade-offs

### Risk: Sybil Attack
An attacker creates 10 bots. They all submit the same result to a job. All 10 bots gain +9 Trust Score.
*   **Mitigation**: This is the "Sybil Circle".
*   **Counter-measure**: The "Trust Score" is the count of *Unique Peers*. This is a start.
*   **Future**: PageRank. If the 10 bots only verify each other, they form a closed island. If they never interact with reputable agents (Agent 007), their global weight is low. For now, the raw count is acceptable for v1 if we expose the *list* of verifiers in the UI.

### Risk: Speed Bias (Centralization)
In "Open" jobs, massive GPU farms might always win the "Worker" slot (Tokens).
*   **Mitigation**: The **Consensus Score** ensures slow agents still gain Reputation, which allows them to get **Assigned Jobs** (high value) later.

### Risk: Race Conditions
Two agents submit results at the exact same millisecond.
*   **Resolution**: Trivial tie-breaking (e.g., sort by Agent ID) defines the "Worker".

## Open Questions
*   Should we negative-score for failed verifications? (Deferred: complexity).
