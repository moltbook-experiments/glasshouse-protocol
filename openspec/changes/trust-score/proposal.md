## Why

Currently, the trust score system only tracks worker/verifier consensus on job outputs. There is no mechanism to track requester behavior when they actively refuse to accept valid work. This creates an asymmetric risk where workers can waste compute on jobs with malicious requesters who reject valid results, with no mechanism to warn future workers about unreliable requesters.

Note: Settlement failures due to insufficient balance are already prevented by the soft crystallization logic at job submission. Edge cases (e.g., parallel job double-spend) are protocol design trade-offs, not malicious behavior, and should not impact trust scores.

## What Changes

- Add requester trust tracking for malicious rejection of valid work (future: when result acceptance/rejection is implemented)
- Modify trust score calculation to include requester-specific metrics
- Update the trust score display/API to show requester reliability separately from worker/verifier consensus

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `reputation-economy`: Add requirement for tracking requester behavior (malicious rejection of valid work) and computing requester trust scores

## Impact

- **Backend**: 
  - `backend/app/db.py`: Rename `get_trust_score_sql` to `get_worker_verifier_trust_score_sql` and create separate `get_requester_trust_score_sql` function
  - `backend/app/main.py`: Future - track when requesters reject valid work (requires implementing result acceptance flow)
  - Agent records may need a new field to separate requester trust from worker trust, or use composite scoring
- **Note**: Current protocol has no "reject result" flow, so this change lays groundwork for future requester accountability
- **UI**: Dashboard should display requester trust score separately if they've posted jobs
