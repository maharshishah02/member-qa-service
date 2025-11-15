from typing import List, Dict
from .schemas import NormalizedMessage


class MessageIndex:

    def __init__(self):
        self.messages: List[NormalizedMessage] = []
        self.by_member: Dict[str, List[NormalizedMessage]] = {}
        self.member_names: List[str] = []

    def build(self, messages: List[NormalizedMessage]) -> None:
        self.messages = messages
        self.by_member = {}
        names = set()

        for m in messages:
            if m.member_name:
                key = m.member_name.strip()
                if key:
                    names.add(key)
                    self.by_member.setdefault(key.lower(), []).append(m)

        self.member_names = sorted(names)

    def get_all(self) -> List[NormalizedMessage]:
        return self.messages
