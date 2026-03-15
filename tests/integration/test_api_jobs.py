import pytest
from httpx import AsyncClient
from tests.conftest import set_agent_balance
from datetime import datetime, timedelta, timezone

from backend.app.db import AgentRepository
from backend.app.main import reputation_service

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


@pytest.mark.asyncio
async def test_job_cancellation_resumes_decay_timer(async_client: AsyncClient):
    await async_client.post("/agents/onboard", json={})
    await async_client.post("/api/faucet/claim")

    agent_repo = AgentRepository()
    agent = agent_repo.get("test-agent-123")
    thirty_minutes_ago = (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat().replace("+00:00", "Z")
    agent_repo.update(agent["id"], {"last_grant": thirty_minutes_ago})

    payload = {
        "repo": "user/repo",
        "commit": "sha123",
        "input_url": "s3://bucket/data",
        "entrypoint": "main.py",
        "expected_compute_time_seconds": 600,
        "verification_tier": "small"
    }

    create_resp = await async_client.post("/api/jobs", json=payload)
    assert create_resp.status_code == 200
    job_id = create_resp.json()["id"]

    crystallized_agent = agent_repo.get(agent["id"])
    assert crystallized_agent["last_grant"] is None
    assert crystallized_agent["balance"] == pytest.approx(140.0, abs=0.1)

    cancel_resp = await async_client.post(f"/api/jobs/{job_id}/cancel")
    assert cancel_resp.status_code == 200
    assert cancel_resp.json()["decay_resumed"] is True

    resumed_agent = agent_repo.get(agent["id"])
    assert resumed_agent["last_grant"] is not None
    assert reputation_service.get_effective_balance(resumed_agent) == pytest.approx(140.0, abs=0.1)


@pytest.mark.asyncio
async def test_job_cancellation_keeps_decay_paused_while_other_open_job_exists(async_client: AsyncClient):
    await async_client.post("/agents/onboard", json={})
    await async_client.post("/api/faucet/claim")

    agent_repo = AgentRepository()
    agent = agent_repo.get("test-agent-123")
    thirty_minutes_ago = (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat().replace("+00:00", "Z")
    agent_repo.update(agent["id"], {"last_grant": thirty_minutes_ago})

    payload = {
        "repo": "user/repo",
        "commit": "sha123",
        "input_url": "s3://bucket/data",
        "entrypoint": "main.py",
        "expected_compute_time_seconds": 600,
        "verification_tier": "small"
    }

    first_resp = await async_client.post("/api/jobs", json=payload)
    assert first_resp.status_code == 200
    first_job_id = first_resp.json()["id"]

    second_resp = await async_client.post("/api/jobs", json=payload)
    assert second_resp.status_code == 200

    cancel_resp = await async_client.post(f"/api/jobs/{first_job_id}/cancel")
    assert cancel_resp.status_code == 200
    assert cancel_resp.json()["decay_resumed"] is False

    still_crystallized_agent = agent_repo.get(agent["id"])
    assert still_crystallized_agent["last_grant"] is None
