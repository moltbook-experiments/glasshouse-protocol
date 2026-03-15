from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
from math import floor

# Constants from original reputation.py
DECAY_RATE_PER_MINUTE = 1.0 / 3.0  # 1 REP every 3 mins = 0.333/min
FAUCET_GRANT_AMOUNT = 150.0
JOB_COST = 100.0
WORKER_REWARD = 90.0

# Verifier Rewards
VERIFIER_BOUNTY_BASE = 5.0
VERIFIER_BOUNTY_RATIO = 0.5
CONSENSUS_THRESHOLD = 0.67  # 67% Supermajority


def calculate_effective_balance(
    current_balance: float, 
    last_grant_time: Optional[datetime], 
    now_time: datetime
) -> float:
    """
    Pure function: Calculate balance with continuous decay applied.
    Decay only applies if a grant time is present (since last faucet claim/spend).
    Ensures balance never drops below zero.
    """
    if last_grant_time is None:
        return max(0.0, current_balance)

    elapsed_minutes = (now_time - last_grant_time).total_seconds() / 60.0
    elapsed_minutes = max(0.0, elapsed_minutes)
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def attempt_spend(
    current_balance: float,
    last_grant_time: Optional[datetime],
    now_time: datetime,
    amount: float
) -> Tuple[bool, float]:
    """
    Pure function: Returns whether the spend is successful and the resulting (crystallized) balance.
    """
    effective = calculate_effective_balance(current_balance, last_grant_time, now_time)
    
    if effective >= amount:
        return True, effective - amount
        
    return False, effective


def calculate_verifier_bounty(rank: int) -> float:
    """
    Pure function: Geometric series for verifier rewards based on rank (0-indexed).
    """
    return VERIFIER_BOUNTY_BASE * (VERIFIER_BOUNTY_RATIO ** rank)


def calculate_consensus(worker_output: str, verifier_outputs: List[str]) -> Optional[str]:
    """
    Pure function: Determine if consensus matches worker output.
    Returns 'HONEST', 'DISHONEST', or None (if no verifiers).
    """
    if not verifier_outputs:
        return None
        
    matching = sum(1 for output in verifier_outputs if output == worker_output)
    total_verifiers = len(verifier_outputs)
    
    # >= 67% consensus = HONEST
    if matching / total_verifiers >= CONSENSUS_THRESHOLD:
        return "HONEST"
    return "DISHONEST"


def calculate_worker_stake_deduction(
    worker_payment: float, 
    stake_percentage: float
) -> Optional[float]:
    """
    Pure function: Calculate how much a worker needs to stake based on percentage.
    Returns None if percentage is out of bounds (0-100).
    """
    if stake_percentage < 0 or stake_percentage > 100:
        return None
        
    return worker_payment * (stake_percentage / 100.0)
