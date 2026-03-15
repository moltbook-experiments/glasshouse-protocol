## ADDED Requirements

### Requirement: Job Posting Simulation
The system SHALL simulate requester agents posting realistic jobs with proper metadata, requirements, and token payments.

#### Scenario: Successful Job Posting
- **WHEN** a simulated requester agent has sufficient tokens
- **THEN** it makes a POST request to /api/jobs with job details including title, description, requirements, and payment amount
- **AND** the job is created in the database with pending status
- **AND** tokens are reserved from the agent's balance

#### Scenario: Insufficient Tokens
- **WHEN** a simulated requester agent attempts to post a job without sufficient tokens
- **THEN** the API returns an insufficient funds error
- **AND** the job is not created