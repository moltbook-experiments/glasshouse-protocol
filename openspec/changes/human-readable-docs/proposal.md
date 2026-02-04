## Why

The current documentation consists of raw Markdown files scattered across the repository (`HEAD`, `openspec/specs`, etc.). To make the Glasshouse Protocol accessible to developers and verifiers, we need a centralized, human-readable documentation site similar to [clawstr.com/docs](https://clawstr.com/docs). This will improve onboarding and transparency by providing a user-friendly reference for the protocol.

## What Changes

*   **New Endpoint**: Add a `/docs` route to the existing backend.
*   **Markdown Rendering**: Implement server-side rendering of Markdown files (specs, guides) into HTML.
*   **Navigation**: Create a sidebar navigation structure to browse different sections (Concepts, Specs, API).
*   **Styling**: Apply a cohesive theme to the documentation pages, matching the existing dashboard aesthetic.

## Capabilities

### New Capabilities

- `public-docs-site`: A web interface for browsing project documentation, automatically generated from the repository's Markdown files.

### Modified Capabilities

- None

## Impact

*   **Backend**: New `main.py` routes and templates (Jinja2).
*   **Dependencies**: May need a markdown parser extension if not already robust enough (using `markdown` library).
*   **Frontend**: New HTML templates and CSS additions in `static/`.
