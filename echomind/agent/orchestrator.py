from __future__ import annotations

import asyncio
from collections import deque
from typing import Deque, Optional

import numpy as np

from echomind.audio import AudioCapture
from echomind.stt import WhisperTranscriber, OpenAITranscriber
from echomind.llm import ConversationSummarizer
from echomind.memory import MeetingMemory
from echomind.telemetry import MEETING_FRAMES, STT_SEGMENTS, MEETING_SUMMARIES
from echomind.config import settings


class MeetingAgent:
    def __init__(self, device: str = "default", session_id: str = "session-1"):
        self.device = device
        self.session_id = session_id
        self.cap = AudioCapture(device_name=device)
        if settings.stt_provider == "openai":
            self.stt = OpenAITranscriber()
        else:
            self.stt = WhisperTranscriber()
        self.summarizer = ConversationSummarizer()
        self.memory = MeetingMemory()
        self.buffer: Deque[np.ndarray] = deque(maxlen=50)  # sliding window

    def start(self) -> None:
        self.cap.start()

    def stop(self) -> None:
        self.cap.stop()

    async def step(self) -> Optional[str]:
        # Pull frames and accumulate
        for _ in range(5):
            frame = next(self.cap.frames())
            self.buffer.append(frame)
            MEETING_FRAMES.inc()
            await asyncio.sleep(0)
        if len(self.buffer) < self.buffer.maxlen:
            return None
        # Transcribe current window
        segments = list(self.stt.transcribe_blocks(list(self.buffer)))
        for _ in segments:
            STT_SEGMENTS.inc()
        text = " ".join(s.text for s in segments if s.text)
        if not text.strip():
            return None
        # Persist to memory
        self.memory.add_transcript(self.session_id, text)
        # Summarize
        summary = self.summarizer.summarize(text)
        MEETING_SUMMARIES.inc()
        return summary


