import os
from typing import List, Dict

from openai import OpenAI  # pip install openai

from .config import LLM_MODEL

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = OpenAI()


class LLMClient:

    def __init__(self, model: str = LLM_MODEL):
        self.model = model

    def generate_answer(self, question: str, context_messages: List[Dict]) -> str:
        if not context_messages:
            return "I couldn't find an answer to that question in the member messages."

        # If no key configured or model unavailable, use deterministic fallback
        # (this keeps the service functional without secrets).
        if not OPENAI_API_KEY:
            return self._simple_fallback_answer(question, context_messages)

        context_block = self._format_context(context_messages)

        system_prompt = (
            "You are an assistant that answers questions about members using ONLY the provided messages.\n"
            "Rules:\n"
            "- Use only the information from the messages.\n"
            "- If the answer is not clearly supported, say you cannot find that information.\n"
            "- Be concise, clear, and factual.\n"
        )

        user_prompt = (
            f"Question: {question}\n\n"
            f"Relevant messages:\n{context_block}\n\n"
            "Answer the question in one or two concise sentences."
        )

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()

    def _format_context(self, context_messages: List[Dict]) -> str:
        lines = []
        for m in context_messages:
            who = m.get("user_name") or m.get("member_name") or "Unknown"
            ts = m.get("timestamp") or "Unknown time"
            text = m.get("message") or m.get("text") or ""
            lines.append(f"- [{ts}] {who}: {text}")
        return "\n".join(lines)

    def _simple_fallback_answer(self, question: str, context_messages: List[Dict]) -> str:
        """
        Used if no OPENAI_API_KEY is set.
        Just surfaces the top message as a natural-ish answer.
        """
        m = context_messages[0]
        who = m.get("user_name") or m.get("member_name") or "the member"
        ts = m.get("timestamp")
        text = m.get("message") or m.get("text") or ""

        prefix = f"Based on {who}'s message"
        if ts:
            prefix += f" on {ts}"
        return f"{prefix}, {text}"
