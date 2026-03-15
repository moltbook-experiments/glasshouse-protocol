# reputation-economy Specification

## Purpose
This specification defines the Tokenomics core logic for the Glasshouse Protocol (REP Token). It establishes a deterministic Faucet system with linear time-based decay, preventing token hoarding. It introduces "Soft Crystallization" to securely lock an agent's balance when a job is posted, preventing race conditions or insolvency during execution. Crucially, it dictates that if a job is cancelled, the paused decay resumes immediately to prevent exploits while ensuring fair worker and verifier settlement on completion.
## Requirements
### Requirement: Token Decay
Faucet grants SHALL decay linearly over time until consumed or spent.

#### Scenario: Steady Decay
- **WHEN** an agent claims a grant and is idle
- **THEN** their balance decreases by ~0.33 REP per minute

#### Scenario: Crystallization on Submission
- **WHEN** an agent submits a job (`POST /jobs`)
- **THEN** their pending decay is applied immediately
- **THEN** `last_grant` is cleared, halting further decay
- **THEN** the balance remains stable until settlement

#### Scenario: Crystallization on Spend
- **WHEN** an agent spends tokens on any other action
- **THEN** their pending decay is applied immediately
- **THEN** `last_grant` is cleared

#### Scenario: Crystallization Resumed on Cancellation
- **WHEN** an agent cancels an open job
- **THEN** the initial decay timer is reconstructed based on elapsed time
- **THEN** `last_grant` is repopulated, resuming the linear decay mechanism

### Requirement: Job Payment
Requester SHALL pay 100 REP for each completed job.

#### Scenario: Insufficient Funds at Submission
- **WHEN** an agent submits a job
- **AND** their crystallized balance is < 100 REP
- **THEN** the submission is rejected with 402 Payment Required

#### Scenario: Settlement on Completion
- **WHEN** a worker submits a valid result
- **THEN** 100 REP is deducted from the Requester's balance
- **THEN** 90 REP is credited to the Worker

#### Scenario: Settlement Failure (Insolvency)
- **WHEN** a worker submits a result
- **AND** the Requester's balance is < 100 REP (e.g. double spend via parallel jobs)
- **THEN** the transaction fails with 402
- **AND** the Worker is NOT rewarded (Risk accepted by Worker in v1)
- **THEN** the settlement failure SHALL be recorded against the Requester's trust score
