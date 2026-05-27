# Local Interview Help Bot

Fast local interview-answer library for technical, scenario, and behavioral questions.

## Current version

- SQLite-backed local Q&A library
- Scenario and technical seed packs
- Fast lexical matching with no network calls
- Instant and detailed answer modes
- Natural read-aloud answer adaptation using `memory/speech_style`
- Browser UI with Quick, Natural, Stored, and Keywords sections
- Session logging for review
- API request validation with clean error responses
- Optional Faster-Whisper speech-to-text hooks
- Unit tests for matching, speech style, and web validation

## Run

```bash
cd interview_bot
python3 scripts/build_database.py
python3 -m app.main "How do you handle a P1 production outage?"
python3 -m app.main --mode detailed "AKS pod keeps restarting"
python3 -m app.main --voice raw "How do you handle Kafka lag?"
```

## Web UI

```bash
python3 -m app.web --port 8765
```

Open `http://127.0.0.1:8765`.

The UI shows:

- Quick version
- Natural read-aloud version
- Stored answer
- Keywords to mention

## Speech Style Layer

The shared planning chat added an important requirement: answers should sound like Ashwini can naturally read them in an interview, not like generic corporate AI text.

Speech style files live under:

```text
memory/speech_style/
├── interview_tone_profiles.json
├── filler_words.json
├── speaking_patterns.json
├── confidence_patterns.json
├── slang_patterns.json
└── technical_explanation_style.json
```

The current style target is casual professional, practical, calm, and production-support focused. Stored answers remain clean, while the app generates a natural read-aloud version on top.

Example:

```text
Usually what I do is first validate the impact and check the logs and alerts properly.
Then mostly I check recent deployments or config changes, because many production issues start from there.
```

## Add a cached answer

```bash
python3 scripts/add_question.py \
  --pack scenarios/custom.json \
  --id scenario_custom_001 \
  --category scenario \
  --topic "Production Support" \
  --question "How do you handle multiple incidents at once?" \
  --answer "I prioritize by business impact and severity, stabilize the highest-impact issue first, delegate parallel checks, and keep communication structured." \
  --keywords "incident,priority,SLA,stakeholders"

python3 scripts/build_database.py
```

## Add personal memory

Add resume and project notes as Markdown, text, or JSON:

```bash
python3 scripts/import_memory.py /path/to/resume_summary.md
```

## Latency check

```bash
python3 scripts/benchmark.py
```

## Tests

```bash
python3 -m unittest discover -s tests
python3 -m compileall app scripts tests
```

## Optional speech-to-text

The core app does not require speech dependencies. To try local voice input:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-voice.txt
python3 scripts/check_voice_setup.py
python3 scripts/list_audio_devices.py
python3 scripts/transcribe_audio.py /path/to/question.wav
python3 scripts/voice_answer.py --seconds 8
```

Voice flow:

```text
microphone audio
-> local wav file
-> Faster-Whisper transcription
-> local Q&A matching
-> natural read-aloud answer
```

On macOS, if no input device is visible, grant microphone permission to the terminal app you are using and rerun `python3 scripts/list_audio_devices.py`.

## Docs

- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Voice Setup](docs/VOICE_SETUP.md)

## Next upgrades

- Add true embedding search with a local model
- Add streaming speech-to-text in the web UI
- Add a floating desktop overlay
