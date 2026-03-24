from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
import threading
import time
from .db import AgentRepository, ResultRepository
from .core_logic.reputation_math import (
    calculate_effective_balance,
    attempt_spend as math_attempt_spend,
    calculate_verifier_bounty,
    calculate_consensus as math_calculate_consensus,
    calculate_worker_stake_deduction,
    DECAY_RATE_PER_MINUTE,
    FAUCET_GRANT_AMOUNT,
    JOB_COST,
    WORKER_REWARD
)


def _parse_timestamp(timestamp: Optional[str]) -> Optional[datetime]:
    if not timestamp:
        return None
    try:
        return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    except Exception:
        return None

class TokenBucket:
    """In-memory Token Bucket for rate limiting."""
    def __init__(self):
        self._tokens = 1.0 # Start with 1 token available
        self._last_update = time.time()
        self._lock = threading.Lock()
        
    def consume(self, rate_per_minute: float, capacity: float) -> bool:
        """
        Attempt to consume 1 token.
        Refills based on rate_per_minute.
        Capacity caps the burst size.
        """
        with self._lock:
            now = time.time()
            elapsed = now - self._last_update
            
            # Avoid huge time jumps (e.g. system sleep) messing up simple math? 
            # Standard algo is fine.
            self._last_update = now
            
            rate_per_sec = rate_per_minute / 60.0
            # Refill
            self._tokens = min(capacity, self._tokens + (elapsed * rate_per_sec))
            
            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return True
            return False

class ReputationService:
    def __init__(self):
        self.agent_repo = AgentRepository()
        self.result_repo = ResultRepository()
        self.faucet_bucket = TokenBucket()

    def get_effective_balance(self, agent: Dict) -> float:
        """Calculate balance with pending decay applied using pure function."""
        current_balance = float(agent.get('balance', 0.0))
        last_grant_time = _parse_timestamp(agent.get('last_grant'))
                
        now_time = datetime.now(timezone.utc)
        return calculate_effective_balance(current_balance, last_grant_time, now_time)

    def get_decay_elapsed_minutes(self, agent: Dict, now_time: Optional[datetime] = None) -> Optional[float]:
        """Return elapsed decay minutes for an agent with an active grant timer."""
        last_grant_time = _parse_timestamp(agent.get('last_grant'))
        if last_grant_time is None:
            return None

        now_time = now_time or datetime.now(timezone.utc)
        elapsed_minutes = (now_time - last_grant_time).total_seconds() / 60.0
        return max(0.0, elapsed_minutes)

    def process_faucet_claim(self, agent_id: str) -> bool:
        """Process a faucet claim. Enforces Global Rate Limit."""
        
        # 1. Calculate Capacity/Rate based on Active Verifiers
        active_verifiers = self.result_repo.get_active_verifier_count(minutes=5)
        
        # Base rate: 1 per minute (bootstrap)
        # Scale: +1 grant/min per 5 active verifiers? 
        # Let's start conservative: Rate = max(1, active_verifiers // 2)
        # So 10 verifiers = 5 grants/min.
        # Capacity = Rate (1 minute burst)
        
        rate = max(1.0, active_verifiers / 2.0)
        capacity = max(1.0, rate)
        
        if not self.faucet_bucket.consume(rate, capacity):
            return False # Rate limited
            
        agent = self.agent_repo.get(agent_id)
        if not agent:
             # Should not happen if auth middleware works, but safety check
             return False

        # Apply Grant
        updates = {
            'balance': FAUCET_GRANT_AMOUNT,
            'last_grant': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
        self.agent_repo.update(agent_id, updates)
        return True

    def crystallize_balance(self, agent_id: str) -> float:
        """Apply pending decay and stabilize balance (clear last_grant)."""
        agent = self.agent_repo.get(agent_id)
        if not agent:
            return 0.0
            
        effective = self.get_effective_balance(agent)
        updates = {
            'balance': effective,
            'last_grant': None
        }
        self.agent_repo.update(agent_id, updates)
        return effective

    def crystallize_balance_for_job(self, agent_id: str) -> tuple[float, Optional[float]]:
        """Crystallize balance and capture paused decay elapsed minutes for later restoration."""
        agent = self.agent_repo.get(agent_id)
        if not agent:
            return 0.0, None

        now_time = datetime.now(timezone.utc)
        elapsed_minutes = self.get_decay_elapsed_minutes(agent, now_time)
        effective = calculate_effective_balance(
            float(agent.get('balance', 0.0)),
            _parse_timestamp(agent.get('last_grant')),
            now_time,
        )

        self.agent_repo.update(agent_id, {
            'balance': effective,
            'last_grant': None,
        })
        return effective, elapsed_minutes

    def resume_decay(self, agent_id: str, paused_minutes: Optional[float]) -> Optional[Dict[str, Any]]:
        """Restore linear decay after a crystallized job is canceled."""
        if paused_minutes is None:
            return None

        agent = self.agent_repo.get(agent_id)
        if not agent:
            return None

        if agent.get('last_grant'):
            return agent

        now_time = datetime.now(timezone.utc)
        restored_last_grant = now_time - timedelta(minutes=max(0.0, paused_minutes))
        restored_balance = float(agent.get('balance', 0.0)) + (max(0.0, paused_minutes) * DECAY_RATE_PER_MINUTE)

        return self.agent_repo.update(agent_id, {
            'balance': restored_balance,
            'last_grant': restored_last_grant.isoformat().replace('+00:00', 'Z'),
        })

    def attempt_spend(self, agent_id: str, amount: float) -> bool:
        """Try to deduct amount. Crystallizes decay."""
        agent = self.agent_repo.get(agent_id)
        if not agent:
            return False
            
        current_balance = float(agent.get('balance', 0.0))
        last_grant_time = _parse_timestamp(agent.get('last_grant'))
                
        now_time = datetime.now(timezone.utc)
        
        success, new_balance = math_attempt_spend(current_balance, last_grant_time, now_time, amount)
        
        if success:
            updates = {
                'balance': new_balance,
                'last_grant': None # spending clears decay status
            }
            self.agent_repo.update(agent_id, updates)
            return True
        return False

    def reward_worker(self, agent_id: str):
        """Reward worker with standard fee."""
        self._add_balance(agent_id, WORKER_REWARD)

    def reward_verifier(self, agent_id: str, verifier_rank: int):
        """Reward verifier based on rank (0-indexed). Geometric series."""
        amount = calculate_verifier_bounty(verifier_rank)
        self._add_balance(agent_id, amount)

    def _add_balance(self, agent_id: str, amount: float):
        agent = self.agent_repo.get(agent_id)
        if not agent:
            return
            
        effective = self.get_effective_balance(agent)
        new_balance = effective + amount
        
        updates = {
            'balance': new_balance,
            'last_grant': None
        }
        self.agent_repo.update(agent_id, updates)

    def stake_deduct_worker(self, agent_id: str, stake_percentage: float, worker_payment: float) -> Optional[float]:
        """
        Deduct worker stake based on percentage of payment.
        Returns stake amount if successful, None if insufficient balance or out of bounds.
        """
        stake_amount = calculate_worker_stake_deduction(worker_payment, stake_percentage)
        if stake_amount is None:
            return None
            
        if self.attempt_spend(agent_id, stake_amount):
            return stake_amount
        return None

    def check_verification_window_closed(self, job_id: str, job: Dict) -> bool:
        """
        Check if verification window should close.
        Returns True if either:
        - 24 hours have elapsed since worker submission, OR
        - Required number of verifiers have submitted
        """
        results = self.result_repo.get_by_job(job_id)
        if not results:
            return False
            
        # Find worker result (first one)
        worker_result = results[0]
        window_open = worker_result.get('verification_window_open_at')
        if not window_open:
            return False
            
        try:
            ts = datetime.fromisoformat(window_open.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            elapsed_hours = (now - ts).total_seconds() / 3600.0
            
            # Close after 24 hours
            if elapsed_hours >= 24:
                return True
                
            # Or close early if required verifiers met
            required_verifiers = job.get('required_verifiers', 2)
            verifier_count = len(results) - 1  # Exclude worker
            if verifier_count >= required_verifiers:
                return True
                
        except (ValueError, TypeError) as e:
            print(f"Error checking verification window: {e}")
            return False  # fail-safe: keep window open on parse errors

        return False

    def calculate_consensus(self, job_id: str) -> Optional[str]:
        """
        Calculate consensus based on verifier votes using pure math logic.
        """
        results = self.result_repo.get_by_job(job_id)
        if len(results) < 2:  # Need worker + at least 1 verifier
            return None
            
        worker_output = results[0].get('output')
        verifier_outputs = [r.get('output') for r in results[1:]]
        
        return math_calculate_consensus(worker_output, verifier_outputs)

    def resolve_honest_consensus(self, job_id: str) -> Dict[str, Any]:
        """
        Resolve payments for HONEST consensus.
        - Refund worker stake
        - Pay worker payment (90 REP)
        - Pay verifier bounties
        - Refund verifier stakes if they voted correctly
        """
        results = self.result_repo.get_by_job(job_id)
        worker_result = results[0]
        verifier_results = results[1:]
        worker_output = worker_result.get('output')
        
        # Refund and pay worker
        worker_id = worker_result.get('agent_id')
        worker_stake = worker_result.get('worker_stake', 0.0)
        
        if worker_stake > 0:
            self._add_balance(worker_id, worker_stake)  # Refund stake
        self.reward_worker(worker_id)  # Pay 90 REP
        
        # Pay verifiers
        for idx, verifier_result in enumerate(verifier_results):
            verifier_id = verifier_result.get('agent_id')
            verifier_stake = verifier_result.get('verifier_stake', 0.0)
            verifier_output = verifier_result.get('output')
            
            # Pay bounty
            self.reward_verifier(verifier_id, idx)
            
            # Refund stake if voted correctly
            if verifier_output == worker_output and verifier_stake > 0:
                self._add_balance(verifier_id, verifier_stake)
        
        # Update consensus field
        worker_result['consensus'] = "HONEST"
        self.result_repo.update(worker_result.get('id'), {'consensus': "HONEST"})
        
        return {
            "status": "HONEST",
            "worker_paid": WORKER_REWARD,
            "stake_refunded": worker_stake,
            "verifiers_rewarded": len(verifier_results)
        }

    def resolve_dishonest_consensus(self, job_id: str, job: Dict) -> Dict[str, Any]:
        """
        Resolve payments for DISHONEST consensus.
        - Slash worker stake (50% to verifiers, 50% to requester)
        - No worker payment
        - Refund requester original 100 REP
        - Pay verifier bounties
        - Refund verifier stakes if they voted correctly (against worker)
        """
        results = self.result_repo.get_by_job(job_id)
        worker_result = results[0]
        verifier_results = results[1:]
        worker_output = worker_result.get('output')
        
        worker_id = worker_result.get('agent_id')
        worker_stake = worker_result.get('worker_stake', 0.0)
        requester_id = job.get('created_by')
        
        # Slash worker stake
        verifier_share = worker_stake * 0.5
        requester_share = worker_stake * 0.5
        
        # Refund requester (100 REP + their share of slashed stake)
        if requester_id:
            self._add_balance(requester_id, JOB_COST + requester_share)
        
        # Distribute verifier share among verifiers proportionally
        correct_verifiers = [
            (idx, v) for idx, v in enumerate(verifier_results)
            if v.get('output') != worker_output
        ]
        
        if correct_verifiers:
            per_verifier = verifier_share / len(correct_verifiers)
            for idx, verifier_result in correct_verifiers:
                verifier_id = verifier_result.get('agent_id')
                verifier_stake = verifier_result.get('verifier_stake', 0.0)
                
                # Pay share of slashed stake
                self._add_balance(verifier_id, per_verifier)
                
                # Pay bounty
                self.reward_verifier(verifier_id, idx)
                
                # Refund their stake (voted correctly)
                if verifier_stake > 0:
                    self._add_balance(verifier_id, verifier_stake)
        
        # Update consensus field
        worker_result['consensus'] = "DISHONEST"
        self.result_repo.update(worker_result.get('id'), {'consensus': "DISHONEST"})
        
        return {
            "status": "DISHONEST",
            "worker_paid": 0,
            "stake_slashed": worker_stake,
            "requester_refunded": JOB_COST + requester_share,
            "verifiers_rewarded": len(correct_verifiers)
        }
