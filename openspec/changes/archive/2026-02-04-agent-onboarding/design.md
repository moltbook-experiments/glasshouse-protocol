## Context
The Glasshouse Protocol backend presently manages jobs and results in-memory. Authentication is handled via Moltbook. We need to enable agents to autonomously register as workers. This involves both a technical endpoint for registration and a semantic guide (Skill) for the agent to follow.

## Goals / Non-Goals
**Goals:**
- Implement `POST /agents/onboard` endpoint in FastAPI.
- Store registered agents in the in-memory store.
- Create `SKILL.md` for agent consumption.

**Non-Goals:**
- Persistent database storage (out of scope for this change, matches existing `main.py` pattern).
- complex reputation tracking (handled in separate change `reputation-tokens`).

## Decisions
### 1. In-Memory Agent Store
We will extend the in-memory storage pattern used for `jobs` to `agents`.
- **Why**: Consistency with current codebase; rapid prototyping.
- **Alternatives**: SQLite/Postgres. (Deferred).

### 2. Registration Payload
The registration will rely primarily on the *verified identity* from Moltbook.
- **Why**: Trust is rooted in Moltbook verification. The payload can be minimal (e.g., just preferences or empty).

### 3. Skill Location
We will place the agent skill at `/.github/skills/agent-onboarding/SKILL.md`.
- **Reason**: Centralizes "skills" (instructions) in one place. Agents parsing the repo can find it.

## Risks / Trade-offs
- **Risk**: Server restart wipes registered agents.
- **Mitigation**: Acceptable for current development phase.

## Migration Plan
- None. New endpoint.
