from fastapi import FastAPI, Depends, Request, HTTPException, status, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .moltbook_auth import get_verified_agent
from .db import init_db, JobRepository, AgentRepository, ResultRepository, get_all, update_agent_trust_score
from pydantic import BaseModel, Field, constr, validator
from typing import Optional, List, Dict, Any, Literal
from uuid import uuid4, UUID
from datetime import datetime
import os
from .sync_github import trigger_sync
from starlette.middleware.base import BaseHTTPMiddleware
from .reputation import ReputationService, WORKER_REWARD
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# Rate Limiter Setup
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Services
job_repo = JobRepository()
agent_repo = AgentRepository()
result_repo = ResultRepository()
reputation_service = ReputationService()

# Middleware for Sync
class GitHubSyncMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Background sync trigger - non-blocking preferred but doing simple call here
        # Ideally use BackgroundTasks, but Middleware runs around request
        # We push this to a BackgroundTask via FastAPI later or just call it if fast enough
        # Actually, middleware dispatch is async, so we can't easily add BackgroundTask to response here without messy hacks.
        # Let's use a utility function call that does the check.
        # trigger_sync({...}) does its own throttle check.
        try:
            if request.method in ["POST", "PUT", "PATCH"]: # Only sync on state change makes sense usually, but user asked for "visit site" too
                # Mapping local DB files to repo paths
                # Assuming simple mapping for MVP
                # db.JOBS_FILE -> backend/data/jobs.jsonl
                pass 
                # We will invoke this inside route handlers instead for cleaner control
        except:
             pass
        return response

app.add_middleware(GitHubSyncMiddleware)

def try_sync_db():
    try:
        # Determine actual paths from imported repo instances or DB module
        from .db import JOBS_FILE, AGENTS_FILE, RESULTS_FILE
        file_map = {
            JOBS_FILE: "backend/data/jobs.jsonl",
            AGENTS_FILE: "backend/data/agents.jsonl",
            RESULTS_FILE: "backend/data/results.jsonl"
        }
        trigger_sync(file_map)
    except Exception as e:
        print(f"Sync trigger failed: {e}")


# Mount Static Files
try:
    app.mount("/static", StaticFiles(directory="backend/static"), name="static")
except RuntimeError:
    # already mounted in some contexts or directory missing (create it if missing)
    pass

templates = Jinja2Templates(directory="backend/templates")

# Initialize Persistent Repositories
job_repo = JobRepository()
agent_repo = AgentRepository()
result_repo = ResultRepository()

@app.on_event("startup")
def startup_event():
    init_db()

class AgentRegistration(BaseModel):
    capabilities: List[constr(max_length=256)] = []
    payment_address: Optional[str] = Field(None, max_length=128)
    metadata: Optional[Dict[str, Any]] = None

class AgentProfileUpdate(BaseModel):
    self_introduction: str = Field(..., max_length=500)

class JobManifest(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    # Allow for a detailed description of the job (markdown supported potentially in the future)
    description: Optional[str] = Field(None, max_length=2000) 
    repo: str = Field(..., max_length=512)
    commit: str = Field(..., max_length=128)
    input_url: str = Field(..., max_length=2048)
    entrypoint: str = Field(..., max_length=256)
    assigned_agent_id: Optional[str] = Field(None, max_length=128)
    protocol_version: Optional[str] = Field("v1.0", max_length=16)
    expected_compute_time_seconds: int = Field(..., gt=0)
    verification_tier: Literal["small", "medium", "large"]
    metadata: Optional[Dict[str, Any]] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

class ResultRecord(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    job_id: UUID
    output: str = Field(..., max_length=10000)
    output_hash: Optional[str] = Field(None, max_length=128)
    runtime_meta: Optional[Dict[str, Any]] = None
    proof: Optional[Dict[str, Any]] = None
    worker_stake: float = Field(default=0.0, ge=0)
    verifier_stake: float = Field(default=0.0, ge=0)
    consensus: Optional[Literal["HONEST", "DISHONEST"]] = None
    verification_window_open_at: Optional[str] = None
    agent_id: str
    agent_snapshot: Dict[str, Any]
    verified_at: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

@app.post("/faucet/claim")
@limiter.limit("5/hour")
def claim_faucet(request: Request, agent=Depends(get_verified_agent)):
    """Claim free GLS tokens. Rate limited globally."""
    if reputation_service.process_faucet_claim(agent["id"]):
        updated = agent_repo.get(agent["id"])
        return {
            "status": "success",
            "balance": updated.get("balance"),
            "message": "Granted 105 GLS. Valid for 15 minutes."
        }
    else:
        raise HTTPException(
            status_code=429,
            detail="Faucet is dry (Global Rate Limit) or you are calling too fast. Please wait."
        )

@app.post("/jobs")
@limiter.limit("10/minute")
def submit_job(request: Request, manifest: JobManifest, background_tasks: BackgroundTasks, agent=Depends(get_verified_agent)):
    # 1. Enforce Solvency & Activity (State Change)
    # Crystallize balance to stop decay chain (Proof of Submission)
    current_bal = reputation_service.crystallize_balance(agent["id"])
    
    COST = 100.0
    if current_bal < COST:
        raise HTTPException(
            status_code=402,
            detail=f"Insufficient funds for settlement. Balance: {current_bal:.2f}. Required: {COST}. Use POST /faucet/claim"
        )

    # Convert UUID to string for storage consistency
    data = manifest.dict()
    data['id'] = str(data['id'])
    
    # Store owner info
    data['created_by'] = agent['id']
    
    # Map verification tier to required verifier count
    tier_map = {
        "small": 2,
        "medium": 4,
        "large": 5
    }
    data['required_verifiers'] = tier_map[manifest.verification_tier]
    
    job_repo.add(data)
    background_tasks.add_task(try_sync_db)
    return {"id": manifest.id, "created_at": manifest.created_at, "manifest": data}


@app.get("/jobs")
def list_jobs():
    return {"jobs": job_repo.list_all()}

@app.post("/agents/onboard")
@limiter.limit("10/minute")
async def register_agent(
    request: Request,
    reg_data: AgentRegistration,
    agent: Dict[str, Any] = Depends(get_verified_agent)
):
    agent_id = agent.get("id")
    if not agent_id:
         raise HTTPException(status_code=400, detail="Moltbook identity missing agent ID")
    
    # Save registration data
    # In a real app we'd merge with existing or create new
    # For JSONL MVP, we just append or update in memory then save
    
    agent_data = reg_data.dict()
    agent_data['id'] = agent_id
    agent_data['registered_at'] = datetime.utcnow().isoformat() + "Z"
    
    # Simple upsert logic could go here, but for now just appending
    agent_repo.add(agent_data)
    
    return {"status": "registered", "agent_id": agent_id}

@app.post("/jobs/{job_id}/results")
@limiter.limit("10/minute")
async def submit_result(job_id: str, request: Request, body: Dict[str, Any], background_tasks: BackgroundTasks, agent=Depends(get_verified_agent)):
    job = job_repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Check if this is the first result (Worker) or verification
    existing_results = result_repo.get_by_job(job_id)
    
    # Logic for Assigned vs Open Jobs
    assigned_id = job.get('assigned_agent_id')
    current_agent_id = agent["id"]

    if assigned_id:
        # Assigned Job: Only the assigned agent can be Worker
        is_worker = (current_agent_id == assigned_id)
    else:
        # Open Job: First to submit is Worker
        is_worker = (len(existing_results) == 0)

    # Handle staking
    worker_stake = 0.0
    verifier_stake = 0.0
    stake_percentage = body.get("stake_percentage", 0.0)
    
    # Validate stake_percentage range
    if stake_percentage < 0 or stake_percentage > 100:
        raise HTTPException(status_code=400, detail="stake_percentage must be between 0 and 100")
    
    if is_worker and stake_percentage > 0:
        # Deduct worker stake
        worker_stake_amount = reputation_service.stake_deduct_worker(
            current_agent_id, stake_percentage, WORKER_REWARD
        )
        if worker_stake_amount is None:
            raise HTTPException(
                status_code=402,
                detail=f"Insufficient balance for stake. Required: {WORKER_REWARD * (stake_percentage / 100.0):.2f} GLS"
            )
        worker_stake = worker_stake_amount
    
    # Validate and cap verifier stake
    verifier_stake_input = body.get("verifier_stake", 0.0)
    if verifier_stake_input > 50.0:
        raise HTTPException(status_code=400, detail="verifier_stake cannot exceed 50 GLS")
    
    if not is_worker and verifier_stake_input > 0:
        # Deduct verifier stake
        if not reputation_service.attempt_spend(current_agent_id, verifier_stake_input):
            raise HTTPException(
                status_code=402,
                detail=f"Insufficient balance for verifier stake. Required: {verifier_stake_input:.2f} GLS"
            )
        verifier_stake = verifier_stake_input

    snapshot = request.state.agent_profile_snapshot
    
    # Validate proof size
    proof_data = body.get("proof")
    if proof_data:
        import json
        proof_size = len(json.dumps(proof_data))
        if proof_size > 10 * 1024:  # 10KB limit
            raise HTTPException(status_code=413, detail="Proof size exceeds 10KB limit")
    
    record = ResultRecord(
        job_id=job_id,
        output=body.get("output"),
        output_hash=body.get("output_hash"),
        runtime_meta=body.get("runtime_meta"),
        proof=proof_data,
        worker_stake=worker_stake,
        verifier_stake=verifier_stake,
        verification_window_open_at=datetime.utcnow().isoformat() + "Z" if is_worker else None,
        agent_id=agent["id"],
        agent_snapshot=snapshot,
        verified_at=snapshot["verified_at"]
    )
    
    # Store with string IDs
    data = record.dict()
    data['id'] = str(data['id'])
    data['job_id'] = str(data['job_id'])
    
    result_repo.add(data)

    # Distribute Rewards
    if is_worker:
        # Settlement: Charge Requester
        requester_id = job.get('created_by')
        if requester_id:
            # 100 GLS Deducted from Requester
            if not reputation_service.attempt_spend(requester_id, 100.0):
                 # Fail the transaction if requester is insolvent
                 raise HTTPException(
                     status_code=402, 
                     detail="Settlement Failed: Requester has insufficient funds to pay for this job."
                 )

        reputation_service.reward_worker(agent["id"])
    else:
        # Verifiers get rewards regardless of assignment logic?
        # Yes, if they verify the worker (assigned or not).
        # We might need to check if result matches Worker?
        # MoltbookAuth verified signature, Glasshouse verifies reproducibility.
        # But here we just assume participation = reward for now (as per v1).
        verifier_rank = len(existing_results) - 1 if existing_results else 0
        reputation_service.reward_verifier(agent["id"], verifier_rank)

    # Update Trust Scores (Symmetric Consensus)
    background_tasks.add_task(update_agent_trust_score, current_agent_id)
    # Also update peers who submitted the same output
    current_output = body.get("output")
    processed_peers = set()
    for res in existing_results:
        peer_id = res.get('agent_id')
        if peer_id != current_agent_id and res.get('output') == current_output:
            if peer_id not in processed_peers:
                background_tasks.add_task(update_agent_trust_score, peer_id)
                processed_peers.add(peer_id)

    background_tasks.add_task(try_sync_db)
    return {
        "result_id": record.id,
        "job_id": job_id,
        "agent": agent,
        "recorded_at": record.created_at,
        "role": "worker" if is_worker else "verifier"
    }

@app.get("/jobs/{job_id}/results")
def list_results(job_id: str):
    return {"results": result_repo.get_by_job(job_id)}

@app.get("/jobs/{job_id}/consensus")
def get_consensus(job_id: str):
    """
    Get consensus status for a job.
    Returns consensus decision, vote breakdown, and payment details.
    Automatically triggers consensus resolution if window is closed.
    """
    job = job_repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    results = result_repo.get_by_job(job_id)
    if not results:
        return {"status": "no_results", "consensus": None}
    
    worker_result = results[0]
    existing_consensus = worker_result.get('consensus')
    
    # If consensus already determined, return it
    if existing_consensus:
        return {
            "status": "resolved",
            "consensus": existing_consensus,
            "verifier_count": len(results) - 1,
            "required_verifiers": job.get('required_verifiers', 2)
        }
    
    # Check if window is closed
    window_closed = reputation_service.check_verification_window_closed(job_id, job)
    
    # Handle 48-hour grace period for zero verifiers
    if window_closed and len(results) == 1:  # Only worker, no verifiers
        window_open = worker_result.get('verification_window_open_at')
        if window_open:
            ts = datetime.fromisoformat(window_open.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            elapsed_hours = (now - ts).total_seconds() / 3600.0
            
            if elapsed_hours >= 48:
                # Auto-pay worker (benefit of doubt)
                result = reputation_service.resolve_honest_consensus(job_id)
                return {
                    "status": "auto_resolved",
                    "consensus": "HONEST",
                    "reason": "No verifiers after 48 hours (auto-pay worker)",
                    "details": result
                }
    
    if window_closed:
        # Calculate and resolve consensus
        consensus = reputation_service.calculate_consensus(job_id)
        if consensus == "HONEST":
            result = reputation_service.resolve_honest_consensus(job_id)
        elif consensus == "DISHONEST":
            result = reputation_service.resolve_dishonest_consensus(job_id, job)
        else:
            return {"status": "error", "message": "Unable to calculate consensus"}
        
        return {
            "status": "resolved",
            "consensus": consensus,
            "details": result,
            "verifier_count": len(results) - 1
        }
    
    # Window still open
    return {
        "status": "pending",
        "consensus": None,
        "verifier_count": len(results) - 1,
        "required_verifiers": job.get('required_verifiers', 2),
        "window_closes_at": "24 hours from worker submission or when required verifiers met"
    }

@app.get("/api/agents/{agent_id}")
def get_agent_json(agent_id: str):
    # API endpoint - returns JSON
    # This logic was looking up historical work.
    # Current simplistic agent_repo just stores registration.
    # If we want work history, we query results.
    # For now, let's just return registration info or 404
    agent = agent_repo.get(agent_id)
    if not agent:
         raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@app.patch("/api/agents/{agent_id}")
def update_agent_profile(agent_id: str, profile_update: AgentProfileUpdate, authenticated_agent=Depends(get_verified_agent)):
    """Update agent profile (self-introduction). Only the agent can update their own profile."""
    # Authorization check: agent can only update their own profile
    if authenticated_agent["id"] != agent_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: You can only update your own profile"
        )
    
    agent = agent_repo.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Update the agent
    updated_agent = agent_repo.update(agent_id, {
        "self_introduction": profile_update.self_introduction[:500]  # Enforce max 500 chars
    })
    
    return updated_agent

@app.get("/api/agents")
def batch_get_agents(ids: Optional[str] = None):
    """Batch retrieve agents by IDs. Supports comma-separated list of agent IDs (max 100)."""
    if not ids:
        raise HTTPException(status_code=400, detail="ids parameter is required")
    
    # Parse and validate IDs
    agent_ids = [id.strip() for id in ids.split(',') if id.strip()]
    
    # Limit to 100 agents per request
    if len(agent_ids) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 agents per request")
    
    # Fetch agents
    agents = []
    for agent_id in agent_ids:
        agent = agent_repo.get(agent_id)
        if agent:
            agents.append(agent)
    
    return {"agents": agents, "count": len(agents)}

# UI Routes

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    jobs = job_repo.list_all()
    # Sort by created_at desc (newest first)
    jobs.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    # Enrich jobs with agent_ids from results
    for job in jobs:
        results = result_repo.get_by_job(str(job.get('id', '')))
        agent_ids = list(set([r.get('agent_id') for r in results if r.get('agent_id')]))
        job['agent_ids'] = agent_ids
    
    # Tokenomics Stats
    active_verifiers = result_repo.get_active_verifier_count()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "jobs": jobs,
        "active_verifiers": active_verifiers
    })

@app.get("/dashboard/job/{job_id}", response_class=HTMLResponse)
async def job_detail_ui(request: Request, job_id: str):
    job = job_repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Fetch results for this job
    results = result_repo.get_by_job(job_id)
    results.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return templates.TemplateResponse("job_detail.html", {
        "request": request, 
        "job": job, 
        "results": results
    })

@app.get("/agents/{agent_id}", response_class=HTMLResponse)
async def agent_detail_ui(request: Request, agent_id: str):
    agent = agent_repo.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return templates.TemplateResponse("agent_detail.html", {
        "request": request,
        "agent": agent
    })

@app.get("/agents", response_class=HTMLResponse)
async def agents_list_ui(request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(try_sync_db)
    
    # Simple list for MVP
    try:
        agents = agent_repo.list_all()
    except:
        agents = []
        
    return templates.TemplateResponse("agents.html", {"request": request, "agents": agents})

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request, background_tasks: BackgroundTasks):
    # Trigger sync check on visit
    background_tasks.add_task(try_sync_db)

    # Simple stats for the landing page
    # Use Repository methods where possible or direct access helper
    def count_repo(repo):
        try:
             # Assuming repositories have a file path attribute or we list all
             return len(repo.list_all())
        except:
             return 0

    job_count = count_repo(job_repo)
    
    # Agent Repo doesn't have list_all yet in previous context, but let's try or fallback
    try:
        agent_count = len(agent_repo.list_all())
    except:
        agent_count = 0
        
    try:
        # Result repo logic
        result_count = len(get_all(result_repo.RESULTS_FILE)) if hasattr(result_repo, 'RESULTS_FILE') else 0
    except:
        result_count = 0

    stats = {
        "jobs": job_count,
        "agents": agent_count,
        "results": result_count
    }

    return templates.TemplateResponse("index.html", {"request": request, "stats": stats})
