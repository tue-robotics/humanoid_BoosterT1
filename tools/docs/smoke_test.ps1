# Local smoke test for the L1 docs. The venv lives outside the repo.
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$venv = Join-Path $env:TEMP "l1-docs-venv"
Push-Location $repo
try {
    if (-not (Test-Path $venv)) { python -m venv $venv; if ($LASTEXITCODE) { throw "venv creation failed" } }
    $py = Join-Path $venv "Scripts\python.exe"
    & $py -m pip install --quiet -r tools/docs/requirements.txt
    if ($LASTEXITCODE) { throw "pip install failed" }
    # git-revision-date-localized warns (fatal in strict mode) on pages git does not track yet
    # (it timestamps them twice with the clock). Untracked drafts are normal while editing, so skip
    # the date stamps for this run when there are any; CI only sees committed pages.
    $untracked = git ls-files --others --exclude-standard docs -- "*.md"
    if ($untracked) { $env:DOCS_GIT_DATES = "false"; Write-Host "Untracked pages ($($untracked -join ', ')): page dates skipped for this run." } else { $env:DOCS_GIT_DATES = "true" }
    $env:DOCS_PRIVACY = "false"   # privacy plugin needs symlinks on Windows; CI (Linux) keeps it on
    & $py -m mkdocs build --strict
    if ($LASTEXITCODE) { throw "mkdocs build --strict failed" }
    & $py tools/docs/check_wikilink_leak.py
    if ($LASTEXITCODE) { throw "wikilink leak check failed" }
    Write-Host "PASS"
} catch {
    Write-Host "FAIL: $_"
    exit 1
} finally {
    Pop-Location
}
