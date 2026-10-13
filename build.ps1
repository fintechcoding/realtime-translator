<#
    RealTime Translator - Windows build script
    1) Builds the app into a single folder with PyInstaller (dist\RealTimeTranslator\)
    2) If Inno Setup (ISCC.exe) is found, compiles the setup installer

    Usage:
        powershell -ExecutionPolicy Bypass -File build.ps1
        powershell -ExecutionPolicy Bypass -File build.ps1 -SkipInstaller
#>
param(
    [switch]$SkipInstaller
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host "==> RealTime Translator build" -ForegroundColor Cyan

# --- 0. Ensure PyInstaller is available ---
python -c "import PyInstaller" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller not found, installing..." -ForegroundColor Yellow
    python -m pip install pyinstaller
}

# --- 1. (Re)generate the app icon ---
Write-Host "==> Generating app icon..." -ForegroundColor Cyan
python tools\make_icon.py

# --- 2. Clean previous build ---
foreach ($d in @("build", "dist", "installer_output")) {
    if (Test-Path $d) { Remove-Item $d -Recurse -Force }
}

# --- 3. PyInstaller bundle ---
Write-Host "==> Running PyInstaller..." -ForegroundColor Cyan
python -m PyInstaller RealTimeTranslator.spec --noconfirm --clean
if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed." }

$ExePath = Join-Path $Root "dist\RealTimeTranslator\RealTimeTranslator.exe"
if (-not (Test-Path $ExePath)) { throw "Expected exe not found: $ExePath" }
Write-Host "    Bundle ready: dist\RealTimeTranslator\" -ForegroundColor Green

if ($SkipInstaller) {
    Write-Host "==> Done (installer skipped)." -ForegroundColor Green
    exit 0
}

# --- 4. Inno Setup installer ---
$IsccCandidates = @(
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe",
    "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe",
    "C:\Program Files (x86)\Inno Setup 5\ISCC.exe"
)
$Iscc = $IsccCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $Iscc) {
    $cmd = Get-Command ISCC.exe -ErrorAction SilentlyContinue
    if ($cmd) { $Iscc = $cmd.Source }
}

if (-not $Iscc) {
    Write-Host "==> Inno Setup (ISCC.exe) not found." -ForegroundColor Yellow
    Write-Host "    The portable app is ready in dist\RealTimeTranslator\." -ForegroundColor Yellow
    Write-Host "    To build the setup installer, install Inno Setup 6:" -ForegroundColor Yellow
    Write-Host "      https://jrsoftware.org/isdl.php" -ForegroundColor Yellow
    Write-Host "    then re-run this script (or: ISCC.exe installer.iss)." -ForegroundColor Yellow
    exit 0
}

Write-Host "==> Compiling installer with Inno Setup..." -ForegroundColor Cyan
& $Iscc "installer.iss"
if ($LASTEXITCODE -ne 0) { throw "Inno Setup compilation failed." }

Write-Host "==> Done." -ForegroundColor Green
Write-Host "    Installer: installer_output\" -ForegroundColor Green
Get-ChildItem installer_output -Filter *.exe | ForEach-Object { Write-Host "      $($_.Name)" -ForegroundColor Green }
