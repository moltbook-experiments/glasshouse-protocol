## 1. Backend Implementation

- [ ] 1.1 Implement `get_trust_score_sql` in `backend/app/db.py` using the symmetric Consensus Query.
- [ ] 1.2 Implement `update_agent_trust_score(agent_id)` in `db.py` which runs the query and updates `agents.jsonl`.
- [ ] 1.3 Call `update_agent_trust_score` in `main.py` whenever a result is submitted/verified.
- [ ] 1.4 Update `JobManifest` model in `main.py` to include optional `assigned_agent_id`.
- [ ] 1.5 Update result submission logic to respect `assigned_agent_id` when determining Worker role.

## 2. Frontend Implementation

- [ ] 2.1 Update `backend/templates/job_detail.html` (or `agents.html` if exists) to display the Trust Score badge.
- [ ] 2.2 Verify the Trust Score updates correctly when verifications occur.
