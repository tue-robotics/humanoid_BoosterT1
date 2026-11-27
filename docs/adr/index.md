---
doc:
  order: 5
  quadrant: explanation
---
# Decision records


# 0001 Docs as code 

### Context

The team needs documentation that is reviewable, versioned and publicly readable.

### Decision

Write documentation in Markdown, keep it in Git on GitHub, and publish it with MkDocs Material to GitHub Pages. Authors may use Obsidian for editing.

### Consequences

- Changes are reviewed like code.
- Material is in maintenance mode until 2027-05-05, so the plugin stack stays minimal and replaceable.
- Wikilinks are resolved at build time.

# 0002 Divide the on-robot code with football team
13/10/2026

Status: accepted; the football team is informed. The deployment protocol is still open.
### Context
We need to deploy code onto the robot's onboard PC, but we share COSMO with the football team. We need dedicated storage space on the robot so our code does not get mixed up with theirs.

### Decision
- All our code lives in the folder `athome` in the home folder of the Orin user. Nothing of ours goes on the x86 board for now.
- `athome` is a plain colcon workspace; repositories are cloned into `athome/src`.
- We will keep everything in a single repo for now, but split it into separate repositories in the future.

# 0003 Robot choice
Status: accepted

### Context
- the team chose TU-BT1-01 as the main research robot