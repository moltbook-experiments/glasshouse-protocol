## ADDED Requirements

### Requirement: Persistent State Storage
The system SHALL persist all Jobs, Results, and Agents to the local file system in a human-readable, line-delimited JSON format (JSONL) to ensure transparency and auditability via Git.

#### Scenario: Server Restart
- **WHEN** the backend server is restarted
- **THEN** it must reload the previous state from the data files
- **AND** no data should be lost

#### Scenario: Data Write Transparency
- **WHEN** a new job is submitted or an agent registers
- **THEN** the system must append a new line to the corresponding `.jsonl` file
- **AND** the file content must be valid JSON

### Requirement: SQL Query Capability
The system SHALL use an embedded SQL engine (DuckDB) to query the persistent JSONL files, enabling complex data retrieval and aggregation.

#### Scenario: Querying Data
- **WHEN** the system needs to retrieve a job by ID or filter agents
- **THEN** it executes a SQL query against the JSONL files
- **AND** returns the correct result set
