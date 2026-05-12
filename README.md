# QueryBridge AI

A full-stack AI-powered developer tool that translates natural language prompts into optimized MySQL queries and MongoDB aggregation pipelines.

## Tech Stack
- **Frontend**: React (Vite), Vanilla CSS, Monaco Editor
- **Backend**: FastAPI, MySQL, MongoDB, Groq API (llama3-70b-8192)

## Setup

1. Configure `.env` in the backend directory.
2. Run backend: `cd backend && .\venv\Scripts\activate && uvicorn app.main:app --reload`
3. Run frontend: `cd frontend && npm run dev`
