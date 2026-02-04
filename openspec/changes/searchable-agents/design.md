# Design: Interactive Agent Search

## Architecture
The search and filtering mechanism will be implemented entirely on the client-side within the `agents.html` template. This avoids unnecessary server round-trips for the current scale of data.

## Components

### 1. Search Interface
*   **Location**: Header area of the Agents page, above the table.
*   **Elements**: 
    *   Input field for free text search.
    *   Optional: "Active Filter" pills if a specific capability is selected via click.

### 2. Capabilities Display
*   Existing capability text lists will be converted to clickable "badges" or links.
*   Action: Clicking a badge sets the search input to that capability (or a specific filter state) and triggers the filter.

### 3. JavaScript Logic
*   **Event Listener**: Listens to `input` events on the search box.
*   **Filtering**:
    *   Iterates through all table rows (`tbody tr`).
    *   Retrieves text content of `Agent ID`, `Identity`, and `Capabilities` columns.
    *   Matches against the search term (case-insensitive).
    *   Toggles `display: none` on rows that don't match.
*   **UX**: Updates a "Showing X of Y agents" counter (optional but good).

## Data Flow
User Input -> DOM Event -> Filter Function -> Row Visibility Toggled.
