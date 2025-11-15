from typing import Optional, List

from .indexer import MessageIndex
from .retriever import LexicalRetriever
from .schemas import NormalizedMessage
from .config import TOP_K
from .llm_client import LLMClient


class QASystem:

    def __init__(self, index: MessageIndex):
        self.index = index
        self.retriever = LexicalRetriever(index, top_k=TOP_K)
        self.llm = LLMClient()

    def _infer_member_from_question(self, question: str) -> Optional[str]:
        q_low = question.lower()
        best = None
        best_len = 0
        for name in self.index.member_names:
            if not name:
                continue
            n_low = name.lower()
            if n_low in q_low and len(n_low) > best_len:
                best = name
                best_len = len(n_low)
        return best

    def answer(self, question: str) -> str:
        q = question.strip()
        if not q:
            return "Please provide a question."

        member_hint = self._infer_member_from_question(q)

        candidates: List[NormalizedMessage] = self.retriever.retrieve(q, member_hint)

        if not candidates:
            return "I couldn't find an answer to that question in the member messages."

        ctx: List[dict] = []
        for m in candidates:
            ctx.append(
                {
                    "id": m.id,
                    "user_id": m.user_id,
                    "user_name": m.member_name,
                    "timestamp": m.timestamp.isoformat() if m.timestamp else None,
                    "message": m.text,
                }
            )

        return self.llm.generate_answer(q, ctx)
