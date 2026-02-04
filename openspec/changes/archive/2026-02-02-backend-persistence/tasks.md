## 1. Setup

- [x] 1.1 Add `duckdb` to `backend/requirements.txt`
- [x] 1.2 Create `backend/data` directory and helper module `backend/app/db.py`

## 2. Implementation

- [x] 2.1 Implement `JobRepository` with JSONL storage in `db.py`
- [x] 2.2 Implement `AgentRepository` with JSONL storage in `db.py`
- [x] 2.3 Refactor `backend/app/main.py` to use repositories instead of in-memory dicts
