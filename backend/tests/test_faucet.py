import pytest
import os
import time
from fastapi.testclient import TestClient

# Use temp dir for tests BEFORE importing main
os.environ["VERCEL"] = "1" 

from backend.app.main import app, get_verified_agent, reputation_service
from backend.app.db import AgentRepository, AGENTS_FILE

# Setup Mock Auth
MOCK_AGENT_ID = "test-agent-faucet"
def mock_auth():
    return {"id": MOCK_AGENT_ID, "is_verified": True}

app.dependency_overrides[get_verified_agent] = mock_auth
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_data():
    repo = AgentRepository()
    if not repo.get(MOCK_AGENT_ID):
        repo.add({"id": MOCK_AGENT_ID, "balance": 0.0})
    else:
        repo.update(MOCK_AGENT_ID, {"balance": 0.0, "last_grant": None})
        
    # Reset Faucet Bucket
    reputation_service.faucet_bucket._tokens = 1.0

def test_faucet_flow():
    """Test full Faucet -> Job cycle."""
    
    # 1. Initial State: 0 Balance
    # Try to post job (Should fail)
    job_payload = {
        "repo": "https://github.com/test/repo",
        "commit": "sha123",
        "entrypoint": "main.py",
        "input_url": "http://input"
    }
    resp = client.post("/api/jobs", json=job_payload)
    assert resp.status_code == 402 # Payment Required

    # 2. Claim Faucet
    resp = client.post("/api/faucet/claim")
    assert resp.status_code == 200
    data = resp.json()
    assert data["balance"] == 105.0

    # 3. Post Job (Should succeed)
    resp = client.post("/api/jobs", json=job_payload)
    assert resp.status_code == 200
    
    # 4. Check Balance
    # We can check via faucet again (it returns balance even if rate limited? No, it 429s).
    # Check via Agent Repo
    repo = AgentRepository()
    agent = repo.get(MOCK_AGENT_ID)
    # Balance is checked but not deducted until result settlement.
    # Should still be 105.0
    assert 104.9 <= agent["balance"] <= 105.1

def test_faucet_rate_limit():
    """Test that faucet enforces limits."""
    # 1. Claim
    resp = client.post("/api/faucet/claim")
    assert resp.status_code == 200

    # 2. Immediate Claim (Should 429)
    resp = client.post("/api/faucet/claim")
    assert resp.status_code == 429
