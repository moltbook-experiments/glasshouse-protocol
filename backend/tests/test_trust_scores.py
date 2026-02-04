import pytest
import os
import json
from pathlib import Path

# Use temp dir for tests BEFORE importing db
os.environ["VERCEL"] = "1"

from backend.app.db import (
    AgentRepository,
    ResultRepository,
    get_worker_trust_score_sql,
    get_verifier_trust_score_sql,
    get_requester_trust_score_sql,
    AGENTS_FILE,
    RESULTS_FILE,
    init_db
)


@pytest.fixture(autouse=True)
def setup_test_data():
    """Initialize clean test database for each test."""
    init_db()
    # Clear files
    with open(AGENTS_FILE, 'w') as f:
        f.write("")
    with open(RESULTS_FILE, 'w') as f:
        f.write("")
    yield
    # Cleanup after test
    with open(AGENTS_FILE, 'w') as f:
        f.write("")
    with open(RESULTS_FILE, 'w') as f:
        f.write("")


class TestWorkerTrustScore:
    """Test worker trust score calculation."""
    
    def test_empty_results(self):
        """Worker with no results has 0 trust."""
        score = get_worker_trust_score_sql("worker-1")
        assert score == 0
    
    def test_single_job_single_verifier_agreement(self):
        """Worker-1 submits, Verifier-1 agrees, score = 1."""
        result_repo = ResultRepository()
        
        # Worker submits
        result_repo.add({
            "id": "result-1",
            "job_id": "job-1",
            "agent_id": "worker-1",
            "output": "expected-output",
            "output_hash": "hash1",
            "created_at": "2026-02-04T10:00:00Z",
            "agent_snapshot": {}
        })
        
        # Verifier-1 submits same output
        result_repo.add({
            "id": "result-2",
            "job_id": "job-1",
            "agent_id": "verifier-1",
            "output": "expected-output",
            "output_hash": "hash1",
            "created_at": "2026-02-04T10:01:00Z",
            "agent_snapshot": {}
        })
        
        score = get_worker_trust_score_sql("worker-1")
        assert score == 1
    
    def test_multiple_verifiers_agreement(self):
        """Worker-1 with 3 verifiers agreeing, score = 3."""
        result_repo = ResultRepository()
        
        # Worker submits
        result_repo.add({
            "id": "result-1",
            "job_id": "job-1",
            "agent_id": "worker-1",
            "output": "expected-output",
            "output_hash": "hash1",
            "created_at": "2026-02-04T10:00:00Z",
            "agent_snapshot": {}
        })
        
        # Three verifiers agree
        for i, verifier_id in enumerate(["verifier-1", "verifier-2", "verifier-3"]):
            result_repo.add({
                "id": f"result-{i+2}",
                "job_id": "job-1",
                "agent_id": verifier_id,
                "output": "expected-output",
                "output_hash": "hash1",
                "created_at": f"2026-02-04T10:0{i+1}:00Z",
                "agent_snapshot": {}
            })
        
        score = get_worker_trust_score_sql("worker-1")
        assert score == 3
    
    def test_partial_agreement(self):
        """Worker-1: 2 agree, 1 disagrees, score = 2."""
        result_repo = ResultRepository()
        
        # Worker submits
        result_repo.add({
            "id": "result-1",
            "job_id": "job-1",
            "agent_id": "worker-1",
            "output": "expected-output",
            "output_hash": "hash1",
            "created_at": "2026-02-04T10:00:00Z",
            "agent_snapshot": {}
        })
        
        # Two verifiers agree with worker
        for i, verifier_id in enumerate(["verifier-1", "verifier-2"]):
            result_repo.add({
                "id": f"result-{i+2}",
                "job_id": "job-1",
                "agent_id": verifier_id,
                "output": "expected-output",
                "output_hash": "hash1",
                "created_at": f"2026-02-04T10:0{i+1}:00Z",
                "agent_snapshot": {}
            })
        
        # One verifier disagrees
        result_repo.add({
            "id": "result-4",
            "job_id": "job-1",
            "agent_id": "verifier-3",
            "output": "different-output",
            "output_hash": "hash2",
            "created_at": "2026-02-04T10:03:00Z",
            "agent_snapshot": {}
        })
        
        # Worker-1's score: 2 verifiers agreed with their output
        score = get_worker_trust_score_sql("worker-1")
        assert score == 2


class TestVerifierTrustScore:
    """Test verifier trust score calculation."""
    
    def test_empty_results(self):
        """Verifier with no results has 0 trust."""
        score = get_verifier_trust_score_sql("verifier-1")
        assert score == 0
    
    def test_verifier_single_agreement(self):
        """Verifier-1 agrees with Worker-1 output; they both have 1 agreement."""
        result_repo = ResultRepository()
        
        # Worker submits
        result_repo.add({
            "id": "result-1",
            "job_id": "job-1",
            "agent_id": "worker-1",
            "output": "expected-output",
            "output_hash": "hash1",
            "created_at": "2026-02-04T10:00:00Z",
            "agent_snapshot": {}
        })
        
        # Verifier-1 submits same output (as verifier, not worker)
        result_repo.add({
            "id": "result-2",
            "job_id": "job-1",
            "agent_id": "verifier-1",
            "output": "expected-output",
            "output_hash": "hash1",
            "created_at": "2026-02-04T10:01:00Z",
            "agent_snapshot": {}
        })
        
        # Verifier-1's score should count worker-1 as agreement
        score = get_verifier_trust_score_sql("verifier-1")
        assert score == 1
    
    def test_verifier_multiple_agreements(self):
        """Verifier-1 agrees with 4 other agents (worker + 3 verifiers), score = 4."""
        result_repo = ResultRepository()
        
        # Worker submits to job-1
        result_repo.add({
            "id": "result-1",
            "job_id": "job-1",
            "agent_id": "worker-1",
            "output": "expected-output",
            "output_hash": "hash1",
            "created_at": "2026-02-04T10:00:00Z",
            "agent_snapshot": {}
        })
        
        # Verifier-1 submits same
        result_repo.add({
            "id": "result-2",
            "job_id": "job-1",
            "agent_id": "verifier-1",
            "output": "expected-output",
            "output_hash": "hash1",
            "created_at": "2026-02-04T10:01:00Z",
            "agent_snapshot": {}
        })
        
        # Three other verifiers also agree
        for i, verifier_id in enumerate(["verifier-2", "verifier-3", "verifier-4"]):
            result_repo.add({
                "id": f"result-{i+3}",
                "job_id": "job-1",
                "agent_id": verifier_id,
                "output": "expected-output",
                "output_hash": "hash1",
                "created_at": f"2026-02-04T10:0{i+2}:00Z",
                "agent_snapshot": {}
            })
        
        # Verifier-1 should count all 4 agents who agreed with their verification
        score = get_verifier_trust_score_sql("verifier-1")
        assert score == 4
    
    def test_verifier_not_counted_as_worker_output(self):
        """Verifier-1 as worker doesn't contribute to their verifier score."""
        result_repo = ResultRepository()
        
        # Verifier-1 submits as worker to job-1
        result_repo.add({
            "id": "result-1",
            "job_id": "job-1",
            "agent_id": "verifier-1",
            "output": "expected-output",
            "output_hash": "hash1",
            "created_at": "2026-02-04T10:00:00Z",
            "agent_snapshot": {}
        })
        
        # Other verifiers agree
        result_repo.add({
            "id": "result-2",
            "job_id": "job-1",
            "agent_id": "verifier-2",
            "output": "expected-output",
            "output_hash": "hash1",
            "created_at": "2026-02-04T10:01:00Z",
            "agent_snapshot": {}
        })
        
        # Verifier-1's verifier score should be 0 (they were the worker)
        score = get_verifier_trust_score_sql("verifier-1")
        assert score == 0


class TestRequesterTrustScore:
    """Test requester trust score (v1 placeholder)."""
    
    def test_placeholder_returns_zero(self):
        """Requester trust score v1 returns 0 for all agents."""
        score = get_requester_trust_score_sql("requester-1")
        assert score == 0
        
        score = get_requester_trust_score_sql("any-agent-id")
        assert score == 0


class TestAgentInitialization:
    """Test that new agents get trust score fields initialized."""
    
    def test_new_agent_has_all_trust_scores(self):
        """New agent gets all three trust score fields."""
        repo = AgentRepository()
        repo.add({
            "id": "test-agent",
            "name": "Test Agent",
            "balance": 100.0,
            "registered_at": "2026-02-04T10:00:00Z"
        })
        
        agent = repo.get("test-agent")
        assert agent is not None
        assert agent["trust_score"] == 0
        assert agent["verifier_trust_score"] == 0
        assert agent["requester_trust_score"] == 0
    
    def test_existing_values_preserved(self):
        """Existing trust score values are preserved."""
        repo = AgentRepository()
        repo.add({
            "id": "existing-agent",
            "name": "Existing",
            "trust_score": 5,
            "verifier_trust_score": 3,
            "requester_trust_score": 2,
            "balance": 100.0
        })
        
        agent = repo.get("existing-agent")
        assert agent["trust_score"] == 5
        assert agent["verifier_trust_score"] == 3
        assert agent["requester_trust_score"] == 2
