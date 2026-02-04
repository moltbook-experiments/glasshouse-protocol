## 1. Dependencies and Setup

- [ ] 1.1 Add `markdown` library to `backend/requirements.txt`.
- [ ] 1.2 Create `backend/app/docs.py` module for documentation utilities (rendering, scanning).

## 2. Backend Implementation

- [ ] 2.1 Implement `MarkdownRenderer` class in `backend/app/docs.py` using `python-markdown`.
- [ ] 2.2 Implement `DocScanner` class in `backend/app/docs.py` to build navigation tree from `openspec/`.
- [ ] 2.3 Add `/docs` routes to `backend/app/main.py`:
    - `GET /docs` (landing)
    - `GET /docs/{category}/{page}` (content pages)

## 3. Frontend Implementation

- [ ] 3.1 Create `backend/templates/docs_base.html` Jinja2 template (inheriting from `base.html` or standalone with dashboard styles).
- [ ] 3.2 Create `backend/templates/docs_page.html` for rendering content + sidebar.
- [ ] 3.3 Add documentation specific styles to `backend/static/style.css` (e.g., markdown headers, code blocks, sidebar).

## 4. Content and Verification

- [ ] 4.1 Ensure a generic landing page content exists (e.g. read from `README.md` or a dedicated `openspec/index.md`).
- [ ] 4.2 Verify `/docs` renders main page.
- [ ] 4.3 Verify `/docs/specs/public-docs-site` renders the new spec correctly.
- [ ] 4.4 Verify navigation sidebar links work correctly.
