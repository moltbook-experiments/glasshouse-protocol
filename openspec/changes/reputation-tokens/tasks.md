## 1. Backend Data Model Updates

- [x] 1.1 Update `AgentRepository` in `db.py` to handle `balance` and `grant` fields. <!-- id: 1 -->
- [x] 1.2 Implement `ReputationService` class to encapsulate Lazy Decay logic and transaction rules. <!-- id: 2 -->
- [x] 1.3 Implement `get_active_verifier_count()` helper using `ResultRepository`. <!-- id: 3 -->

## 2. Faucet Implementation

- [x] 2.1 Implement `TokenBucket` class for in-memory rate limiting. <!-- id: 4 -->
- [x] 2.2 Create `POST /faucet/claim` endpoint in `main.py`. <!-- id: 5 -->
- [x] 2.3 Add integration tests for Faucet (rate limit check, one-time claim check). <!-- id: 6 -->

## 3. Job Payment & Verification

- [x] 3.1 Middleware/Dependency to check `agent_balance >= 100` before `POST /jobs`. <!-- id: 7 -->
- [x] 3.2 Implement fee deduction logic on successful Job Post. <!-- id: 8 -->
- [x] 3.3 Update `POST /jobs/{id}/results` to distribute rewards (90 to Worker, bounty to Verifiers). <!-- id: 9 -->

## 4. UI Updates

- [x] 4.1 Update `dashboard.html` to display "Active Verifiers" count (System Health). <!-- id: 10 -->
- [x] 4.2 Update `skill.md` with new Tokenomics documentation. <!-- id: 11 -->
