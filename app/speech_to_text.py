from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union


class SpeechToTextUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class TranscriptionResult:
    text: str
    language: Optional[str] = None
    duration: Optional[float] = None


class FasterWhisperTranscriber:
    def __init__(self, model_size: str = "base.en", device: str = "auto") -> None:
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise SpeechToTextUnavailable(
                "faster-whisper is not installed. Install it with: pip install faster-whisper"
            ) from exc

        self.model = WhisperModel(model_size, device=device)

    def transcribe_file(self, audio_path: Union[str, Path]) -> TranscriptionResult:
        segments, info = self.model.transcribe(str(audio_path), vad_filter=True)
        text = " ".join(segment.text.strip() for segment in segments if segment.text.strip())
        return TranscriptionResult(
            text=text.strip(),
            language=getattr(info, "language", None),
            duration=getattr(info, "duration", None),
        )


def transcribe_file(audio_path: Union[str, Path], model_size: str = "base.en") -> TranscriptionResult:
    return FasterWhisperTranscriber(model_size=model_size).transcribe_file(audio_path)
