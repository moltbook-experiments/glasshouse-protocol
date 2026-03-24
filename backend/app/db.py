import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import duckdb

from .core_logic.trust_math import (
    get_requester_trust_score,
    get_verifier_trust_score,
    get_worker_trust_score,
)

# Use /tmp on Vercel (read-only filesystem), otherwise backend/data/
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
            with open(f, "w") as fp:
                pass


def append_record(file_path: str, record: Dict[str, Any]):
    """Append a dictionary as a JSON line to the specified file."""
    with open(file_path, "a") as f:
        f.write(json.dumps(record, default=str) + "\n")


def execute_query(query: str) -> List[Dict[str, Any]]:
    """Execute SQL and return list of dicts."""
    rel = duckdb.sql(query)
    if not rel:
        return []
    columns = rel.columns
    return [dict(zip(columns, row)) for row in rel.fetchall()]


def get_all(file_path: str) -> List[Dict[str, Any]]:
    """Retrieve all records from a JSONL file using DuckDB with line-read fallback."""
    if os.path.getsize(file_path) == 0:
        return []

    try:
        query = f"SELECT * FROM read_json_auto('{file_path}')"
        return execute_query(query)
    except duckdb.Error as e:
        print(f"DuckDB read failed: {e}. Falling back to line read.")
        data = []
        with open(file_path, "r") as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
        return data


def query_sql(sql_query: str) -> List[Dict[str, Any]]:
    """Execute raw SQL against the data files."""
    try:
        return execute_query(sql_query)
    except duckdb.Error as e:
        print(f"SQL execution failed: {e}")
        return []


class JobRepository:
    def add(self, job: Dict[str, Any]):
        append_record(JOBS_FILE, job)

    def update(self, job_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a job by appending a new record with the changed fields."""
        current = self.get(job_id)
        if not current:
            return None
        current.update(updates)
        append_record(JOBS_FILE, current)
        return current

    def list_all(self) -> List[Dict[str, Any]]:
        """Return jobs created within the last 48 hours (TTL filter)."""
        all_jobs = get_all(JOBS_FILE)
        cutoff = datetime.now(timezone.utc) - timedelta(hours=48)
        valid_jobs = []
        for j in all_jobs:
            try:
                c_str = j.get("created_at")
                if not c_str:
                    continue
                dt = datetime.fromisoformat(c_str.replace("Z", "+00:00"))
                if dt > cutoff:
                    valid_jobs.append(j)
            except (ValueError, TypeError) as e:
                print(f"Skipping job with invalid created_at: {e}")
                continue
        return valid_jobs

    def get(self, job_id: str) -> Optional[Dict[str, Any]]:
        if os.path.getsize(JOBS_FILE) == 0:
            return None
        try:
            query = f"SELECT * FROM read_json_auto('{JOBS_FILE}') WHERE CAST(id AS VARCHAR) = '{job_id}'"
            res = execute_query(query)
            return res[0] if res else None
        except duckdb.Error:
            jobs = get_all(JOBS_FILE)
            for j in jobs:
                if str(j.get("id")) == job_id:
                    return j
            return None


class AgentRepository:
    def add(self, agent: Dict[str, Any]):
        defaults = {
            "balance": 0.0,
            "last_grant": None,
            "self_introduction": "",
            "trust_score": 0,
            "verifier_trust_score": 0,
            "requester_trust_score": 0,
            "moltbook_profile_url": "",
        }
        for key, default_val in defaults.items():
            if key not in agent:
                agent[key] = default_val

        if isinstance(agent.get("self_introduction"), str):
            agent["self_introduction"] = agent["self_introduction"][:500]

        append_record(AGENTS_FILE, agent)

    def list_all(self) -> List[Dict[str, Any]]:
        return get_all(AGENTS_FILE)

    def get(self, agent_id: str) -> Optional[Dict[str, Any]]:
        if os.path.getsize(AGENTS_FILE) == 0:
            return None
        try:
            query = f"SELECT * FROM read_json_auto('{AGENTS_FILE}') WHERE CAST(id AS VARCHAR) = '{agent_id}'"
            res = execute_query(query)
            return res[-1] if res else None
        except duckdb.Error:
            agents = get_all(AGENTS_FILE)
            for a in reversed(agents):
                if str(a.get("id")) == agent_id:
                    return a
            return None

    def update(self, agent_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an agent by appending a new record with the changed fields."""
        current = self.get(agent_id)
        if not current:
            return None
        current.update(updates)
        append_record(AGENTS_FILE, current)
        return current


def get_worker_trust_score_sql(agent_id: str) -> int:
    try:
        all_results = get_all(RESULTS_FILE)
        return get_worker_trust_score(agent_id, all_results)
    except Exception as e:
        print(f"Worker trust score calculation failed: {e}")
        return 0


def get_verifier_trust_score_sql(agent_id: str) -> int:
    try:
        all_results = get_all(RESULTS_FILE)
        return get_verifier_trust_score(agent_id, all_results)
    except Exception as e:
        print(f"Verifier trust score calculation failed: {e}")
        return 0


def get_requester_trust_score_sql(agent_id: str) -> int:
    return get_requester_trust_score(agent_id, [])


def update_agent_trust_score(agent_id: str):
    """Calculate and persist all three trust scores for an agent."""
    worker_score = get_worker_trust_score_sql(agent_id)
    verifier_score = get_verifier_trust_score_sql(agent_id)
    requester_score = get_requester_trust_score_sql(agent_id)

    repo = AgentRepository()
    repo.update(agent_id, {
        "trust_score": worker_score,
        "verifier_trust_score": verifier_score,
        "requester_trust_score": requester_score,
    })


class ResultRepository:
    def add(self, result: Dict[str, Any]):
        append_record(RESULTS_FILE, result)

    def get_all_results(self) -> List[Dict[str, Any]]:
        """Return all result records."""
        return get_all(RESULTS_FILE)

    def update(self, result_id: str, updates: Dict[str, Any]):
        """Update a result record by rewriting the JSONL file."""
        results = get_all(RESULTS_FILE)
        for r in results:
            if str(r.get("id")) == str(result_id):
                r.update(updates)

        with open(RESULTS_FILE, "w") as f:
            for r in results:
                f.write(json.dumps(r) + "\n")

    def get_by_job(self, job_id: str) -> List[Dict[str, Any]]:
        if os.path.getsize(RESULTS_FILE) == 0:
            return []
        try:
            query = f"SELECT * FROM read_json_auto('{RESULTS_FILE}') WHERE CAST(job_id AS VARCHAR) = '{job_id}'"
            return execute_query(query)
        except duckdb.Error:
            all_results = get_all(RESULTS_FILE)
            return [r for r in all_results if str(r.get("job_id")) == job_id]

    def get_active_verifier_count(self, minutes: int = 5) -> int:
        """Count unique agents who submitted results in the last N minutes."""
        if os.path.getsize(RESULTS_FILE) == 0:
            return 0
        try:
            cutoff_dt = datetime.now(timezone.utc) - timedelta(minutes=minutes)
            cutoff_str = cutoff_dt.strftime("%Y-%m-%dT%H:%M:%S")

            query = f"""
                SELECT COUNT(DISTINCT agent_id) as count
                FROM read_json_auto('{RESULTS_FILE}')
                WHERE CAST(created_at AS TIMESTAMP) > CAST('{cutoff_str}' AS TIMESTAMP)
            """
            res = execute_query(query)
            return res[0]["count"] if res else 0
        except duckdb.Error as e:
            print(f"Stats query warning: {e}")
            try:
                cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
                results = get_all(RESULTS_FILE)
                unique = {
                    r["agent_id"]
                    for r in results
                    if "created_at" in r
                    and datetime.fromisoformat(r["created_at"].replace("Z", "+00:00")) > cutoff
                }
                return len(unique)
            except (ValueError, KeyError):
                return 0
