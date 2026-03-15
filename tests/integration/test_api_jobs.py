import pytest
from httpx import AsyncClient
from tests.conftest import set_agent_balance

@pytest.mark.asyncio
async def test_job_flow(async_client: AsyncClient):
    # 1. Register Agent (gives 500 REP initial balance)
    resp = await async_client.post("/agents/onboard", json={})
    assert resp.status_code == 200
    agent_id = resp.json()["agent_id"]
    
    # 2. Set balance to 0 for testing economic flow
    set_agent_balance(agent_id, 0.0)
    
    # 3. Try to post job (Should fail - 0 balance)
    payload = {
        "repo": "user/repo",
        "commit": "sha123",
        "input_url": "s3://bucket/data",
        "entrypoint": "main.py",
        "expected_compute_time_seconds": 600,
        "verification_tier": "medium"
    }
    resp = await async_client.post("/api/jobs", json=payload)
    assert resp.status_code == 402, f"Expected 402 Insufficient Funds, got {resp.status_code}: {resp.text}"
    assert "Insufficient funds" in resp.json()["detail"]
    
    # 4. Claim Faucet
    resp = await async_client.post("/api/faucet/claim")
    assert resp.status_code == 200
    assert resp.json()["balance"] == 150.0
    
    # 5. Post Job (Should succeed - 150 balance > 100 cost)
    resp = await async_client.post("/api/jobs", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    job_id = data["id"]
    
    # 6. List Jobs
    resp = await async_client.get("/api/jobs")
    assert resp.status_code == 200
    jobs = resp.json()["jobs"]
    assert len(jobs) == 1
    assert jobs[0]["id"] == job_id
