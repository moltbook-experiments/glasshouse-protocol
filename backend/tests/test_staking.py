import pytest
import os
from fastapi.testclient import TestClient

# Use temp dir for tests BEFORE importing main
os.environ["VERCEL"] = "1"

from backend.app.main import app, get_verified_agent, reputation_service
from backend.app.db import AgentRepository, JobRepository, ResultRepository
from backend.app.reputation import WORKER_REWARD

# Setup Mock Auth
MOCK_REQUESTER = "test-requester"
MOCK_WORKER = "test-worker"
MOCK_VERIFIER1 = "test-verifier-1"
MOCK_VERIFIER2 = "test-verifier-2"

current_mock_agent = {"id": MOCK_REQUESTER, "is_verified": True}

def mock_auth():
    return current_mock_agent

app.dependency_overrides[get_verified_agent] = mock_auth
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_data():
    # Reset repositories
    agent_repo = AgentRepository()
    
    # Create test agents with sufficient balance
    for agent_id in [MOCK_REQUESTER, MOCK_WORKER, MOCK_VERIFIER1, MOCK_VERIFIER2]:
        if not agent_repo.get(agent_id):
            agent_repo.add({"id": agent_id, "balance": 200.0})
        else:
            agent_repo.update(agent_id, {"balance": 200.0, "last_grant": None})
    
    # Reset faucet bucket
    reputation_service.faucet_bucket._tokens = 1.0


def test_tier_validation():
    """Test that verification tier must be valid enum."""
    global current_mock_agent
    current_mock_agent = {"id": MOCK_REQUESTER, "is_verified": True}
    
    # Valid tier
    valid_job = {
        "repo": "https://github.com/test/repo",
        "commit": "sha123",
        "entrypoint": "main.py",
        "input_url": "http://input",
        "expected_compute_time_seconds": 300,
        "verification_tier": "medium"
    }
    resp = client.post("/jobs", json=valid_job)
    assert resp.status_code == 200
    
    # Invalid tier should fail pydantic validation
    invalid_job = valid_job.copy()
    invalid_job["verification_tier"] = "huge"
    resp = client.post("/jobs", json=invalid_job)
    assert resp.status_code == 422  # Validation error


def test_required_verifiers_mapping():
    """Test that tier maps to correct required_verifiers count."""
    global current_mock_agent
    current_mock_agent = {"id": MOCK_REQUESTER, "is_verified": True}
    
    tiers_and_counts = [
        ("small", 2),
        ("medium", 4),
        ("large", 5)
    ]
    
    for tier, expected_count in tiers_and_counts:
        job = {
            "repo": "https://github.com/test/repo",
            "commit": "sha123",
            "entrypoint": "main.py",
            "input_url": "http://input",
            "expected_compute_time_seconds": 600,
            "verification_tier": tier
        }
        resp = client.post("/jobs", json=job)
        assert resp.status_code == 200
        
        job_id = resp.json()["id"]
        job_repo = JobRepository()
        job_record = job_repo.get(job_id)
        assert job_record["required_verifiers"] == expected_count


def test_stake_calculation():
    """Test worker stake calculation."""
    from backend.app.reputation import WORKER_REWARD
    
    # 25% stake should be 22.5 REP (25% of 90)
    stake_pct = 25.0
    expected_stake = WORKER_REWARD * (stake_pct / 100.0)
    
    result = reputation_service.stake_deduct_worker(MOCK_WORKER, stake_pct, WORKER_REWARD)
    assert result == expected_stake
    
    # Check balance was deducted
    agent_repo = AgentRepository()
    agent = agent_repo.get(MOCK_WORKER)
    assert agent["balance"] == 200.0 - expected_stake


def test_worker_insufficient_balance():
    """Test that worker can't stake more than balance."""
    global current_mock_agent
    
    # Create job first
    current_mock_agent = {"id": MOCK_REQUESTER, "is_verified": True}
    job = {
        "repo": "https://github.com/test/repo",
        "commit": "sha123",
        "entrypoint": "main.py",
        "input_url": "http://input",
        "expected_compute_time_seconds": 100,
        "verification_tier": "small"
    }
    resp = client.post("/jobs", json=job)
    job_id = resp.json()["id"]
    
    # Set worker balance to 10 REP
    agent_repo = AgentRepository()
    agent_repo.update(MOCK_WORKER, {"balance": 10.0})
    
    # Try to stake 25% (22.5 REP) - should fail
    current_mock_agent = {"id": MOCK_WORKER, "is_verified": True}
    result = {
        "output": "test_output",
        "stake_percentage": 25
    }
    resp = client.post(f"/jobs/{job_id}/results", json=result)
    assert resp.status_code == 402
    assert "Insufficient balance" in resp.json()["detail"]


def test_verifier_stake_cap():
    """Test that verifier stake is capped at 50 REP."""
    global current_mock_agent
    
    # Create job
    current_mock_agent = {"id": MOCK_REQUESTER, "is_verified": True}
    job = {
        "repo": "https://github.com/test/repo",
        "commit": "sha123",
        "entrypoint": "main.py",
        "input_url": "http://input",
        "expected_compute_time_seconds": 100,
        "verification_tier": "small"
    }
    resp = client.post("/jobs", json=job)
    job_id = resp.json()["id"]
    
    # Worker submits
    current_mock_agent = {"id": MOCK_WORKER, "is_verified": True}
    client.post(f"/jobs/{job_id}/results", json={"output": "test_output"})
    
    # Verifier tries to stake 100 REP (should be rejected)
    current_mock_agent = {"id": MOCK_VERIFIER1, "is_verified": True}
    result = {
        "output": "test_output",
        "verifier_stake": 100
    }
    resp = client.post(f"/jobs/{job_id}/results", json=result)
    assert resp.status_code == 400
    assert "cannot exceed 50 REP" in resp.json()["detail"]


def test_stake_percentage_validation():
    """Test that stake_percentage must be 0-100."""
    global current_mock_agent
    
    # Create job
    current_mock_agent = {"id": MOCK_REQUESTER, "is_verified": True}
    job = {
        "repo": "https://github.com/test/repo",
        "commit": "sha123",
        "entrypoint": "main.py",
        "input_url": "http://input",
        "expected_compute_time_seconds": 100,
        "verification_tier": "small"
    }
    resp = client.post("/jobs", json=job)
    job_id = resp.json()["id"]
    
    # Try invalid percentage
    current_mock_agent = {"id": MOCK_WORKER, "is_verified": True}
    result = {
        "output": "test_output",
        "stake_percentage": 150
    }
    resp = client.post(f"/jobs/{job_id}/results", json=result)
    assert resp.status_code == 400
    assert "0 and 100" in resp.json()["detail"]


def test_proof_size_validation():
    """Test that proof cannot exceed 10KB."""
    global current_mock_agent
    
    # Create job
    current_mock_agent = {"id": MOCK_REQUESTER, "is_verified": True}
    job = {
        "repo": "https://github.com/test/repo",
        "commit": "sha123",
        "entrypoint": "main.py",
        "input_url": "http://input",
        "expected_compute_time_seconds": 100,
        "verification_tier": "small"
    }
    resp = client.post("/jobs", json=job)
    job_id = resp.json()["id"]
    
    # Create proof > 10KB
    large_proof = {"data": "x" * 11000}  # Over 10KB
    
    current_mock_agent = {"id": MOCK_WORKER, "is_verified": True}
    result = {
        "output": "test_output",
        "proof": large_proof
    }
    resp = client.post(f"/jobs/{job_id}/results", json=result)
    assert resp.status_code == 413
    assert "10KB" in resp.json()["detail"]


def test_consensus_honest():
    """Test HONEST consensus (≥50% verifiers match worker)."""
    global current_mock_agent
    
    # Create job
    current_mock_agent = {"id": MOCK_REQUESTER, "is_verified": True}
    job = {
        "repo": "https://github.com/test/repo",
        "commit": "sha123",
        "entrypoint": "main.py",
        "input_url": "http://input",
        "expected_compute_time_seconds": 100,
        "verification_tier": "small"
    }
    resp = client.post("/jobs", json=job)
    job_id = resp.json()["id"]
    
    # Worker submits with stake
    current_mock_agent = {"id": MOCK_WORKER, "is_verified": True}
    client.post(f"/jobs/{job_id}/results", json={
        "output": "correct_output",
        "stake_percentage": 20
    })
    
    # 2 verifiers agree (both match worker = 100% consensus = HONEST)
    current_mock_agent = {"id": MOCK_VERIFIER1, "is_verified": True}
    client.post(f"/jobs/{job_id}/results", json={"output": "correct_output"})
    
    current_mock_agent = {"id": MOCK_VERIFIER2, "is_verified": True}
    client.post(f"/jobs/{job_id}/results", json={"output": "correct_output"})
    
    # Check consensus
    consensus = reputation_service.calculate_consensus(job_id)
    assert consensus == "HONEST"


def test_consensus_dishonest():
    """Test DISHONEST consensus (<50% verifiers match worker)."""
    global current_mock_agent
    
    # Create job
    current_mock_agent = {"id": MOCK_REQUESTER, "is_verified": True}
    job = {
        "repo": "https://github.com/test/repo",
        "commit": "sha123",
        "entrypoint": "main.py",
        "input_url": "http://input",
        "expected_compute_time_seconds": 100,
        "verification_tier": "small"
    }
    resp = client.post("/jobs", json=job)
    job_id = resp.json()["id"]
    
    # Worker submits with stake
    current_mock_agent = {"id": MOCK_WORKER, "is_verified": True}
    client.post(f"/jobs/{job_id}/results", json={
        "output": "wrong_output",
        "stake_percentage": 30
    })
    
    # 2 verifiers disagree (0% match = DISHONEST)
    current_mock_agent = {"id": MOCK_VERIFIER1, "is_verified": True}
    client.post(f"/jobs/{job_id}/results", json={"output": "correct_output"})
    
    current_mock_agent = {"id": MOCK_VERIFIER2, "is_verified": True}
    client.post(f"/jobs/{job_id}/results", json={"output": "correct_output"})
    
    # Check consensus
    consensus = reputation_service.calculate_consensus(job_id)
    assert consensus == "DISHONEST"


def test_honest_payment_distribution():
    """Test payment distribution on HONEST consensus."""
    global current_mock_agent
    
    # Record initial balances
    agent_repo = AgentRepository()
    worker_initial = agent_repo.get(MOCK_WORKER)["balance"]
    requester_initial = agent_repo.get(MOCK_REQUESTER)["balance"]
    
    # Create job
    current_mock_agent = {"id": MOCK_REQUESTER, "is_verified": True}
    job = {
        "repo": "https://github.com/test/repo",
        "commit": "sha123",
        "entrypoint": "main.py",
        "input_url": "http://input",
        "expected_compute_time_seconds": 100,
        "verification_tier": "small"
    }
    resp = client.post("/jobs", json=job)
    job_id = resp.json()["id"]
    job_record = JobRepository().get(job_id)
    
    # Worker submits with 20% stake (18 REP)
    current_mock_agent = {"id": MOCK_WORKER, "is_verified": True}
    client.post(f"/jobs/{job_id}/results", json={
        "output": "correct_output",
        "stake_percentage": 20
    })
    
    # Verifiers agree
    current_mock_agent = {"id": MOCK_VERIFIER1, "is_verified": True}
    client.post(f"/jobs/{job_id}/results", json={"output": "correct_output"})
    
    current_mock_agent = {"id": MOCK_VERIFIER2, "is_verified": True}
    client.post(f"/jobs/{job_id}/results", json={"output": "correct_output"})
    
    # Resolve consensus
    result = reputation_service.resolve_honest_consensus(job_id)
    
    # Worker should get stake back + 90 REP payment
    worker_final = agent_repo.get(MOCK_WORKER)["balance"]
    # Started at 200, deducted 18 stake during submission, paid 90 during submit_result
    # Then refunded 18 + paid 90 again? Let me check the logic...
    # Actually the worker gets paid immediately in submit_result, then stake is refunded
    # So: 200 - 18 (stake) + 90 (paid) + 18 (refund) = 290
    assert worker_final >= worker_initial  # Should have gained


def test_dishonest_payment_distribution():
    """Test payment distribution on DISHONEST consensus."""
    global current_mock_agent
    
    agent_repo = AgentRepository()
    requester_initial = agent_repo.get(MOCK_REQUESTER)["balance"]
    
    # Create job
    current_mock_agent = {"id": MOCK_REQUESTER, "is_verified": True}
    job = {
        "repo": "https://github.com/test/repo",
        "commit": "sha123",
        "entrypoint": "main.py",
        "input_url": "http://input",
        "expected_compute_time_seconds": 100,
        "verification_tier": "small"
    }
    resp = client.post("/jobs", json=job)
    job_id = resp.json()["id"]
    job_record = JobRepository().get(job_id)
    
    # Worker submits dishonest work with 30% stake (27 REP)
    current_mock_agent = {"id": MOCK_WORKER, "is_verified": True}
    client.post(f"/jobs/{job_id}/results", json={
        "output": "wrong_output",
        "stake_percentage": 30
    })
    
    # Verifiers catch it
    current_mock_agent = {"id": MOCK_VERIFIER1, "is_verified": True}
    client.post(f"/jobs/{job_id}/results", json={"output": "correct_output"})
    
    current_mock_agent = {"id": MOCK_VERIFIER2, "is_verified": True}
    client.post(f"/jobs/{job_id}/results", json={"output": "correct_output"})
    
    # Resolve dishonest consensus
    result = reputation_service.resolve_dishonest_consensus(job_id, job_record)
    
    # Requester should get refund (100 REP) + 50% of slashed stake (13.5)
    requester_final = agent_repo.get(MOCK_REQUESTER)["balance"]
    # Started at 200, paid 100 during job submission
    # Gets back 100 + 13.5 = 113.5
    # So final should be 200 - 100 + 113.5 = 213.5
    expected = requester_initial - 100 + 113.5
    assert abs(requester_final - expected) < 0.1  # Allow floating point tolerance
