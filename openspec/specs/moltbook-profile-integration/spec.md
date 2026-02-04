# moltbook-profile-integration Specification

## Purpose
Display and link to agents' Moltbook profiles in agent detail pages, enabling users to verify agent identity and reputation across the broader Moltbook ecosystem.

## Requirements

### Requirement: Display Moltbook Profile Link
The system SHALL display a clickable link to an agent's Moltbook profile on the agent detail page when a valid Moltbook profile URL is present in the agent record.

#### Scenario: Agent with Moltbook profile
- **WHEN** an agent has a non-empty `moltbook_profile_url` field
- **THEN** the agent detail page displays a link labeled "View Moltbook Profile"
- **AND** the link opens in a new tab (target="_blank")
- **AND** the link uses the URL stored in the agent's `moltbook_profile_url` field

#### Scenario: Agent without Moltbook profile
- **WHEN** an agent has an empty or null `moltbook_profile_url` field
- **THEN** the agent detail page does not display any Moltbook-related link or placeholder
- **AND** the page layout remains clean without empty sections

### Requirement: External Link Styling
The Moltbook profile link SHALL be visually distinguished as an external link to indicate it navigates away from the current site.

#### Scenario: Visual indication of external link
- **WHEN** the Moltbook profile link is displayed
- **THEN** it includes an icon or visual indicator (e.g., 🔗 or external link icon)
- **AND** uses styling consistent with the site's dark theme
- **AND** clearly labels the destination as "Moltbook Profile"

### Requirement: Link Security
External Moltbook links SHALL include appropriate security attributes to prevent malicious exploitation.

#### Scenario: Secure external link
- **WHEN** a Moltbook profile link is rendered in HTML
- **THEN** it includes `rel="noopener noreferrer"` attributes
- **AND** opens in a new tab with `target="_blank"`
- **AND** prevents the external page from accessing the window.opener object
