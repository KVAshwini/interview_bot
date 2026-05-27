$ErrorActionPreference = "Stop"

Set-Location (Split-Path -Parent $PSScriptRoot)

python -m pip install -r requirements-app.txt
python -m PyInstaller `
  --noconfirm `
  --onefile `
  --windowed `
  --name InterviewHelpBotOverlay `
  --add-data "qa_library;qa_library" `
  --add-data "memory;memory" `
  --add-data "prompts;prompts" `
  --add-data "models;models" `
  "app\overlay.py"

Write-Host "Built dist\InterviewHelpBotOverlay.exe"
