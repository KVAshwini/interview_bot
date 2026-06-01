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

Status: done for local MVP.

## Phase 2: Better Matching

- Add local embeddings.
- Store embeddings in `data/embeddings`.
- Add match explanations.
- Expand match explanations.
- Add a guided missed-question promotion workflow.

Status: local concept scoring, profession-specific search evaluation tests, pack manifests, and pack manager UI are in place. Local embeddings remain the main open item.

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

Status: Windows native overlay exists with transparency, screen-capture hiding, always-on-top behavior, and pack selection. Streaming transcription and low-latency auto-updates remain open.

## Phase 5: Career Memory

- Add incident stories.
- Add achievements.
- Add STAR stories.
- Add interview feedback loop.
