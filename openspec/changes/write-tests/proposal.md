## Why

The current codebase lacks a comprehensive automated testing suite. As the protocol grows (e.g., adding reputation logic, rate limiting), manual verification becomes inefficient and error-prone. We need a safety net to prevent regressions, document expected behavior, and ensure critical paths (payments, verification) work as intended.

## What Changes

*   **infrastructure**: Setup `pytest` as the testing framework with `httpx` for API testing.
*   **structure**: Create a `tests/` directory mirroring the `backend/app` structure.
*   **unit-tests**: Implement tests for:
    *   `ReputationService` (logic for karma, spending, rewards).
    *   `JobRepository`, `AgentRepository`, `ResultRepository` (persistence).
    *   `MoltbookAuth` (mocked authentication flow).
*   **api-tests**: Implement integration tests for FastAPI endpoints (`main.py`) using `TestClient`.
*   **refactoring**: Minor adjustments to code to improve testability (e.g., dependency injection for DB path).

## Capabilities

### New Capabilities
- `test-suite`: A comprehensive set of unit and integration tests covering the backend services and API.

### Modified Capabilities
<!-- No changes to existing functional specs, this is a quality assurance layer. -->

## Impact

*   **Dependencies**: Adds `pytest`, `pytest-asyncio`, `httpx` to `requirements.txt`.
*   **Filesystem**: New `tests/` folder at root.
*   **Developer Workflow**: Developers will be able to run `pytest` to verify changes locally.
