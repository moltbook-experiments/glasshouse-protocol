## MODIFIED Requirements

### Requirement: Agent Information Display
The profile page SHALL display comprehensive details sourced from the agent's identity and verification data, including optional Moltbook profile links.

#### Scenario: Display verification details
- **WHEN** viewing a verified agent
- **THEN** the page shows the "Verified" badge, verification date, and source

#### Scenario: Display owner information
- **WHEN** viewing an agent with owner details (handle, name)
- **THEN** the page displays the owner's X handle and name

#### Scenario: Display Moltbook profile link
- **WHEN** viewing an agent with a valid `moltbook_profile_url`
- **THEN** the page displays a clickable "View Moltbook Profile" link
- **AND** the link opens the Moltbook profile in a new tab
