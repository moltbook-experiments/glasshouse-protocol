import os
import sys
import json
from datetime import datetime
from uuid import uuid4

# Add backend to sys.path so we can import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db import init_db, JobRepository, AgentRepository, ResultRepository, JOBS_FILE

def verify():
    print("--- 1. Initializing DB ---")
    init_db()
    
    if os.path.exists(JOBS_FILE):
        print(f"✅ DB File created: {JOBS_FILE}")
    else:
        print(f"❌ DB File missing: {JOBS_FILE}")
        return

    print("\n--- 2. Working with Jobs ---")
    job_repo = JobRepository()
    
    # Create a dummy job
    job_id = str(uuid4())
    new_job = {
        "id": job_id,
        "repo": "https://github.com/example/repo",
        "commit": "abcdef123456",
        "input_url": "https://arxiv.org/abs/2301.0001",
        "entrypoint": "python run.py",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    print(f"Adding Job: {job_id}")
    job_repo.add(new_job)
    
    # Read back via List
    all_jobs = job_repo.list_all()
    print(f"Total Jobs in DB: {len(all_jobs)}")
    for j in all_jobs:
        print(f" - Found Job ID: {j.get('id')} (Type: {type(j.get('id'))})")
    
    # Read back via Get
    print(f"Attempting to fetch {job_id}")
    fetched_job = job_repo.get(job_id)
    if fetched_job:
        print(f"Fetched: {fetched_job.get('id')} (Type: {type(fetched_job.get('id'))})")
        if str(fetched_job['id']) == job_id:
             print(f"✅ Verified: Retrieved Job {job_id} correctly")
        else:
             print(f"❌ Failed: ID Mismatch. Got {fetched_job['id']}, expected {job_id}")
    else:
        print(f"❌ Failed: Could not retrieve job {job_id}")

    print("\n--- 3. Verifying File Persistence (Cat) ---")
    print(f"Reading raw content of {JOBS_FILE}:")
    with open(JOBS_FILE, 'r') as f:
        print(f.read().strip())

    print("\n--- 4. Working with Agents ---")
    agent_repo = AgentRepository()
    agent_id = "agent-007"
    new_agent = {
        "id": agent_id,
        "name": "James Bond",
        "registered_at": datetime.utcnow().isoformat() + "Z"
    }
    agent_repo.add(new_agent)
    
    fetched_agent = agent_repo.get(agent_id)
    if fetched_agent and fetched_agent['id'] == agent_id:
         print(f"✅ Verified: Retrieved Agent {agent_id} correctly")
    else:
         print(f"❌ Failed: Could not retrieve agent {agent_id}")

    print("\n--- 5. Working with Results ---")
    result_repo = ResultRepository()
    result_id = str(uuid4())
    new_result = {
        "id": result_id,
        "job_id": job_id,
        "agent_id": agent_id,
        "output": "42",
        "verified_at": datetime.utcnow().isoformat() + "Z"
    }
    print(f"Adding Result: {result_id} for Job {job_id}")
    result_repo.add(new_result)

    fetched_results = result_repo.get_by_job(job_id)
    print(f"Fetched {len(fetched_results)} results for job {job_id}")
    
    found = False
    for r in fetched_results:
        if str(r.get('id')) == result_id:
            found = True
            break
            
    if found:
        print(f"✅ Verified: Retrieved Result {result_id} correctly")
    else:
        print(f"❌ Failed: Could not retrieve result {result_id}")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    verify()
