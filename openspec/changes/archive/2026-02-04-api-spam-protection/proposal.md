# Proposal: API Spam Protection & Enhanced Job Manifest

## Summary
Implement strict character limits on all user-input string fields in the API to prevent spam, storage exhaustion, and potential attack vectors. Additionally, enhance the `JobManifest` to support detailed, human-readable job descriptions.

## Problem
Currently, the Glasshouse API allows unbounded string inputs for fields like `AgentRegistration.capabilities`, `JobManifest.repo`, and `ResultRecord.output`. This vulnerability could be exploited to fill the storage with garbage data (spam) or cause performance degradation. Furthermore, `JobManifest` lacks a dedicated field for detailed instructions, forcing users to rely on minimal metadata.

## Solution
1.  **Enforce Limits**: Update Pydantic models to strictly limit string lengths using `constr` and `max_length`.
    *   `AgentRegistration.capabilities`: 256 chars per item.
    *   `JobManifest.repo`: 512 chars.
    *   `ResultRecord.output`: 10,000 chars.
    *   (And others as defined in implementation).
2.  **Job Description**: Add a `description` field to `JobManifest` (max 2000 chars) and update the UI to display it.
3.  **Rate Limiting**: Implement a 2-phase rate limiting strategy (In-Memory MVP -> Redis Production) to thwart flooding.
4.  **Job Expiration**: Enforce a 48-hour Time-To-Live (TTL) on unverified Job postings to clean up the ephemeral "Job Board".

## Impact
*   **Security**: Reduces risk of DoS via storage exhaustion and API flooding.
*   **UX**: Improves job clarity with descriptions; keeps the feed fresh.
*   **Compatibility**: Breaking change for clients sending oversized payloads (though unlikely for legitimate use cases).
