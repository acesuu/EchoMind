from __future__ import annotations

import asyncio
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from echomind.config import settings
from echomind.audio import list_input_devices, AudioCapture
from echomind.agent import MeetingAgent


app = typer.Typer(add_completion=False)
console = Console()


@app.command()
def ask(question: str = typer.Argument(..., help="Ask a question about past meetings")):
    """
    Ask a follow-up question grounded in memory of past meetings.
    """
    from echomind.qa import MeetingQA

    qa = MeetingQA()
    answer = qa.ask(question)
    console.print(Panel(answer, title="Answer", border_style="cyan"))


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
    agent = MeetingAgent(device=device, session_id=session)
    agent.start()
    console.print(f"[dim]Audio device open: {device} at {settings.sample_rate_hz} Hz[/dim]")
    try:
        while True:
            out = await agent.step()
            if out:
                console.print(Panel(out, title="Summary", border_style="green"))
            await asyncio.sleep(summarize_every_s)
    finally:
        agent.stop()


if __name__ == "__main__":
    app()


