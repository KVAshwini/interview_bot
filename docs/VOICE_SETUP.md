# Voice Setup

Voice support is optional. The typed CLI and web UI work without these packages.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-voice.txt
```

## Verify

```bash
python3 scripts/check_voice_setup.py
python3 scripts/list_audio_devices.py
```

If audio devices are visible, test push-to-talk:

```bash
python3 scripts/voice_answer.py --seconds 8 --model tiny.en
```

To transcribe an existing file:

```bash
python3 scripts/transcribe_audio.py /path/to/question.wav --model tiny.en
```

## Current Local Verification

- Voice dependencies installed successfully in `.venv`.
- `faster-whisper`, `sounddevice`, and `soundfile` import successfully.
- Faster-Whisper `tiny.en` model initialized successfully using a generated silence WAV.
- This Codex process currently cannot see a microphone input device.

If the microphone is not visible on macOS, grant microphone access to the terminal app running Python, then rerun:

```bash
python3 scripts/list_audio_devices.py
```
