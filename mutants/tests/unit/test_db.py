import os
import pytest
from datetime import datetime, timedelta
from backend.app import db
from backend.app.db import JobRepository, AgentRepository, ResultRepository

def test_init_db(isolate_db):
    """Test that init_db creates the necessary files."""
    assert os.path.exists(db.JOBS_FILE)
    assert os.path.exists(db.AGENTS_FILE)
    assert os.path.exists(db.RESULTS_FILE)

def test_job_repo_crud():
    repo = JobRepository()
    job = {
        "id": "job-1", 
        "title": "Test Job", 
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    # Test Add
    repo.add(job)
    
    # Test Get
    fetched = repo.get("job-1")
    assert fetched is not None
    assert fetched["id"] == "job-1"
    
    # Test List
    jobs = repo.list_all()
    assert len(jobs) == 1
    assert jobs[0]["id"] == "job-1"

def test_job_repo_48h_filter():
    repo = JobRepository()
    
    # Job from 3 days ago
    old_job = {
        "id": "old-job",
        "created_at": (datetime.utcnow() - timedelta(days=3)).isoformat() + "Z"
    }
    repo.add(old_job)
    
    # Job from 1 hour ago
    new_job = {
        "id": "new-job",
        "created_at": (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z"
    }
    repo.add(new_job)
    
    # Verify filter
    jobs = repo.list_all()
    ids = [j["id"] for j in jobs]
    
    assert "new-job" in ids
    assert "old-job" not in ids

def test_agent_repo_crud():
    repo = AgentRepository()
    agent = {"id": "agent-1", "name": "Bond"}
    
    # Test Add
    repo.add(agent)
    
    # Test Get
    fetched = repo.get("agent-1")
    assert fetched["name"] == "Bond"
    assert fetched["balance"] == 0.0 # Default value logic
    
    # Test Update
    repo.update("agent-1", {"karma": 10})
    updated = repo.get("agent-1")
    assert updated["karma"] == 10
    
    # Ensure it appended a new record but get returns latest
    # (Implementation detail: update appends, get finds latest)
    # We can check file content length or just trust public API behavior used here.

def test_result_repo_queries():
    repo = ResultRepository()
    result1 = {"job_id": "j1", "agent_id": "a1", "output": "foo"}
    result2 = {"job_id": "j1", "agent_id": "a2", "output": "bar"}
    
    repo.add(result1)
    repo.add(result2)
    
    results = repo.get_by_job("j1")
    assert len(results) == 2

def test_active_verifier_count():
    repo = ResultRepository()
    # Old result
    old_time = (datetime.utcnow() - timedelta(minutes=10)).isoformat() + "Z"
    repo.add({"agent_id": "a1", "created_at": old_time})
    
    # New result
    new_time = datetime.utcnow().isoformat() + "Z"
    repo.add({"agent_id": "a2", "created_at": new_time})
    
    # Default window is 5 minutes
    count = repo.get_active_verifier_count(minutes=5)
    assert count == 1
