📄 Design Document
Contract Intelligence API (AI Developer Assignment – Aviara Labs)
Author

Ankit Kumar

1. Problem Overview

Legal contracts are typically stored as unstructured PDFs, making it difficult to:

Extract key business/legal terms

Answer questions accurately with evidence

Identify risky clauses (e.g., unlimited liability, auto-renewal traps)

Provide transparent, explainable AI outputs

The goal of this system is to build a production-oriented Contract Intelligence API that:

Ingests PDF contracts

Extracts structured legal metadata

Answers user questions using Retrieval Augmented Generation (RAG)

Audits contracts for risky clauses with severity and evidence

Streams answers for better UX

Runs fully locally using Docker

2. High-Level Architecture
┌────────────┐
│   Client   │
│ (Swagger / │
│ Mini UI)   │
└─────┬──────┘
      │ HTTP / SSE
      ▼
┌──────────────────────┐
│      FastAPI App     │
│----------------------│
│ Ingest | Extract     │
│ Ask    | Audit       │
│ Stream | Metrics     │
└─────┬────────────────┘
      │
      ▼
┌────────────────────────────┐
│ Document Processing Layer  │
│----------------------------│
│ PDF Parsing (PyPDF)        │
│ Chunking                   │
│ Metadata tagging           │
└─────┬──────────────────────┘
      │
      ▼
┌────────────────────────────┐
│ Vector Store (ChromaDB)    │
│----------------------------│
│ Embeddings                 │
│ Similarity Search          │
└─────┬──────────────────────┘
      │
      ▼
┌────────────────────────────┐
│ LLM Layer (OpenAI)         │
│----------------------------│
│ Extraction (JSON)          │
│ RAG Q&A                    │
│ Clause Risk Audit          │
└────────────────────────────┘

3. Technology Stack & Rationale
Backend Framework – FastAPI

Async-first → ideal for I/O heavy tasks (PDFs, LLM calls)

Automatic OpenAPI/Swagger (excellent reviewer UX)

Native streaming support (SSE)

Widely adopted in AI startups

Why not Django?
Django is heavier and synchronous by default. FastAPI fits AI microservices better.

LLM & GenAI

OpenAI GPT-4o-mini

Strong reasoning

Cost-efficient

Reliable JSON outputs

Used for:

Structured contract extraction

RAG-based Q&A

Risk clause analysis

Vector Database – ChromaDB

Lightweight, local-first

No external dependency

Ideal for assignment scope

Easy migration to Pinecone/Weaviate later

Embeddings

text-embedding-3-small

Good semantic recall

Low latency

Storage

PDFs + extracted text → local filesystem

Vector embeddings → ChromaDB

Metadata → embedded via vector store

This keeps the system simple, inspectable, and local-first.

4. Ingestion & Chunking Strategy
PDF Ingestion

PDFs uploaded via /ingest

Stored with UUID-based document IDs

Text extracted page-by-page using PyPDF

Chunking Design
Chunk size: 800 characters  
Overlap:   100 characters


Why this works for contracts:

Legal clauses often span paragraphs

Overlap preserves clause continuity

Prevents context loss at chunk boundaries

Avoids token overflow during LLM calls

Trade-off:
Slight embedding redundancy, but better recall → preferred for legal accuracy.

5. Structured Extraction (/extract)
Objective

Convert unstructured contract text into machine-readable JSON.

Approach

Prompt-driven extraction

Strict JSON schema

Missing fields explicitly returned as null

Extracted Fields

Parties

Effective date

Term

Governing law

Payment & termination clauses

Auto-renewal

Confidentiality

Indemnity

Liability cap (amount + currency)

Signatories (name, title)

Why LLM-based extraction?

Contracts vary heavily in formatting

Regex/rules fail at scale

LLM handles semantic variability better

6. RAG-Based Question Answering (/ask)
Why RAG?

Prevents hallucination

Answers grounded only in uploaded contracts

No fine-tuning required

Transparent & auditable

Flow

User asks a question

Vector DB retrieves top-K relevant chunks

Chunks injected into prompt as context

LLM answers strictly from context

Response returned with citations

Citations

Each chunk contains document_id metadata

Returned alongside the answer

Enables explainability and trust

7. Clause Risk Audit (/audit)
Risks Detected

Auto-renewal with short notice

Unlimited liability

Broad indemnity obligations

Missing termination rights

Design

LLM-based reasoning

JSON output with:

Risk type

Severity (LOW / MEDIUM / HIGH)

Evidence text

Why LLM over pure rules?

Clause language varies widely

Semantics matter more than keywords

LLM identifies implicit risks

Fallback (Design Consideration)

If LLM fails or times out:

Simple rule-based heuristics can be applied

Ensures system never fully fails

8. Streaming Responses (/ask/stream)
Purpose

Improves perceived latency

Demonstrates real-time AI interaction

Enhances UX during demos

Implementation

Server-Sent Events (SSE)

Tokens streamed incrementally

Graceful fallback to non-streaming /ask

9. UI/UX Design
Philosophy

“Simple, fast, demo-friendly”

Instead of a full frontend app:

A minimal AI console UI

Tailwind-styled

Served directly by FastAPI

Why this works

Zero frontend build complexity

Perfect for Loom demo

Shows streaming visually

Reviewer can test instantly

Swagger UI is also intentionally polished:

Clear endpoint naming

Logical grouping

Strong descriptions

10. Observability & Metrics
Health

/healthz for readiness checks

Metrics

/metrics exposes Prometheus counters

Tracks request volume

Demonstrates production awareness

11. Error Handling & Failure Scenarios
LLM Failure

Timeouts → safe error message

JSON parsing failure → retry or fallback

Vector DB Empty

Returns “Not found in provided documents”

Partial Ingest

Each document independently processed

One failure doesn’t block others

12. Security Considerations
API Keys

Stored only in environment variables

Never logged

Never committed

Prompt Injection

RAG prompt restricts answers to context

System instructions override user input

PII Handling

No sensitive data stored long-term

Logs avoid raw contract content

Data Privacy

Documents are not used for training

Local-only processing

13. Testing Strategy

Unit test for /healthz

Manual integration tests via Swagger

Demonstrated in Loom

Future Improvements

Mock LLM for deterministic tests

Vector retrieval accuracy benchmarks

14. Scalability Considerations
What would break first?

Single-node vector store

LLM API rate limits

How to scale

External vector DB (Pinecone)

Async task queue (Celery / SQS)

Background ingestion workers

Caching embeddings

15. If I Had One More Hour

Add async background jobs

Add user authentication

Improve citation granularity (page + char range)

Add rule-engine fallback toggle

16. Decisions I’m Proud Of

RAG instead of fine-tuning

Prompt discipline via /prompts folder

Streaming UX

Clean separation of concerns

17. Decisions I’d Revisit

Local filesystem → object storage

In-memory Chroma → managed vector DB

18. Conclusion

This system is designed with production realism in mind:

Clear architecture

Explainable AI

Strong UX

Safe defaults

Scalable foundations

It balances engineering discipline with practical GenAI usage, noting both strengths and limitations — exactly how real AI systems are built.