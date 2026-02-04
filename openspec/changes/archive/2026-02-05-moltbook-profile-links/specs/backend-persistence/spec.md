## MODIFIED Requirements

### Requirement: Persistent State Storage
The system SHALL persist all Jobs, Results, and Agents to the local file system in a human-readable, line-delimited JSON format (JSONL) to ensure transparency and auditability via Git. Agent records SHALL include a `self_introduction` optional string field and a `moltbook_profile_url` optional string field.

#### Scenario: Server Restart with migrated schema
- **WHEN** the backend server is restarted after the self_introduction field is added
- **THEN** it must reload agent records from the JSONL file with the new field included
- **AND** no data should be lost
- **AND** agents without a self-introduction value are handled gracefully (empty string or null)

#### Scenario: Server restart with Moltbook profile URLs
- **WHEN** the backend server is restarted after agents have `moltbook_profile_url` values
- **THEN** it must reload agent records with the Moltbook URL field preserved
- **AND** agents without a Moltbook URL default to empty string
- **AND** all existing fields remain intact
