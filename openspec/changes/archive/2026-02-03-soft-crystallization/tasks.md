## 1. Reputation Service Updates

- [x] 1.1 Implement `crystallize_balance` in `ReputationService`. <!-- id: 1 -->
- [x] 1.2 Update `attempt_spend` logic (if needed clarity, but likely reusable). <!-- id: 2 -->

## 2. API Endpoint Updates

- [x] 2.1 Update `submit_job` to use `crystallize_balance` + check instead of `attempt_spend`. <!-- id: 3 -->
- [x] 2.2 Update `submit_result` to call `attempt_spend` against Requester (Settlement). <!-- id: 4 -->
- [ ] 2.3 Verify error handling for 402 cases. <!-- id: 5 -->
