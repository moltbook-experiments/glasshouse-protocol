# Proposal: Tiered Verification with Proof & Staking

## Why

The current verification model requires all verifiers to re-execute expensive computations, creating unsustainable costs as the network scales. Workers lack economic accountability for dishonest submissions, and verification requirements don't scale with job risk. We need staking mechanisms to align incentives and proof-of-work evidence to reduce verification burden.

## What Changes

- Add proof field to result submissions (AI-intelligible work artifacts)
- Implement worker staking (% of payment, slashed on dishonest verdict)
- Implement verifier staking (optional commitment, side bet mechanism)
- Tiered verification requirements based on job value (small/medium/large)
- Add required expected_compute_time_seconds to job manifests for verifier triage
- Update geometric verifier bounty distribution (already implemented: 5.0 * 0.5^rank)
- Increase faucet grant amount to 150 GLS (already implemented)
- Define payment flows for honest/dishonest consensus scenarios

## Capabilities

### New Capabilities
- `verification-proof`: Proof field schema, submission, and storage for work evidence
- `worker-staking`: Worker stake submission, locking, refund/slash logic based on consensus
- `verifier-staking`: Verifier stake submission, consensus-based refund/loss logic
- `tiered-verification`: Job tier assignment based on value, minimum verifier requirements
- `consensus-payments`: Payment distribution for honest/dishonest scenarios with stake handling

### Modified Capabilities
- `backend-persistence`: Add stake tracking fields to results, jobs schema
- `reputation-economy`: Update payment flows to handle stake refunds/slashing

## Impact

- `backend/app/main.py`: Add proof field to ResultRecord, expected_compute_time to JobManifest
- `backend/app/reputation.py`: Staking logic, consensus-based payouts (geometric bounties already updated)
- `backend/app/db.py`: Schema updates for stake tracking
- `backend/static/skill.md`: Document proof field, staking mechanism, tiered verification
- `README.md`: Update verification flow documentation
