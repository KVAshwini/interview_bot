import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.audio_listener import AudioCaptureUnavailable, list_audio_devices


def main() -> None:
    try:
        devices = list_audio_devices()
    except AudioCaptureUnavailable as exc:
        raise SystemExit(str(exc)) from exc
    print(devices if devices.strip() else "No audio devices visible to this Python process.")


if __name__ == "__main__":
    main()
