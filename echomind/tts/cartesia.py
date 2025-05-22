from __future__ import annotations

import io
from typing import Optional

import numpy as np
import sounddevice as sd
import soundfile as sf
import httpx

from echomind.config import settings


class CartesiaTTS:
    def __init__(self, api_key: Optional[str] = None, voice_id: Optional[str] = None):
        self.api_key = api_key or settings.cartesia_api_key
        self.voice_id = voice_id or settings.cartesia_voice_id
        self._client = httpx.Client(timeout=30.0)

    def synthesize(self, text: str) -> np.ndarray:
        if not self.api_key:
            raise RuntimeError("CARTESIA_API_KEY not set")
        # Hypothetical Cartesia REST API; adapt to actual endpoint if differs.
        url = "https://api.cartesia.ai/v1/tts"
        payload = {"voice_id": self.voice_id, "text": text, "format": "wav"}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = self._client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        wav_bytes = resp.content
        data, sr = sf.read(io.BytesIO(wav_bytes), dtype="float32")
        if data.ndim == 2:
            data = data.mean(axis=1)
        return data

    def play(self, audio: np.ndarray, sample_rate: int = 22050) -> None:
        sd.play(audio, samplerate=sample_rate)
        sd.wait()


