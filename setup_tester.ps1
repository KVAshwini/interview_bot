param(
    [int]$Port = 8765,
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host "Aura Interview Bot tester setup"
Write-Host "Project: $Root"

if (-not $SkipInstall) {
    Write-Host "Installing app requirements..."
    python -m pip install -r requirements-app.txt
}

Write-Host "Generating pack manifest..."
python scripts\generate_pack_manifest.py

Write-Host "Building local Q&A database..."
python scripts\build_database.py

$existing = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Port $Port is already in use. Reusing the running server."
} else {
    Write-Host "Starting local server on port $Port..."
    Start-Process -FilePath python -ArgumentList "-m","app.web","--port",$Port -WorkingDirectory $Root -WindowStyle Hidden
    Start-Sleep -Seconds 2
}

if (-not (Test-NetConnection -ComputerName 127.0.0.1 -Port $Port -InformationLevel Quiet)) {
    throw "Server did not respond on port $Port."
}

$professionsUrl = "http://127.0.0.1:$Port/professions"
$packsUrl = "http://127.0.0.1:$Port/packs"

Write-Host ""
Write-Host "Ready."
Write-Host "Professions UI: $professionsUrl"
Write-Host "Pack Manager:   $packsUrl"
Start-Process $professionsUrl
