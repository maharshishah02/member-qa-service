import math
import re
from typing import List, Optional, Tuple

from .indexer import MessageIndex
from .schemas import NormalizedMessage
from .config import TOP_K


class LexicalRetriever:

    def __init__(self, index: MessageIndex, top_k: int = TOP_K):
        self.index = index
        self.top_k = top_k

    @staticmethod
    def _tokens(text: str) -> List[str]:
        return [t.lower() for t in re.findall(r"\w+", text)]

    def _score(self, question: str, message: NormalizedMessage, member_hint: Optional[str]) -> float:
        q_tokens = set(self._tokens(question))
        m_tokens = set(self._tokens(message.text))

        if not q_tokens or not m_tokens:
            return 0.0

        overlap = len(q_tokens & m_tokens)
        if overlap == 0:
            return 0.0

        score = overlap / math.sqrt(len(m_tokens) + 1)

        if member_hint and message.member_name:
            if message.member_name.lower() == member_hint.lower():
                score *= 1.5

        return score

    def retrieve(self, question: str, member_hint: Optional[str]) -> List[NormalizedMessage]:
        scored: List[Tuple[float, NormalizedMessage]] = []

        for m in self.index.get_all():
            s = self._score(question, m, member_hint)
            if s > 0:
                scored.append((s, m))

        if not scored:
            return []

        scored.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored[: self.top_k]]
