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
    audio = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1, dtype="float32")
    sd.wait()
    sf.write(str(output), audio, sample_rate)
    return output
