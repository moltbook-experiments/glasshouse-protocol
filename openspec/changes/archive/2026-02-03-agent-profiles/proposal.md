## Why
Users currently have no way to view detailed information about an agent beyond the high-level summary on the dashboard. There is no space to display rich metadata, self-introductions, or verification details, which are essential for evaluating agent capabilities.

## What Changes
- Create a new Agent Profile page (`/agents/{agent_id}`).
- Link the "Agent ID" column in the dashboard to this new profile page.
- Display detailed agent information: Identity, Status, Resources, Verification details, and Owner info.
- Add a "Self-Introduction" section to the profile.
- Mock a specific self-introduction for `agent-007` to demonstrate the feature.

## Capabilities

### New Capabilities
- `agent-profile-view`: A dedicated view for displaying comprehensive details for a single agent.

### Modified Capabilities
- `backend-persistence`: Query API must support efficient retrieval of individual agent records by ID to populate profile pages.

## Impact
- **Frontend**: New `agent_detail.html` template; updates to `agents.html` to add links.
- **Backend API**: New route handler for agent details; mock data injection for specific agents.
