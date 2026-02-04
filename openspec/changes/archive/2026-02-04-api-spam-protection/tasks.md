# Tasks

- [x] Update `AgentRegistration` model with `max_length` constraints <!-- id: 1 -->
- [x] Update `JobManifest` model with `max_length` and new `description` field <!-- id: 2 -->
- [x] Update `ResultRecord` model with `max_length` constraints <!-- id: 3 -->
- [x] Implement `slowapi` rate limiting (10/min) on `POST` endpoints <!-- id: 6 -->
- [x] Implement 48-hour TTL filter in `JobRepository.list_jobs` <!-- id: 7 -->
- [x] Update `backend/templates/job_detail.html` to display `job.description` <!-- id: 4 -->
- [x] Verify validation works by running with `uvicorn` and checking imports <!-- id: 5 -->
