import gradio as gr
from typing import List, Tuple

from .qa import QASystem
from .indexer import MessageIndex


def build_gradio_app(qa_system: QASystem, index: MessageIndex):
    """
    Builds a Gradio UI (Blocks + ChatInterface) for chatting with the QA system.
    Fully compatible with Gradio 5.49.1. Includes built-in Retry and Clear buttons.
    """

    # Chat handler
    def respond(message: str, history: List[Tuple[str, str]]):
        if not message or not message.strip():
            return "Please type a question about the member messages."
        return qa_system.answer(message.strip())

    # Build UI
    with gr.Blocks(title="Member QA Chat") as demo:

        gr.Markdown(
            """
            <h2>Member QA Chat</h2>
            <p>Ask any natural-language question about the member messages.</p>
            """,
        )

        gr.ChatInterface(
            fn=respond,
            type="messages",
            chatbot=gr.Chatbot(
                height=450,
                label="Assistant",
                show_copy_button=True,
            ),
            textbox=gr.Textbox(
                placeholder="e.g., When is Sophia planning her trip to Paris?",
                label="Your question",
            ),
            submit_btn="Ask"
        )

    return demo
