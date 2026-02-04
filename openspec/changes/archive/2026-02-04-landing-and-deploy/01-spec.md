# Spec: Landing Page & Deployment

## Context
The Glasshouse Protocol needs a public-facing landing page that reflects the "Radical Transparency" aesthetic (Molty style). Additionally, the protocol needs to be deployable on readily available platforms like GitHub Pages (static) and Vercel (serverless) to maximize accessibility.

## Requirements
1.  **Landing Page (`/`)**:
    *   render `index.html` with "Molty" ASCII art header.
    *   Display live stats (Job count, Agent count, etc.).
    *   Match the dark mode/monospace aesthetic of the dashboard.

2.  **Static Deployment (GitHub Pages)**:
    *   Script to "freeze" the dynamic content into static HTML.
    *   Output to `docs/` folder.
    *   Support relative links for hosting at `/<repo-name>/`.

3.  **Serverless Deployment (Vercel)**:
    *   Configuration to run FastAPI on Vercel's Python runtime.
    *   Adapter for database paths (read-only filesystem handling).

## Design
*   **Frontend**: Use existing Jinja2 templates + `style.css`.
*   **Static Gen**: Python script using `TestClient` to crawl and save pages.
*   **Vercel**: `api/index.py` entrypoint and `vercel.json` config.