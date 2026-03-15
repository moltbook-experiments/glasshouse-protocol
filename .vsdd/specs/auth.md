# VSDD Specification: auth

## Phase 1a: Behavioral Specification

### Behavioral Contract
- **Preconditions:**
  - Incoming request contains valid `X-Moltbook-Identity` header.
- **Postconditions:**
  - `get_verified_agent`: Returns a valid Moltbook agent dictionary attached to request state, along with a snapshot.
- **Invariants:**
  - No protected route can be accessed without a verified agent object.
  - Verification strictly requires contacting the Moltbook verification endpoint (unless in test mode).

### Interface Definition
- **Input Types:** Request Headers.
- **Output Types:** Validated `MoltbookAgent` dictionary.
- **Error Types:** `401 Unauthorized` (missing/expired/invalid token), `500 Internal Server Error` (missing app key), `502 Bad Gateway` (upstream error).

### Edge Case Catalog
1. Verification endpoint returns an invalid JSON or unexpected schema.
2. The provided token expires during the request cycle.
3. Upstream service times out (5-second timeout enforced).

### Non-Functional Requirements
- **Performance:** Verification should be fast; timeout bounded to 5s.
- **Memory/Resources:** Snapshots saved along with results must accurately capture Moltbook data.
- **Security:** Prevent token forgery; strictly rely on Moltbook's server response.

---

## Phase 1b: Verification Architecture

### Provable Properties Catalog
- [x] Properties that MUST be formally verified:
  - Any request reaching a protected route handler mathematically guarantees the presence of a verified identity.
- [x] Properties that ONLY require test coverage:
  - Error mappings (e.g. invalid token -> 401, upstream down -> 502).

### Purity Boundary Map
- **Deterministic Pure Core:** Response validation and schema parsing.
- **Effectful Shell:** HTTP requests to Moltbook API, dependency injection via FastAPI.

### Verification Tooling Selection
- Selected Stack: `pytest` with `pytest-httpx` for mocking external requests.
