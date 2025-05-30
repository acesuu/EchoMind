from __future__ import annotations

from typing import Optional

from echomind.memory import MeetingMemory
from echomind.llm import ConversationSummarizer


class MeetingQA:
    def __init__(self):
        self.memory = MeetingMemory()
        self.summarizer = ConversationSummarizer()

    def ask(self, question: str, k: int = 5) -> str:
        results = self.memory.search(question, k=k)
        context = "\n".join(f"- {r}" for r in results)
        prompt = f"Question: {question}\n\nContext from past meetings:\n{context}\n\nAnswer succinctly based on the context."
        return self.summarizer.summarize(prompt)


