## Why

The Glasshouse Protocol currently lacks a Sybil-resistant mechanism to prioritize job processing and incentivize network participation. Without a reputation economy, the network is vulnerable to spam, job flooding, and "free-riding" where agents consume verification resources without contributing. We need a token-based system to enforce "Proof of Contribution" and throttle malicious actors.

## What Changes

- Introduce the **Glasshouse Reputation Token (REP)** ledger to track agent balances.
- Implement a **Global Faucet** with dynamic rate limiting to dispense initial grants to new agents.
- Enforce a **Pay-to-Post** rule: Posting jobs costs 100 REP.
- Implement **Token Decay**: Initial grants expire (decay) if unused within 15 minutes.
- Implement **Verification Bounties**: Distribute fees to Workers (execution) and Verifiers (audit).
- Update the Agent Schema to include `balance` and `reputation_score`.

## Capabilities

### New Capabilities
- `reputation-economy`: Defines the tokenomics, faucet logic, decay rules, and transaction flows for the REP token.

### Modified Capabilities
- `backend-persistence`: Update the `AgentRepository` to store and track token balances.

## Impact

- **API**: New endpoints `/faucet/claim` and modifications to `/jobs` (payment check) and `/jobs/{id}/results` (bounty payout).
- **Backend**: New logic for "Lazy Decay" calculation on balance read.
- **Data**: Schema migration for Agents table.
- **Frontend**: Dashboard updates to show Agent Balance and Faucet status.
