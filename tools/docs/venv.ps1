# Shared by preview.ps1 and smoke_test.ps1. Dot-source it, then call Initialize-DocsVenv.
# The venv is permanent (outside the repo, outside OneDrive, not in %TEMP%) and self-healing:
# if it is missing or `mkdocs --version` fails, it is deleted and rebuilt. Uses uv when installed
# (fast), otherwise plain `python -m venv` + pip.
$script:DocsVenv = Join-Path $env:LOCALAPPDATA "l1-docs-venv"

function Initialize-DocsVenv([string]$Repo) {
    $py  = Join-Path $script:DocsVenv "Scripts\python.exe"
    $req = Join-Path $Repo "tools/docs/requirements.txt"
    $uv  = Get-Command uv -ErrorAction SilentlyContinue

    $healthy = $false
    if (Test-Path $py) {
        $prev = $ErrorActionPreference
        $ErrorActionPreference = "Continue"   # a broken venv writes to stderr; don't let "Stop" abort the check
        & $py -m mkdocs --version *> $null
        $healthy = ($LASTEXITCODE -eq 0)
        $ErrorActionPreference = $prev
    }
    if (-not $healthy) {
        if (Test-Path $script:DocsVenv) {
            Write-Host "Docs venv is missing or broken; rebuilding $script:DocsVenv"
            Remove-Item -Recurse -Force $script:DocsVenv
        }
        if ($uv) { & uv venv --quiet $script:DocsVenv } else { python -m venv $script:DocsVenv }
        if ($LASTEXITCODE) { throw "venv creation failed" }
    }

    if ($uv) { & uv pip install --quiet --python $py -r $req } else { & $py -m pip install --quiet -r $req }
    if ($LASTEXITCODE) { throw "installing docs requirements failed" }
    return $py
}
