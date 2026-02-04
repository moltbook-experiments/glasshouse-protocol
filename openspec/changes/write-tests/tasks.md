## 1. Setup

- [x] 1.1 Add `pytest`, `pytest-asyncio`, `httpx` to `backend/requirements.txt`
- [x] 1.2 Create `tests/` directory structure (`tests/unit`, `tests/integration`)
- [x] 1.3 Create `tests/conftest.py` with DB isolation and Auth override fixtures

## 2. Unit Tests

- [x] 2.1 Implement `tests/unit/test_db.py` (Repository CRUD operations in isolation)
- [x] 2.2 Implement `tests/unit/test_reputation.py` (Logic for spending, earning, limits)

## 3. Integration Tests

- [x] 3.1 Implement `tests/integration/test_api_jobs.py` (Job lifecycle: Post, List, Get)
- [x] 3.2 Implement `tests/integration/test_api_agents.py` (Agent registration, Auth checks)

## 4. Verification

- [x] 4.1 Run full test suite and verify 100% pass rate
- [x] 4.2 Verify no side effects in `backend/data/` after test run
