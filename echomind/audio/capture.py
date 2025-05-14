from __future__ import annotations

import contextlib
from typing import Generator, Optional

import numpy as np
import sounddevice as sd

from echomind.config import settings


def list_input_devices() -> list[str]:
    devices = sd.query_devices()
    names: list[str] = []
    for d in devices:
        if int(d.get("max_input_channels", 0)) > 0:
            names.append(str(d.get("name")))
    return names


class AudioCapture:
    def __init__(self, device_name: Optional[str] = None, sample_rate_hz: Optional[int] = None, block_size: Optional[int] = None):
        self.device_name = device_name or settings.input_device
        self.sample_rate_hz = sample_rate_hz or settings.sample_rate_hz
        self.block_size = block_size or settings.block_size
        self._stream: Optional[sd.InputStream] = None

    def __enter__(self) -> "AudioCapture":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.stop()

    def start(self) -> None:
        device = None if self.device_name == "default" else self.device_name
        self._stream = sd.InputStream(
            device=device,
            samplerate=self.sample_rate_hz,
            channels=1,
            dtype="float32",
            blocksize=self.block_size,
        )
        self._stream.start()

    def stop(self) -> None:
        if self._stream is not None:
            with contextlib.suppress(Exception):
                self._stream.stop()
                self._stream.close()
            self._stream = None

    def frames(self) -> Generator[np.ndarray, None, None]:
        if self._stream is None:
            raise RuntimeError("Stream is not started")
        while True:
            data, _ = self._stream.read(self.block_size)
            yield data.copy()


