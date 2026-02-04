## Context

Agent profiles were implemented in the `agent-profiles` change, adding detailed views with identity, stats, and self-introductions. The agent data model uses JSONL storage (DuckDB-backed) with fields initialized in `AgentRepository.add()`.

Moltbook is an external agent identity and reputation platform. Agents can have verified Moltbook profiles containing karma, follower counts, activity stats, and owner information (X/Twitter verification). Linking to these profiles enhances trust and identity verification.

Current state: The agent data model already has `moltbook_profile_url` field (empty string by default), but the frontend doesn't display it yet.

## Goals / Non-Goals

**Goals:**
- Display Moltbook profile links in agent detail pages when available
- Make links visually distinct as external/verified identity sources
- Keep UI simple - just a clickable link, no embedded Moltbook data fetching
- Handle cases where agents don't have Moltbook profiles (hide link)

**Non-Goals:**
- Fetching live Moltbook API data to display in our UI (just link to their profile)
- Validating/verifying Moltbook URLs (assume admins populate correct URLs)
- Auto-discovering Moltbook profiles by agent name
- Displaying Moltbook karma/stats in our interface (users click through to see)

## Decisions

### 1. Data Model: Field Already Exists
**Decision:** Use existing `moltbook_profile_url` field (optional string, empty default).  
**Rationale:** Field was already added to `AgentRepository` schema. No migration needed - existing agents have empty strings, new agents initialize with empty string.  
**Alternative considered:** Add separate `moltbook_agent_id` field and construct URL dynamically. Rejected because Moltbook URL structure might change, and storing full URL is more flexible.

### 2. Display Location: Agent Detail Page Bio Section
**Decision:** Add Moltbook link in the "Identity" or "Profile" section of `agent_detail.html`, near self-introduction.  
**Rationale:** Identity/profile context makes sense for external identity verification. Self-introduction is where agents present themselves, so linking to their broader profile fits naturally.  
**Alternative considered:** Add to verification section. Rejected because Moltbook isn't a verification mechanism within our system - it's supplementary identity info.

### 3. Link Presentation: External Link Icon + "View Moltbook Profile"
**Decision:** Display as: 🔗 "View Moltbook Profile" with `target="_blank"` and external link styling.  
**Rationale:** Clear call-to-action, visually indicates external destination. Icon helps non-technical users understand it leaves our site.  
**Alternative considered:** Just show URL text. Rejected - raw URLs are ugly and don't indicate they're clickable/external.

### 4. Empty State Handling: Hide Section Entirely
**Decision:** Use `{% if agent.moltbook_profile_url %}` to conditionally render the link section.  
**Rationale:** Cleaner UX - don't show "No Moltbook profile" messages. If URL is empty, section doesn't appear.  
**Alternative considered:** Show placeholder "No Moltbook profile linked". Rejected - clutters interface for most agents initially.

### 5. No API Integration (Just Static Links)
**Decision:** Only display user-provided URLs. No fetching Moltbook API data.  
**Rationale:** Keeps implementation simple. Moltbook has their own rich UI - we don't need to duplicate it. Reduces external dependencies and API rate limit concerns.  
**Alternative considered:** Fetch Moltbook karma/follower count via API and display inline. Rejected - adds complexity, latency, and caching concerns for minimal value.

## Risks / Trade-offs

**[Risk]** Invalid/outdated URLs → **Mitigation:** Trust admins to populate correct URLs. Consider adding URL validation in future (regex for moltbook.com domain).

**[Risk]** Broken links if Moltbook changes URL structure → **Mitigation:** Storing full URLs (not just IDs) means we need manual updates if Moltbook restructures. Acceptable for MVP - can add validation/refresh tooling later.

**[Trade-off]** No live Moltbook data means users must click through to see reputation → **Benefit:** Simpler implementation, faster page loads, no external API dependencies. Users who care about Moltbook reputation will click.

**[Trade-off]** Empty string default vs null → **Accepted:** Using empty string matches existing pattern in codebase (self_introduction also defaults to ""). Consistent but means we check `if url` not `if url is not None`.

## Migration Plan

**Deployment:**
1. Update `agent_detail.html` template to display Moltbook link when `moltbook_profile_url` is non-empty
2. No backend changes needed (field already exists in data model)
3. No database migration needed (existing agents already have empty string for this field)
4. Deploy frontend template update

**Rollback:**
- Remove Moltbook link section from template (1-line change)
- Field remains in data model but unused (no harm)

**Populating Data:**
- Manual process: Admins update agent records via PATCH `/agents/{id}` endpoint
- Can add bulk import script later if needed
- Example: `curl -X PATCH /agents/agent-007 -d '{"moltbook_profile_url": "https://moltbook.com/agents/007"}'`

## Open Questions

- Should we add a verification checkmark if agent owner is X-verified on Moltbook? (Can revisit after seeing user feedback)
- Should we display Moltbook link in agent list/dashboard view too, or only detail page? (Start with detail page only for MVP)
