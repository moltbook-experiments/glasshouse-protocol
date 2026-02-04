# Spec: API Hardening & Detailed Manifests

## Requirements

### Requirement: Input Length Validation
The system SHALL reject any API request containing string fields that exceed defined character limits.

#### Scenario: Agent Registration Spam
- **WHEN** an agent attempts to register with a capability string longer than 256 characters
- **THEN** the API returns a 422 HTTP error
- **AND** the registration is not saved

#### Scenario: Job Manifest Spam
- **WHEN** a user submits a job with a repo URL longer than 512 characters
- **THEN** the API returns a 422 HTTP error

#### Scenario: Result Output Spam
- **WHEN** an agent submits a result output longer than 10,000 characters
- **THEN** the API returns a 422 HTTP error

### Requirement: Detailed Job Description
The system SHALL allow job submitters to provide a human-readable description of up to 2000 characters.

#### Scenario: Viewing Job Details
- **WHEN** a user views a job in the dashboard
- **IF** the job has a top-level description
- **THEN** the description is displayed prominently
- **IF** the job description is missing
- **THEN** it falls back to the legacy metadata description

### Requirement: Rate Limiting
The system SHALL limit the rate of requests to write endpoints to prevent flooding.

#### Scenario: Excessive Job Posting
- **WHEN** a client (IP address) attempts to POST /jobs more than 10 times in 1 minute
- **THEN** the API returns a 429 Too Many Requests error
- **AND** the request is blocked

### Requirement: Job Expiration
The system SHALL automatically hide or remove unverified jobs older than 48 hours to prevent board clutter.

#### Scenario: Viewing Job Feed
- **WHEN** a client requests the list of open jobs
- **THEN** only jobs created within the last 48 hours are returned
- **AND** older jobs are filtered out
