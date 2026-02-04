# Plan: Landing Page & Deployment Implementation

## 1. Landing Page Implementation
*   Create `backend/templates/index.html`.
*   Update `backend/app/main.py` with `/` route and stats logic.
*   Verify ASCII art and styles.

## 2. Static Site Generator (CANCELLED)
*   (Removed) Create `generate_site.py`.
*   (Removed) Implement crawling logic.
*   We are deploying to Vercel instead of GitHub Pages for dynamic functionality.

## 3. Vercel Configuration
*   Create `vercel.json`.
*   Create `api/index.py` entrypoint.
*   Update `backend/app/db.py` to handle `VERCEL` env var (use `/tmp` for writing).

## 4. Verification
*   Verify local server (`uvicorn`).
*   Verify static generation (`python generate_site.py`).