from __future__ import annotations

from typing import List, Optional

from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatHuggingFace

from echomind.config import settings


SUMMARY_SYSTEM = """You are an expert meeting assistant.
Summarize the conversation accurately and concisely.
Highlight decisions, action items, owners, and deadlines when present."""

SUMMARY_TEMPLATE = PromptTemplate.from_template(
    "Summarize the following transcript chunk:\n\n{chunk}\n\nReturn a crisp bullet list."
)


class ConversationSummarizer:
    def __init__(self, model: Optional[str] = None):
        self.model_name = model or settings.llm_model
        self.provider = settings.llm_provider
        self._llm = None

    def _get_llm(self):
        if self._llm is not None:
            return self._llm
        if self.provider == "openai":
            self._llm = ChatOpenAI(model=self.model_name, api_key=settings.openai_api_key, temperature=0.2)
        else:
            # huggingface hub chat wrapper
            self._llm = ChatHuggingFace(model_name=self.model_name, huggingface_api_key=settings.huggingface_api_key)
        return self._llm

    def summarize(self, transcript_chunk: str) -> str:
        llm = self._get_llm()
        messages = [
            SystemMessage(content=SUMMARY_SYSTEM),
            HumanMessage(content=SUMMARY_TEMPLATE.format(chunk=transcript_chunk)),
        ]
        resp = llm(messages)
        return resp.content.strip()


