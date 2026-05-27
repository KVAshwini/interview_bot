import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.answer_engine import answer_payload
from app.audio_listener import AudioCaptureUnavailable, record_push_to_talk
from app.speech_to_text import SpeechToTextUnavailable, transcribe_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Record a short voice question and answer it locally")
    parser.add_argument("--seconds", type=int, default=8)
    parser.add_argument("--model", default="base.en")
    parser.add_argument("--mode", choices=["instant", "detailed"], default="instant")
    parser.add_argument("--voice", choices=["natural", "raw"], default="natural")
    args = parser.parse_args()

    audio_path = ROOT / "outputs" / "voice_questions" / "latest.wav"
    try:
        record_push_to_talk(audio_path, seconds=args.seconds)
        transcript = transcribe_file(audio_path, model_size=args.model).text
    except (AudioCaptureUnavailable, SpeechToTextUnavailable) as exc:
        raise SystemExit(str(exc)) from exc

    payload = answer_payload(transcript, mode=args.mode, limit=1, voice=args.voice)
    print(f"Transcript: {transcript}\n")
    if payload["matches"]:
        print(payload["matches"][0]["versions"]["natural"])
    else:
        print("No local answer found.")


if __name__ == "__main__":
    main()
