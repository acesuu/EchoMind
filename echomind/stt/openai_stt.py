from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Generator, Iterable

import numpy as np
import soundfile as sf
from openai import OpenAI

from echomind.config import settings


@dataclass
class TranscriptionSegment:
    start: float
    end: float
    text: str


class OpenAITranscriber:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    def transcribe_blocks(self, blocks: Iterable[np.ndarray]) -> Generator[TranscriptionSegment, None, None]:
        audio = np.concatenate([b.flatten() for b in blocks], axis=0)
        wav_io = io.BytesIO()
        sf.write(wav_io, audio, samplerate=settings.sample_rate_hz, format="WAV")
        wav_io.seek(0)
        # Whisper API v1
        resp = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.wav", wav_io, "audio/wav"),
            response_format="verbose_json",
        )
        text = resp.text or ""
        yield TranscriptionSegment(start=0.0, end=float(len(audio) / settings.sample_rate_hz), text=text.strip())


