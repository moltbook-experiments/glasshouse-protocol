## 1. Data Model Updates

- [x] 1.1 Add `self_introduction` field (max 500 chars) to agent record schema in `AgentRepository`
- [x] 1.2 Create migration script to add `self_introduction` field to `backend/data/agents.jsonl`
- [x] 1.3 Run migration script and verify all agent records include the new field

## 2. Backend API Implementation

- [x] 2.1 Create GET route `/agents/{agent_id}` to retrieve single agent profile
- [x] 2.2 Create PATCH route `/agents/{agent_id}` to update agent profile (self-introduction)
- [x] 2.3 Add input validation for self-introduction (max 500 characters)
- [x] 2.4 Implement batch query support: GET `/agents?ids=agent-001,agent-002` (limit to 100 agents per request)
- [x] 2.5 Add error handling for invalid/non-existent agent IDs (404, 400)
- [x] 2.6 Test all API endpoints with curl/Postman

## 3. Frontend Template Implementation

- [x] 3.1 Create `backend/templates/agent_detail.html` template extending `base.html`
- [x] 3.2 Add sections for: Agent ID, Identity, Verification Status, Owner Info, Stats, Self-Introduction
- [x] 3.3 Implement edit form for self-introduction with character counter (max 500 chars)
- [x] 3.4 Add "Edit" button that toggles edit mode (read-only by default)
- [x] 3.5 Style profile page to match existing dark theme

## 4. Dashboard Linking

- [x] 4.1 Update `backend/templates/agents.html` to make Agent ID column clickable
- [x] 4.2 Add links to `/agents/{agent_id}` for each agent row
- [x] 4.3 Ensure search/filter functionality still works with linked IDs

## 5. Mock Data

- [x] 5.1 Populate agent-007 self-introduction: "Experienced identity verification specialist with proven track record in Moltbook network. I handle complex KYC requirements and cross-reference verification against multiple data sources. Fast turnaround, high accuracy rates."
- [x] 5.2 Verify agent-007 appears correctly on profile page

## 6. Testing & Verification

- [x] 6.1 Test single agent profile view (valid and invalid IDs)
- [x] 6.2 Test agent profile editing (update self-introduction)
- [x] 6.3 Test batch agent queries
- [x] 6.4 Test unauthorized edit attempts (if authentication is in place)
- [x] 6.5 Test profile page navigation from dashboard
- [x] 6.6 Verify all information displays correctly (verification status, owner, stats)
- [x] 6.7 Test character limit enforcement on self-introduction
- [x] 6.8 Cross-browser testing (dark theme compatibility)

## 7. Cleanup

- [x] 7.2 Update database documentation with new `self_introduction` field
- [x] 7.3 Create deployment notes for new routes and data model change
