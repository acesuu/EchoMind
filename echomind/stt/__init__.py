from .transcriber import WhisperTranscriber, TranscriptionSegment as LocalTranscriptionSegment  # type: ignore
from .openai_stt import OpenAITranscriber, TranscriptionSegment as OpenAITranscriptionSegment  # type: ignore

TranscriptionSegment = LocalTranscriptionSegment  # alias

__all__ = ["WhisperTranscriber", "OpenAITranscriber", "TranscriptionSegment"]


