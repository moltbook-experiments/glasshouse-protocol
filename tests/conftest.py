import os
import shutil
import tempfile
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator

from backend.app.main import app
from backend.app import db
from backend.app.moltbook_auth import get_verified_agent

@pytest.fixture(scope="function", autouse=True)
def disable_rate_limiting():
    """Disable rate limiting for tests to avoid 429 errors."""
    from backend.app.main import limiter
    
    # Store original state
    original_enabled = limiter.enabled
    
    # Force disable
    limiter.enabled = False
    
    yield
    
    # Restore
    limiter.enabled = original_enabled

@pytest.fixture(scope="function", autouse=True)
def isolate_db():
    """
    Create a temporary directory for each test and point 
    backend.app.db paths to it.
    """
    test_dir = tempfile.mkdtemp()
    
    # Save original values
    orig_data_dir = db.DATA_DIR
    orig_jobs = db.JOBS_FILE
    orig_agents = db.AGENTS_FILE
    orig_results = db.RESULTS_FILE
    
    # Monkeypatch the globals
    db.DATA_DIR = test_dir
    db.JOBS_FILE = os.path.join(test_dir, "jobs.jsonl")
    db.AGENTS_FILE = os.path.join(test_dir, "agents.jsonl")
    db.RESULTS_FILE = os.path.join(test_dir, "results.jsonl")
    
    # Initialize the (empty) DB files in the temp dir
    db.init_db()
    
    yield
    
    # Cleanup
    shutil.rmtree(test_dir)
    
    # Restore
    db.DATA_DIR = orig_data_dir
    db.JOBS_FILE = orig_jobs
    db.AGENTS_FILE = orig_agents
    db.RESULTS_FILE = orig_results

@pytest.fixture(scope="function", autouse=True)
def reset_singletons():
    """Reset global stateful services."""
    from backend.app.main import reputation_service
    
    # Mock the consume method to always succeed
    original_consume = reputation_service.faucet_bucket.consume
    reputation_service.faucet_bucket.consume = lambda r, c: True
    
    yield
    
    # Restore
    reputation_service.faucet_bucket.consume = original_consume

@pytest.fixture
def mock_agent_data():
    """Standard test agent payload."""
    return {
        "id": "test-agent-123",
        "name": "TestBot",
        "owner": "user",
        "repo": "repo",
        "karma": 50,
        "token_balance": 100
    }

@pytest.fixture
def override_auth(mock_agent_data):
    """
    Override the get_verified_agent dependency.
    Use this fixture if your test needs authenticated access.
    """
    from fastapi import Request
    from datetime import datetime

    async def mock_auth_dependency(request: Request):
        # Apply side effects expected by endpoints (e.g. submit_result)
        request.state.agent = mock_agent_data
        request.state.agent_profile_snapshot = {
            "agent": mock_agent_data,
            "verified_at": datetime.utcnow().isoformat() + "Z",
            "verify_source": "test-mock"
        }
        return mock_agent_data

    app.dependency_overrides[get_verified_agent] = mock_auth_dependency
    yield
    app.dependency_overrides = {}

@pytest_asyncio.fixture
async def async_client(override_auth) -> AsyncGenerator[AsyncClient, None]:
    """
    Async HTTP client for integration tests.
    Includes auth override by default.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
