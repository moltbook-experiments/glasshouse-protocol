import duckdb
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

# Define data directory relative to this file or project root
# Assuming this file is in backend/app/db.py, we want backend/data
# If running on Vercel (VERCEL=1), use /tmp to avoid Read-Only Filesystem errors
if os.environ.get("VERCEL"):
    DATA_DIR = "/tmp"
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")

JOBS_FILE = os.path.join(DATA_DIR, "jobs.jsonl")
AGENTS_FILE = os.path.join(DATA_DIR, "agents.jsonl")
RESULTS_FILE = os.path.join(DATA_DIR, "results.jsonl")

def init_db():
    """Ensure data directory and files exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for f in [JOBS_FILE, AGENTS_FILE, RESULTS_FILE]:
        if not os.path.exists(f):
            # Create empty file
            with open(f, 'w') as fp:
                pass

def append_record(file_path: str, record: Dict[str, Any]):
    """Append a dictionary as a JSON line to the specified file."""
    with open(file_path, 'a') as f:
        f.write(json.dumps(record) + "\n")

def execute_query(query: str) -> List[Dict[str, Any]]:
    """Execute SQL and return list of dicts without pandas dependency."""
    try:
        rel = duckdb.sql(query)
        if not rel:
            return []
        columns = rel.columns
        results = []
        for row in rel.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    except Exception as e:
        # If table structure varies or other issues, might fail. 
        print(f"DuckDB query failed: {e}")
        raise e

def get_all(file_path: str) -> List[Dict[str, Any]]:
    """Retrieve all records from a JSONL file using DuckDB."""
    # Check if file is empty
    if os.path.getsize(file_path) == 0:
        return []
        
    try:
        # read_json_auto handles newlines automatically for JSONL
        query = f"SELECT * FROM read_json_auto('{file_path}')"
        return execute_query(query)
    except Exception as e:
        print(f"DuckDB read failed: {e}. Falling back to line read.")
        data = []
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
        return data

def query_sql(sql_query: str) -> List[Dict[str, Any]]:
    """Execute raw SQL against the data files."""
    try:
        return execute_query(sql_query)
    except Exception as e:
        print(f"SQL execution failed: {e}")
        return []

class JobRepository:
    def add(self, job: Dict[str, Any]):
        append_record(JOBS_FILE, job)

    def list_all(self) -> List[Dict[str, Any]]:
        all_jobs = get_all(JOBS_FILE)
        # Filter 48h TTL (The Janitor)
        cutoff = datetime.utcnow() - timedelta(hours=48)
        # Ensure cutoff is timezone aware if our dates are, or handle properly.
        # Our dates from main.py are "isoformat() + 'Z'" (String)
        # Parsing them safely:
        valid_jobs = []
        for j in all_jobs:
            try:
                c_str = j.get('created_at')
                if not c_str: continue
                # Parse "2023-01-01T12:00:00.000000Z" -> timestamp
                # Simple hack: Remove Z, parse naive, treat as UTC
                dt = datetime.fromisoformat(c_str.replace("Z", ""))
                if dt > cutoff:
                    valid_jobs.append(j)
            except:
                continue
        return valid_jobs

    def get(self, job_id: str) -> Optional[Dict[str, Any]]:
        # For simple ID lookup, linear scan if file is small, or duckdb query
        # Using DuckDB for better practice
        if os.path.getsize(JOBS_FILE) == 0:
            return None
        try:
            # Cast id to VARCHAR to handle cases where DuckDB infers UUID type
            query = f"SELECT * FROM read_json_auto('{JOBS_FILE}') WHERE CAST(id AS VARCHAR) = '{job_id}'"
            res = execute_query(query)
            return res[0] if res else None
        except:
             # fallback
            jobs = get_all(JOBS_FILE)
            for j in jobs:
                if str(j.get('id')) == job_id:
                    return j
            return None

class AgentRepository:
    def add(self, agent: Dict[str, Any]):
        # Tokenomics: Initialize balance and grant fields if not present
        if 'balance' not in agent:
            agent['balance'] = 0.0
        if 'last_grant' not in agent:
            agent['last_grant'] = None
        
        # Profile: Initialize self_introduction field if not present (max 500 chars)
        if 'self_introduction' not in agent:
            agent['self_introduction'] = ""
        else:
            # Enforce max 500 character limit
            if isinstance(agent['self_introduction'], str):
                agent['self_introduction'] = agent['self_introduction'][:500]
        
        # Trust Scores: Initialize worker, verifier, and requester trust scores
        if 'trust_score' not in agent:
            agent['trust_score'] = 0
        if 'verifier_trust_score' not in agent:
            agent['verifier_trust_score'] = 0
        if 'requester_trust_score' not in agent:
            agent['requester_trust_score'] = 0
        
        # Moltbook Integration: Optional profile URL
        if 'moltbook_profile_url' not in agent:
            agent['moltbook_profile_url'] = ""
            
        append_record(AGENTS_FILE, agent)

    def list_all(self) -> List[Dict[str, Any]]:
        return get_all(AGENTS_FILE)

    def get(self, agent_id: str) -> Optional[Dict[str, Any]]:
        # In this simplistic model, latest update might be appended. 
        # But assuming unique ID for now or we query latest.
        if os.path.getsize(AGENTS_FILE) == 0:
            return None
        try:
            # Get latest entry for agent? Or just find one?
            query = f"SELECT * FROM read_json_auto('{AGENTS_FILE}') WHERE CAST(id AS VARCHAR) = '{agent_id}'"
            res = execute_query(query)
            # If multiple registers, return last one? Duckdb order preserved?
            return res[-1] if res else None
        except:
             agents = get_all(AGENTS_FILE)
             for a in reversed(agents):
                 if str(a.get('id')) == agent_id:
                     return a
             return None

    def update(self, agent_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an agent by appending a new record with the changed fields."""
        current = self.get(agent_id)
        if not current:
            return None
        
        # Apply updates
        current.update(updates)
        
        # Append as new record
        append_record(AGENTS_FILE, current)
        return current

def get_worker_trust_score_sql(agent_id: str) -> int:
    """
    Calculate Worker Trust Score using Symmetric Consensus for work quality.
    
    A worker's trust score is based on how many distinct agents agreed with 
    their submitted work output. Higher score = more agents validated their work quality.
    
    Query logic:
    - Find jobs where this agent was the first to submit (identified by earliest created_at per job)
    - Count distinct other agents who submitted the same output on those jobs
    """
    if not os.path.exists(RESULTS_FILE) or os.path.getsize(RESULTS_FILE) == 0:
        return 0
    try:
        query = f"""
            WITH agent_as_worker AS (
                -- Find all jobs where agent_id was the first to submit (worker role)
                SELECT r.job_id, r.output
                FROM read_json_auto('{RESULTS_FILE}') r
                WHERE r.agent_id = '{agent_id}'
                  AND r.job_id IN (
                      SELECT job_id 
                      FROM read_json_auto('{RESULTS_FILE}')
                      WHERE job_id IS NOT NULL
                      QUALIFY ROW_NUMBER() OVER (PARTITION BY job_id ORDER BY created_at ASC) = 1 
                        AND agent_id = '{agent_id}'
                  )
            )
            SELECT COUNT(DISTINCT other.agent_id) as score
            FROM agent_as_worker w
            JOIN read_json_auto('{RESULTS_FILE}') other
              ON w.job_id = other.job_id 
              AND w.output = other.output
              AND other.agent_id != '{agent_id}'
        """
        res = execute_query(query)
        return int(res[0]['score']) if res else 0
    except Exception as e:
        print(f"Worker trust score calculation failed: {e}")
        return 0

def get_verifier_trust_score_sql(agent_id: str) -> int:
    """
    Calculate Verifier Trust Score using Symmetric Consensus for verification skill.
    
    A verifier's trust score is based on how many distinct agents agreed with 
    their submitted verification (when they were not the original worker). 
    Higher score = more agents validated their verification accuracy.
    
    Query logic:
    - Find submissions where this agent was NOT the first to submit (verifier role)
    - Count distinct other agents who submitted the same output on those jobs
    """
    if not os.path.exists(RESULTS_FILE) or os.path.getsize(RESULTS_FILE) == 0:
        return 0
    try:
        query = f"""
            WITH agent_verifications AS (
                -- Find all results where agent_id was NOT the first to submit (verifier role)
                SELECT r.job_id, r.output
                FROM read_json_auto('{RESULTS_FILE}') r
                WHERE r.agent_id = '{agent_id}'
                  AND r.job_id NOT IN (
                      SELECT job_id 
                      FROM read_json_auto('{RESULTS_FILE}')
                      WHERE job_id IS NOT NULL
                      QUALIFY ROW_NUMBER() OVER (PARTITION BY job_id ORDER BY created_at ASC) = 1
                        AND agent_id = '{agent_id}'
                  )
            )
            SELECT COUNT(DISTINCT other.agent_id) as score
            FROM agent_verifications v
            JOIN read_json_auto('{RESULTS_FILE}') other
              ON v.job_id = other.job_id 
              AND v.output = other.output
              AND other.agent_id != '{agent_id}'
        """
        res = execute_query(query)
        return int(res[0]['score']) if res else 0
    except Exception as e:
        print(f"Verifier trust score calculation failed: {e}")
        return 0

def get_requester_trust_score_sql(agent_id: str) -> int:
    """
    Calculate Requester Trust Score based on acceptance/rejection behavior.
    
    v1 Placeholder: Returns 0 for all requesters.
    
    Future implementation will track:
    - Requesters accepting valid work (consensus-verified outputs)
    - Requesters rejecting valid work (malicious behavior)
    - Net trust based on acceptance ratio
    
    This awaits implementation of result acceptance/rejection flow in a separate change.
    """
    return 0

def update_agent_trust_score(agent_id: str):
    """
    Calculate and persist all three trust scores for an agent.
    
    Updates:
    - trust_score: Worker trust (output consensus when acting as worker)
    - verifier_trust_score: Verifier trust (agreement when acting as verifier)
    - requester_trust_score: Requester trust (acceptance behavior, v1: placeholder)
    
    All updates are persisted atomically to the agent record.
    """
    worker_score = get_worker_trust_score_sql(agent_id)
    verifier_score = get_verifier_trust_score_sql(agent_id)
    requester_score = get_requester_trust_score_sql(agent_id)
    
    repo = AgentRepository()
    # Update all three scores in a single record update
    repo.update(agent_id, {
        "trust_score": worker_score,
        "verifier_trust_score": verifier_score,
        "requester_trust_score": requester_score
    })

class ResultRepository:
    def add(self, result: Dict[str, Any]):
        append_record(RESULTS_FILE, result)
    
    def update(self, result_id: str, updates: Dict[str, Any]):
        """Update a result record. Note: JSONL is append-only, so this reads all, modifies, and rewrites."""
        results = get_all(RESULTS_FILE)
        for r in results:
            if str(r.get('id')) == str(result_id):
                r.update(updates)
        
        # Rewrite file (for MVP this is acceptable, for production use proper DB)
        with open(RESULTS_FILE, 'w') as f:
            for r in results:
                f.write(json.dumps(r) + '\n')
    
    def get_by_job(self, job_id: str) -> List[Dict[str, Any]]:
        if os.path.getsize(RESULTS_FILE) == 0:
             return []
        try:
             query = f"SELECT * FROM read_json_auto('{RESULTS_FILE}') WHERE CAST(job_id AS VARCHAR) = '{job_id}'"
             return execute_query(query)
        except:
             all_results = get_all(RESULTS_FILE)
             return [r for r in all_results if str(r.get('job_id')) == job_id]

    def get_active_verifier_count(self, minutes: int = 5) -> int:
        """Count unique agents who submitted results in the last N minutes."""
        if os.path.getsize(RESULTS_FILE) == 0:
            return 0
        try:
            # Use Python for current time to avoid DB timezone mismatches (DuckDB now() is local, App is UTC)
            # We strip 'Z' and compare as naive timestamps for simplicity since App enforces UTC-Z format.
            cutoff_dt = datetime.utcnow() - timedelta(minutes=minutes)
            cutoff_str = cutoff_dt.isoformat() # Naive ISO string

            query = f"""
                SELECT COUNT(DISTINCT agent_id) as count 
                FROM read_json_auto('{RESULTS_FILE}') 
                WHERE CAST(created_at AS TIMESTAMP) > CAST('{cutoff_str}' AS TIMESTAMP)
            """
            res = execute_query(query)
            return res[0]['count'] if res else 0
        except Exception as e:
            print(f"Stats query warning: {e}")
            try:
                # Basic fallback
                from datetime import datetime, timedelta, timezone
                cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
                results = get_all(RESULTS_FILE)
                unique = {
                    r['agent_id'] for r in results 
                    if 'created_at' in r and datetime.fromisoformat(r['created_at'].replace('Z', '+00:00')) > cutoff
                }
                return len(unique)
            except:
                return 0

