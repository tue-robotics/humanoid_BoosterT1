# Local preview while editing in Obsidian: http://127.0.0.1:8000/humanoid_BoosterT1/
# Safe to run any number of times: if a preview is already running, it just opens the browser.
# Lenient on purpose: a broken link shows as plain text plus a WARNING line here, instead of stopping
# the server. Run tools/docs/smoke_test.ps1 (strict) before opening a PR.
# Easiest start: double-click tools\docs\preview.cmd. Stop: close the window (or Ctrl+C).
$url  = "http://127.0.0.1:8000/humanoid_BoosterT1/"
$repo = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$venv = Join-Path $env:TEMP "l1-docs-venv"

try {
    Invoke-WebRequest $url -UseBasicParsing -TimeoutSec 3 | Out-Null
    Write-Host "Preview is already running. Opening $url"
    Start-Process $url
    return
} catch { }

if (-not (Test-Path $venv)) { python -m venv $venv }
& (Join-Path $venv "Scripts\python.exe") -m pip install --quiet -r (Join-Path $repo "tools/docs/requirements.txt")
$env:DOCS_STRICT = "false"
$env:DOCS_GIT_DATES = "true"        # show page dates; lenient preview only warns on untracked pages
$env:DOCS_PRIVACY = "false"       # privacy plugin needs symlinks on Windows; CI (Linux) keeps it on
Write-Host "Starting preview at $url  (keep this window open; close it to stop)"
Push-Location $repo
try { & (Join-Path $venv "Scripts\python.exe") -m mkdocs serve -a 127.0.0.1:8000 --open } finally { Pop-Location }
