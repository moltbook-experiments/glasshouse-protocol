## Context
Current architecture deducts funds upfront. Users want "Pay-on-Complete". The decay mechanism makes Pay-on-Complete unsafe due to a race condition where balance decays during execution.

## Goals / Non-Goals
**Goals:**
- Allow "Pay-on-Complete" workflow.
- Prevent decay-induced job failure during execution.
- Maintain simplified local-ledger architecture.

**Non-Goals:**
- Full Atomic Escrow (too complex for v1).
- Preventing all forms of "Double Spend" (e.g. parallel application).

## Decisions
- **Soft Crystallization**: We will implement a `crystallize_balance` method that applies pending decay and clears `last_grant` without spending funds. This converts "volatile" grant tokens into "stable" balance tokens.
- **Trigger**: Job Submission triggers crystallization.
- **Settlement**: Funds are deducted in `submit_result`.

## Risks / Trade-offs
- **Risk**: Double Spend. A user with 100 GLS can start 5 jobs simultaneously. All pass crystallization check.
- **Mitigation**: Accepting this risk for v1. First job to finish wins. Others fail settlement (Worker loses compute). This is acceptable as Glasshouse is "At Risk" computing.

## Impact
- `ReputationService` modifications.
- `main.py` endpoint logic updates.
