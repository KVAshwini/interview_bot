from pathlib import Path
from typing import Union


class AudioCaptureUnavailable(RuntimeError):
    pass


def record_push_to_talk(output_path: Union[str, Path], seconds: int = 8, sample_rate: int = 16000) -> Path:
    try:
        import sounddevice as sd
        import soundfile as sf
    except ImportError as exc:
        raise AudioCaptureUnavailable(
            "Audio capture needs sounddevice and soundfile. Install with: pip install sounddevice soundfile"
        ) from exc

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        audio = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1, dtype="float32")
        sd.wait()
    except Exception as exc:
        raise AudioCaptureUnavailable(
            "No microphone input device is available to this Python process. "
            "Check macOS microphone permissions and run scripts/list_audio_devices.py."
        ) from exc
    sf.write(str(output), audio, sample_rate)
    return output


def list_audio_devices() -> str:
    try:
        import sounddevice as sd
    except ImportError as exc:
        raise AudioCaptureUnavailable(
            "Audio device listing needs sounddevice. Install with: pip install sounddevice"
        ) from exc
    return str(sd.query_devices())
