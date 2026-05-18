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

$srcPath = Join-Path $ProjectRoot "src"
$env:PYTHONPATH = $srcPath

Write-Host "Verifying subtitle_masker imports..."
& $Python -c "import sys; print(sys.path); import subtitle_masker; import subtitle_masker.main; print('subtitle_masker import ok:', subtitle_masker.__file__)"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Import precheck failed. Build stopped."
    exit 1
}

Write-Host "Cleaning old build artifacts..."
Remove-Item -Recurse -Force "build" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "dist" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "release" -ErrorAction SilentlyContinue

& $Python -m PyInstaller --noconfirm --clean "SubtitleMasker.spec"
if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller build failed."
    exit 1
}

Write-Host "Running executable self-test..."
$proc = Start-Process -FilePath "dist\SubtitleMasker.exe" -ArgumentList "--self-test" -PassThru
if (-not $proc.WaitForExit(15000)) {
    $proc.Kill()
    throw "SubtitleMasker.exe self-test timed out"
}
if ($proc.ExitCode -ne 0) {
    throw "SubtitleMasker.exe self-test failed with exit code $($proc.ExitCode)"
}

Write-Host "Build finished: dist\SubtitleMasker.exe"
