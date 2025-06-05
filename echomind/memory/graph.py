from __future__ import annotations

import os
from typing import List, Optional

import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langsmith import Client as LangSmithClient

from echomind.config import settings


class MeetingMemory:
    def __init__(self, vector_dir: Optional[str] = None):
        self.vector_dir = vector_dir or settings.vector_dir
        os.makedirs(self.vector_dir, exist_ok=True)
        self.embed_fn = SentenceTransformerEmbeddingFunction(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self._client: Optional[chromadb.PersistentClient] = None
        self._collection = None
        self.langsmith = LangSmithClient(api_key=settings.langsmith_api_key) if settings.langsmith_api_key else None

    def _load_or_create(self) -> None:
        if self._client is None:
            self._client = chromadb.PersistentClient(path=self.vector_dir, settings=ChromaSettings(allow_reset=False))
        if self._collection is None:
            name = "echomind_memory"
            existing = [c.name for c in self._client.list_collections()]
            if name in existing:
                self._collection = self._client.get_collection(name=name, embedding_function=self.embed_fn)
            else:
                self._collection = self._client.create_collection(name=name, embedding_function=self.embed_fn)

    def add_transcript(self, session_id: str, text: str) -> None:
        self._load_or_create()
        meta = {"session_id": session_id}
        self._collection.add(documents=[text], metadatas=[meta], ids=[f"{session_id}-{abs(hash(text))}"])
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
        res = self._collection.query(query_texts=[query], n_results=k)
        docs = res.get("documents", [[]])[0]
        return list(docs)


