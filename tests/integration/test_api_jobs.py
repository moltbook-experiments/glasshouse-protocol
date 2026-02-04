import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_job_flow(async_client: AsyncClient):
    # 1. Register Agent (needed for Reputation Service DB lookup)
    resp = await async_client.post("/agents/onboard", json={})
    assert resp.status_code == 200
    
    # 2. Try to post job (Should fail - 0 balance)
    payload = {
        "repo": "user/repo",
        "commit": "sha123",
        "input_url": "s3://bucket/data",
        "entrypoint": "main.py"
    }
    resp = await async_client.post("/jobs", json=payload)
    assert resp.status_code == 402, f"Expected 402 Insufficient Funds, got {resp.status_code}: {resp.text}"
    assert "Insufficient funds" in resp.json()["detail"]
    
    # 3. Claim Faucet
    resp = await async_client.post("/faucet/claim")
    assert resp.status_code == 200
    assert resp.json()["balance"] == 105.0
    
    # 4. Post Job (Should succeed - 105 balance > 100 cost)
    resp = await async_client.post("/jobs", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    job_id = data["id"]
    
    # 5. List Jobs
    resp = await async_client.get("/jobs")
    assert resp.status_code == 200
    jobs = resp.json()["jobs"]
    assert len(jobs) == 1
    assert jobs[0]["id"] == job_id
