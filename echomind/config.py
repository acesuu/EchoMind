from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    # Audio
    input_device: Optional[str] = os.getenv("ECHO_INPUT_DEVICE") or "default"
    sample_rate_hz: int = int(os.getenv("ECHO_SAMPLE_RATE_HZ") or "16000")
    block_size: int = int(os.getenv("ECHO_BLOCK_SIZE") or "2048")

    # STT
    stt_provider: str = os.getenv("ECHO_STT_PROVIDER") or "local"  # local | openai
    whisper_model: str = os.getenv("ECHO_WHISPER_MODEL") or "medium"
    whisper_compute_type: str = os.getenv("ECHO_WHISPER_COMPUTE") or "auto"

    # LLM
    llm_provider: str = os.getenv("ECHO_LLM_PROVIDER") or "openai"  # or "huggingface"
    llm_model: str = os.getenv("ECHO_LLM_MODEL") or "gpt-4o-mini"
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    huggingface_api_key: Optional[str] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    # Memory / Vector store
    vector_dir: str = os.getenv("ECHO_VECTOR_DIR") or "data/vector"
    langsmith_api_key: Optional[str] = os.getenv("LANGSMITH_API_KEY")
    langsmith_project: Optional[str] = os.getenv("LANGSMITH_PROJECT") or "EchoMind"

    # TTS (Cartesia)
    cartesia_api_key: Optional[str] = os.getenv("CARTESIA_API_KEY")
    cartesia_voice_id: str = os.getenv("CARTESIA_VOICE_ID") or "alloy"

    # Telemetry
    metrics_host: str = os.getenv("ECHO_METRICS_HOST") or "127.0.0.1"
    metrics_port: int = int(os.getenv("ECHO_METRICS_PORT") or "9108")

    # General
    log_level: str = os.getenv("ECHO_LOG_LEVEL") or "INFO"


settings = Settings()


