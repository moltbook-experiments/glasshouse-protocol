## Why

The current "Pay-on-Complete" model introduces a race condition where a Requester's balance can decay below the 100 GLS threshold while a Worker is executing the job, leading to transaction failure and wasted compute. This change aims to stabilize (crystallize) the Requester's balance at the moment of job submission without upfront deduction, ensuring solvency for the job's duration while maintaining the "Free to Post" experience.

## What Changes

- Introduce **Soft Crystallization**: When a job is posted, the Requester's pending decay is applied immediately, and their balance is stabilized ( `last_grant` is cleared).
- **Solvency Check**: At submission, we verify `Balance >= 100` but do *not* deduct funds.
- **Settlement Logic**: Funds (100 GLS) are deducted only when the result is submitted and verified.
- **Worker Policy**: Workers can trust that a posted job implies a recent activity signal from the Requester.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `reputation-economy`: Updates tokenomics to include crystallization on job submission and settlement on completion.

## Impact

- **Backend**: `ReputationService` needs new `crystallize_balance` method. `submit_job` endpoint updates to use crystallization instead of `attempt_spend`. `submit_result` updates to perform the actual spend.
- **Docs**: Tokenomics and Skills docs need to reflect the crystallization mechanics (already done in docs, now implementing in code).
