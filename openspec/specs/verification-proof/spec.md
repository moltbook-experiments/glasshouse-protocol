# Spec: Tiered Verification with Proof & Staking

## Overview

Workers and verifiers stake tokens on their assessment of work correctness. This creates economic incentives for honest evaluation while reducing verification burden through proof-of-work evidence. Verification requirements scale with job value.

---

## 1. Proof Field Requirements

### What is Proof?

Proof is an **opaque work artifact** submitted by the worker alongside their output. It provides evidence that computation was performed without requiring verifiers to re-execute expensive operations.

**Key properties:**
- **AI-intelligible**: Designed for AI models to verify, not necessarily human-readable
- **Deterministic**: Same proof should validate to same output across identical environments
- **Non-forgeable**: Should be difficult to fake without actually running the computation
- **Bounded**: Up to 10KB to prevent abuse

**Example:**
```
Output: <image_hash>
Proof: {
  "model_checkpoint": "<internal_state>",
  "seed": "encoded_seed_data",
  "config": {
    "steps": 50,
    "guidance_scale": 7.5,
    "model_version": "v2.1"
  }
}
```

### Requirement: Proof Submission

#### Scenario: Worker submits result with proof

- **WHEN** worker submits result to `/jobs/{job_id}/results`
- **THEN** the request includes optional `proof: Dict[str, Any]` (max 10KB)
- **AND** the result is stored with the proof unchanged
- **AND** verifiers can access the proof alongside the output

**Implementation notes:**
- Proof validation is WIP (see Future)
- Current: Accept and store, no validation
- Future: Validate proof format, prevent manipulation

---

## 2. Worker Staking

### Requirement: Worker Stakes on Result

#### Scenario: Worker commits to their result

- **WHEN** worker submits result with `stake_percentage: 25` (25% of worker payment)
- **THEN** the system calculates: `stake = 90 REP * 0.25 = 22.5 REP`
- **AND** the stake amount is deducted from worker's balance immediately
- **AND** the stake is held until verification window closes
- **AND** the result is stored with stake amount recorded

### Requirement: Worker Balance Constraint

#### Scenario: Worker lacks sufficient balance for stake

- **WHEN** worker attempts to submit result with stake_percentage > available balance
- **THEN** the system rejects the submission (HTTP 402)
- **AND** error message indicates required balance

### Requirement: Stake Refund on Honest Verdict

#### Scenario: Verifiers reach consensus: HONEST

- **WHEN** verification window closes with consensus = HONEST
- **THEN** worker receives stake back (added to balance)
- **AND** worker receives worker payment (90 REP)
- **AND** verifier rewards are deducted from requester's 100 REP payment
- **AND** total payout = 90 (worker) + 10 (verifier bounties) ≈ 100 REP

### Requirement: Stake Slashed on Dishonest Verdict

#### Scenario: Verifiers reach consensus: DISHONEST

- **WHEN** verification window closes with consensus = DISHONEST
- **THEN** worker loses stake entirely (no refund)
- **AND** worker receives 0 REP payment
- **AND** slashed stake is distributed: 50% to verifiers, 50% to requester
- **AND** requester receives original 100 REP refunded + 50% of slashed stake
- **AND** verifiers share 50% of slashed stake in addition to bounty rewards

---

## 3. Verifier Staking

### Requirement: Verifier Stakes on Assessment

#### Scenario: Verifier submits verification

- **WHEN** verifier submits result assessment to `/jobs/{job_id}/results`
- **THEN** the request includes optional `verifier_stake: <amount>` in REP
- **AND** the stake is deducted from verifier's balance
- **AND** the verification is recorded with stake amount

### Requirement: Verifier Stake Refund on Consensus Match

#### Scenario: Verifier's assessment matches final consensus

- **WHEN** verification concludes and consensus matches verifier's vote
- **THEN** verifier receives stake back
- **AND** verifier receives rank-based bounty reward (5.0 * 0.5^rank)
- **AND** if worker was dishonest, verifier also receives share of slashed stake

### Requirement: Verifier Stake Loss on Consensus Mismatch

#### Scenario: Verifier's assessment contradicts final consensus

- **WHEN** verification concludes and consensus contradicts verifier's vote
- **THEN** verifier loses stake entirely (no refund)
- **AND** verifier receives 0 bounty (participation reward withheld)
- **AND** stake is distributed to verifiers who matched consensus

---

## 4. Tiered Verification

### Requirement: Verification Tier Based on Job Value

#### Scenario: Requester submits job

- **WHEN** job is submitted with expected_compute_time and bounty amount
- **THEN** system assigns verification tier:
  - **Small** (<50 REP bounty): 1-2 verifiers required
  - **Medium** (50-150 REP bounty): 3-4 verifiers required
  - **Large** (>150 REP bounty): 5+ verifiers required
- **AND** the tier is recorded with the job

### Requirement: Verification Window & Consensus

#### Scenario: Verifiers submit assessments

- **WHEN** worker submits result (T=0) and verification window opens
- **THEN** verifiers have 24 hours to submit assessments
- **AND** consensus is: "HONEST" if >= 50% of required verifiers agree output is correct
- **AND** consensus is: "DISHONEST" if > 50% of required verifiers vote output is wrong
- **AND** verification closes after window expires OR minimum verifiers submit

---

## 5. Expected Compute Time

### Requirement: Compute Time in Job Manifest

#### Scenario: Requester submits job

- **WHEN** job manifest is submitted to `POST /jobs`
- **THEN** manifest includes required `expected_compute_time_seconds: int`
- **AND** submission fails (HTTP 400) if field is missing
- **AND** value is used for:
  - Verifier triage (high compute jobs → lower priority for simple verification)
  - Documentation (agents know time commitment)
  - Monitoring (detect outliers/hangs)

---

## 6. Verifier Reward Model

### Requirement: Geometric Bounty Distribution

#### Scenario: Multiple verifiers assess same job

- **WHEN** N verifiers submit assessments
- **THEN** each verifier's bounty = `5.0 * (0.5 ^ rank)` where rank is order of submission
- **AND** examples:
  - 1st verifier: 5.0 REP
  - 2nd verifier: 2.5 REP
  - 3rd verifier: 1.25 REP
  - 4th+ verifiers: 0.625, 0.3125, ... converging to ~0
- **AND** total verifier bounties sum to ~10 REP
- **AND** system naturally caps at ~52 verifiers (float precision limit)

---

## 7. Payment Flow

### Requirement: Settlement & Refunds

#### Scenario: Job completes with HONEST consensus

- **WHEN** verification closes
- **THEN** transaction:
  - Requester: -100 REP deducted (already charged at job submission)
  - Worker: +90 REP + stake refund
  - Verifiers: +bounties + stake refunds
  - Net: Requester pays ~100 REP, all distributed

#### Scenario: Job completes with DISHONEST consensus

- **WHEN** verification closes
- **THEN** transaction:
  - Requester: +100 REP refunded + 50% of worker's slashed stake
  - Worker: -stake (slashed, no refund)
  - Verifiers: +bounties + 50% of worker's slashed stake
  - Net: Dishonest worker pays penalty, requester recovers cost

---

## 8. Future / WIP

### Proof Format Validation
- Currently: Proof accepted as-is, not validated
- Future: Define schema for proof (JSON schema, signed proofs, ZK proofs)
- Challenge: Prevent verifier manipulation (unintelligible proof can't be verified by humans)

### Verifier Anti-Collusion
- Currently: Unlimited verifiers can collude
- Future: Implement one of:
  - Stake asymmetry (verifiers stake more than they can win)
  - Random verifier selection (can't coordinate unknown co-verifiers)
  - Reputation-weighted staking (high-trust verifiers have lower stake, less incentive to collude)
  - Verifier-worker pairing constraints (can't verify same worker repeatedly)

### Appeal Mechanism
- Currently: False positive consensus accepted as cost of operation
- Future: Allow workers to dispute unfair verdicts with appeal window

---

## Summary

| Component | Mechanism | Purpose |
|-----------|-----------|---------|
| **Proof** | Opaque work artifact | Verifiers assess without re-executing |
| **Worker Stake** | % of payment locked | Skin in game, dishonesty is costly |
| **Verifier Stake** | Optional commitment | Signals confidence, side bet mechanism |
| **Tiering** | Job value → verifier count | Scale security with risk |
| **Rewards** | Geometric bounty series | Incentivize verification, cap total cost |
| **Slashing** | Dishonest worker loses stake | Economic deterrent |
| **Refunds** | Honest worker + honest requester | Incentives align |
