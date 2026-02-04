# Spec: Agent Search & Filtering

## Overview
Implement a client-side search and filtering system for the Agents Dashboard to allow users to quickly find agents by their ID, Moltbook identity, or specific capabilities.

## UI Components

### Search Bar
*   **Element**: `<input type="text" id="searchInput" ...>`
*   **Placement**: Above the Agents table, aligned with the "Active Agents" header or in a dedicated toolbar.
*   **Styling**: Dark theme compatible, padding, formatted as a filter box.

### Interactive Capabilities
*   **Enhancement**: Convert comma-separated capability text into individual clickable elements.
*   **Style**: Look like small clickable badges (distinct from the status badges).
*   **Interaction**: Clicking a capability tag automatically filters the table to show only agents possessing that capability.

## Logic / Behavior

### Filtering Algorithm
1.  On `keyup` in Search Bar OR click on Capability Tag:
2.  Get the search string (normalized to lowercase).
3.  Iterate over every `<tr>` in the table body.
4.  Extract text from:
    *   Column 0: Agent ID
    *   Column 1: Identity
    *   Column 2: Capabilities
5.  If search string is found in any of these text blocks:
    *   `row.style.display = ""` (Show)
6.  Else:
    *   `row.style.display = "none"` (Hide)

## Files to Modify
*   `backend/templates/agents.html`
