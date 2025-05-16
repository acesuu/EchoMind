from __future__ import annotations

from dataclasses import dataclass
from typing import Generator, Iterable, Optional

import numpy as np
from faster_whisper import WhisperModel

from echomind.config import settings


@dataclass
class TranscriptionSegment:
    start: float
    end: float
    text: str


class WhisperTranscriber:
    def __init__(self, model: Optional[str] = None, compute_type: Optional[str] = None, sample_rate_hz: Optional[int] = None):
        self.model_name = model or settings.whisper_model
        self.compute_type = compute_type or settings.whisper_compute_type
        self.sample_rate_hz = sample_rate_hz or settings.sample_rate_hz
        self._model: Optional[WhisperModel] = None

    def load(self) -> None:
        if self._model is None:
            self._model = WhisperModel(self.model_name, compute_type=self.compute_type)

    def transcribe_blocks(self, blocks: Iterable[np.ndarray]) -> Generator[TranscriptionSegment, None, None]:
        if self._model is None:
            self.load()
        assert self._model is not None
        # Concatenate a window of audio and feed to whisper
        audio = np.concatenate([b.flatten() for b in blocks], axis=0)
        segments, _ = self._model.transcribe(audio, language="en")
        for seg in segments:
            yield TranscriptionSegment(start=float(seg.start), end=float(seg.end), text=str(seg.text).strip())


