## ADDED Requirements

### Requirement: Automated Test Runner
The system SHALL provide an automated mechanism to run a suite of tests that verify the correctness of the backend application.

#### Scenario: Running the full suite
- **WHEN** a developer executes `pytest` in the root directory
- **THEN** all discovered tests in the `tests/` directory are executed
- **AND** a summary of pass/fail results is displayed

### Requirement: Isolated Test Environment
Tests SHALL run in an isolated environment that does not modify the production or development state (data files).

#### Scenario: Data isolation
- **WHEN** a test creates a new Job Record
- **THEN** the record is stored in a temporary directory
- **AND** the main `backend/data/jobs.jsonl` file remains unchanged

### Requirement: Service Unit Verification
The system SHALL have unit tests that verify the logic of core services (Reputation, Repositories).

#### Scenario: Verify Reputation Logic
- **WHEN** the `ReputationService` is tested with a defined balance
- **THEN** logic for spending, earning, and limits is strictly verified against expected values
- **AND** no external API calls are made

### Requirement: API Integration Verification
The system SHALL have integration tests that verify the behavior of public API endpoints (`/jobs`, `/agents`).

#### Scenario: Job Lifecycle API
- **WHEN** a client POSTs to `/jobs` with valid data
- **THEN** it receives a 200 OK
- **AND** a subsequent GET to `/jobs` includes the new job

#### Scenario: Auth Protection
- **WHEN** an unauthenticated client POSTs to `/jobs`
- **THEN** it receives a 401 Unauthorized or 403 Forbidden response
