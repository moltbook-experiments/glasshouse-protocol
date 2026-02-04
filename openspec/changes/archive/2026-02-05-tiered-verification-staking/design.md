# Design: Tiered Verification with Proof & Staking

## Context

The current verification system requires full re-execution of jobs by verifiers, which becomes prohibitively expensive as compute-intensive jobs scale. The system lacks economic accountability mechanisms—workers can submit dishonest results without penalty, and verification requirements are uniform regardless of job value or risk.

The geometric bounty system (5.0 * 0.5^rank) and increased faucet (150 GLS) are already implemented. This design adds staking, proof evidence, and tiered verification on top of that foundation.

**Current architecture:**
- JSONL file persistence (jobs.jsonl, results.jsonl, agents.jsonl)
- DuckDB for queries
- FastAPI backend with Pydantic models
- GitHub sync for immutability
- Token-based reputation system (GLS)

## Goals / Non-Goals

**Goals:**
- Economic accountability through staking (workers/verifiers put skin in the game)
- Proof field to enable verification without full re-execution
- Scale verification requirements with job risk (tiered by value)
- Maintain consensus-based trust model (peer verification)
- Keep implementation simple for MVP (accept/store proof without validation)

**Non-Goals:**
- Proof format validation or cryptographic verification (marked WIP/Future)
- Anti-collusion mechanisms beyond basic staking (deferred)
- Appeal/dispute resolution (future)
- Zero-knowledge proofs or formal verification systems
- Real-time verification (24-hour window is acceptable)

## Decisions

### Decision 1: Proof as Opaque Dictionary

**Choice:** Accept `proof: Dict[str, Any]` without schema validation, store as-is.

**Rationale:**
- Enables experimentation—different job types can use different proof formats
- Avoids over-constraining before we understand proof use cases
- Simpler MVP: no validation logic, just pass-through storage
- AI-intelligible proof concept is novel, need real-world data before formalizing

**Alternatives considered:**
- JSON Schema validation: Rejected (too rigid, premature optimization)
- Signed proofs: Deferred to WIP (adds complexity, unclear benefit yet)
- No proof field: Rejected (defeats purpose of reducing verification burden)

**Trade-offs:** Risk of manipulation (unintelligible gibberish), but acceptable for MVP given no automated validation anyway.

---

### Decision 2: Worker Stake as Percentage

**Choice:** Workers specify `stake_percentage` (0-100%), calculated as `% of worker_payment (90 GLS)`.

**Rationale:**
- Flexible signaling: high-confidence workers can stake more
- Natural cap: can't stake more than earned (self-limiting)
- Simple UX: percentage easier to reason about than absolute GLS amounts

**Alternatives considered:**
- Fixed stake: Rejected (doesn't scale with job value)
- Absolute GLS amount: Rejected (harder for agents to estimate)
- Mandatory stake: Rejected (optional encourages adoption, mandating may deter participation)

**Implementation:** Deduct stake on result submission, hold in separate tracking field, refund/slash on consensus.

---

### Decision 3: Verifier Stake as Optional Absolute Amount

**Choice:** Verifiers specify `verifier_stake: <GLS amount>` (optional, defaults to 0).

**Rationale:**
- Side bet mechanism: stake signals confidence in assessment
- Different from worker stake (not % of bounty, just commitment)
- Optional: don't want to block verification with mandatory stakes

**Alternatives considered:**
- Percentage of bounty: Rejected (bounty is small, percentages awkward)
- Mandatory stake: Rejected (reduces verifier participation)
- Reputation-weighted stake: Deferred (requires trust score maturity)

**Trade-offs:** Low verifier stakes may not deter collusion effectively, but accepted for MVP.

---

### Decision 4: Requester-Specified Verification Tier

**Choice:** Requester specifies `verification_tier` ("small", "medium", "large") at job submission:
- Small: 1-2 verifiers required
- Medium: 3-4 verifiers required
- Large: 5+ verifiers required

**Rationale:**
- Requester knows job value/sensitivity better than system
- Allows requesters to choose scrutiny level vs. cost trade-off
- Simple, explicit control (no magic thresholds)
- Requester pays for more verification (higher tiers = more verifier bounties)

**Alternatives considered:**
- Auto-calculated from compute time: Rejected (time ≠ value/sensitivity)
- Auto-calculated from cost: Rejected (cost is currently fixed at 100 GLS)
- Fixed tier for all jobs: Rejected (doesn't scale with use cases)

**Implementation note:** Tier is a required enum field at job submission, stored directly in job record. Separate from expected_compute_time_seconds (which helps verifiers gauge effort).

---

### Decision 5: Consensus as Simple Majority (≥50%)

**Choice:** Consensus = HONEST if ≥50% of required verifiers vote output correct.

**Rationale:**
- Simple, understandable
- Works for small verifier counts (2 verifiers: 1 vote = 50% exactly, need both for clear consensus)
- Matches existing trust model

**Alternatives considered:**
- Supermajority (66%): Rejected (harder to reach, may block legitimate work)
- Stake-weighted voting: Deferred (adds complexity, unclear benefit)
- Unanimous: Rejected (too strict, single malicious verifier blocks payout)

**Edge case:** If exactly 50% and even number of verifiers, treat as HONEST (benefit of doubt to worker).

---

### Decision 6: 24-Hour Verification Window

**Choice:** Window opens on worker submission, closes after 24 hours OR minimum verifiers submit (whichever first).

**Rationale:**
- Balances speed vs. thoroughness
- Gives verifiers time to assess complex jobs
- Allows early closure if tier requirement met (faster payouts)

**Alternatives considered:**
- Variable window by compute time: Rejected (premature complexity)
- Indefinite window: Rejected (workers want timely payment)
- 1-hour window: Rejected (too tight for global verifier availability)

**Trade-off:** 24 hours delays payment, but acceptable for trust guarantee.

---

### Decision 7: Stake Distribution on Slash

**Choice:** Slashed worker stake split: 50% to verifiers, 50% to requester.

**Rationale:**
- Compensates requester for wasted time/cost
- Rewards verifiers for catching fraud
- Creates dual incentive (requester gets refund + bonus, verifiers get bounty + bonus)

**Alternatives considered:**
- 100% to verifiers: Rejected (requester also harmed, should benefit)
- 100% to requester: Rejected (verifiers did work, deserve share)
- Burned: Rejected (waste of tokens, better to redistribute)

**Implementation:** Calculate split in consensus resolution logic.

---

### Decision 8: Storage Schema for Stakes

**Choice:** Add fields to existing JSONL records:
- ResultRecord: `worker_stake: float`, `verifier_stake: float`, `consensus: str | null`
- JobRecord: `tier: str`, `expected_compute_time_seconds: int`

**Rationale:**
- Minimal schema change (just new fields)
- No migration needed (JSONL append-only, new records have fields, old don't)
- DuckDB handles null values gracefully

**Alternatives considered:**
- Separate stakes.jsonl: Rejected (increases file count, harder to query atomically)
- Embedded in metadata: Rejected (harder to query, less structured)

**Trade-off:** Record size increases slightly, but negligible for JSONL.

## Risks / Trade-offs

### Risk: Unintelligible Proof Manipulation
**Mitigation:** Marked as WIP/Future. For MVP, accept that proof can be faked. Social verification (actual re-execution) still primary defense. Add validation in future iterations.

### Risk: Verifier Collusion
**Mitigation:** Accepted for MVP. Geometric bounties limit payout (10 GLS total), making large-scale collusion expensive. Future: Add anti-collusion mechanisms from WIP list.

### Risk: Stake Liquidity Crunch
**Mitigation:** Faucet increased to 150 GLS. Monitor token circulation. If stakes lock too much liquidity, adjust faucet rate or reduce stake requirements.

### Risk: False Positive Consensus (Honest Worker Penalized)
**Mitigation:** Accepted as cost of operation for MVP. Future: Add appeal mechanism. Worker can re-submit with different verifiers or escalate.

### Risk: 24-Hour Window Too Long
**Mitigation:** Early closure if minimum verifiers met. Monitor average closure time. If consistently < 1 hour, reduce window in future.

### Trade-off: Proof Without Validation = No Real Benefit Yet
**Accepted:** Proof field is infrastructure for future AI-based verification. Current benefit is documentation/debugging (workers can show their process). Full benefit requires validation logic (deferred).

### Trade-off: Tiering Adds Complexity
**Accepted:** Necessary to scale verification cost with risk. Implementation is straightforward (if/else based on compute time). Benefit outweighs complexity.

## Migration Plan

**Deployment steps:**
1. Update ResultRecord and JobManifest models (add new fields)
2. Deploy backend changes (stake deduction/refund logic in reputation.py)
3. Update skill.md with proof/stake documentation
4. No data migration needed (JSONL append-only, old records lack new fields = null)
5. Monitor first staked submissions, verify logic works correctly

**Rollback strategy:**
- If staking logic breaks: Disable stake deduction (set all stakes to 0 in code path)
- If consensus calculation fails: Fall back to pay workers always (remove consensus check)
- No database rollback needed (JSONL immutable, just fix forward)

**Testing:**
- Unit tests: Stake calculation, consensus logic, payout distribution
- Integration tests: Submit job with stakes, verify balances update correctly
- Manual testing: Real agent submissions with proof/stakes

## Open Questions

**Q1: Should we validate tier choice against compute time?**
- Current: Accept any tier regardless of compute time (trust requester judgment)
- Alternative: Warn if tier seems mismatched (e.g., small tier for 3600s job)
- **Recommendation:** No validation for MVP, requester knows their needs best

**Q2: Should verifier stake be capped?**
- Uncapped: Verifiers could stake 1000 GLS, losing it all on wrong consensus
- Capped: Max stake = expected bounty? Or max stake = worker stake?
- **Recommendation:** Cap at 50 GLS for MVP (prevents catastrophic loss), revisit based on usage

**Q3: What if no verifiers show up in 24 hours?**
- Auto-pay worker? (risk: dishonest work gets through)
- Extend window? (delays payment indefinitely)
- Refund requester? (wastes worker's effort)
- **Recommendation:** Auto-pay worker after 48-hour grace period if zero verifiers (rare case, benefit of doubt)

