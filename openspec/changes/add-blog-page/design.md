## Context

Glasshouse is a protocol for verifiable, trustless compute coordination, aiming to onboard both technical and nontechnical users. Currently, there is no /blog page to communicate updates, onboarding tips, or community stories. The first post will target humans running agents overnight, pitching the value of contributing spare compute cycles to Glasshouse jobs for potential rewards. The system uses a Python backend (see backend/app/main.py) and Jinja2 templates (see backend/app/templates/), with no existing blog infrastructure.

## Goals / Non-Goals

**Goals:**
- Add a /blog page accessible from the main navigation.
- Enable publishing and displaying blog posts (starting with a pitch to agent operators).
- Make the blog easy to update and expand for future onboarding and community content.

**Non-Goals:**
- Full-featured CMS (no WYSIWYG editor, comments, or user accounts for blog management).
- Advanced scheduling or moderation features.

## Decisions

- **Static vs. Dynamic:** Start with static Markdown or HTML files for blog posts, rendered via Jinja2 templates. This keeps implementation simple and maintainable.
- **Routing:** Add a /blog route in backend/app/main.py, rendering a new blog.html template.
- **Navigation:** Update base.html to include a /blog link in the main nav.
- **Styling:** Reuse or minimally extend style.css for blog layout.
- **First Post:** Author the first post as a Markdown file (e.g., blog/first-post.md), rendered on the /blog page.
- **Future Posts:** Store additional posts as Markdown files in a blog/ directory, loaded and rendered as needed.

## Risks / Trade-offs

- [Risk] Static files limit dynamic features (e.g., search, tags) → Mitigation: Accept for MVP; revisit if blog adoption grows.
- [Risk] No admin UI for non-technical contributors → Mitigation: Document process for adding posts via PR or file upload.
- [Risk] Blog content may become stale if not maintained → Mitigation: Encourage regular updates as part of onboarding/community workflow.

## Migration Plan

- Add /blog route and template.
- Create blog/ directory and add first-post.md.
- Update navigation in base.html.
- Deploy and verify /blog page loads and displays the first post.
- Document process for adding future posts.

## Open Questions

- Should posts support images or only text/Markdown?
- Should there be a blog index page or just a single post for now?
- Who is responsible for ongoing blog content updates?
