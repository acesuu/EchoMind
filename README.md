EchoMind
========

A real-time voice-based meeting companion in pure Python. It can:

- Join virtual calls
- Transcribe speech (STT)
- Summarize and analyze conversations using LLMs (LangChain / Hugging Face)
- Answer follow-up questions about past meetings (LangGraph memory + LangSmith observability)
- Speak its answers back (TTS via Cartesia)
- Provide a monitoring dashboard (Grafana + Telemetry)

Status: Early prototype.

Quick start
-----------
1) Create and activate a Python 3.10+ virtual environment.
2) Install requirements: `pip install -r requirements.txt`
3) Copy `.env.example` to `.env` and fill your keys as needed.
4) Run the CLI: `python -m echomind.cli --help`

Monitoring
----------
EchoMind exposes Prometheus metrics locally. Grafana dashboards are provided under `grafana/`.

License
-------
MIT © EchoMind contributors


