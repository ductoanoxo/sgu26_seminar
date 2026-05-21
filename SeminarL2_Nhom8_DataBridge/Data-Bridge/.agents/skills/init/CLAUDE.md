# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agent_SQL is a Multi-Agent NL2SQL system that converts natural language questions into SQL queries and executes them against a Supabase PostgreSQL database. Four services run together via Docker Compose.

## Commands

### Start all services (development with hot-reload)
```bash
docker compose up --build
```

### Stop all services
```bash
docker compose down
```

### Frontend (Next.js — Port 3000)
```bash
cd frontend
npm run dev        # dev server
npm run build      # production build
npm run lint       # ESLint
```

### Backend services (run individually without Docker)
```bash
cd services/api-gateway && uvicorn main:app --reload --host 0.0.0.0 --port 8000
cd services/nl2sql-service && uvicorn main:app --reload --host 0.0.0.0 --port 8002
cd services/query-service && uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Run tests
```bash
cd services/<service-name> && pytest
```

### Seed the database
```bash
python database/run_seed.py
```

## Architecture

### Request Flow
```
Frontend (3000) → API Gateway (8000) → NL2SQL Service (8002) [AI pipeline]
                                     → Query Service (8001) → Supabase PostgreSQL
```

### Services

**`services/api-gateway/`** — FastAPI orchestrator. Receives `/ask` requests, calls NL2SQL then Query services in sequence, manages query history in a JSON file, and returns combined results to the frontend.

**`services/nl2sql-service/`** — Three-agent AI pipeline:
1. **Architect Agent** — Analyzes intent, selects tables, plans JOIN/GROUP BY/ORDER strategy
2. **SQL Generator Agent** — Generates PostgreSQL SELECT from the architect's plan
3. **Validator Agent** — Checks validity, safety, and injects corrections if needed

All agents use temperature 0.1 for deterministic output. The LLM provider is pluggable via `LLM_PROVIDER` env variable: `gemini`, `openai`, or `openrouter` (see `core/llm_client.py`).

**`services/query-service/`** — Executes SQL against Supabase. Enforces SELECT-only at the code level (`core/security.py`) before hitting the database — blocks INSERT/UPDATE/DELETE/DROP and dangerous patterns like `--`, `/*`, `xp_`, `LOAD_FILE`, `INTO OUTFILE`.

**`frontend/`** — Next.js 16 App Router dashboard. Components: `HeroSearchInput`, `DataTable`, `ChartVisualization` (Recharts), `SqlPreview`, `AgentPipeline`, `Explanation`. API calls go through `src/lib/api.ts`.

### Database Schema (4 tables)
```
users (id, name, email, city, country, created_at)
products (id, name, category, price, stock_quantity, created_at)
orders (id, user_id→users, order_date, status, total_amount)
order_items (id, order_id→orders, product_id→products, quantity, unit_price)
```

Schema is embedded in `services/nl2sql-service/core/prompts.py` as `DATABASE_SCHEMA` — update it there if the schema changes.

## Environment Setup

Each service has a `.env.example`. Create `.env` files from them:

- `services/nl2sql-service/.env` — `LLM_PROVIDER`, API keys (`GEMINI_API_KEY`, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`)
- `services/query-service/.env` — `SUPABASE_DB_*` connection parameters
- `services/api-gateway/.env` — downstream service URLs, history file path

## Key Patterns

- **LLM JSON parsing**: The LLM client strips markdown fences and retries on parse failures. Agent outputs are Pydantic models — if the LLM returns invalid JSON, the agent catches and re-prompts.
- **Agent initialization**: LLM clients and agents are lazily initialized on first request, not at startup.
- **Security is layered**: The Validator Agent (LLM) checks SQL safety, and `query-service/core/security.py` re-validates before execution. Both must pass.
- **History**: Query history is stored as a JSON file on the API gateway container (path set via env). Not a database.
