# VSDD Specification: reputation

## Phase 1a: Behavioral Specification

### Behavioral Contract
- **Preconditions:**
  - Agent must exist in the system and be verified via Moltbook.
  - Verification requires an active, unexpired session token.
  - A Job must exist to participate as a worker or verifier.
- **Postconditions:**
  - `claim_faucet`: Adds 150 REP to the agent's balance and resets decay timer.
  - `crystallize_balance`: Applies any pending continuous decay and solidifies the new balance.
  - `reward_worker`: Adds 90 REP to worker balance.
  - `reward_verifier`: Adds `5.0 * (0.5 ^ rank)` REP to verifier balance.
  - `stake_deduct_worker`: Deducts requested % of 90 REP from worker's available (crystallized) balance.
  - `calculate_consensus`: Must return `HONEST` if >= 67% (supermajority) of verifiers agree with the worker. Otherwise, it returns `DISHONEST`.
- **Invariants:**
  - An agent's effective balance cannot drop below 0.0 under any circumstances.
  - Decay only reduces the balance added by `faucet`. Earned/crystallized balance remains stable once a transaction forces crystallization (unless > 150 is decayed prior).
  - Verifier bounty sum converges and practically caps around 10 REP per job.
  - Faucet claims are globally rate-limited according to active verifier count.

### Interface Definition
- **Input Types:** `agent_id` (str), `job_id` (str), `amount` (float), `stake_percentage` (float), `verifier_rank` (int)
- **Output Types:** Boolean success flags, effective balance (float), Consensus Result (`HONEST`, `DISHONEST`, `None`)
- **Error Types:** `InsufficientFundsError`, `RateLimitExceededError`.

### Edge Case Catalog
1. Zero verifiers present when verification window closes (48h grace auto-pay).
2. Agent requests faucet claim multiple times within the rate limit window.
3. Worker stakes more than their effective balance.
4. Total decay exceeds current balance.
5. Large number of verifiers causes floating point underflow in geometric series reward.

### Non-Functional Requirements
- **Performance:** Decay calculation must be O(1) time complexity.
- **Memory/Resources:** Purity boundaries require state to be managed entirely outside the math module.
- **Security:** Floating point arithmetic must not be vulnerable to rounding exploits (e.g. negative stakes, tiny bypasses).

---

## Phase 1b: Verification Architecture

### Provable Properties Catalog
- [x] Properties that MUST be formally verified:
  - Consensus threshold calculation strictly requires >= 67% agreement for `HONEST`.
  - Balance decay strictly monotonic and bounded at zero.
  - No operation can cause an agent's balance to reflect a negative value.
- [x] Properties that ONLY require test coverage:
  - Faucet rate-limiting based on time.
  - Geometric series sum limits.

### Purity Boundary Map
- **Deterministic Pure Core:** `backend/app/core_logic/reputation_math.py`. Pure functions for decay math, consensus threshold logic, reward distributions.
- **Effectful Shell:** `backend/app/reputation.py`. Reads from `AgentRepository`, passes data to the core, and writes the mutated data back.

### Verification Tooling Selection
- Selected Stack: `pytest` for unit testing, `hypothesis` for property-based testing of the tokenomics/math invariant.
