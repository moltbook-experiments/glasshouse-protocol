from typing import List, Dict, Any

def calculate_symmetric_trust_score(
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

def get_worker_trust_score(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, all_results, "worker")

def get_verifier_trust_score(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    return calculate_symmetric_trust_score(agent_id, all_results, "verifier")

def get_requester_trust_score(agent_id: str, all_results: List[Dict[str, Any]]) -> int:
    # v1 Placeholder
    return 0
