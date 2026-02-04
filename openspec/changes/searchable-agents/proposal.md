# Proposal: Searchable Agents by Capability

## Problem
Currently, the agents table is a static list. Users cannot easily find agents with specific capabilities (e.g., "text-generation", "image-analysis") without manually scanning the list. As the network grows, this will become unusable.

## Solution
1.  **Frontend**: 
    *   Add a "Search" input field to the Agents dashboard.
    *   Implement client-side filtering (JavaScript) to hide/show table rows based on the search query (matching ID, name, or capabilities).
    *   Allow clicking on capability tags to filter by that capability.

## User Experience
*   User visits `/agents`.
*   User types "text" in the search box.
*   Table filters to show only agents with "text" in their ID or Capabilities.
*   User clicks a capability tag (e.g., "text-generation") on an agent row.
*   Table filters to only show agents with that capability.

## Technical Considerations
*   Purely client-side implementation using vanilla JavaScript for simplicity and speed.
*   No backend changes required as capabilities are already passed to the template.
*   Scale: Fine for current number of agents.
