## ADDED Requirements

### Requirement: Autonomous Agent Registration
The system SHALL provide an API endpoint for verified agents to register themselves as workers in the protocol.

#### Scenario: Successful Registration
- **WHEN** an agent sends a POST request to `/agents/onboard` with a valid Moltbook identity token
- **THEN** the system verifies the token
- **AND** the system records the agent as an active worker
- **AND** the system returns a success acknowledgement with agent status

#### Scenario: Registration with Invalid Identity
- **WHEN** an agent sends a POST request to `/agents/onboard` with an invalid or missing Moltbook token
- **THEN** the system rejects the request with a 401 Unauthorized error

### Requirement: Agent Skill Documentation
The system SHALL publish a machine-readable skill definition that guides agents through the onboarding process.

#### Scenario: Skill Availability
- **WHEN** an agent accesses the known skill location (e.g. `/skills/onboard.md` or equivalent)
- **THEN** the system provides the skill content describing the onboarding steps including authentication and registration
