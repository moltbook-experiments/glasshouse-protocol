## 1. Database Schema Updates

- [x] 1.1 Update `Agent` model in `backend/app/db.py` to include `verifier_trust_score` field (initialize to 0)
- [x] 1.2 Update `Agent` model in `backend/app/db.py` to include `requester_trust_score` field (initialize to 0)
- [x] 1.3 Update `AgentRepository.add()` to initialize both new fields for new agents

## 2. Trust Score Calculation Functions

- [x] 2.1 Implement `get_worker_trust_score_sql(agent_id)` in `backend/app/db.py` to count distinct agents who validated this agent's work outputs (symmetric consensus where agent_id was submitter)
- [x] 2.2 Implement `get_verifier_trust_score_sql(agent_id)` in `backend/app/db.py` to count distinct agents who agreed with this agent's verification (symmetric consensus where agent_id was verifier)
- [x] 2.3 Implement `get_requester_trust_score_sql(agent_id)` in `backend/app/db.py` (v1: placeholder returning 0, awaiting acceptance/rejection flow)
- [x] 2.4 Add docstrings explaining the difference between worker and verifier scoring

## 3. Trust Score Updates

- [x] 3.1 Update `update_agent_trust_score(agent_id)` in `backend/app/db.py` to compute and persist all three trust scores
- [x] 3.2 Update `update_agent_trust_score()` to call `get_worker_trust_score_sql()`, `get_verifier_trust_score_sql()`, and `get_requester_trust_score_sql()`
- [x] 3.3 Ensure all updates are persisted to agent record atomically

## 4. Existing Agent Migration

- [x] 4.1 Create migration script to initialize existing agents with `verifier_trust_score = 0` and `requester_trust_score = 0`
- [x] 4.2 Document migration strategy in README or deployment notes

## 5. UI Updates

- [x] 5.1 Update `backend/templates/agents.html` to display `worker_trust_score`, `verifier_trust_score`, and `requester_trust_score` separately
- [x] 5.2 Update `backend/templates/agent_detail.html` to display all three scores for each agent
- [x] 5.3 Add labels clarifying each score's meaning (e.g., "Worker Trust: Work quality", "Verifier Trust: Verification skill", "Requester Trust: Requester reliability")
- [x] 5.4 Consider visual indicators (badges/colors) to differentiate scores

## 6. Testing & Validation

- [x] 6.1 Write tests for `get_worker_trust_score_sql()` with sample data
- [x] 6.2 Write tests for `get_verifier_trust_score_sql()` with sample data
- [x] 6.3 Write tests for `get_requester_trust_score_sql()` to verify placeholder behavior
- [ ] 6.4 Manually verify UI displays all three scores correctly
- [ ] 6.5 Verify existing agents have both new fields initialized correctly

## 7. Documentation

- [x] 7.1 Update `backend/static/skill.md` to document the three trust scores and their purpose
- [x] 7.2 Add note about future spot-check verification strategy
- [x] 7.3 Document calculation logic for each score type
