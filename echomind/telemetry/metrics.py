from __future__ import annotations

from prometheus_client import Counter

MEETING_FRAMES = Counter("echomind_meeting_frames_total", "Audio frames processed")
STT_SEGMENTS = Counter("echomind_stt_segments_total", "STT segments produced")
MEETING_SUMMARIES = Counter("echomind_meeting_summaries_total", "Summaries generated")


