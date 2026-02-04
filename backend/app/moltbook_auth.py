# FastAPI Moltbook Authentication Dependency
# Reads MOLTBOOK_APP_KEY from environment
# Verifies X-Moltbook-Identity header using Moltbook verify endpoint

import os
from datetime import datetime
from typing import Optional, Dict

from fastapi import Header, HTTPException, status, Request
import httpx
from pydantic import BaseModel, Field

MOLTBOOK_VERIFY_URL = "https://moltbook.com/api/v1/agents/verify-identity"
APP_KEY = os.getenv("MOLTBOOK_APP_KEY")

if not APP_KEY:
    import warnings
    warnings.warn("MOLTBOOK_APP_KEY is not set. Moltbook auth will fail until this env var is configured.", RuntimeWarning)

# --- Pydantic Models for Moltbook API Response ---

class MoltbookStats(BaseModel):
    posts: int
    comments: int

class MoltbookOwner(BaseModel):
    x_handle: Optional[str] = None
    x_name: Optional[str] = None
    x_verified: bool = False
    x_follower_count: int = 0

class MoltbookAgent(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    karma: int = 0
    avatar_url: Optional[str] = None
    is_claimed: bool = False
    created_at: str
    follower_count: int = 0
    stats: Optional[MoltbookStats] = None
    owner: Optional[MoltbookOwner] = None

class MoltbookVerifyResponse(BaseModel):
    success: bool = False
    valid: bool = False
    agent: Optional[MoltbookAgent] = None
    error: Optional[str] = None

async def get_verified_agent(request: Request, x_moltbook_identity: str = Header(None)):
    if x_moltbook_identity is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"error": "missing_identity_header", "message": "X-Moltbook-Identity header is required"})

    if not APP_KEY:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"error": "server_misconfiguration", "message": "MOLTBOOK_APP_KEY not set on server"})

    async with httpx.AsyncClient(timeout=5) as client:
        try:
            resp = await client.post(
                MOLTBOOK_VERIFY_URL,
                json={"token": x_moltbook_identity},
                headers={"X-Moltbook-App-Key": APP_KEY, "Content-Type": "application/json"},
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                                detail={"error": "verification_service_unavailable", "message": str(exc)})

    # Parse with Pydantic for validation
    try:
        data = resp.json() if resp.content else {}
        # Relaxed validation: construct model but don't crash if extra fields (default behavior usually ignores extras, or we can use safe parsing)
        verification = MoltbookVerifyResponse(**data)
    except Exception:
        # Fallback if JSON is malformed or schema is wildly different
        # We also treat missing required fields as invalid response
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, 
                            detail={"error": "invalid_upstream_response", "message": "Moltbook returned invalid JSON or schema mismatch"})

    if verification.valid is True and verification.agent:
        # Convert Pydantic model back to dict for consistency with existing app usage
        agent_dict = verification.agent.dict()

        # attach to request.state so route handlers can use it
        request.state.agent = agent_dict
        # build agent_profile_snapshot
        snapshot = {
            "agent": agent_dict,
            "verified_at": datetime.utcnow().isoformat() + "Z",
            "verify_source": "moltbook-v1-verify-identity",
            "verify_schema_version": "1.0",
            "raw_response": data
        }
        request.state.agent_profile_snapshot = snapshot
        return agent_dict

    err = verification.error or "invalid_token"
    if err == "invalid_app_key":
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"error": err, "message": "App key invalid (server misconfiguration)"})
    if err == "identity_token_expired":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"error": err, "message": "Identity token expired"})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail={"error": err, "message": "Invalid identity token"})
