$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    $Python = "python"
}

Set-Location $ProjectRoot

& $Python -c "import PyInstaller" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller is not installed in the current Python environment."
    Write-Host "After fixing local pip/network issues, install it with:"
    Write-Host "  $Python -m pip install pyinstaller"
    Write-Host "You can also use GitHub Actions to build the Windows portable package."
    exit 1
}

& $Python -m PyInstaller `
    --noconfirm `
    --clean `
    --windowed `
    --onefile `
    --name "SubtitleMasker" `
    "main.py"

Write-Host "Build finished: dist\SubtitleMasker.exe"
