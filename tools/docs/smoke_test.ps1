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
    # git-revision-date-localized warns (fatal in strict mode) for files git does not track yet.
    # Disable it for this run until docs/ is committed.
    $tracked = git ls-files docs
    if ($tracked) { $env:DOCS_GIT_DATES = "true" } else { $env:DOCS_GIT_DATES = "false"; Write-Host "docs/ not tracked yet: git date plugin disabled for this run." }
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
