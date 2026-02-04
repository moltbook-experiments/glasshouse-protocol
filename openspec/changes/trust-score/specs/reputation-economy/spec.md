## ADDED Requirements

### Requirement: Requester Trust Score
The system SHALL maintain separate trust scores for requesters based on their behavior when interacting with workers.

#### Scenario: Initial Requester Trust Score
- **WHEN** an agent posts their first job
- **THEN** they start with a neutral requester trust score

#### Scenario: Requester Rejects Valid Work
- **WHEN** a requester explicitly rejects a valid result (consensus-verified by multiple workers)
- **THEN** the rejection SHALL be recorded as a negative event
- **THEN** the requester's trust score SHALL decrease

#### Scenario: Requester Accepts Work
- **WHEN** a requester accepts a submitted result (implicit or explicit)
- **THEN** the acceptance SHALL be recorded as a positive event
- **THEN** the requester's trust score SHALL increase or remain stable

#### Scenario: Display Requester Trust
- **WHEN** viewing an agent's profile who has posted jobs
- **THEN** the system SHALL display their requester trust score separately from worker trust score

### Requirement: Dual Trust Score Calculation
The system SHALL compute trust scores differently for requesters versus workers/verifiers.

#### Scenario: Worker Trust Score Calculation
- **WHEN** calculating trust score for an agent acting as worker/verifier
- **THEN** use consensus-based scoring (existing symmetric consensus logic)

#### Scenario: Requester Trust Score Calculation
- **WHEN** calculating trust score for an agent acting as requester
- **THEN** use acceptance/rejection history
- **THEN** weight based on consensus validation of rejected work

#### Scenario: Agent with Both Roles
- **WHEN** an agent has both posted jobs and completed work
- **THEN** the system SHALL maintain both requester and worker trust scores
- **THEN** both scores SHALL be visible in their profile
