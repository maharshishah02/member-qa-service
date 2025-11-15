📘 Member QA Service

A lightweight FastAPI application that answers natural-language questions using member messages retrieved from the provided public API.


👉 Live Deployment:

https://maharshi02-member-qa-service.hf.space/chat/


✨ Goal

The service answers natural language questions such as:

“When is Layla planning her trip to London?”

“How many cars does Vikram Desai have?”

“What are Amira’s favorite restaurants?”

Given a question, the API returns:

{ "answer": "..." }


🚀 Features

✅ FastAPI endpoint /ask

Accepts a question via a query parameter and returns the inferred answer based on member messages.

✅ Gradio UI (/chat)

A simple web interface for interactive Q&A.

✅ Data Source Integration

The service pulls member messages from the official assessment API:

GET https://november7-730026606190.europe-west1.run.app/messages

✅ Deployed on Hugging Face

Runs in a Docker-based FastAPI Space and is publicly accessible.

📡 API Endpoints

1️⃣ Ask a Question

GET /ask?query=hello

Response:

{

  "answer": "Layla’s trip to London is planned for June 2024."
  
}

2️⃣ Docs

Swagger UI documentation
/docs

3️⃣ Gradio Chat UI

Interactive UI:
/chat/

🧠 System Architecture
               ┌─────────────────────┐
               │  /messages API      │
               │  External Data Src  │
               └─────────┬───────────┘
                         │
                Fetch & Normalize
                         │
        ┌────────────────▼────────────────┐
        │       Indexer / Retriever       │
        │  (semantic search over messages)│
        └────────────────┬────────────────┘
                         │
               LLM Reasoning Layer
                         │
          FastAPI `/ask` → Returns JSON

🔧 Tech Stack
FastAPI – core backend
Gradio – UI
OpenAI model – natural-language reasoning
Python requests/httpx – message fetching
Docker – for Hugging Face deployment

🧪 How It Works
Downloads all member messages from the /messages API
Normalizes & indexes messages
Performs semantic retrieval to select the most relevant messages
Sends the question + selected messages to the LLM
Returns the final answer as JSON


⭐ Bonus 1: Design Notes
Alternative Approaches Considered
1) Rule-Based Parsing:
Extract keywords and map them to message fields.
Rejected because it breaks easily with flexible natural language.
2) Embedding-Based Vector Search (Chosen Approach):
Convert messages into embeddings, retrieve top-k related messages.
Works well with varied language and is simple to implement.
3) Fine-Tuned QA Model:
Could train a domain-specific model on historical QA pairs.
Considered too heavy for the assignment scope.

⭐ Bonus 2: Data Insights
From inspecting the member messages dataset:
Anomalies & Inconsistencies Found
1) Inconsistent date formats
Some messages contain dates in natural language (“next June”), others use exact formats.
2) Ambiguous references
Some messages reference events or people not fully identifiable (e.g., “her trip”, “my car”).
3) Missing information
Several messages hint at a topic (e.g., travel plans) without explicit details.
4) Name variations
Some members appear to have nicknames or spelling variations (“Vikram” vs “Vik”).

Such inconsistencies require using semantic retrieval + LLM reasoning rather than direct parsing.

🏗️ Running Locally
Install dependencies:
pip install -r requirements.txt
Run FastAPI server:
uvicorn app.main:app --reload
Open:
API → http://localhost:8000/docs
Chat UI → http://localhost:8000/chat/

📦 Deployment
The service is deployed using a Docker-based Hugging Face Space:
It exposes FastAPI on port 7860 and runs automatically.
