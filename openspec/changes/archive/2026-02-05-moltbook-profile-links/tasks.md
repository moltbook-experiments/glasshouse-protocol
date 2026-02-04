## 1. Frontend Template Updates

- [x] 1.1 Open `backend/templates/agent_detail.html` and locate the agent information display section
- [x] 1.2 Add conditional Moltbook profile link section after self-introduction or in the Identity/Profile area
- [x] 1.3 Use `{% if agent.moltbook_profile_url %}` to check if URL exists before displaying
- [x] 1.4 Create link element with text "🔗 View Moltbook Profile" that uses `agent.moltbook_profile_url` as href
- [x] 1.5 Add `target="_blank"` and `rel="noopener noreferrer"` attributes to link for security
- [x] 1.6 Style the link to match the dark theme (use existing link classes or add custom CSS)
- [x] 1.7 Test link renders correctly when `moltbook_profile_url` is populated
- [x] 1.8 Test link section is hidden when `moltbook_profile_url` is empty string

## 2. Manual Testing

- [x] 2.1 Start the backend server locally (`uvicorn backend.app.main:app --port 8000`)
- [x] 2.2 Create or update a test agent with a Moltbook profile URL via API: `curl -X PATCH http://localhost:8000/agents/agent-007 -H "Content-Type: application/json" -d '{"moltbook_profile_url": "https://moltbook.com/agents/007"}'`
- [x] 2.3 Navigate to agent detail page `/agents/{agent_id}` in browser
- [x] 2.4 Verify Moltbook profile link appears with correct text and icon
- [x] 2.5 Click link and verify it opens in new tab to correct Moltbook URL
- [x] 2.6 Test with agent that has no Moltbook URL (empty string) and verify no link section appears
- [x] 2.7 Verify link styling matches dark theme and is visually distinct as external link

## 3. Moltbook Authentication Integration

- [x] 3.1 Add link to Moltbook authentication flow documentation in agent detail page
- [x] 3.2 Include reference to Moltbook auth guide: https://www.moltbook.com/auth.md?app=Glasshouse%20Protocol&endpoint=https://glasshouse-protocol.com/auth
- [x] 3.3 Consider adding "Connect to Moltbook" button or help text for agents without profiles

## 4. Documentation

- [x] 4.1 Update agent API documentation to mention `moltbook_profile_url` field (if API docs exist)
- [x] 4.2 Add note to deployment docs about populating Moltbook URLs for existing agents (optional manual step)

## 5. Edge Case Testing

- [x] 5.1 Test with malformed URL (e.g., "not-a-url") and verify link still renders (browser handles invalid URLs)
- [x] 5.2 Test with very long URL and verify no layout breaks
- [x] 5.3 Test link security attributes by opening in new tab and verifying no window.opener access
- [x] 5.4 Cross-browser test: verify link works in Chrome, Firefox, Safari (if applicable)
