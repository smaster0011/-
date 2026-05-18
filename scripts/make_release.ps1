$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    $Python = "python"
}

Set-Location $ProjectRoot

$Version = (& $Python "scripts\get_version.py").Trim()
if (-not $Version) {
    Write-Host "Could not read APP_VERSION."
    exit 1
}

$PackageName = "SubtitleMasker_v${Version}_Windows_Portable"
$ReleaseRoot = Join-Path $ProjectRoot "release"
$PackageDir = Join-Path $ReleaseRoot $PackageName
$ZipPath = Join-Path $ReleaseRoot "$PackageName.zip"
$ExePath = Join-Path $ProjectRoot "dist\SubtitleMasker.exe"

if (-not (Test-Path $ExePath)) {
    Write-Host "Missing dist\SubtitleMasker.exe."
    Write-Host "Run scripts\build_exe.ps1 first, or use GitHub Actions to build the portable package."
    exit 1
}

if (Test-Path $PackageDir) {
    Remove-Item $PackageDir -Recurse -Force
}
New-Item -ItemType Directory -Path $PackageDir | Out-Null

Copy-Item $ExePath -Destination $PackageDir
Copy-Item "README.txt" -Destination $PackageDir
Copy-Item "README.md" -Destination $PackageDir
Copy-Item "CHANGELOG.md" -Destination $PackageDir
Copy-Item "LICENSE.txt" -Destination $PackageDir

$DocsDir = Join-Path $PackageDir "docs"
New-Item -ItemType Directory -Path $DocsDir | Out-Null
Copy-Item "docs\PRIVACY.md" -Destination $DocsDir
Copy-Item "docs\UPDATE_POLICY.md" -Destination $DocsDir

if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}
Compress-Archive -Path $PackageDir -DestinationPath $ZipPath

Write-Host "Release package created:"
Write-Host $PackageDir
Write-Host $ZipPath
