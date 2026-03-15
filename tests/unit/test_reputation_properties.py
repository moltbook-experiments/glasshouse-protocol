from datetime import datetime, timedelta, timezone
from hypothesis import given, strategies as st
import pytest

from backend.app.core_logic.reputation_math import (
    calculate_effective_balance,
    attempt_spend,
    calculate_verifier_bounty,
    calculate_worker_stake_deduction,
    FAUCET_GRANT_AMOUNT
)

# 1. Properties for get_effective_balance
@given(
    current_balance=st.floats(min_value=0.0, max_value=10000.0, allow_nan=False, allow_infinity=False),
    minutes_passed=st.floats(min_value=0.0, max_value=500000.0, allow_nan=False, allow_infinity=False)
)
def test_balance_never_negative(current_balance, minutes_passed):
    now = datetime.now(timezone.utc)
    last_grant = now - timedelta(minutes=minutes_passed)
    
    effective = calculate_effective_balance(current_balance, last_grant, now)
    
    # Invariant: Balance can never be negative
    assert effective >= 0.0
    # Invariant: Effective balance can never exceed current balance from decay
    assert effective <= current_balance

# 2. Properties for Attempt Spend
@given(
    current_balance=st.floats(min_value=0.0, max_value=10000.0, allow_nan=False, allow_infinity=False),
    amount=st.floats(min_value=0.0, max_value=20000.0, allow_nan=False, allow_infinity=False),
    minutes_passed=st.floats(min_value=0.0, max_value=500000.0, allow_nan=False, allow_infinity=False)
)
def test_attempt_spend_properties(current_balance, amount, minutes_passed):
    now = datetime.now(timezone.utc)
    last_grant = now - timedelta(minutes=minutes_passed)
    
    success, new_balance = attempt_spend(current_balance, last_grant, now, amount)
    
    if success:
        # Invariant: new balance >= 0
        assert new_balance >= 0.0
        # Invariant: new balance must equal effective balance minus amount
        effective = calculate_effective_balance(current_balance, last_grant, now)
        assert abs(new_balance - (effective - amount)) < 1e-5
    else:
        # Invariant: if spend fails, new_balance returned is just effective balance
        effective = calculate_effective_balance(current_balance, last_grant, now)
        assert new_balance == effective

# 3. Properties for Verifier Bounty
@given(rank=st.integers(min_value=0, max_value=1000))
def test_verifier_bounty_bounds(rank):
    bounty = calculate_verifier_bounty(rank)
    # Invariant: Bounty is strictly monotonic decreasing but never negative
    assert bounty >= 0.0
    # Invariant: Maximum possible bounty is the base
    from backend.app.core_logic.reputation_math import VERIFIER_BOUNTY_BASE
    assert bounty <= VERIFIER_BOUNTY_BASE

# 4. Properties for Stake Deduction
@given(
    worker_payment=st.floats(min_value=0.0, max_value=1000.0, allow_nan=False, allow_infinity=False),
    stake_percentage=st.floats(min_value=-10.0, max_value=150.0, allow_nan=False, allow_infinity=False)
)
def test_worker_stake_deduction(worker_payment, stake_percentage):
    deduction = calculate_worker_stake_deduction(worker_payment, stake_percentage)
    
    if stake_percentage < 0 or stake_percentage > 100:
        # Invariant: must reject stakes outside 0-100%
        assert deduction is None
    else:
        # Invariant: deduction never exceeds payment
        assert deduction <= worker_payment
        assert deduction >= 0.0
