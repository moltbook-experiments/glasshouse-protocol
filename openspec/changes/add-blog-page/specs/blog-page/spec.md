## ADDED Requirements

### Requirement: Blog page is accessible
The system SHALL provide a public /blog route accessible from the main navigation.

#### Scenario: User visits /blog
- **WHEN** a user navigates to /blog
- **THEN** the system displays the blog page with the latest posts

### Requirement: Blog posts are rendered from Markdown
The system SHALL render blog posts from Markdown files stored in a designated directory.

#### Scenario: Render first blog post
- **WHEN** the first blog post Markdown file exists in the blog/ directory
- **THEN** the system displays its content on the /blog page

### Requirement: Blog supports future posts
The system SHALL support displaying multiple blog posts, ordered by date or filename.

#### Scenario: Multiple posts present
- **WHEN** multiple Markdown files exist in the blog/ directory
- **THEN** the system displays a list or index of posts, each linking to its full content
