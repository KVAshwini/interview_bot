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

Status: done for local MVP.

## Phase 2: Better Matching

- Add local embeddings.
- Store embeddings in `data/embeddings`.
- Add match explanations.
- Save missed questions automatically.

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

## Phase 5: Career Memory

- Add incident stories.
- Add achievements.
- Add STAR stories.
- Add interview feedback loop.
