# Resumizer

AI-powered resume analyzer that compares your resume against job descriptions to provide ATS scores and actionable feedback.

## Features

- **ATS Scoring**: Detailed breakdown of skills, experience, education, and quality.
- **AI Analysis**: Uses LangGraph and Groq (Llama 3) for intelligent parsing and feedback.
- **RAG Architecture**: Uses Pinecone for vector search to find relevant experience contexts.
- **Modern UI**: Clean, responsive React interface.

## Tech Stack

- **Frontend**: React, Vite
- **Backend**: FastAPI, LangGraph, LangChain
- **AI/ML**: Groq (LLM), Pinecone (Vector DB), Sentence Transformers (Embeddings)

## Local Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- API Keys: Groq, Pinecone

### 1. Backend

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set up environment variables in `.env`:

```
GROQ_API_KEY=your_key
PINECONE_API_KEY=your_key
PINECONE_INDEX_NAME=resume-rag
```

Run the server:

```bash
python main.py
```

### 2. Frontend

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies and start the dev server:

```bash
npm install
npm run dev
```

The application will be available at `http://localhost:5173`.

## Deployment

This project is configured for deployment on Render as a single web service.
See [Deployment Guide](deploy-guide.md) for detailed instructions.
