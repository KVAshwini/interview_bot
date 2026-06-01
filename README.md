# Local Interview Help Bot

Fast local interview-answer library for technical, scenario, and behavioral questions.

## Current version

- SQLite-backed local Q&A library
- Scenario and technical seed packs
- Enriched DevOps/SRE/cloud question bank with 1,100 practical production-style answers
- Multi-profession starter library for developer, QA, data, BA, PM, product, security, cloud, and DBA interviews
- Fast lexical matching with no network calls
- Local semantic concept scoring for better wording tolerance
- Instant and detailed answer modes
- Category/focus filters and single-answer interview mode
- Natural read-aloud answer adaptation using `memory/speech_style`
- Browser UI with Quick, Natural, Stored, Keywords, health, voice input, and missed-question review
- Session logging for review
- API request validation with clean error responses
- Optional Faster-Whisper speech-to-text hooks
- Unit tests for matching, speech style, and web validation
- Low-confidence missed-question capture for library improvement
- Private Windows overlay with transparency and screen-capture hiding support

## Run

```bash
cd interview_bot
python3 scripts/build_database.py
python3 -m app.main "How do you handle a P1 production outage?"
python3 -m app.main --mode detailed "AKS pod keeps restarting"
python3 -m app.main --voice raw "How do you handle Kafka lag?"
python3 -m app.main --category kubernetes --interview "pod keeps dying in AKS"
```

The local database currently loads 1,822 Q&A items after running `scripts/build_database.py`.

## Tester Setup

On Windows, a tester can run one command after cloning or pulling the repo:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_tester.ps1
```

This installs app requirements, generates pack metadata, rebuilds the local SQLite database, starts the local web server, and opens the Professions UI.

## Question Library

The largest pack lives at:

```text
qa_library/technical/devops_massive_interview_bank.json
```

It contains 1,100 DevOps, SRE, cloud, Kubernetes, Linux, Docker, Terraform, CI/CD, monitoring, and scenario-based answers. The answers are stored as local JSON and loaded into SQLite so runtime lookup does not read the source Markdown file.

Additional profession-specific starter answers live at:

```text
qa_library/professions/starter_professions.json
```

Expanded QA Engineer answers live at:

```text
qa_library/professions/qa_engineer.json
```

The profession registry is in:

```text
app/professions.py
```

To add another profession later, add a `Profession` entry in `app/professions.py`, add Q&A items under `qa_library/professions/`, then run `python3 scripts/build_database.py`.

## Web UI

```bash
python3 -m app.web --port 8765
```

Open `http://127.0.0.1:8765`.

The default `/` UI remains DevOps-focused for the original realtime interview workflow.

The multi-profession branch UI is available separately at:

```text
http://127.0.0.1:8765/professions
```

Pack metadata and checksums are available at:

```text
http://127.0.0.1:8765/packs
http://127.0.0.1:8765/api/packs
```

The UI shows:

- Quick version
- Natural read-aloud version
- Stored answer
- Keywords to mention
- Focus-area filters
- Profession filters
- Interview mode for the single best answer
- Library health status
- Missed-question review and save flow
- Browser voice input when speech recognition is available

Use the `Transparent` button in the header when you want the browser UI to be semi-transparent.

## Matching and Review Workflow

Answer matching combines lexical similarity with a local semantic concept scorer. It recognizes related terms such as `pod keeps dying`, `CrashLoopBackOff`, `rollback`, `consumer lag`, `state drift`, and `Key Vault` without calling a network service.

Low-confidence answers are written to `outputs/missed_questions/*.jsonl`. In the web UI, use the missed-question panel to add a reviewed answer. Saved reviewed answers go to:

```text
qa_library/custom/reviewed_questions.json
```

They are upserted into the running SQLite database immediately, and will also persist after the next `python3 scripts/build_database.py`.

## Private Windows Overlay

For interviews where you share your screen in Zoom, Webex, or Teams, use the Windows overlay instead of the browser UI:

```bash
python3 -m app.overlay
```

On Windows you can also double-click:

```text
run_overlay.bat
```

The overlay has:

- `Transparency` button to switch between normal and semi-transparent opacity.
- `Hide from screen capture` enabled by default on Windows using `SetWindowDisplayAffinity`.
- Always-on-top behavior so it stays accessible during interviews.

Important: the browser UI cannot hide itself from screen sharing. The screen-capture hiding behavior only applies to the native Windows overlay, and it depends on the meeting app using normal Windows capture APIs. Test it once with your exact Zoom/Webex/Teams sharing mode before relying on it.

See [Private Overlay App](docs/OVERLAY_APP.md) for the test checklist and EXE packaging command.

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

## Health Check

```bash
curl http://127.0.0.1:8765/api/health
```

The health response includes database path, loaded item count, categories, and topics.

## Review missed questions

Low-confidence questions are saved automatically when answers are logged.

```bash
python3 scripts/review_missed.py
```

Use these records to add new cached answers with `scripts/add_question.py`.

## Tests

```bash
python3 -m pytest
python3 -m compileall app scripts tests
python3 -m json.tool qa_library/technical/devops_massive_interview_bank.json
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
- Improve the browser voice flow with streaming transcription
- Package the Windows overlay as a one-click launcher or executable
