import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.speech_to_text import SpeechToTextUnavailable, transcribe_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe an audio file with Faster-Whisper")
    parser.add_argument("audio_path")
    parser.add_argument("--model", default="base.en")
    args = parser.parse_args()

    try:
        result = transcribe_file(args.audio_path, model_size=args.model)
    except SpeechToTextUnavailable as exc:
        raise SystemExit(str(exc)) from exc

    print(result.text)


if __name__ == "__main__":
    main()
