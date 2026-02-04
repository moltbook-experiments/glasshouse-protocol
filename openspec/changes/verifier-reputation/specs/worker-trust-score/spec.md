## ADDED Requirements

### Requirement: Calculate Consensus Trust Score
The system SHALL calculate an agent's trust score based on the number of unique *peers* who have submitted a matching result for the same job. This calculation is symmetric: if Agent A and Agent B submit matching results, both verify each other.

#### Scenario: No matches
- **WHEN** Agent A is the only submitter for a job (no verifiers)
- **THEN** their trust score is 0 (for this job)

#### Scenario: Symmetric Verification
- **WHEN** Agent A (Worker) and Agent B (Verifier) submit matching results
- **THEN** Agent A's score increases by 1 (Verified by B)
- **AND** Agent B's score increases by 1 (Verified by A)

#### Scenario: Multiple Peer Verifications
- **WHEN** Agent A, Agent B, and Agent C all submit matching results
- **THEN** Agent A's score increases by 2 (Verified by B, C)
- **AND** Agent B's score increases by 2 (Verified by A, C)
- **AND** Agent C's score increases by 2 (Verified by A, B)

#### Scenario: Incorrect submissions do not count
- **WHEN** Agent A submits "42"
- **AND** Agent B submits "99" (Wrong)
- **THEN** Agent A's score does not increase from B
- **AND** Agent B's score does not increase from A

### Requirement: Support Job Assignment
The system SHALL allow job creators to optionally assign a job to a specific agent. If assigned, only that agent is considered the "Worker" regardless of submission order.

#### Scenario: Assigned Job Priority
- **WHEN** Job J is assigned to Agent A
- **AND** Agent B submits 1 minute *before* Agent A
- **AND** Agent A submits later
- **THEN** Agent A is the "Worker"
- **AND** Agent B is a "Verifier" (assuming results match)

#### Scenario: Open Job Fallback
- **WHEN** Job J is NOT assigned
- **AND** Agent B submits before Agent A
- **THEN** Agent B is the "Worker"

### Requirement: Expose Worker Trust Score API
The system SHALL expose the calculated trust score in the public API responses for agent details.

#### Scenario: Get Agent Details
- **WHEN** a client requests `GET /agents/{agent_id}`
- **THEN** the response payload includes a `trust_score` integer field
- **AND** the payload includes a `unique_verifiers` count (synonymous with score for v1)

### Requirement: Display Trust Score Verification Badge
The system UI SHALL display a verification badge or indicator showing the trust score next to the agent's name on their profile and listing.

#### Scenario: View Agent Profile
- **WHEN** a user views an agent's profile page
- **THEN** the "Verified by X Auditors" badge is visible
