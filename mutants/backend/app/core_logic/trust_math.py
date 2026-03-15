from typing import List, Dict, Any
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

def calculate_symmetric_trust_score(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    args = [target_agent_id, all_results, role]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_calculate_symmetric_trust_score__mutmut_orig, x_calculate_symmetric_trust_score__mutmut_mutants, args, kwargs, None)

def x_calculate_symmetric_trust_score__mutmut_orig(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_1(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = None
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_2(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = None
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_3(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(None)
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_4(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get(None, ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_5(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', None))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_6(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get(''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_7(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_8(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('XXjob_idXX', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_9(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('JOB_ID', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_10(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', 'XXXX'))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_11(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_12(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            break
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_13(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_14(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = None
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_15(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(None)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_16(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = None

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_17(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_18(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            break
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_19(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = None
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_20(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(None, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_21(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=None)
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_22(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_23(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, )
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_24(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: None)
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_25(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get(None, ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_26(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', None))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_27(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get(''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_28(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_29(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('XXcreated_atXX', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_30(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('CREATED_AT', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_31(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', 'XXXX'))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_32(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = None

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_33(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = None
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_34(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[1]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_35(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = None
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_36(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get(None) == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_37(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('XXagent_idXX') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_38(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('AGENT_ID') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_39(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') != target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_40(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = ""
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_41(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" or is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_42(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role != "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_43(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "XXworkerXX" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_44(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "WORKER" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_45(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = None
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_46(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get(None)
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_47(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('XXoutputXX')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_48(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('OUTPUT')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_49(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" or not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_50(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role != "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_51(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "XXverifierXX" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_52(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "VERIFIER" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_53(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_54(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[2:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_55(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get(None) == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_56(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('XXagent_idXX') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_57(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('AGENT_ID') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_58(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') != target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_59(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = None
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_60(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get(None)
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_61(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('XXoutputXX')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_62(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('OUTPUT')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_63(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    return
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_64(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_65(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = None
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_66(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get(None)
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_67(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('XXagent_idXX')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_68(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('AGENT_ID')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_69(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id or r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_70(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id == target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_71(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get(None) == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_72(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('XXoutputXX') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_73(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('OUTPUT') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_74(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') != agent_output_in_this_job:
                    agreements_from_distinct_agents.add(peer_id)

    return len(agreements_from_distinct_agents)

def x_calculate_symmetric_trust_score__mutmut_75(
    target_agent_id: str,
    all_results: List[Dict[str, Any]],
    role: str
) -> int:
    """
    Pure function: Calculate trust scores over all results without DuckDB parsing.
    role can be "worker" or "verifier".

    - worker: How many distinct agents agreed with this agent when it was the worker?
    - verifier: How many distinct agents agreed with this agent when it was a verifier?
    """
    # Group results by job_id
    jobs: Dict[str, List[Dict[str, Any]]] = {}
    for r in all_results:
        job_id = str(r.get('job_id', ''))
        if not job_id:
            continue
        if job_id not in jobs:
            jobs[job_id] = []
        jobs[job_id].append(r)
        
    agreements_from_distinct_agents = set()

    for job_id, job_results in jobs.items():
        if not job_results:
            continue
            
        # Assuming job_results is ordered by created_at ascending as it relies on caller ordering it correctly.
        # But to be safe, sort them purely based on created_at iso string.
        try:
            sorted_results = sorted(job_results, key=lambda x: x.get('created_at', ''))
        except:
            sorted_results = job_results

        worker_result = sorted_results[0]
        is_agent_worker = (worker_result.get('agent_id') == target_agent_id)
        
        agent_output_in_this_job = None
        
        # Determine if the target agent participated in the requested role for this job
        if role == "worker" and is_agent_worker:
            agent_output_in_this_job = worker_result.get('output')
            
        elif role == "verifier" and not is_agent_worker:
            # Find the agent's verifier submission
            for r in sorted_results[1:]:
                if r.get('agent_id') == target_agent_id:
                    agent_output_in_this_job = r.get('output')
                    break
                    
        if agent_output_in_this_job is not None:
            # Look for other agents in the same job who output the exact same thing
            for r in sorted_results:
                peer_id = r.get('agent_id')
                if peer_id != target_agent_id and r.get('output') == agent_output_in_this_job:
                    agreements_from_distinct_agents.add(None)

    return len(agreements_from_distinct_agents)

x_calculate_symmetric_trust_score__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_calculate_symmetric_trust_score__mutmut_1': x_calculate_symmetric_trust_score__mutmut_1, 
    'x_calculate_symmetric_trust_score__mutmut_2': x_calculate_symmetric_trust_score__mutmut_2, 
    'x_calculate_symmetric_trust_score__mutmut_3': x_calculate_symmetric_trust_score__mutmut_3, 
    'x_calculate_symmetric_trust_score__mutmut_4': x_calculate_symmetric_trust_score__mutmut_4, 
    'x_calculate_symmetric_trust_score__mutmut_5': x_calculate_symmetric_trust_score__mutmut_5, 
    'x_calculate_symmetric_trust_score__mutmut_6': x_calculate_symmetric_trust_score__mutmut_6, 
    'x_calculate_symmetric_trust_score__mutmut_7': x_calculate_symmetric_trust_score__mutmut_7, 
    'x_calculate_symmetric_trust_score__mutmut_8': x_calculate_symmetric_trust_score__mutmut_8, 
    'x_calculate_symmetric_trust_score__mutmut_9': x_calculate_symmetric_trust_score__mutmut_9, 
    'x_calculate_symmetric_trust_score__mutmut_10': x_calculate_symmetric_trust_score__mutmut_10, 
    'x_calculate_symmetric_trust_score__mutmut_11': x_calculate_symmetric_trust_score__mutmut_11, 
    'x_calculate_symmetric_trust_score__mutmut_12': x_calculate_symmetric_trust_score__mutmut_12, 
    'x_calculate_symmetric_trust_score__mutmut_13': x_calculate_symmetric_trust_score__mutmut_13, 
    'x_calculate_symmetric_trust_score__mutmut_14': x_calculate_symmetric_trust_score__mutmut_14, 
    'x_calculate_symmetric_trust_score__mutmut_15': x_calculate_symmetric_trust_score__mutmut_15, 
    'x_calculate_symmetric_trust_score__mutmut_16': x_calculate_symmetric_trust_score__mutmut_16, 
    'x_calculate_symmetric_trust_score__mutmut_17': x_calculate_symmetric_trust_score__mutmut_17, 
    'x_calculate_symmetric_trust_score__mutmut_18': x_calculate_symmetric_trust_score__mutmut_18, 
    'x_calculate_symmetric_trust_score__mutmut_19': x_calculate_symmetric_trust_score__mutmut_19, 
    'x_calculate_symmetric_trust_score__mutmut_20': x_calculate_symmetric_trust_score__mutmut_20, 
    'x_calculate_symmetric_trust_score__mutmut_21': x_calculate_symmetric_trust_score__mutmut_21, 
    'x_calculate_symmetric_trust_score__mutmut_22': x_calculate_symmetric_trust_score__mutmut_22, 
    'x_calculate_symmetric_trust_score__mutmut_23': x_calculate_symmetric_trust_score__mutmut_23, 
    'x_calculate_symmetric_trust_score__mutmut_24': x_calculate_symmetric_trust_score__mutmut_24, 
    'x_calculate_symmetric_trust_score__mutmut_25': x_calculate_symmetric_trust_score__mutmut_25, 
    'x_calculate_symmetric_trust_score__mutmut_26': x_calculate_symmetric_trust_score__mutmut_26, 
    'x_calculate_symmetric_trust_score__mutmut_27': x_calculate_symmetric_trust_score__mutmut_27, 
    'x_calculate_symmetric_trust_score__mutmut_28': x_calculate_symmetric_trust_score__mutmut_28, 
    'x_calculate_symmetric_trust_score__mutmut_29': x_calculate_symmetric_trust_score__mutmut_29, 
    'x_calculate_symmetric_trust_score__mutmut_30': x_calculate_symmetric_trust_score__mutmut_30, 
    'x_calculate_symmetric_trust_score__mutmut_31': x_calculate_symmetric_trust_score__mutmut_31, 
    'x_calculate_symmetric_trust_score__mutmut_32': x_calculate_symmetric_trust_score__mutmut_32, 
    'x_calculate_symmetric_trust_score__mutmut_33': x_calculate_symmetric_trust_score__mutmut_33, 
    'x_calculate_symmetric_trust_score__mutmut_34': x_calculate_symmetric_trust_score__mutmut_34, 
    'x_calculate_symmetric_trust_score__mutmut_35': x_calculate_symmetric_trust_score__mutmut_35, 
    'x_calculate_symmetric_trust_score__mutmut_36': x_calculate_symmetric_trust_score__mutmut_36, 
    'x_calculate_symmetric_trust_score__mutmut_37': x_calculate_symmetric_trust_score__mutmut_37, 
    'x_calculate_symmetric_trust_score__mutmut_38': x_calculate_symmetric_trust_score__mutmut_38, 
    'x_calculate_symmetric_trust_score__mutmut_39': x_calculate_symmetric_trust_score__mutmut_39, 
    'x_calculate_symmetric_trust_score__mutmut_40': x_calculate_symmetric_trust_score__mutmut_40, 
    'x_calculate_symmetric_trust_score__mutmut_41': x_calculate_symmetric_trust_score__mutmut_41, 
    'x_calculate_symmetric_trust_score__mutmut_42': x_calculate_symmetric_trust_score__mutmut_42, 
    'x_calculate_symmetric_trust_score__mutmut_43': x_calculate_symmetric_trust_score__mutmut_43, 
    'x_calculate_symmetric_trust_score__mutmut_44': x_calculate_symmetric_trust_score__mutmut_44, 
    'x_calculate_symmetric_trust_score__mutmut_45': x_calculate_symmetric_trust_score__mutmut_45, 
    'x_calculate_symmetric_trust_score__mutmut_46': x_calculate_symmetric_trust_score__mutmut_46, 
    'x_calculate_symmetric_trust_score__mutmut_47': x_calculate_symmetric_trust_score__mutmut_47, 
    'x_calculate_symmetric_trust_score__mutmut_48': x_calculate_symmetric_trust_score__mutmut_48, 
    'x_calculate_symmetric_trust_score__mutmut_49': x_calculate_symmetric_trust_score__mutmut_49, 
    'x_calculate_symmetric_trust_score__mutmut_50': x_calculate_symmetric_trust_score__mutmut_50, 
    'x_calculate_symmetric_trust_score__mutmut_51': x_calculate_symmetric_trust_score__mutmut_51, 
    'x_calculate_symmetric_trust_score__mutmut_52': x_calculate_symmetric_trust_score__mutmut_52, 
    'x_calculate_symmetric_trust_score__mutmut_53': x_calculate_symmetric_trust_score__mutmut_53, 
    'x_calculate_symmetric_trust_score__mutmut_54': x_calculate_symmetric_trust_score__mutmut_54, 
    'x_calculate_symmetric_trust_score__mutmut_55': x_calculate_symmetric_trust_score__mutmut_55, 
    'x_calculate_symmetric_trust_score__mutmut_56': x_calculate_symmetric_trust_score__mutmut_56, 
    'x_calculate_symmetric_trust_score__mutmut_57': x_calculate_symmetric_trust_score__mutmut_57, 
    'x_calculate_symmetric_trust_score__mutmut_58': x_calculate_symmetric_trust_score__mutmut_58, 
    'x_calculate_symmetric_trust_score__mutmut_59': x_calculate_symmetric_trust_score__mutmut_59, 
    'x_calculate_symmetric_trust_score__mutmut_60': x_calculate_symmetric_trust_score__mutmut_60, 
    'x_calculate_symmetric_trust_score__mutmut_61': x_calculate_symmetric_trust_score__mutmut_61, 
    'x_calculate_symmetric_trust_score__mutmut_62': x_calculate_symmetric_trust_score__mutmut_62, 
    'x_calculate_symmetric_trust_score__mutmut_63': x_calculate_symmetric_trust_score__mutmut_63, 
    'x_calculate_symmetric_trust_score__mutmut_64': x_calculate_symmetric_trust_score__mutmut_64, 
    'x_calculate_symmetric_trust_score__mutmut_65': x_calculate_symmetric_trust_score__mutmut_65, 
    'x_calculate_symmetric_trust_score__mutmut_66': x_calculate_symmetric_trust_score__mutmut_66, 
    'x_calculate_symmetric_trust_score__mutmut_67': x_calculate_symmetric_trust_score__mutmut_67, 
    'x_calculate_symmetric_trust_score__mutmut_68': x_calculate_symmetric_trust_score__mutmut_68, 
    'x_calculate_symmetric_trust_score__mutmut_69': x_calculate_symmetric_trust_score__mutmut_69, 
    'x_calculate_symmetric_trust_score__mutmut_70': x_calculate_symmetric_trust_score__mutmut_70, 
    'x_calculate_symmetric_trust_score__mutmut_71': x_calculate_symmetric_trust_score__mutmut_71, 
    'x_calculate_symmetric_trust_score__mutmut_72': x_calculate_symmetric_trust_score__mutmut_72, 
    'x_calculate_symmetric_trust_score__mutmut_73': x_calculate_symmetric_trust_score__mutmut_73, 
    'x_calculate_symmetric_trust_score__mutmut_74': x_calculate_symmetric_trust_score__mutmut_74, 
    'x_calculate_symmetric_trust_score__mutmut_75': x_calculate_symmetric_trust_score__mutmut_75
}
x_calculate_symmetric_trust_score__mutmut_orig.__name__ = 'x_calculate_symmetric_trust_score'

def get_worker_trust_score(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    args = [agent_id, all_results]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_worker_trust_score__mutmut_orig, x_get_worker_trust_score__mutmut_mutants, args, kwargs, None)

def x_get_worker_trust_score__mutmut_orig(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, all_results, "worker")

def x_get_worker_trust_score__mutmut_1(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(None, all_results, "worker")

def x_get_worker_trust_score__mutmut_2(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, None, "worker")

def x_get_worker_trust_score__mutmut_3(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, all_results, None)

def x_get_worker_trust_score__mutmut_4(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(all_results, "worker")

def x_get_worker_trust_score__mutmut_5(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, "worker")

def x_get_worker_trust_score__mutmut_6(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, all_results, )

def x_get_worker_trust_score__mutmut_7(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, all_results, "XXworkerXX")

def x_get_worker_trust_score__mutmut_8(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, all_results, "WORKER")

x_get_worker_trust_score__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_worker_trust_score__mutmut_1': x_get_worker_trust_score__mutmut_1, 
    'x_get_worker_trust_score__mutmut_2': x_get_worker_trust_score__mutmut_2, 
    'x_get_worker_trust_score__mutmut_3': x_get_worker_trust_score__mutmut_3, 
    'x_get_worker_trust_score__mutmut_4': x_get_worker_trust_score__mutmut_4, 
    'x_get_worker_trust_score__mutmut_5': x_get_worker_trust_score__mutmut_5, 
    'x_get_worker_trust_score__mutmut_6': x_get_worker_trust_score__mutmut_6, 
    'x_get_worker_trust_score__mutmut_7': x_get_worker_trust_score__mutmut_7, 
    'x_get_worker_trust_score__mutmut_8': x_get_worker_trust_score__mutmut_8
}
x_get_worker_trust_score__mutmut_orig.__name__ = 'x_get_worker_trust_score'

def get_verifier_trust_score(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    args = [agent_id, all_results]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_verifier_trust_score__mutmut_orig, x_get_verifier_trust_score__mutmut_mutants, args, kwargs, None)

def x_get_verifier_trust_score__mutmut_orig(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, all_results, "verifier")

def x_get_verifier_trust_score__mutmut_1(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(None, all_results, "verifier")

def x_get_verifier_trust_score__mutmut_2(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, None, "verifier")

def x_get_verifier_trust_score__mutmut_3(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, all_results, None)

def x_get_verifier_trust_score__mutmut_4(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(all_results, "verifier")

def x_get_verifier_trust_score__mutmut_5(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, "verifier")

def x_get_verifier_trust_score__mutmut_6(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, all_results, )

def x_get_verifier_trust_score__mutmut_7(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, all_results, "XXverifierXX")

def x_get_verifier_trust_score__mutmut_8(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, all_results, "VERIFIER")

x_get_verifier_trust_score__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_verifier_trust_score__mutmut_1': x_get_verifier_trust_score__mutmut_1, 
    'x_get_verifier_trust_score__mutmut_2': x_get_verifier_trust_score__mutmut_2, 
    'x_get_verifier_trust_score__mutmut_3': x_get_verifier_trust_score__mutmut_3, 
    'x_get_verifier_trust_score__mutmut_4': x_get_verifier_trust_score__mutmut_4, 
    'x_get_verifier_trust_score__mutmut_5': x_get_verifier_trust_score__mutmut_5, 
    'x_get_verifier_trust_score__mutmut_6': x_get_verifier_trust_score__mutmut_6, 
    'x_get_verifier_trust_score__mutmut_7': x_get_verifier_trust_score__mutmut_7, 
    'x_get_verifier_trust_score__mutmut_8': x_get_verifier_trust_score__mutmut_8
}
x_get_verifier_trust_score__mutmut_orig.__name__ = 'x_get_verifier_trust_score'

def get_requester_trust_score(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    args = [agent_id, all_results]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_requester_trust_score__mutmut_orig, x_get_requester_trust_score__mutmut_mutants, args, kwargs, None)

def x_get_requester_trust_score__mutmut_orig(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    # v1 Placeholder
    return 0

def x_get_requester_trust_score__mutmut_1(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    # v1 Placeholder
    return 1

x_get_requester_trust_score__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_requester_trust_score__mutmut_1': x_get_requester_trust_score__mutmut_1
}
x_get_requester_trust_score__mutmut_orig.__name__ = 'x_get_requester_trust_score'
