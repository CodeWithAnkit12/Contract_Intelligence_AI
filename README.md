📄 Contract Intelligence API

AI Developer Assignment – Aviara Labs

An AI-powered backend system that ingests legal contracts (PDFs), extracts structured data, answers questions using Retrieval-Augmented Generation (RAG), audits risky clauses, and streams responses — all running locally via Docker.

🚀 Overview

Legal contracts are unstructured and difficult to analyze programmatically. This project demonstrates how Generative AI + backend engineering can be combined to:

Ingest and process contract PDFs

Extract structured legal metadata

Answer user questions grounded strictly in uploaded documents

Detect risky clauses with severity and evidence

Stream LLM responses in real time

Provide production-style observability (health & metrics)

The system is designed with clean architecture, explainability, and scalability in mind.

🧠 Key Features
1️⃣ PDF Ingestion

Upload one or more PDF contracts

Automatic text extraction

UUID-based document IDs

Chunked and indexed for semantic search

2️⃣ Structured Contract Extraction

Extracts the following fields as strict JSON:

Parties

Effective date

Term

Governing law

Payment terms

Termination

Auto-renewal

Confidentiality

Indemnity

Liability cap (amount + currency)

Signatories (name, title)

Missing fields are returned as null.

3️⃣ RAG-based Question Answering

Uses vector similarity search over uploaded contracts

LLM answers are grounded only in retrieved context

Returns answers with citations (document IDs)

Prevents hallucination

4️⃣ Clause Risk Audit

Detects risky clauses such as:

Auto-renewal with short notice

Unlimited liability

Broad indemnity

Missing termination rights

Each finding includes:

Risk description

Severity (LOW / MEDIUM / HIGH)

Evidence snippet

5️⃣ Streaming Responses (SSE)

Token-by-token streaming for /ask/stream

Improves perceived latency

Excellent demo UX

6️⃣ Mini UI (Bonus UX)

Minimal Tailwind-based UI

Ask questions and see streamed answers

Served directly by FastAPI (no frontend build required)

7️⃣ Production Signals

/healthz readiness endpoint

/metrics Prometheus-compatible metrics

Clean logging

Dockerized setup

🏗️ Architecture
Client (Swagger / Mini UI)
        ↓
FastAPI Application
        ↓
PDF Parsing & Chunking
        ↓
Vector Store (ChromaDB)
        ↓
LLM (Extraction / RAG / Audit)

🛠️ Tech Stack

Backend

Python 3.11

FastAPI

Uvicorn

AI / GenAI

OpenAI GPT-4o-mini

OpenAI Embeddings (text-embedding-3-small)

Prompt-driven extraction & auditing

Vector Store

ChromaDB (local)

PDF Processing

PyPDF

Observability

Prometheus client

Infra

Docker

Docker Compose

📁 Project Structure
contract-intelligence-ai/
│
├── app/
│   ├── api/            # API routes
│   ├── core/           # LLM & config
│   ├── services/       # Business logic
│   ├── utils/          # Helpers (chunking)
│   ├── prompts/        # LLM prompts (verbatim)
│   └── eval/           # Evaluation scripts
│
├── ui/                 # Mini UI
├── data/               # PDFs & vector data
├── tests/              # Tests
│
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md

⚙️ Setup & Installation
1️⃣ Clone the repository
git clone <your-repo-url>
cd contract-intelligence-ai

2️⃣ Create .env
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4o-mini


⚠️ Do not commit .env

3️⃣ Run with Docker (recommended)
docker compose up --build


The API will be available at:

API: http://localhost:8000

Swagger Docs: http://localhost:8000/docs

Mini UI: http://localhost:8000/

🔌 API Endpoints
🔹 Ingest

POST /ingest

Upload one or more PDFs.

Response

{
  "document_ids": ["uuid-1", "uuid-2"]
}

🔹 Extract

POST /extract/{document_id}

Returns structured JSON fields extracted from the contract.

🔹 Ask (RAG)

POST /ask

{
  "question": "What is the liability cap?"
}


Response

{
  "answer": "...",
  "citations": [{ "doc_id": "uuid" }]
}

🔹 Ask (Streaming)

POST /ask/stream

Streams tokens via Server-Sent Events (SSE).

🔹 Audit

POST /audit/{document_id}

Returns detected risky clauses with severity and evidence.

🔹 Health & Metrics

GET /healthz

GET /metrics

🧪 Tests

Run tests locally:

pytest


Includes basic API health validation.

📊 Evaluation

The app/eval/ folder contains:

Sample Q&A pairs

Simple evaluation script

One-line accuracy summary

Used to sanity-check RAG answer quality.

🧩 Design Decisions & Trade-offs

FastAPI over Django → async, AI-friendly, better streaming

RAG over fine-tuning → safer, cheaper, explainable

ChromaDB (local) → simplicity for assignment, easy migration later

Prompt discipline → reproducibility & transparency

Minimal UI → demo-focused, reviewer-friendly

🔐 Security Notes

API keys stored only in environment variables

No training on user-uploaded data

RAG restricts LLM answers to provided context

Logs avoid raw contract content

🔮 Future Improvements

Background task processing

Authentication & authorization

Page-level citations

Managed vector DB (Pinecone)

Async ingestion workers

Rule-based audit fallback toggle

🎥 Loom Demo

A Loom walkthrough (8–10 minutes) is provided demonstrating:

Docker startup

Swagger docs

PDF ingestion

Extraction

RAG Q&A

Clause audit

Streaming

Metrics & tests

👤 Author

Ankit Kumar
Backend / AI Engineer
Python • FastAPI • GenAI • RAG