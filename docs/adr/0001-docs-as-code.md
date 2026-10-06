---
doc:
  quadrant: explanation
  adr_status: accepted
  adr_date: 2026-09-18
---
# 0001 Docs as code (Example page)

Status: accepted (2026-09-18)

## Context

The team needs documentation that is reviewable, versioned and publicly readable.

## Decision

Write documentation in Markdown, keep it in Git on GitHub, and publish it with MkDocs Material to GitHub Pages. Authors may use Obsidian for editing.

## Consequences

- Changes are reviewed like code.
- Material is in maintenance mode until 2027-05-05, so the plugin stack stays minimal and replaceable.
- Wikilinks are resolved at build time; a leftover literal `[[` is a build defect (see `tools/docs/check_wikilink_leak.py`).
