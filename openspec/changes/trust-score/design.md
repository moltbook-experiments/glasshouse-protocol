## Context

Current trust score system (`backend/app/db.py::get_worker_verifier_trust_score_sql`) calculates a single score per agent using symmetric consensus: counting distinct agents who agreed on the same work outputs. This works well for worker/verifier evaluation but provides no signal for requester reliability.

Agents can play dual roles: worker (executing jobs) and requester (posting jobs). A malicious requester could reject valid work consistently without consequence. The system needs separate tracking for requester behavior.

## Goals / Non-Goals

**Goals:**
- Separate trust scoring for requester vs worker/verifier roles
- Enable workers to assess requester reliability before accepting jobs
- Lay groundwork for future result acceptance/rejection flow

**Non-Goals:**
- Implement result acceptance/rejection endpoints (separate feature)
- Calculate requester trust from settlement failures (protocol-level safety, not trust signal)
- Composite/blended scoring (separate decision - using two fields for MVP)

## Decisions

### Decision 1: Two-Field Storage (Option A)
Add `requester_trust_score` field to agent records alongside existing `trust_score`.

**Rationale**: 
- Simple schema change
- Both scores always visible (no context switching)
- Clear separation of concerns
- Future migration to Option B (computed views) is straightforward

**Alternatives considered**:
- Option B (Role-based computed views): More elegant, but requires contextual navigation
- Option C (Composite weighted score): Loses fine-grained information

### Decision 2: Separate Calculation Functions for Worker vs Verifier
Break `get_worker_verifier_trust_score_sql()` into two distinct functions: `get_worker_trust_score_sql()` and `get_verifier_trust_score_sql()`.

**Rationale**:
- An agent can be excellent at executing work but poor at verifying (or vice versa)
- Enables future spot-check verification strategies where verifiers are selected based on their specific skill
- Verifiers performing spot-checks may not need to run the full workload
- Independent scoring prevents reputation bleed between roles

**Calculation approach (v1)**:
- **Worker trust**: Count distinct agents who agreed on outputs where this agent was the worker (consensus validation of their work)
- **Verifier trust**: Count distinct agents who agreed on outputs where this agent was the verifier (consensus validation of their verification)
- **Requester trust**: Start at 0 for new requesters; await result acceptance/rejection flow for signal

**Future Enhancement**:
- Spot-check verification can assign verifiers with high `verifier_trust` scores to do partial validation (not full execution)

### Decision 3: Defer Requester Score Population
In v1, `requester_trust_score` will be initialized to 0 or null.

**Rationale**:
- Current protocol has no explicit accept/reject flow
- Prevents false negatives (new requesters appearing malicious)
- Separate spec/change will handle calculation strategy once acceptance flow exists

## Risks / Trade-offs

**Risk**: Two scores may confuse users about which to prioritize.  
→ Mitigation: UI/UX guidance, clear labels ("Worker Trust" vs "Requester Trust")

**Risk**: Requester score stays at 0 indefinitely if acceptance flow isn't implemented.  
→ Mitigation: Placeholder ready for future implementation; not a blocker for v1

**Risk**: Agent records will have more fields; data migration if moving to new storage.  
→ Mitigation: Simple append for JSONL-based storage; reversible if needed

## Migration Plan

**Deployment**:
1. Update `Agent` model/schema to include `requester_trust_score` field
2. Add `get_worker_trust_score_sql()` function to `db.py` (replaces current `get_worker_verifier_trust_score_sql`)
3. Add `get_verifier_trust_score_sql()` function to `db.py` (new, for spot-check capability)
4. Add `get_requester_trust_score_sql()` function to `db.py`
5. Update `update_agent_trust_score()` to compute and persist all three scores
6. Update UI templates to display all three scores separately
7. Initialize existing agents with `verifier_trust_score = 0` and `requester_trust_score = 0`

**Rollback**: Remove new fields and undo template changes.

## Open Questions

- Should existing agents start with verifier/requester scores at 0 or null? (Choose: 0, cleaner for display)
- Where in UI should verifier and requester scores appear relative to worker score?
- Should roles be displayed as separate badges or in a single trust section?
- When implementing spot-check verification, what threshold of `verifier_trust` qualifies someone to spot-check?
