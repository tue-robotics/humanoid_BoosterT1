---
doc:
  quadrant: explanation
  adr_status: accepted
  adr_date: 2026-09-18
---
# 0001 Docs as code 

## Context

The team needs documentation that is reviewable, versioned and publicly readable.

## Decision

Write documentation in Markdown, keep it in Git on GitHub, and publish it with MkDocs Material to GitHub Pages. Authors may use Obsidian for editing.

## Consequences

- Changes are reviewed like code.
- Material is in maintenance mode until 2027-05-05, so the plugin stack stays minimal and replaceable.
- Wikilinks are resolved at build time.

# 0002 Devide the on-robot code with football team
13/10/2026

Status: agreed within the team, still need to discuss with football team.
## Context
We need to deploy code onto the robot's onboard PC, but we share the Booster with the football team. We need dedicated storage space on the robot so our code does not get mixed up with theirs.

## Decision
- We agreed to create a folder named @home in the root directory and put all our code (or repository) inside it.
- We will keep everything in a single repo for now, but split it into separate repositories in the future.

# 0003 Robot choice
Status: accepted

## Context
- the team chose TU-BT1-01 as the main research robot