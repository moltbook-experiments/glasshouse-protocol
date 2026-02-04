## Context

The Glasshouse Protocol backend is a FastAPI application using DuckDB/JSONL for persistence. Currently, there is no automated testing. All verification is manual. As we add complex logic like Reputation/Tokenomics and Rate Limiting, we need a robust test harness.

The application relies on:
*   File-system persistence (`data/*.jsonl`).
*   External Auth (Moltbook).
*   Globals in `main.py` (repositories, services).

## Goals / Non-Goals

**Goals:**
*   Establish a standard `pytest` harness.
*   Enable `pytest` command to run all tests in < 5 seconds.
*   Isolate test data from development data (no side effects on `backend/data/`).
*   Provide patterns for testing Async API endpoints.
*   Mock external dependencies (Moltbook Auth).

**Non-Goals:**
*   Browser-based E2E testing (Selenium/Playwright).
*   Performance/Load testing (Locust).
*   Testing the GitHub Sync logic (mocking file I/O is sufficient).

## Decisions

### 1. Test Framework: Pytest + HTTPX
*   **Choice**: `pytest` with `httpx` and `pytest-asyncio`.
*   **Rationale**: Industry standard for Python/FastAPI. `TestClient` (from Starlette) is synchronous; `AsyncClient` (from `httpx`) is better for async/await routes, though `TestClient` is often simpler for blocking apps. Since we use `async def` routes, `httpx.AsyncClient` + `pytest-asyncio` is the correct modern approach.

### 2. Database Isolation: Temporary Directories
*   **Problem**: `db.py` relies on `DATA_DIR` which defaults to `backend/data`.
*   **Solution**: We will not rely on mocking the `open()` calls globally. Instead, we will use `pytest` fixtures to:
    1.  Create a temporary directory.
    2.  Set `os.environ["VERCEL"] = "1"` or inject a config to force `db.py` to use that path.
    3.  Alternatively, refactor `db.py` to allow passing `data_dir` to `init_db`.
*   **Decision**: Patch `db.DATA_DIR` (or equivalent) in a `conftest.py` fixture that runs `autouse=True`. This ensures *every* test runs against a fresh, empty isolated DB.

### 3. Auth Mocking: Dependency Overrides
*   **Problem**: `get_verified_agent` calls Moltbook API.
*   **Solution**: Use FastAPI's native `app.dependency_overrides`.
*   **Pattern**:
    ```python
    def mock_get_agent():
        return {"id": "test-agent", "name": "Test", "karma": 100}
    
    app.dependency_overrides[get_verified_agent] = mock_get_agent
    ```

### 4. Structure
Mirror the source:
```
tests/
  conftest.py        # Global fixtures (client, db, auth)
  unit/
    test_reputation.py
    test_db.py
  integration/
    test_api_jobs.py
    test_api_agents.py
```

## Risks / Trade-offs

*   **Global State**: `backend/app/main.py` initializes repositories (`job_repo = JobRepository()`) at module level. These might cling to the old file paths if initialized before our patch.
    *   *Mitigation*: We must ensure `db` module is re-initialized or our fixtures update the internal state of those instances. Refactoring `main.py` to use dependency injection for repos would be cleaner, but patching is faster for now.

