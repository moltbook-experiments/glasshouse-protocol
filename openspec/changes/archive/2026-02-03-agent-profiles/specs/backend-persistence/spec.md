## MODIFIED Requirements

### Requirement: Persistent State Storage
The system SHALL persist all Jobs, Results, and Agents to the local file system in a human-readable, line-delimited JSON format (JSONL) to ensure transparency and auditability via Git. Agent records SHALL include a `self_introduction` optional string field.

#### Scenario: Server Restart with migrated schema
- **WHEN** the backend server is restarted after the self_introduction field is added
- **THEN** it must reload agent records from the JSONL file with the new field included
- **AND** no data should be lost
- **AND** agents without a self-introduction value are handled gracefully (empty string or null)

### Requirement: Data Migration for Schema Changes
The system SHALL support non-breaking migrations to add new optional fields to agent records.

#### Scenario: Migrate existing agents
- **WHEN** a migration script is run on an existing `agents.jsonl` file
- **THEN** all agent records are updated to include the `self_introduction` field
- **AND** existing records without this field default to an empty string
- **AND** the script is idempotent (safe to run multiple times)

### Requirement: SQL Query Capability
The system SHALL use an embedded SQL engine (DuckDB) to query the persistent JSONL files, enabling complex data retrieval and aggregation. Query API SHALL support efficient retrieval of individual agent records by ID.

#### Scenario: Querying Data
- **WHEN** the system needs to retrieve a job by ID or filter agents
- **THEN** it executes a SQL query against the JSONL files
- **AND** returns the correct result set

#### Scenario: Retrieve Agent by ID
- **WHEN** the system needs to fetch a single agent's details for the profile page
- **THEN** it executes a targeted SQL query for the specific agent ID
- **AND** returns the agent record with all fields (identity, verification, owner info, self_introduction, etc.)

### Requirement: Update Agent Records
The system SHALL support updating agent records (e.g., self_introduction field) and persist changes to the JSONL file.

#### Scenario: Update agent self-introduction
- **WHEN** an agent updates their self-introduction via the API
- **THEN** the system updates the agent record in `agents.jsonl`
- **AND** the change is persisted and visible on the next read
