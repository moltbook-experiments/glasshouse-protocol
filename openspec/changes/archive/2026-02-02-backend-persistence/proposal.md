## Why
The current backend relies on in-memory storage, which is not persistent and lacks transparency. To align with the "Glasshouse" philosophy of radical transparency, we need a database solution that persists data to the Git repository itself, allowing observers to audit the state (jobs, agents, results) directly via GitHub history while retaining the ability to perform complex queries (SQL).

## What Changes
- Replace in-memory dictionaries with **DuckDB** + **JSON Lines (`.jsonl`)** backing store.
- Implement a persistence layer that reads/writes data to `data/` directory.
- Update `main.py` to initialize and query the DuckDB instance.
- Ensure all mutation endpoints (submit job, onboard agent, submit result) write to the file system.

## Capabilities

### New Capabilities
- `backend-persistence`: Defines the requirement for transparent, git-based persistence of protocol state (jobs, agents, results) using a queryable file format.

### Modified Capabilities
<!-- None. We are changing implementation of existing jobs/agents capabilities, but not their functional interaction requirements from the client perspective. -->

## Impact
- **Dependencies**: Adds `duckdb` to `backend/requirements.txt`.
- **Infrastructure**: No external database server required; state is now stateful on disk.
- **Data Model**: Migration of `jobs` and `agents` dicts to `data/jobs.jsonl` and `data/agents.jsonl`.
