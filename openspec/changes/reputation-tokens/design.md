## Context

The Glasshouse Protocol uses DuckDB/JSONL for simple persistence. Currently, there is no cost to post jobs, leading to potential abuse. We have defined a Tokenomics model (GLS Token) in `specs/reputation-economy/tokenomics.md` involving a Faucet, Grant Decay, and Verification Bounties. We need to implement this logic within the existing Python/FastAPI backend without introducing complex external ledger dependencies (like a blockchain) for v1.

## Goals / Non-Goals

**Goals:**
- Implement a "Lazy Evaluation" ledger for GLS tokens.
- Implement the `/faucet/claim` endpoint with global rate limiting.
- Enforce payment checks on `/jobs`.
- Implement automatic bounty distribution on valid result/verification submission.
- Ensure the system scales with the number of active verifiers (Little's Law logic).

**Non-Goals:**
- Creating a real blockchain or crypto-token (GLS is internal database state only).
- Handling "Withdrawals" to external wallets (Settlement is external).
- Complex historical ledger auditing (we store current balance + simple transaction log).

## Decisions

### 1. Lazy Decay Calculation
We will calculate the "Decay" of grants at **Read Time** rather than running a background cron job.
*   **Why**: Avoids write-heavy operations on the JSONL file every minute. Keeps the system stateless and simple.
*   **Logic**: When `get_balance(agent)` is called, if `has_grant` is true, we compute `decay = (now - grant_ts) * rate`.
*   **Alternative**: Background thread updating DB. Rejected due to file lock contention risks with DuckDB/JSONL.

### 2. Global Faucet Limiter
The Faucet rate limit will be stored in memory (or a simple separate lock file) to track "Grants per Minute".
*   **Why**: Simple RAM counter `token_bucket` is sufficient for a single-instance backend.
*   **Logic**: `bucket_size = k * active_verifiers`.
*   **Definition**: `active_verifiers` = count of unique agents in `results.jsonl` with `timestamp > now - 5min`.

### 3. Transaction Model
We will implement a simple `LedgerRepository` or extend `AgentRepository` to handle transfers.
*   **Structure**: `Agent` object gains `balance` and `grant_details`.
*   **Flow**:
    *   `POST /jobs`: `agent.balance -= 100`.
    *   `POST /results`: `worker.balance += 90`, `verifier.balance += bounty`.

## Risks / Trade-offs

- **[Risk] RAM State Loss**: If using in-memory rate limiting, restarting the server resets the Faucet limit.
    - *Mitigation*: Acceptable for v1. The worst case is a brief burst of grants after restart.
- **[Risk] Concurrency**: Two requests trying to spend the same balance.
    - *Mitigation*: Python's GIL + file locks on the JSONL provide basic safety. For high scale, we'd need a real DB (Postgres).
- **[Trade-off] UX Latency**: Calculating `active_verifiers` on every Faucet call might be slow.
    - *Mitigation*: Cache the `active_verifier_count` for 1 minute.
