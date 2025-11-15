from typing import List, Dict, Any, Optional
from datetime import datetime
from .schemas import NormalizedMessage


class MessageNormalizer:
    TEXT_FIELDS = ("message", "text", "body", "content")
    MEMBER_DIRECT_FIELDS = ("user_name", "member_name", "memberName", "name")

    def normalize_many(self, raw_messages: List[Dict[str, Any]]) -> List[NormalizedMessage]:
        normalized: List[NormalizedMessage] = []

        for raw in raw_messages:
            text = self._extract_text(raw)
            if not text:
                continue

            msg = NormalizedMessage(
                id=self._extract_id(raw),
                user_id=self._extract_user_id(raw),
                member_name=self._extract_member_name(raw),
                text=text,
                timestamp=self._extract_timestamp(raw),
                raw=raw,
            )
            normalized.append(msg)

        return normalized

    def _extract_text(self, msg: Dict[str, Any]) -> str:
        for key in self.TEXT_FIELDS:
            val = msg.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
        return ""

    def _extract_member_name(self, msg: Dict[str, Any]) -> Optional[str]:
        for key in self.MEMBER_DIRECT_FIELDS:
            val = msg.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
        return None

    def _extract_user_id(self, msg: Dict[str, Any]) -> Optional[str]:
        val = msg.get("user_id")
        if isinstance(val, (str, int)):
            return str(val)
        return None

    def _extract_id(self, msg: Dict[str, Any]) -> Optional[str]:
        for key in ("id", "message_id", "uuid"):
            if key in msg and isinstance(msg[key], (str, int)):
                return str(msg[key])
        return None

    def _extract_timestamp(self, msg: Dict[str, Any]) -> Optional[datetime]:
        ts = msg.get("timestamp")
        if not isinstance(ts, str):
            return None
        try:
            return datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            return None
