$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    $Python = "python"
}

Set-Location $ProjectRoot

& $Python -m py_compile "main.py"
& $Python -m compileall -q "src" "scripts\get_version.py"

Write-Host "Basic checks passed."
