## 1. Schema Updates

- [x] 1.1 Add `expected_compute_time_seconds: int` field to JobManifest model in main.py
- [x] 1.2 Add `verification_tier: str` field to JobManifest model (enum: "small", "medium", "large")
- [x] 1.3 Add `tier: str` field to JobRecord model (copy from JobManifest)
- [x] 1.4 Add `proof: Dict[str, Any] | None` field to ResultRecord model
- [x] 1.5 Add `worker_stake: float` field to ResultRecord model
- [x] 1.6 Add `verifier_stake: float` field to ResultRecord model
- [x] 1.7 Add `consensus: str | None` field to ResultRecord model (values: "HONEST", "DISHONEST", null)
- [x] 1.8 Add `stake_percentage: float` field to result submission endpoint (0-100)

## 2. Verification Tier Handling

- [x] 2.1 Validate verification_tier enum in JobManifest (must be "small", "medium", or "large")
- [x] 2.2 Store verification_tier from JobManifest to JobRecord in jobs.jsonl
- [x] 2.3 Map tier to required_verifiers count (small=1-2, medium=3-4, large=5+)
- [x] 2.4 Store required_verifiers count in JobRecord

## 3. Worker Staking Logic

- [x] 3.1 Add stake_deduct_worker(agent_id, stake_percentage, worker_payment) function to reputation.py
- [x] 3.2 Calculate stake amount: stake = worker_payment * (stake_percentage / 100)
- [x] 3.3 Validate worker has sufficient balance before accepting result submission
- [x] 3.4 Deduct stake from worker balance on result submission
- [x] 3.5 Store worker_stake amount in ResultRecord

## 4. Verifier Staking Logic

- [x] 4.1 Add optional verifier_stake parameter to verification submission endpoint
- [x] 4.2 Validate verifier has sufficient balance for stake (if provided)
- [x] 4.3 Deduct verifier_stake from verifier balance on verification submission
- [x] 4.4 Store verifier_stake amount in ResultRecord (default 0 if not provided)
- [x] 4.5 Cap verifier_stake at 50 GLS maximum (per design decision)

## 5. Verification Window & Consensus

- [x] 5.1 Add verification_window_open_at timestamp to ResultRecord
- [x] 5.2 Implement check_verification_window_closed(job_id) function (24 hours OR minimum verifiers met)
- [x] 5.3 Implement calculate_consensus(job_id) function: count verifier votes, return "HONEST" if ≥50%, else "DISHONEST"
- [x] 5.4 Add scheduled task or endpoint to trigger consensus calculation when window closes
- [x] 5.5 Handle edge case: zero verifiers after 48 hours → auto-pay worker (benefit of doubt)

## 6. Payment Distribution on Consensus

- [x] 6.1 Implement resolve_honest_consensus(job_id) function in reputation.py
- [x] 6.2 Refund worker_stake to worker on HONEST consensus
- [x] 6.3 Pay worker payment (90 GLS) on HONEST consensus
- [x] 6.4 Pay verifier bounties (geometric: 5.0 * 0.5^rank) on HONEST consensus
- [x] 6.5 Implement resolve_dishonest_consensus(job_id) function in reputation.py
- [x] 6.6 Slash worker_stake on DISHONEST consensus (no refund)
- [x] 6.7 Distribute slashed stake: 50% to verifiers (split proportionally), 50% to requester
- [x] 6.8 Refund requester original 100 GLS on DISHONEST consensus
- [x] 6.9 Refund/slash verifier stakes based on whether their vote matched consensus

## 7. Proof Field Handling

- [x] 7.1 Accept proof field in result submission (Dict[str, Any], max 10KB)
- [x] 7.2 Validate proof size ≤ 10KB (reject with HTTP 413 if too large)
- [x] 7.3 Store proof in ResultRecord as-is (no validation for MVP)
- [x] 7.4 Return proof in result detail endpoint (for verifiers to access)
- [x] 7.5 Add proof to GitHub sync output (include in results.jsonl)

## 8. API Endpoint Updates

- [x] 8.1 Update POST /jobs endpoint to require expected_compute_time_seconds and verification_tier fields
- [x] 8.2 Update POST /jobs/{job_id}/results endpoint to accept proof, stake_percentage, verifier_stake
- [x] 8.3 Add GET /jobs/{job_id}/consensus endpoint (returns consensus status and vote breakdown)
- [x] 8.4 Update error responses for insufficient balance (HTTP 402 with clear message)
- [x] 8.5 Add validation for stake_percentage (0-100 range)

## 9. Documentation Updates

- [x] 9.1 Update backend/static/skill.md: Document proof field schema and examples
- [x] 9.2 Update skill.md: Document stake_percentage parameter and calculation
- [x] 9.3 Update skill.md: Document verifier_stake parameter (optional, capped at 50 GLS)
- [x] 9.4 Update skill.md: Document verification_tier parameter (small/medium/large, requester-specified)
- [x] 9.5 Update skill.md: Document expected_compute_time_seconds (helps verifiers gauge effort)
- [x] 9.6 Update skill.md: Document consensus calculation and payment flows
- [x] 9.7 Update skill.md: Document verification window (24 hours, early closure)

## 10. Testing

- [x] 10.1 Write unit test: tier validation (reject invalid tier values)
- [x] 10.2 Write unit test: required_verifiers mapping (small=1-2, medium=3-4, large=5+)
- [x] 10.3 Write unit test: stake calculation (worker_payment * stake_percentage / 100)
- [x] 10.3 Write unit test: consensus calculation (≥50% = HONEST, <50% = DISHONEST)
- [x] 10.4 Write unit test: payment distribution on HONEST consensus (refund stake, pay worker, pay verifiers)
- [x] 10.5 Write unit test: payment distribution on DISHONEST consensus (slash stake, refund requester, distribute 50/50)
- [x] 10.6 Write integration test: Submit job → worker submits with stake → verifiers vote → consensus resolves → balances updated
- [x] 10.7 Write integration test: Insufficient balance rejection (worker tries to stake more than balance)
- [x] 10.8 Write integration test: Proof too large rejection (>10KB)
