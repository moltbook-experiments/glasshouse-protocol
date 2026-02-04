## 1. Setup & Infrastructure

- [x] 1.1 Add `jinja2` to `backend/requirements.txt`
- [x] 1.2 Create directory structure `backend/templates` and `backend/static`

## 2. Frontend Assets

- [x] 2.1 Create `backend/static/style.css` implementing the "Molty" terminal aesthetic

## 3. Backend Routes

- [x] 3.1 Update `backend/app/main.py` to mount `/static` and configure `Jinja2Templates`
- [x] 3.2 Implement `GET /dashboard` (or `/jobs` HTML) route in `main.py`
- [x] 3.3 Implement `GET /jobs/{job_id}` user-facing route in `main.py`

## 4. Templates Implementation

- [x] 4.1 Implement `backend/templates/base.html` (layout, header, footer)
- [x] 4.2 Implement `backend/templates/dashboard.html` (Jobs List table)
- [x] 4.3 Implement `backend/templates/job_detail.html` (Manifest + Result Timeline + Agent Snapshot)

## 5. Verification

- [x] 5.1 Verify dashboard loads and correctly renders data from `backend/data/*.jsonl`
- [x] 5.2 Verify navigation between dashboard and job detail pages works
