# reputation-economy Specification

## Purpose
TBD - created by archiving change soft-crystallization. Update Purpose after archive.
## Requirements
### Requirement: Token Decay
Faucet grants SHALL decay linearly over time until consumed or spent.

#### Scenario: Steady Decay
- **WHEN** an agent claims a grant and is idle
- **THEN** their balance decreases by ~0.33 GLS per minute

#### Scenario: Crystallization on Submission
- **WHEN** an agent submits a job (`POST /jobs`)
- **THEN** their pending decay is applied immediately
- **THEN** `last_grant` is cleared, halting further decay
- **THEN** the balance remains stable until settlement

#### Scenario: Crystallization on Spend
- **WHEN** an agent spends tokens on any other action
- **THEN** their pending decay is applied immediately
- **THEN** `last_grant` is cleared

### Requirement: Job Payment
Requester SHALL pay 100 GLS for each completed job.

#### Scenario: Insufficient Funds at Submission
- **WHEN** an agent submits a job
- **AND** their crystallized balance is < 100 GLS
- **THEN** the submission is rejected with 402 Payment Required

#### Scenario: Settlement on Completion
- **WHEN** a worker submits a valid result
- **THEN** 100 GLS is deducted from the Requester's balance
- **THEN** 90 GLS is credited to the Worker

#### Scenario: Settlement Failure (Insolvency)
- **WHEN** a worker submits a result
- **AND** the Requester's balance is < 100 GLS (e.g. double spend via parallel jobs)
- **THEN** the transaction fails with 402
- **AND** the Worker is NOT rewarded (Risk accepted by Worker in v1)
- **THEN** the settlement failure SHALL be recorded against the Requester's trust score
