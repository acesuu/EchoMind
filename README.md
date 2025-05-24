# EchoMind

Real-time voice-based meeting companion in pure Python.

EchoMind can:
- Join virtual calls (via selectable audio device loopback)
- Transcribe speech (STT)
- Summarize and analyze conversations using LLMs (LangChain / Hugging Face)
- Answer follow-up questions about past meetings (LangGraph memory + LangSmith observability)
- Speak answers back (TTS via Cartesia)
- Provide a monitoring dashboard (Prometheus metrics + Grafana)

## Status
Initial scaffolding. See roadmap in commit history.

## Quickstart
1) Create and activate a virtual environment
```
python -m venv .venv
.venv\\Scripts\\activate
```
2) Install dependencies
```
pip install -r requirements.txt
```
3) Copy env and edit
```
copy .env.example .env
```
4) Run EchoMind CLI (transcribe + summarize)
```
python -m echomind.app --device \"default\" --session \"demo-session\"
```
5) Start metrics server
```
python -m echomind.telemetry.server
```

Grafana dashboard and setup located in `grafana/`.


## License
MIT


