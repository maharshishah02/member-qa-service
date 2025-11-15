import os

# External messages API (provided in the assignment)
MESSAGES_URL = os.getenv(
    "MESSAGES_URL",
    "https://november7-730026606190.europe-west1.run.app/messages/"
)

# Retrieval config
TOP_K = int(os.getenv("TOP_K", "5"))

# LLM config
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")  # or gpt-4.1, gpt-4o, etc.
# OPENAI_API_KEY is read directly from env in llm_client.py