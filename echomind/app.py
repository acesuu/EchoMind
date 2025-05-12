from __future__ import annotations

import asyncio
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from echomind.config import settings


app = typer.Typer(add_completion=False)
console = Console()


@app.command()
def run(
    device: str = typer.Option(settings.input_device, help="Audio input device name or 'default'"),
    session: str = typer.Option("session-1", help="Meeting session id"),
    summarize_every_s: int = typer.Option(60, help="Summarization interval"),
):
    """
    Run EchoMind: capture audio, transcribe, summarize periodically.
    Placeholder pipeline; later commits will wire STT/LLM/memory/tts.
    """
    console.print(
        Panel.fit(
            f"[bold cyan]EchoMind[/bold cyan]\n"
            f"Device: {device}\nSession: {session}\nSummarize interval: {summarize_every_s}s",
            title="Startup",
        )
    )
    try:
        asyncio.run(_main_loop(device, session, summarize_every_s))
    except KeyboardInterrupt:
        console.print("[yellow]Exiting...[/yellow]")


async def _main_loop(device: str, session: str, summarize_every_s: int) -> None:
    # Placeholder: later we will integrate capture → STT → LLM → memory → TTS
    while True:
        console.print("[dim]Listening... (stub)[/dim]")
        await asyncio.sleep(summarize_every_s)
        console.print("[green]Summary (stub):[/green] Meeting continues smoothly.")


if __name__ == "__main__":
    app()


