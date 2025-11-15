from typing import Any, Dict, Optional
from datetime import datetime
from pydantic import BaseModel


class AskResponse(BaseModel):
    answer: str


class NormalizedMessage(BaseModel):
    """
    Internal normalized representation of a message from /messages.
    """
    id: Optional[str]
    user_id: Optional[str]
    member_name: Optional[str]  # maps from user_name
    text: str
    timestamp: Optional[datetime]
    raw: Dict[str, Any]
