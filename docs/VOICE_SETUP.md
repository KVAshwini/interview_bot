# Voice Setup

Voice support is optional. The typed CLI, web UI, Pack Manager, and Windows overlay work without these packages.

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

- File transcription and push-to-talk scripts exist.
- Voice dependency checks and audio-device listing scripts exist.
- The Windows overlay does not yet include streaming transcription.
- System-audio capture from Zoom/Webex/Teams is still future work.

If the microphone is not visible on macOS, grant microphone access to the terminal app running Python, then rerun:

```bash
python3 scripts/list_audio_devices.py
```

## Future Voice Work

- Windows system-audio capture through WASAPI loopback.
- Streaming transcription instead of fixed-duration recording.
- Automatic question detection from transcript chunks.
- Low-latency lookup against local packs.
- Overlay updates while the meeting continues.
