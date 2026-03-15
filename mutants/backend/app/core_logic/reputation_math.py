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
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


def calculate_effective_balance(
    current_balance: float, 
    last_grant_time: Optional[datetime], 
    now_time: datetime
) -> float:
    args = [current_balance, last_grant_time, now_time]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_calculate_effective_balance__mutmut_orig, x_calculate_effective_balance__mutmut_mutants, args, kwargs, None)


def x_calculate_effective_balance__mutmut_orig(
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


def x_calculate_effective_balance__mutmut_1(
    current_balance: float, 
    last_grant_time: Optional[datetime], 
    now_time: datetime
) -> float:
    """
    Pure function: Calculate balance with continuous decay applied.
    Decay only applies if a grant time is present (since last faucet claim/spend).
    Ensures balance never drops below zero.
    """
    if last_grant_time is not None:
        return max(0.0, current_balance)

    elapsed_minutes = (now_time - last_grant_time).total_seconds() / 60.0
    elapsed_minutes = max(0.0, elapsed_minutes)
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_2(
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
        return max(None, current_balance)

    elapsed_minutes = (now_time - last_grant_time).total_seconds() / 60.0
    elapsed_minutes = max(0.0, elapsed_minutes)
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_3(
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
        return max(0.0, None)

    elapsed_minutes = (now_time - last_grant_time).total_seconds() / 60.0
    elapsed_minutes = max(0.0, elapsed_minutes)
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_4(
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
        return max(current_balance)

    elapsed_minutes = (now_time - last_grant_time).total_seconds() / 60.0
    elapsed_minutes = max(0.0, elapsed_minutes)
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_5(
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
        return max(0.0, )

    elapsed_minutes = (now_time - last_grant_time).total_seconds() / 60.0
    elapsed_minutes = max(0.0, elapsed_minutes)
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_6(
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
        return max(1.0, current_balance)

    elapsed_minutes = (now_time - last_grant_time).total_seconds() / 60.0
    elapsed_minutes = max(0.0, elapsed_minutes)
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_7(
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

    elapsed_minutes = None
    elapsed_minutes = max(0.0, elapsed_minutes)
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_8(
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

    elapsed_minutes = (now_time - last_grant_time).total_seconds() * 60.0
    elapsed_minutes = max(0.0, elapsed_minutes)
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_9(
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

    elapsed_minutes = (now_time + last_grant_time).total_seconds() / 60.0
    elapsed_minutes = max(0.0, elapsed_minutes)
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_10(
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

    elapsed_minutes = (now_time - last_grant_time).total_seconds() / 61.0
    elapsed_minutes = max(0.0, elapsed_minutes)
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_11(
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
    elapsed_minutes = None
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_12(
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
    elapsed_minutes = max(None, elapsed_minutes)
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_13(
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
    elapsed_minutes = max(0.0, None)
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_14(
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
    elapsed_minutes = max(elapsed_minutes)
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_15(
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
    elapsed_minutes = max(0.0, )
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_16(
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
    elapsed_minutes = max(1.0, elapsed_minutes)
    
    decay = elapsed_minutes * DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_17(
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
    
    decay = None
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_18(
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
    
    decay = elapsed_minutes / DECAY_RATE_PER_MINUTE
    effective = current_balance - decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_19(
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
    effective = None
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_20(
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
    effective = current_balance + decay
    
    return max(0.0, effective)


def x_calculate_effective_balance__mutmut_21(
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
    
    return max(None, effective)


def x_calculate_effective_balance__mutmut_22(
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
    
    return max(0.0, None)


def x_calculate_effective_balance__mutmut_23(
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
    
    return max(effective)


def x_calculate_effective_balance__mutmut_24(
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
    
    return max(0.0, )


def x_calculate_effective_balance__mutmut_25(
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
    
    return max(1.0, effective)

x_calculate_effective_balance__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_calculate_effective_balance__mutmut_1': x_calculate_effective_balance__mutmut_1, 
    'x_calculate_effective_balance__mutmut_2': x_calculate_effective_balance__mutmut_2, 
    'x_calculate_effective_balance__mutmut_3': x_calculate_effective_balance__mutmut_3, 
    'x_calculate_effective_balance__mutmut_4': x_calculate_effective_balance__mutmut_4, 
    'x_calculate_effective_balance__mutmut_5': x_calculate_effective_balance__mutmut_5, 
    'x_calculate_effective_balance__mutmut_6': x_calculate_effective_balance__mutmut_6, 
    'x_calculate_effective_balance__mutmut_7': x_calculate_effective_balance__mutmut_7, 
    'x_calculate_effective_balance__mutmut_8': x_calculate_effective_balance__mutmut_8, 
    'x_calculate_effective_balance__mutmut_9': x_calculate_effective_balance__mutmut_9, 
    'x_calculate_effective_balance__mutmut_10': x_calculate_effective_balance__mutmut_10, 
    'x_calculate_effective_balance__mutmut_11': x_calculate_effective_balance__mutmut_11, 
    'x_calculate_effective_balance__mutmut_12': x_calculate_effective_balance__mutmut_12, 
    'x_calculate_effective_balance__mutmut_13': x_calculate_effective_balance__mutmut_13, 
    'x_calculate_effective_balance__mutmut_14': x_calculate_effective_balance__mutmut_14, 
    'x_calculate_effective_balance__mutmut_15': x_calculate_effective_balance__mutmut_15, 
    'x_calculate_effective_balance__mutmut_16': x_calculate_effective_balance__mutmut_16, 
    'x_calculate_effective_balance__mutmut_17': x_calculate_effective_balance__mutmut_17, 
    'x_calculate_effective_balance__mutmut_18': x_calculate_effective_balance__mutmut_18, 
    'x_calculate_effective_balance__mutmut_19': x_calculate_effective_balance__mutmut_19, 
    'x_calculate_effective_balance__mutmut_20': x_calculate_effective_balance__mutmut_20, 
    'x_calculate_effective_balance__mutmut_21': x_calculate_effective_balance__mutmut_21, 
    'x_calculate_effective_balance__mutmut_22': x_calculate_effective_balance__mutmut_22, 
    'x_calculate_effective_balance__mutmut_23': x_calculate_effective_balance__mutmut_23, 
    'x_calculate_effective_balance__mutmut_24': x_calculate_effective_balance__mutmut_24, 
    'x_calculate_effective_balance__mutmut_25': x_calculate_effective_balance__mutmut_25
}
x_calculate_effective_balance__mutmut_orig.__name__ = 'x_calculate_effective_balance'


def attempt_spend(
    current_balance: float,
    last_grant_time: Optional[datetime],
    now_time: datetime,
    amount: float
) -> Tuple[bool, float]:
    args = [current_balance, last_grant_time, now_time, amount]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_attempt_spend__mutmut_orig, x_attempt_spend__mutmut_mutants, args, kwargs, None)


def x_attempt_spend__mutmut_orig(
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


def x_attempt_spend__mutmut_1(
    current_balance: float,
    last_grant_time: Optional[datetime],
    now_time: datetime,
    amount: float
) -> Tuple[bool, float]:
    """
    Pure function: Returns whether the spend is successful and the resulting (crystallized) balance.
    """
    effective = None
    
    if effective >= amount:
        return True, effective - amount
        
    return False, effective


def x_attempt_spend__mutmut_2(
    current_balance: float,
    last_grant_time: Optional[datetime],
    now_time: datetime,
    amount: float
) -> Tuple[bool, float]:
    """
    Pure function: Returns whether the spend is successful and the resulting (crystallized) balance.
    """
    effective = calculate_effective_balance(None, last_grant_time, now_time)
    
    if effective >= amount:
        return True, effective - amount
        
    return False, effective


def x_attempt_spend__mutmut_3(
    current_balance: float,
    last_grant_time: Optional[datetime],
    now_time: datetime,
    amount: float
) -> Tuple[bool, float]:
    """
    Pure function: Returns whether the spend is successful and the resulting (crystallized) balance.
    """
    effective = calculate_effective_balance(current_balance, None, now_time)
    
    if effective >= amount:
        return True, effective - amount
        
    return False, effective


def x_attempt_spend__mutmut_4(
    current_balance: float,
    last_grant_time: Optional[datetime],
    now_time: datetime,
    amount: float
) -> Tuple[bool, float]:
    """
    Pure function: Returns whether the spend is successful and the resulting (crystallized) balance.
    """
    effective = calculate_effective_balance(current_balance, last_grant_time, None)
    
    if effective >= amount:
        return True, effective - amount
        
    return False, effective


def x_attempt_spend__mutmut_5(
    current_balance: float,
    last_grant_time: Optional[datetime],
    now_time: datetime,
    amount: float
) -> Tuple[bool, float]:
    """
    Pure function: Returns whether the spend is successful and the resulting (crystallized) balance.
    """
    effective = calculate_effective_balance(last_grant_time, now_time)
    
    if effective >= amount:
        return True, effective - amount
        
    return False, effective


def x_attempt_spend__mutmut_6(
    current_balance: float,
    last_grant_time: Optional[datetime],
    now_time: datetime,
    amount: float
) -> Tuple[bool, float]:
    """
    Pure function: Returns whether the spend is successful and the resulting (crystallized) balance.
    """
    effective = calculate_effective_balance(current_balance, now_time)
    
    if effective >= amount:
        return True, effective - amount
        
    return False, effective


def x_attempt_spend__mutmut_7(
    current_balance: float,
    last_grant_time: Optional[datetime],
    now_time: datetime,
    amount: float
) -> Tuple[bool, float]:
    """
    Pure function: Returns whether the spend is successful and the resulting (crystallized) balance.
    """
    effective = calculate_effective_balance(current_balance, last_grant_time, )
    
    if effective >= amount:
        return True, effective - amount
        
    return False, effective


def x_attempt_spend__mutmut_8(
    current_balance: float,
    last_grant_time: Optional[datetime],
    now_time: datetime,
    amount: float
) -> Tuple[bool, float]:
    """
    Pure function: Returns whether the spend is successful and the resulting (crystallized) balance.
    """
    effective = calculate_effective_balance(current_balance, last_grant_time, now_time)
    
    if effective > amount:
        return True, effective - amount
        
    return False, effective


def x_attempt_spend__mutmut_9(
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
        return False, effective - amount
        
    return False, effective


def x_attempt_spend__mutmut_10(
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
        return True, effective + amount
        
    return False, effective


def x_attempt_spend__mutmut_11(
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
        
    return True, effective

x_attempt_spend__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_attempt_spend__mutmut_1': x_attempt_spend__mutmut_1, 
    'x_attempt_spend__mutmut_2': x_attempt_spend__mutmut_2, 
    'x_attempt_spend__mutmut_3': x_attempt_spend__mutmut_3, 
    'x_attempt_spend__mutmut_4': x_attempt_spend__mutmut_4, 
    'x_attempt_spend__mutmut_5': x_attempt_spend__mutmut_5, 
    'x_attempt_spend__mutmut_6': x_attempt_spend__mutmut_6, 
    'x_attempt_spend__mutmut_7': x_attempt_spend__mutmut_7, 
    'x_attempt_spend__mutmut_8': x_attempt_spend__mutmut_8, 
    'x_attempt_spend__mutmut_9': x_attempt_spend__mutmut_9, 
    'x_attempt_spend__mutmut_10': x_attempt_spend__mutmut_10, 
    'x_attempt_spend__mutmut_11': x_attempt_spend__mutmut_11
}
x_attempt_spend__mutmut_orig.__name__ = 'x_attempt_spend'


def calculate_verifier_bounty(rank: int) -> float:
    args = [rank]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_calculate_verifier_bounty__mutmut_orig, x_calculate_verifier_bounty__mutmut_mutants, args, kwargs, None)


def x_calculate_verifier_bounty__mutmut_orig(rank: int) -> float:
    """
    Pure function: Geometric series for verifier rewards based on rank (0-indexed).
    """
    return VERIFIER_BOUNTY_BASE * (VERIFIER_BOUNTY_RATIO ** rank)


def x_calculate_verifier_bounty__mutmut_1(rank: int) -> float:
    """
    Pure function: Geometric series for verifier rewards based on rank (0-indexed).
    """
    return VERIFIER_BOUNTY_BASE / (VERIFIER_BOUNTY_RATIO ** rank)


def x_calculate_verifier_bounty__mutmut_2(rank: int) -> float:
    """
    Pure function: Geometric series for verifier rewards based on rank (0-indexed).
    """
    return VERIFIER_BOUNTY_BASE * (VERIFIER_BOUNTY_RATIO * rank)

x_calculate_verifier_bounty__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_calculate_verifier_bounty__mutmut_1': x_calculate_verifier_bounty__mutmut_1, 
    'x_calculate_verifier_bounty__mutmut_2': x_calculate_verifier_bounty__mutmut_2
}
x_calculate_verifier_bounty__mutmut_orig.__name__ = 'x_calculate_verifier_bounty'


def calculate_consensus(worker_output: str, verifier_outputs: List[str]) -> Optional[str]:
    args = [worker_output, verifier_outputs]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_calculate_consensus__mutmut_orig, x_calculate_consensus__mutmut_mutants, args, kwargs, None)


def x_calculate_consensus__mutmut_orig(worker_output: str, verifier_outputs: List[str]) -> Optional[str]:
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


def x_calculate_consensus__mutmut_1(worker_output: str, verifier_outputs: List[str]) -> Optional[str]:
    """
    Pure function: Determine if consensus matches worker output.
    Returns 'HONEST', 'DISHONEST', or None (if no verifiers).
    """
    if verifier_outputs:
        return None
        
    matching = sum(1 for output in verifier_outputs if output == worker_output)
    total_verifiers = len(verifier_outputs)
    
    # >= 67% consensus = HONEST
    if matching / total_verifiers >= CONSENSUS_THRESHOLD:
        return "HONEST"
    return "DISHONEST"


def x_calculate_consensus__mutmut_2(worker_output: str, verifier_outputs: List[str]) -> Optional[str]:
    """
    Pure function: Determine if consensus matches worker output.
    Returns 'HONEST', 'DISHONEST', or None (if no verifiers).
    """
    if not verifier_outputs:
        return None
        
    matching = None
    total_verifiers = len(verifier_outputs)
    
    # >= 67% consensus = HONEST
    if matching / total_verifiers >= CONSENSUS_THRESHOLD:
        return "HONEST"
    return "DISHONEST"


def x_calculate_consensus__mutmut_3(worker_output: str, verifier_outputs: List[str]) -> Optional[str]:
    """
    Pure function: Determine if consensus matches worker output.
    Returns 'HONEST', 'DISHONEST', or None (if no verifiers).
    """
    if not verifier_outputs:
        return None
        
    matching = sum(None)
    total_verifiers = len(verifier_outputs)
    
    # >= 67% consensus = HONEST
    if matching / total_verifiers >= CONSENSUS_THRESHOLD:
        return "HONEST"
    return "DISHONEST"


def x_calculate_consensus__mutmut_4(worker_output: str, verifier_outputs: List[str]) -> Optional[str]:
    """
    Pure function: Determine if consensus matches worker output.
    Returns 'HONEST', 'DISHONEST', or None (if no verifiers).
    """
    if not verifier_outputs:
        return None
        
    matching = sum(2 for output in verifier_outputs if output == worker_output)
    total_verifiers = len(verifier_outputs)
    
    # >= 67% consensus = HONEST
    if matching / total_verifiers >= CONSENSUS_THRESHOLD:
        return "HONEST"
    return "DISHONEST"


def x_calculate_consensus__mutmut_5(worker_output: str, verifier_outputs: List[str]) -> Optional[str]:
    """
    Pure function: Determine if consensus matches worker output.
    Returns 'HONEST', 'DISHONEST', or None (if no verifiers).
    """
    if not verifier_outputs:
        return None
        
    matching = sum(1 for output in verifier_outputs if output != worker_output)
    total_verifiers = len(verifier_outputs)
    
    # >= 67% consensus = HONEST
    if matching / total_verifiers >= CONSENSUS_THRESHOLD:
        return "HONEST"
    return "DISHONEST"


def x_calculate_consensus__mutmut_6(worker_output: str, verifier_outputs: List[str]) -> Optional[str]:
    """
    Pure function: Determine if consensus matches worker output.
    Returns 'HONEST', 'DISHONEST', or None (if no verifiers).
    """
    if not verifier_outputs:
        return None
        
    matching = sum(1 for output in verifier_outputs if output == worker_output)
    total_verifiers = None
    
    # >= 67% consensus = HONEST
    if matching / total_verifiers >= CONSENSUS_THRESHOLD:
        return "HONEST"
    return "DISHONEST"


def x_calculate_consensus__mutmut_7(worker_output: str, verifier_outputs: List[str]) -> Optional[str]:
    """
    Pure function: Determine if consensus matches worker output.
    Returns 'HONEST', 'DISHONEST', or None (if no verifiers).
    """
    if not verifier_outputs:
        return None
        
    matching = sum(1 for output in verifier_outputs if output == worker_output)
    total_verifiers = len(verifier_outputs)
    
    # >= 67% consensus = HONEST
    if matching * total_verifiers >= CONSENSUS_THRESHOLD:
        return "HONEST"
    return "DISHONEST"


def x_calculate_consensus__mutmut_8(worker_output: str, verifier_outputs: List[str]) -> Optional[str]:
    """
    Pure function: Determine if consensus matches worker output.
    Returns 'HONEST', 'DISHONEST', or None (if no verifiers).
    """
    if not verifier_outputs:
        return None
        
    matching = sum(1 for output in verifier_outputs if output == worker_output)
    total_verifiers = len(verifier_outputs)
    
    # >= 67% consensus = HONEST
    if matching / total_verifiers > CONSENSUS_THRESHOLD:
        return "HONEST"
    return "DISHONEST"


def x_calculate_consensus__mutmut_9(worker_output: str, verifier_outputs: List[str]) -> Optional[str]:
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
        return "XXHONESTXX"
    return "DISHONEST"


def x_calculate_consensus__mutmut_10(worker_output: str, verifier_outputs: List[str]) -> Optional[str]:
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
        return "honest"
    return "DISHONEST"


def x_calculate_consensus__mutmut_11(worker_output: str, verifier_outputs: List[str]) -> Optional[str]:
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
    return "XXDISHONESTXX"


def x_calculate_consensus__mutmut_12(worker_output: str, verifier_outputs: List[str]) -> Optional[str]:
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
    return "dishonest"

x_calculate_consensus__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_calculate_consensus__mutmut_1': x_calculate_consensus__mutmut_1, 
    'x_calculate_consensus__mutmut_2': x_calculate_consensus__mutmut_2, 
    'x_calculate_consensus__mutmut_3': x_calculate_consensus__mutmut_3, 
    'x_calculate_consensus__mutmut_4': x_calculate_consensus__mutmut_4, 
    'x_calculate_consensus__mutmut_5': x_calculate_consensus__mutmut_5, 
    'x_calculate_consensus__mutmut_6': x_calculate_consensus__mutmut_6, 
    'x_calculate_consensus__mutmut_7': x_calculate_consensus__mutmut_7, 
    'x_calculate_consensus__mutmut_8': x_calculate_consensus__mutmut_8, 
    'x_calculate_consensus__mutmut_9': x_calculate_consensus__mutmut_9, 
    'x_calculate_consensus__mutmut_10': x_calculate_consensus__mutmut_10, 
    'x_calculate_consensus__mutmut_11': x_calculate_consensus__mutmut_11, 
    'x_calculate_consensus__mutmut_12': x_calculate_consensus__mutmut_12
}
x_calculate_consensus__mutmut_orig.__name__ = 'x_calculate_consensus'


def calculate_worker_stake_deduction(
    worker_payment: float, 
    stake_percentage: float
) -> Optional[float]:
    args = [worker_payment, stake_percentage]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_calculate_worker_stake_deduction__mutmut_orig, x_calculate_worker_stake_deduction__mutmut_mutants, args, kwargs, None)


def x_calculate_worker_stake_deduction__mutmut_orig(
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


def x_calculate_worker_stake_deduction__mutmut_1(
    worker_payment: float, 
    stake_percentage: float
) -> Optional[float]:
    """
    Pure function: Calculate how much a worker needs to stake based on percentage.
    Returns None if percentage is out of bounds (0-100).
    """
    if stake_percentage < 0 and stake_percentage > 100:
        return None
        
    return worker_payment * (stake_percentage / 100.0)


def x_calculate_worker_stake_deduction__mutmut_2(
    worker_payment: float, 
    stake_percentage: float
) -> Optional[float]:
    """
    Pure function: Calculate how much a worker needs to stake based on percentage.
    Returns None if percentage is out of bounds (0-100).
    """
    if stake_percentage <= 0 or stake_percentage > 100:
        return None
        
    return worker_payment * (stake_percentage / 100.0)


def x_calculate_worker_stake_deduction__mutmut_3(
    worker_payment: float, 
    stake_percentage: float
) -> Optional[float]:
    """
    Pure function: Calculate how much a worker needs to stake based on percentage.
    Returns None if percentage is out of bounds (0-100).
    """
    if stake_percentage < 1 or stake_percentage > 100:
        return None
        
    return worker_payment * (stake_percentage / 100.0)


def x_calculate_worker_stake_deduction__mutmut_4(
    worker_payment: float, 
    stake_percentage: float
) -> Optional[float]:
    """
    Pure function: Calculate how much a worker needs to stake based on percentage.
    Returns None if percentage is out of bounds (0-100).
    """
    if stake_percentage < 0 or stake_percentage >= 100:
        return None
        
    return worker_payment * (stake_percentage / 100.0)


def x_calculate_worker_stake_deduction__mutmut_5(
    worker_payment: float, 
    stake_percentage: float
) -> Optional[float]:
    """
    Pure function: Calculate how much a worker needs to stake based on percentage.
    Returns None if percentage is out of bounds (0-100).
    """
    if stake_percentage < 0 or stake_percentage > 101:
        return None
        
    return worker_payment * (stake_percentage / 100.0)


def x_calculate_worker_stake_deduction__mutmut_6(
    worker_payment: float, 
    stake_percentage: float
) -> Optional[float]:
    """
    Pure function: Calculate how much a worker needs to stake based on percentage.
    Returns None if percentage is out of bounds (0-100).
    """
    if stake_percentage < 0 or stake_percentage > 100:
        return None
        
    return worker_payment / (stake_percentage / 100.0)


def x_calculate_worker_stake_deduction__mutmut_7(
    worker_payment: float, 
    stake_percentage: float
) -> Optional[float]:
    """
    Pure function: Calculate how much a worker needs to stake based on percentage.
    Returns None if percentage is out of bounds (0-100).
    """
    if stake_percentage < 0 or stake_percentage > 100:
        return None
        
    return worker_payment * (stake_percentage * 100.0)


def x_calculate_worker_stake_deduction__mutmut_8(
    worker_payment: float, 
    stake_percentage: float
) -> Optional[float]:
    """
    Pure function: Calculate how much a worker needs to stake based on percentage.
    Returns None if percentage is out of bounds (0-100).
    """
    if stake_percentage < 0 or stake_percentage > 100:
        return None
        
    return worker_payment * (stake_percentage / 101.0)

x_calculate_worker_stake_deduction__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_calculate_worker_stake_deduction__mutmut_1': x_calculate_worker_stake_deduction__mutmut_1, 
    'x_calculate_worker_stake_deduction__mutmut_2': x_calculate_worker_stake_deduction__mutmut_2, 
    'x_calculate_worker_stake_deduction__mutmut_3': x_calculate_worker_stake_deduction__mutmut_3, 
    'x_calculate_worker_stake_deduction__mutmut_4': x_calculate_worker_stake_deduction__mutmut_4, 
    'x_calculate_worker_stake_deduction__mutmut_5': x_calculate_worker_stake_deduction__mutmut_5, 
    'x_calculate_worker_stake_deduction__mutmut_6': x_calculate_worker_stake_deduction__mutmut_6, 
    'x_calculate_worker_stake_deduction__mutmut_7': x_calculate_worker_stake_deduction__mutmut_7, 
    'x_calculate_worker_stake_deduction__mutmut_8': x_calculate_worker_stake_deduction__mutmut_8
}
x_calculate_worker_stake_deduction__mutmut_orig.__name__ = 'x_calculate_worker_stake_deduction'
