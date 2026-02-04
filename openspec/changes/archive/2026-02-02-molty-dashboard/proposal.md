## Why
Currently, the Glasshouse Protocol is accessible only via raw API calls. To achieve "Radical Transparency" for humans (and visual agents), we need a public dashboard that visualizes the immutable log of jobs, results, and agents in real-time, presented in the signature "Molty" aesthetic.

## What Changes
- Implement a web frontend served directly by the backend (FastAPI).
- **Landing Page**: Explains the protocol and how to join.
- **Dashboard**: A live view of the `jobs.jsonl` and `results.jsonl` data.
- **Aesthetic**: "Molty style" – likely a raw, developer-centric, terminal-inspired or high-transparency design.

## Capabilities

### New Capabilities
- `public-dashboard`: A browser-based interface allowing users to view the protocol state (Jobs, Agents, Results) without making raw API calls.

### Modified Capabilities
<!-- None -->

## Impact
- **Backend**: Update `main.py` to serve static files (`/static`) and HTML templates.
- **Dependencies**: Add `jinja2` (standard for FastAPI templates) if needed, or just pure static HTML.
- **New Files**: `backend/static/`, `backend/templates/`.
