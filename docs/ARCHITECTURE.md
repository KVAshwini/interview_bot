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

## Personality Layer

Stored answers remain clean and structured. The speech layer adapts them into a natural read-aloud version using files in `memory/speech_style/`.

The target style is casual professional, practical, and production-support focused.
