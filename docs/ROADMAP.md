# Roadmap

## Phase 1: Local MVP

- SQLite answer cache.
- Scenario and technical packs.
- Local web UI.
- Session logging.
- Speech personality layer.
- Resume/project memory notes.
- API validation.
- Unit tests.
- Static web assets split out of Python.
- Low-confidence missed-question capture.
- Pack manifest and Pack Manager UI.
- Tester setup script.
- Pack quality audit and normalization scripts.

Status: done for local MVP.

## Phase 2: Better Matching

- Add local embeddings.
- Store embeddings in `data/embeddings`.
- Add match explanations.
- Expand match explanations.
- Add a guided missed-question promotion workflow.

Status: local concept scoring, profession-specific search evaluation tests, pack manifests, and Pack Manager UI are in place. Local embeddings remain the main open item.

## Phase 3: Voice Prep Mode

- Add push-to-talk voice input.
- Use Faster-Whisper for local transcription.
- Show partial answers quickly.
- Keep transcript per session.

Status: optional file transcription, push-to-talk scripts, voice dependency checks, and audio-device listing exist; web UI voice capture is not added yet.

## Phase 4: Real-Time Assistant

- Streaming transcription.
- Floating overlay.
- Low-latency answer updates.
- Company-specific prep packs.

Status: Windows native overlay exists with transparency, screen-capture hiding, always-on-top behavior, pack selection, and a verified PyInstaller EXE build. Streaming transcription and low-latency auto-updates remain open.

## Phase 4.5: Desktop Packaging

- Build Windows EXE.
- Bundle local SQLite database and packs.
- Add tester checklist.
- Later: signed installer.
- Later: macOS app package.

Status: Windows EXE builds successfully at `dist\InterviewHelpBotOverlay.exe`. Installer/signing and macOS packaging remain open.

## Phase 5: Career Memory

- Add incident stories.
- Add achievements.
- Add STAR stories.
- Add interview feedback loop.

## Current Open Engineering Items

- Local embeddings for stronger paraphrase matching.
- Streaming system-audio transcription for Zoom/Webex/Teams.
- Low-latency transcript-to-answer updates in the overlay.
- Optional downloadable profession-pack install/update/remove workflow.
- Code signing and installer packaging for Windows.
- macOS desktop packaging and audio-capture strategy.
