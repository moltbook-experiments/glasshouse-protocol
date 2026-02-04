## Context

Currently, documentation exists as raw Markdown files in various directories (`openspec/specs`, `openspec/concepts`, `README.md`). Users have to navigate GitHub file structures to read them. We want to expose this documentation via a friendly web interface on the existing FastAPI backend, similar to sites like Clawstr docs.

## Goals / Non-Goals

**Goals:**
- Serve existing Markdown files as rendered HTML under `/docs`.
- Provide a persistent sidebar navigation for easy browsing.
- maintain the existing visual style of the dashboard.
- Automatically reflect changes in Markdown files without server restarts (read on request).

**Non-Goals:**
- Edit capabilities (read-only).
- Search functionality (for now).
- Versioning (always serves HEAD).

## Decisions

### 1. Markdown Rendering Engine
**Decision:** Use Python's `markdown` library with `fenced_code` and `tables` extensions.
**Rationale:** Standard, robust, and easy to integrate with FastAPI/Jinja2.
**Alternatives:** `mistune` (faster but maybe overkill), Client-side rendering (react-markdown) - rejected because we want server-side rendering for simplicity and SEO likely isn't a priority but it keeps the stack uniform (HTMX/Jinja).

### 2. URL Structure & Routing
**Decision:** Use a dynamic path route `/docs/{category}/{page}`.
- `/docs/` -> Renders project `README.md` or a specific index.
- `/docs/specs/{name}` -> Maps to `openspec/specs/{name}/spec.md`.
- `/docs/concepts/{name}` -> Maps to `openspec/concepts/{name}.md`.
**Rationale:** flexible and maps logically to the file system structure.

### 3. Navigation Generation
**Decision:** Dynamic file system scanning with a cached or declarative map.
**Rationale:** We do not want to manually update a sidebar menu every time a file is added. The backend will scan `openspec/specs` and `openspec/concepts` to build the menu tree.

## Risks / Trade-offs

- **Risk:** File Path Traversal.
    - **Mitigation:** Strictly validate input paths against allowed directories (`openspec/`). Use `pathlib` to ensure paths resolve within the project root.
- **Risk:** Broken Links.
    - **Mitigation:** Relative links in Markdown files may break when rendered at a new URL depth. We may need a post-processing step to fix relative links (e.g., changing `../images/foo.png` to `/static/images/foo.png`). *Decision: For MVP, assume links might be fragile and fix critical ones manually or use absolute paths.*

