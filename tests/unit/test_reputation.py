import pytest
import time
from datetime import datetime, timedelta, timezone
from backend.app.reputation import ReputationService, TokenBucket, DECAY_RATE_PER_MINUTE

@pytest.fixture
def rep_service():
    return ReputationService()

def test_token_bucket():
    bucket = TokenBucket()
    # Initial state: 1 token
    assert bucket.consume(rate_per_minute=60, capacity=10) is True
    # Now empty (started with 1). Depending on float precision and timing, it should be near 0.
    
    # Try consume again immediately -> False
    assert bucket.consume(rate_per_minute=60, capacity=10) is False
    
    # Simulate waiting 1.1 second (rate=60/min = 1/sec)
    # Manual overriding of _last_update for deterministic testing mechanism
    bucket._last_update = time.time() - 1.1 # Backdate 1.1s
    
    assert bucket.consume(rate_per_minute=60, capacity=10) is True

def test_effective_balance_decay(rep_service):
    now = datetime.now(timezone.utc)
    # Gifted 10 minutes ago
    last_grant = (now - timedelta(minutes=10)).isoformat().replace("+00:00", "Z")
    
    agent = {
        "balance": 100.0,
        "last_grant": last_grant
    }
    
    effective = rep_service.get_effective_balance(agent)
    # Expected: 100 - (10 * DECAY_RATE)
    # DECAY_RATE = 1/3 = 0.3333...
    expected = 100.0 - (10.0 * DECAY_RATE_PER_MINUTE)
    
    assert abs(effective - expected) < 0.001

def test_attempt_spend_success(rep_service, isolate_db):
    repo = rep_service.agent_repo
    repo.add({"id": "spender", "balance": 200.0, "last_grant": None})
    
    success = rep_service.attempt_spend("spender", 100.0)
    assert success is True
    
    updated = repo.get("spender")
    assert updated["balance"] == 100.0

def test_attempt_spend_insufficient(rep_service, isolate_db):
    repo = rep_service.agent_repo
    repo.add({"id": "broke", "balance": 50.0, "last_grant": None})
    
    success = rep_service.attempt_spend("broke", 100.0)
    assert success is False
    
    updated = repo.get("broke")
    assert updated["balance"] == 50.0

def test_faucet_claim(rep_service, isolate_db):
    repo = rep_service.agent_repo
    repo.add({"id": "needy", "balance": 0.0})
    
    # Ensure bucket has tokens (mock active verifiers effectively)
    # Active verifiers count defaults to 0 -> Rate = 1.0 (code says max(1.0, count/2))
    # Bucket starts with 1.0 token
    
    success = rep_service.process_faucet_claim("needy")
    assert success is True
    
    updated = repo.get("needy")
    assert updated["balance"] == 105.0 # FAUCET_GRANT_AMOUNT
    assert updated["last_grant"] is not None

def test_rewards(rep_service, isolate_db):
    repo = rep_service.agent_repo
    repo.add({"id": "worker", "balance": 0.0})
    
    rep_service.reward_worker("worker")
    updated = repo.get("worker")
    assert updated["balance"] == 90.0
    
    rep_service.reward_verifier("worker", 0) # 1st place -> +5.0
    updated = repo.get("worker")
    assert updated["balance"] == 95.0 # 90 + 5
