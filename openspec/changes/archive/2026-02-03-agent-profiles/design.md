## Context

Currently, the agents dashboard displays a summary table of all active agents with basic information (ID, Identity, Capabilities, Trust Score, Last Seen). Users cannot drill down to view comprehensive agent details or self-introductions. The backend uses a file-based persistence layer (JSONL) with DuckDB for queries, and serves HTML templates via FastAPI.

The agent profile feature will extend this by:
1. Adding a `self_introduction` field to agent records in the JSONL file
2. Migrating existing agent records to include the new field
3. Creating a new agent detail route that queries the database for a single agent by ID
4. Adding a new HTML template to display the profile with self-introduction
5. Linking the Agent ID column in the dashboard to the profile page

## Goals / Non-Goals

**Goals:**
- Enable users to click on an Agent ID and view a comprehensive profile page
- Display agent details including Moltbook verification, owner information, and stats
- Add a "Self-Introduction" field to the agent data model
- Allow agents to update their profile information including self-introduction
- Support batch queries for multiple agents at once, limited by bandwidth
- Populate self-introduction for agent-007 as a demonstration
- Maintain consistency with existing dark theme styling

**Non-Goals:**
- Create a real-time updates mechanism for profile data
- Build a full agent directory search/filtering experience (covered by searchable-agents)
- Implement profile favorites or bookmarking
- Build an admin interface for managing all agent profiles

## Decisions

### Decision 1: Route Structure and Database Query
**Choice**: Add a new GET route `/agents/{agent_id}` that queries the database for a single agent.

**Rationale**: This follows REST conventions and allows the backend to leverage the existing DuckDB query capability from `backend-persistence`. The route will fetch the agent record from the JSONL file via DuckDB query.

**Alternatives Considered**:
- Store additional profile metadata in a separate document → Too much duplication; agent data already exists in the database
- Client-side filtering from the dashboard data → Not scalable as agent base grows

### Decision 2: Data Model Extension
**Choice**: Add a `self_introduction` optional string field to all agent records in the JSONL file and migrate existing records to include this field (defaulting to null/empty for existing agents).

**Rationale**: Adds self-introduction as first-class data in the persistence layer, version-controlled in Git alongside agent data. Allows agents to update their introductions through future API endpoints. Simplifies profile display logic (no special mock handling needed).

**Alternatives Considered**:
- Store mock self-introduction text in Python dictionary → Mock data not version-controlled; requires special handling in code
- Create a separate mock data file → Adds complexity and data duplication

### Decision 3: Frontend Template
**Choice**: Create a new `agent_detail.html` template that extends `base.html` and displays agent information in a structured layout with sections for Verification, Owner, Stats, and Self-Introduction.

**Rationale**: Follows existing project structure and reuses the established dark theme. Sections provide clear organization of information.

**Alternatives Considered**:
- Single-column card layout → Less room for information; less scannable
- JSON endpoint only → No user-facing interface for non-developers

### Decision 4: Linking from Dashboard
**Choice**: Make the Agent ID column text a clickable link that routes to `/agents/{agent_id}`.

**Rationale**: Intuitive—users naturally expect the ID to be the clickable element. Non-disruptive to existing table structure.

**Alternatives Considered**:
- Add a separate "View Profile" button in the Actions column → Takes up space; duplicates navigation intent

## Risks / Trade-offs

**[Risk] Performance of single-agent queries**: If many users simultaneously request the same agent profile, the DuckDB query could become a bottleneck.
→ **Mitigation**: Support batch queries via the API (e.g., `/agents?ids=agent-001,agent-002,agent-007`) to allow efficient retrieval of multiple agents. Limit request size by bandwidth to prevent abuse.

**[Risk] JSONL file schema change**: Adding a new field to agent records changes the schema.
→ **Mitigation**: Update the agent schema directly. No migration needed since this code is not yet deployed and the JSONL file is not yet in production.

**Requirement: Agent Profile Editing**: Allow agents to update their own profile information including self-introduction.

## Migration Plan

1. Update `AgentRepository` model to include `self_introduction` optional string field
2. Create a new GET route `/agents/{agent_id}` to fetch a single agent's profile
3. Create a new PATCH route `/agents/{agent_id}` to allow agents to update their profile information (with optional authentication)
4. Populate self-introduction for agent-007: "The name's Bond. James Bond. I verify identities and shake martinis."
5. Create `agent_detail.html` template with profile layout and edit form
6. Update `agents.html` to make Agent ID column clickable, linking to `/agents/{agent_id}`
7. Add an optional query parameter to support batch retrieval (e.g., `/agents?ids=agent-001,agent-002`)
8. Test navigation from dashboard to profile page and verify self-introduction displays
9. Test profile editing functionality
10. Deploy alongside existing dashboard without breaking changes

## Open Questions

- Should we display agent activity history or verification timeline on the profile?
- How should we handle deleted or inactive agents (404 vs. archived state)?
- Character limit for self-introductions: **500 characters** (allows detailed pitches with skills, experience, and availability)
