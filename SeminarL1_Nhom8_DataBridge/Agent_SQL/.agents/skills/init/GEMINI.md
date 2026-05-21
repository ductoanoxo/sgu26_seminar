# 🤖 Agent SQL: Multi-Agent NL2SQL System - Gemini Context

This document provides essential context and instructions for the Agent SQL project, a Multi-Agent system designed to convert natural language into SQL queries and execute them on Supabase (PostgreSQL).

## 🏗️ Project Overview & Architecture

Agent SQL is built using a modern microservices architecture, orchestrated with Docker Compose. It leverages LLMs (Gemini/OpenRouter) through a multi-agent pipeline to ensure accurate and safe SQL generation.

### Core Services
1.  **🚀 API Gateway (Port 8000)**: `services/api-gateway`. Orchestrates data flow between the frontend and backend services. Manages query history in `query_history.json`.
2.  **🧠 NL2SQL Service (Port 8002)**: `services/nl2sql-service`. Implements the Multi-Agent Pipeline:
    *   **Architect Agent**: Analyzes intent and selects tables.
    *   **SQL Generator Agent**: Generates SQL based on the architecture plan.
    *   **Validator Agent**: Checks SQL for correctness and safety.
3.  **🗄️ Query Service (Port 8001)**: `services/query-service`. Connects to Supabase PostgreSQL using `psycopg2` and executes validated SQL queries.
4.  **🌐 Frontend (Port 3000)**: `frontend`. A Next.js (React 19) application providing a dashboard for user interaction, SQL preview, and data visualization (using `recharts`).

### Tech Stack
*   **Backend**: Python (FastAPI, Pydantic, Psycopg2).
*   **Frontend**: Next.js, TypeScript, TailwindCSS, Recharts.
*   **AI**: Google Gemini SDK (`google-generativeai`), OpenRouter/OpenAI SDK.
*   **Database**: Supabase PostgreSQL.
*   **Infrastructure**: Docker, Docker Compose.

---

## 🛠️ Building and Running

### Prerequisites
*   Docker and Docker Compose installed.
*   `.env` files configured for each service (see `.env.example` in each service directory).

### Key Commands

| Action | Command |
| :--- | :--- |
| **Start Everything** | `docker compose up --build` |
| **Stop System** | `docker compose down` |
| **View Logs** | `docker compose logs -f` |
| **Seed Database** | `python database/run_seed.py` |
| **Run Backend Tests**| `pytest` (inside respective service directories) |
| **Run Frontend Lint**| `npm run lint` (inside `frontend` directory) |

### Environment Setup
Each service requires specific environment variables:
*   `services/nl2sql-service/.env`: `GOOGLE_API_KEY` or `OPENROUTER_API_KEY`, `LLM_PROVIDER`.
*   `services/query-service/.env`: `DATABASE_URL` (Supabase connection string).
*   `services/api-gateway/.env`: Service URLs (usually configured via Docker).

---

## 📂 Directory Structure

*   `frontend/`: Next.js source code, components, and types.
*   `services/`:
    *   `api-gateway/`: FastAPI orchestrator and history management.
    *   `nl2sql-service/`: Multi-agent logic, prompts, and LLM clients.
    *   `query-service/`: Database connection and execution logic.
*   `database/`: SQL seed scripts.
*   `.agents/`: Local agent-specific configurations or skills.

---

## 💡 Development Conventions

*   **Microservices Communication**: Services communicate via HTTP/REST. API Gateway is the entry point for the frontend.
*   **Pydantic Models**: Used across all backend services for data validation and serialization (see `domain/models.py` and `schemas/`).
*   **Multi-Agent Flow**: Any changes to the SQL generation logic should be verified in `services/nl2sql-service/services/agents/`.
*   **Database Safety**: The `Query Service` sets sessions to `readonly=True` to prevent accidental mutations.
*   **Hot Reload**: Enabled in Docker via volume mounting for both Python (Uvicorn `--reload`) and Next.js.

---

## 📝 TODOs & Future Improvements
*   [ ] Implement more robust error handling for LLM timeouts.
*   [ ] Add integration tests covering the full pipeline from Gateway to Query Service.
*   [ ] Enhance schema detection in the NL2SQL service to handle more complex database structures.
