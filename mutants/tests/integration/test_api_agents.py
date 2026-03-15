import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_agent_registration(async_client: AsyncClient):
    payload = {
        "capabilities": ["python", "duckdb"], 
        "payment_address": "0x123"
    }
    resp = await async_client.post("/agents/onboard", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "registered"
    assert "agent_id" in data

@pytest.mark.asyncio
async def test_submit_result(async_client: AsyncClient):
    # Setup: Register, Faucet, Job
    await async_client.post("/agents/onboard", json={})
    await async_client.post("/api/faucet/claim")
    
    job_payload = {
        "repo": "user/repo", 
        "commit": "c1", 
        "input_url": "u1", 
        "entrypoint": "e1",
        "expected_compute_time_seconds": 300,
        "verification_tier": "small"
    }
    resp = await async_client.post("/api/jobs", json=job_payload)
    assert resp.status_code == 200
    job_id = resp.json()["id"]
    
    # Submit Result
    result_payload = {
        "output": "result-data",
        "proof": {"type": "t1"},
        "runtime_meta": {"duration": 5}
    }
    
    # Submit to correct endpoint
    path = f"/api/jobs/{job_id}/results"
    resp = await async_client.post(path, json=result_payload)
    assert resp.status_code == 200, f"Failed to submit result: {resp.text}"
