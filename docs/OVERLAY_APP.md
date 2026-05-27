# Private Overlay App

Use the native overlay for interview screen sharing. The browser UI can become visually transparent, but it cannot hide itself from Zoom, Webex, or Teams capture.

## Run Locally

```powershell
cd D:\interview_bot
.\run_overlay.bat
```

or:

```powershell
python -m app.overlay
```

## Privacy Behavior

The overlay enables `Hide from screen capture` by default on Windows. It calls `SetWindowDisplayAffinity` with `WDA_EXCLUDEFROMCAPTURE`, then falls back to `WDA_MONITOR` when needed.

This depends on the meeting app using normal Windows capture APIs. Test your exact workflow before an interview:

- Zoom full-screen share
- Zoom window share
- Webex full-screen share
- Webex window share
- Teams full-screen share
- Teams window share

## Build EXE

Install packaging dependencies and build:

```powershell
cd D:\interview_bot
.\scripts\build_overlay_exe.ps1
```

Output:

```text
dist\InterviewHelpBotOverlay.exe
```

## App Readiness Checklist

- Rebuild DB with `python scripts\build_database.py`.
- Run tests with `python -m pytest`.
- Launch `run_overlay.bat`.
- Confirm the overlay is always on top.
- Toggle `Transparency`.
- Confirm `Hide from screen capture` says hidden.
- Verify meeting participants cannot see it in Zoom/Webex/Teams.
