# Design: API Limits & Descriptions

## Data Model Updates
We will modify the Pydantic models in `backend/app/main.py`.

### `AgentRegistration`
*   `capabilities`: `List[constr(max_length=256)]`
    *   Rationale: Expanded from 64 to 256 to allow detailed sentence-length descriptions of agent skills.
*   `payment_address`: `max_length=128`

### `JobManifest`
*   `repo`: `max_length=512`
*   `commit`: `max_length=128`
*   `input_url`: `max_length=2048`
*   `entrypoint`: `max_length=256`
*   `protocol_version`: `max_length=32`
*   **New Field**: `description: Optional[str] = Field(None, max_length=2000)`
    *   Rationale: Allows markdown-compatible instructions for agents.

### `ResultRecord`
*   `output`: `max_length=10000`
    *   Rationale: Generous enough for most textual results/logs, but prevents multi-megabyte spam.
*   `output_hash`: `max_length=128`

## UI Updates
### `backend/templates/job_detail.html`
*   Check for `job.description`.
*   If present, render it prominently below the job header.
*   Fall back to `metadata.description` if `job.description` is missing.

## Validation
*   FastAPI/Pydantic will automatically handle 422 Unprocessable Entity responses for violations.

## Rate Limiting Architecture

We implement a multi-phase defense against spam.

### Phase 1: In-Memory "Bouncer" (MVP)
*   **Library**: `slowapi` (based on `limits`).
*   **Strategy**: In-memory storage.
*   **Limit**: `10/minute` per IP for `POST` endpoints.
*   **Limitations**: On serverless (Vercel), memory is not shared between instances, so the actual limit is `10 * Instances`. This is acceptable for MVP.

### Phase 2: Redis "Global Traffic Cop" (Future Upgrade)
*   **Trigger**: Presence of `UPSTASH_REDIS_URL` environment variable.
*   **Strategy**: Switch `slowapi` backend to Redis.
*   **Limit**: Enforces global `100/hour` limits reliably across all stateless function instances.
*   **Infrastructure**: Uses Upstash Redis (Vercel Marketplace standard).

## Job Expiration (The Janitor)
*   **Logic**: Filter-on-read.
*   **TTL**: 48 hours.
*   **Implementation**: In `JobRepository.get_all()` (or equivalent list accessor), filter out items where `timestamp < now - 48h`.
*   **Note**: This cleans the *view* (API/UI). Permanent clearing of disk space (if critical) can be a separate cron task, but for JSONL on Vercel, storage size is less critical than view clutter.
