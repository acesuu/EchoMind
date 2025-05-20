from __future__ import annotations

import os
from typing import List, Optional

import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langsmith import Client as LangSmithClient

from echomind.config import settings


class MeetingMemory:
    def __init__(self, vector_dir: Optional[str] = None):
        self.vector_dir = vector_dir or settings.vector_dir
        os.makedirs(self.vector_dir, exist_ok=True)
        self.embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.store = None  # lazy
        self.langsmith = LangSmithClient(api_key=settings.langsmith_api_key) if settings.langsmith_api_key else None

    def _load_or_create(self) -> None:
        if self.store is not None:
            return
        index_path = os.path.join(self.vector_dir, "index.faiss")
        if os.path.exists(index_path):
            self.store = FAISS.load_local(self.vector_dir, self.embed, allow_dangerous_deserialization=True)
        else:
            self.store = FAISS.from_texts(texts=[], embedding=self.embed)
            self.store.save_local(self.vector_dir)

    def add_transcript(self, session_id: str, text: str) -> None:
        self._load_or_create()
        meta = {"session_id": session_id}
        self.store.add_texts([text], [meta])
        self.store.save_local(self.vector_dir)
        if self.langsmith:
            self.langsmith.create_feedback(
                run_id=None,
                key="memory_add",
                score=1.0,
                comment=f"Added transcript to session {session_id}",
                source="echomind",
                project_name=settings.langsmith_project,
            )

    def search(self, query: str, k: int = 5) -> List[str]:
        self._load_or_create()
        docs = self.store.similarity_search(query, k=k)
        return [d.page_content for d in docs]


