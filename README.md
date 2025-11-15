# Member QA Service

A lightweight FastAPI application that answers natural-language questions using member messages retrieved from the provided public API.

## Live Deployment:
```
https://maharshi02-member-qa-service.hf.space/chat/
```
## Goal

The service answers natural language questions such as:

“When is Layla planning her trip to London?”

“How many cars does Vikram Desai have?”

“What are Amira’s favorite restaurants?”

Given a question, the API returns:
```
{ "answer": "..." }
```
## Features

✅ FastAPI endpoint /ask

Accepts a question via query parameter and returns the inferred answer.

✅ Gradio UI (/chat)

Interactive chat interface for natural-language Q&A.

✅ Data Source Integration

Reads all member messages from:

```https://november7-730026606190.europe-west1.run.app/docs#/default/get_messages_messages__get```

✅ Public Deployment

Docker-based FastAPI Space deployed on Hugging Face.

## API Endpoints

1️⃣ Ask a Question

```GET /ask?query=hello```

Example Response:
```
{
  "answer": "Layla’s trip to London is planned for June 2024."
}
```

2️⃣ API Docs (Swagger UI)

```/docs```

3️⃣ Gradio Chat UI

```/chat/```

## System Architecture

               ┌─────────────────────┐
               │   /messages API     │
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
               FastAPI `/ask` Endpoint
                         │
                  JSON Answer Output

## Tech Stack

1. FastAPI – backend API

2. Gradio – chat interface

3. OpenAI model – reasoning engine

4. httpx / requests – data fetching

5. Docker – deployment on Hugging Face

## How It Works

1) Downloads all messages from the /messages API

2) Normalizes & indexes the messages

3) Performs semantic retrieval to find relevant messages

4) Sends question + retrieved context to an LLM

Returns:

```{ "answer": "..." }```

## Bonus 1: Design Notes (Alternative Approaches)

1) Rule-Based Parsing

- Keyword mapping to message fields.

- ❌ Too brittle for free-form natural language.

2) Embedding-Based Semantic Retrieval (Chosen Approach)

- Retrieve relevant messages using vector search.
 - Generalizable
 - Simple
 - Works with varied phrasing

3) Fine-Tuned QA Model

- omain-specific training.

- ❌ Too heavy for assignment scope.

## Bonus 2: Data Insights

From analyzing the member message dataset:

1) Inconsistent date formats

 - “next June”, “6/10/2024”, “June 2024”
 → Requires LLM interpretation.

2) Ambiguous references

 - “her trip”, “my car”
 → Needs context-based disambiguation.

3) Missing information

 - Some messages imply details but never state them explicitly.

4) Name variations

 - “Vikram”, “Vik”
 → Must reference same member.

These inconsistencies justify using semantic retrieval + LLM reasoning instead of rule-based parsing.

## Running Locally

Install dependencies:

```pip install -r requirements.txt```


Run development server:

```uvicorn app.main:app --reload```


Open in browser:

API Docs → http://localhost:8000/docs

Chat UI → http://localhost:8000/chat/

## Deployment

This application is deployed using a Dockerized FastAPI Space on Hugging Face.

It exposes FastAPI on port 7860 and automatically loads via:

```uvicorn server:app --host 0.0.0.0 --port 7860```

## Author

Maharshi Shah
