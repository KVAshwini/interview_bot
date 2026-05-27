import json
from pathlib import Path

from app.config import MEMORY_DIR


DEFAULT_PROFILE = "ashwini_interview_style"


def _profile_path(profile: str = DEFAULT_PROFILE) -> Path:
    return MEMORY_DIR / "speech_style" / "interview_tone_profiles.json"


def load_profile(profile: str = DEFAULT_PROFILE) -> dict:
    path = _profile_path(profile)
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    profiles = payload.get("profiles", {})
    return profiles.get(profile, {})


def _clean_step_text(answer: str) -> str:
    lines = [line.strip() for line in answer.splitlines() if line.strip()]
    cleaned = []
    for line in lines:
        if line.startswith("step_"):
            _, value = line.split(":", 1)
            cleaned.append(value.strip())
        else:
            cleaned.append(line)
    return " ".join(cleaned)


def _join_starter(starter: str, sentence: str) -> str:
    sentence = sentence.strip()
    if sentence.lower().startswith("i "):
        sentence = sentence[2:].strip()
    if sentence:
        sentence = sentence[0].lower() + sentence[1:]
    return f"{starter} {sentence}."


def adapt_answer(answer: str, profile_name: str = DEFAULT_PROFILE) -> str:
    profile = load_profile(profile_name)
    if not profile:
        return answer

    phrases = profile.get("sentence_starters", [])
    bridge = profile.get("technical_bridge", "From my experience")
    closer = profile.get("closer", "After that I would do RCA and add preventive actions.")

    compact = _clean_step_text(answer)
    sentences = [part.strip() for part in compact.replace("\n", " ").split(".") if part.strip()]
    if not sentences:
        return answer

    first = sentences[0]
    middle = sentences[1:4]
    starter = phrases[0] if phrases else "Usually what I do is"
    second_starter = phrases[1] if len(phrases) > 1 else "Then mostly"

    natural_parts = [_join_starter(starter, first)]
    if middle:
        natural_parts.append(f"{second_starter} " + ". ".join(middle) + ".")
    natural_parts.append(f"{bridge}, I try to keep it practical: stabilize first, communicate clearly, and then fix the root cause.")
    natural_parts.append(closer)
    return " ".join(natural_parts)


def quick_versions(answer: str, natural_answer: str) -> dict[str, str]:
    quick = answer.split(".")[0].strip()
    if quick and not quick.endswith("."):
        quick += "."
    return {
        "quick": quick or answer,
        "natural": natural_answer,
        "detailed": answer,
    }
