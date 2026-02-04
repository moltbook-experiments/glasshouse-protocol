## Context
The application currently uses Python dictionaries (`jobs = {}`, `agents = {}`) for storage. This state is lost on restart. We want to persist this state to disk in a format that is Git-friendly (diffable) to support the "Glasshouse" transparency model.

## Goals / Non-Goals
**Goals:**
- Implement a persistence layer using DuckDB and JSONL files.
- Store data in `data/jobs.jsonl`, `data/results.jsonl`, and `data/agents.jsonl`.
- Ensure the API reads from and writes to these files.

**Non-Goals:**
- High performance transaction processing (OLTP). The focus is transparency, not standard database throughput.
- Automatic Git commits (this will be handled by a separate process or manual agent action later).

## Decisions
### 1. Storage Format: JSON Lines (`.jsonl`)
We will store each record as a single line of JSON.
- **Why**: 
    - **Git Friendly**: Appeding a record is just adding a line. Diffs are clean.
    - **DuckDB Compatible**: DuckDB can query `read_json_auto('*.jsonl')` efficiently.
    - **Human Readable**: Transparent to observers.

### 2. Query Engine: DuckDB
We will use DuckDB as an embedded SQL engine.
- **Why**: It allows us to treat JSONL files as tables ("Virtual Tables"). It supports complex SQL which we need for future features (Reputation).
- **Alternative**: SQLite. Rejected because binary `.db` files are opaque in GitHub diffs.

### 3. Concurrency Strategy
We will implement a simple file lock or append-only strategy.
- **Rationale**: For the Glasshouse prototype, volume is low. Append-only writing is safe enough for now. We will reload the DuckDB connection or use a fresh query per request to ensure latest data visibility.

## Risks / Trade-offs
- **Performance**: Querying text files is slower than binary storage. 
    - *Mitigation*: DuckDB is surprisingly fast. Volume is low.
- **Consistency**: Race conditions if multiple processes write.
    - *Mitigation*: Single worker process for FastAPI (verified by `uvicorn` settings).

## Migration Plan
- Stop server.
- Existing in-memory data is discarded (acceptable for dev).
- Deploy new code.
- Data starts accumulating in `data/`.
