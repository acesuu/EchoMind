from __future__ import annotations

import threading
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, generate_latest
from prometheus_client import multiprocess  # type: ignore
from prometheus_client import REGISTRY
import uvicorn

from echomind.config import settings


app = FastAPI(title="EchoMind Metrics")


@app.get("/healthz", response_class=PlainTextResponse)
def healthz() -> str:
    return "ok"


@app.get("/metrics")
def metrics():
    data = generate_latest(REGISTRY)
    return PlainTextResponse(data.decode("utf-8"), media_type=CONTENT_TYPE_LATEST)


def main() -> None:
    uvicorn.run(app, host=settings.metrics_host, port=settings.metrics_port, log_level="info")


if __name__ == "__main__":
    main()


