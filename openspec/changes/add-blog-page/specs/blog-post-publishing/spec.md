## ADDED Requirements

### Requirement: Publish new blog posts
The system SHALL allow maintainers to add new blog posts by placing Markdown files in a designated directory.

#### Scenario: Maintainer adds a post
- **WHEN** a maintainer adds a new Markdown file to the blog/ directory
- **THEN** the system displays the new post on the /blog page

### Requirement: Blog post metadata
Each blog post Markdown file SHALL support metadata (title, date, author) via frontmatter or filename convention.

#### Scenario: Metadata is present
- **WHEN** a Markdown file includes metadata in frontmatter or filename
- **THEN** the system displays the title, date, and author on the blog page

### Requirement: Blog post ordering
The system SHALL display blog posts in reverse chronological order by date.

#### Scenario: Multiple posts with dates
- **WHEN** multiple posts exist with valid dates
- **THEN** the system displays the newest post first
