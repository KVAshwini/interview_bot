# Architecture

The bot is built around fast local retrieval first, with AI generation only as a fallback.

```text
Question or voice transcript
-> normalize text
-> search local Q&A cache
-> search resume/project memory
-> choose confidence tier
-> apply speech personality layer
-> show quick, natural, detailed, and keywords
-> log session for library improvement
```

## Latency Tiers

| Path | Target |
|---|---:|
| Exact cached Q&A | 50-200 ms |
| Similar local match | 200-700 ms |
| Cached answer plus rewrite | 700 ms-2 sec |
| Fresh generated answer | 2-5+ sec |

Current dependency-free lookup benchmark is around 15 ms for the seed library.

## API Layer

The local web server validates API requests before answer generation:

- `question` is required.
- `mode` must be `instant` or `detailed`.
- `voice` must be `natural` or `raw`.
- `limit` must be between 1 and 10.

Invalid requests return JSON errors instead of crashing the request handler.

## Web UI

The UI is served from `static/`:

```text
static/index.html
static/styles.css
static/app.js
```

The Python server stays focused on routing, validation, static file serving, and API responses.

## Personality Layer

Stored answers remain clean and structured. The speech layer adapts them into a natural read-aloud version using files in `memory/speech_style/`.

The target style is casual professional, practical, and production-support focused.

## Speech-To-Text

Speech-to-text is optional and dependency-gated:

```text
app/audio_listener.py
-> records a push-to-talk wav file when sounddevice/soundfile are installed

app/speech_to_text.py
-> transcribes audio files with Faster-Whisper when installed

scripts/voice_answer.py
-> records, transcribes, matches, and prints a natural answer
```

The default app still works without audio packages.

See [Voice Setup](VOICE_SETUP.md) for installation and local verification notes.
