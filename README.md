# humanoid_BoosterT1


## Repository layout

```
humanoid_BoosterT1/
├── README.md
├── .github/workflows/   CI (docs.yml: strict documentation build on every pull request)
├── mkdocs.yml           documentation site configuration
├── docs/                documentation source (Markdown; also an Obsidian vault)
├── tools/docs/          documentation tooling: build hooks, preview and check scripts
```

## Documentation

The rendered site is built from `docs/` with MkDocs Material.

- **Read:** <https://tue-robotics.github.io/humanoid_BoosterT1/> (published automatically from `master`),
  or open `docs/` as a vault in Obsidian.
- **Preview locally** (Windows PowerShell):
  ```powershell
  powershell -ExecutionPolicy Bypass -File tools\docs\preview.ps1
  ```
  then open <http://127.0.0.1:8000/humanoid_BoosterT1/>. Pages, folders and titles can be renamed or
  added freely: the menu is generated from the folder structure.
- **Check before a pull request:** `tools\docs\smoke_test.ps1` runs the same strict build that CI runs.
