# TDS Virtual TA

This repository contains the backend API for a Virtual Teaching Assistant designed for IIT Madras' Online Degree in Data Science, specifically for the "Tools in Data Science" (TDS) course. This API aims to automatically answer student questions based on course content and Discourse forum posts, providing quick and accurate responses along with relevant sources.

## Project Overview

The Virtual TA is built as a Retrieval-Augmented Generation (RAG) system. It leverages a knowledge base constructed from:
* Course content for TDS Jan 2025 (as of April 15, 2025).
* TDS Discourse posts from January 1, 2025, to April 14, 2025.

The system processes student questions, retrieves the most relevant information from its knowledge base, and then uses a Large Language Model (LLM) to generate a concise answer, citing the sources used. It also supports multimodal queries, allowing students to ask questions with accompanying images.

## Features

* **Intelligent Q&A:** Provides comprehensive answers to student queries based on a curated knowledge base.
* **Source Citation:** All answers are accompanied by URLs and relevant text snippets from the original sources (Discourse posts and documentation).
* **Multimodal Support:** Accepts questions with optional base64 encoded images, allowing for visual context in queries.
* **Scalable API:** Built with FastAPI, designed for easy deployment and robust performance.
* **Knowledge Base:** Utilizes an SQLite database (`knowledge_base.db`) to store text chunks and their embeddings.

## API Endpoint

The application exposes a single POST endpoint for queries:

**`https://tds-virtual-ta-delta-three.vercel.app/query`**

This endpoint is publicly hosted and accepts JSON requests for question answering.

> ⚠️ Note: If you're running the API locally (e.g. for development), replace the URL with `http://127.0.0.1:8000/query`.

---

### Request Format (POST)

The endpoint accepts a JSON payload:

```json
{
  "question": "string",
  "image": "string (base64-encoded, optional)"
}
