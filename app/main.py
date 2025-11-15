from fastapi import FastAPI, Query, HTTPException
from dotenv import load_dotenv
load_dotenv()
from .data_source import MessageClient
from .normalizer import MessageNormalizer
from .indexer import MessageIndex
from .qa import QASystem
from .schemas import AskResponse
from fastapi.responses import RedirectResponse
from .ui import build_gradio_app


app = FastAPI(
    title="Member QA Service (RAG + LLM)",
    version="1.0.0",
    description=(
        "Answers natural-language questions about members using messages from "
        "the /messages API, via retrieval-augmented generation."
    ),
)

message_client = MessageClient()
normalizer = MessageNormalizer()
index = MessageIndex()
qa_system = QASystem(index)


def refresh_index():
    raw = message_client.fetch_messages()
    normalized = normalizer.normalize_many(raw)
    index.build(normalized)


@app.on_event("startup")
def on_startup():
    try:
        refresh_index()
    except Exception as e:
        print(f"[WARN] Failed to build index on startup: {e}")


@app.get("/ask", response_model=AskResponse)
def ask(
    question: str = Query(..., description="Natural-language question about member data"),
    reload: bool = Query(False, description="If true, refetch /messages before answering"),
):
    if reload or not index.get_all():
        try:
            refresh_index()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Failed to refresh data: {e}")

    answer = qa_system.answer(question)
    return AskResponse(answer=answer)

# Build and mount Gradio at /chat
gradio_app = build_gradio_app(qa_system, index)
from gradio.routes import mount_gradio_app  # gradio helper to mount under FastAPI
app = mount_gradio_app(app, gradio_app, path="/chat")

# Optional convenience: redirect root to /chat
@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/chat")
