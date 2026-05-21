# Agent Instructions

## References

- Start with [CLAUDE.md](CLAUDE.md) for commands, architecture, request flow, and env setup.
- For high-level product context, see [README.md](README.md) (Vietnamese).
- For frontend work, read [frontend/AGENTS.md](frontend/AGENTS.md) before coding — Next.js 16 has breaking changes.

## Commands (quick reference)

```bash
docker compose up --build     # start all 4 services with hot-reload
docker compose down           # stop all
cd frontend && npm run dev    # frontend only (port 3000, needs api-gateway on 8000)
cd frontend && npm run lint   # ESLint (no Python lint/typecheck exists)

# Run a single backend service without Docker:
cd services/<service> && uvicorn main:app --reload --host 0.0.0.0 --port <port>

# Tests — must run from within the service directory:
cd services/query-service && pytest
cd services/nl2sql-service && pytest
cd services/api-gateway && pytest

# Seed database (paths inside run_seed.py are hardcoded — fix before running):
python database/run_seed.py
```

## Ports and URLs

| Service | Host port | Docker internal listener | Health check |
|---|---|---|---|
| api-gateway | 8000 | 8000 | `GET /` |
| query-service | 8001 | 8000 | `GET /health` |
| nl2sql-service | 8002 | 8000 | `GET /health` |
| frontend | 3000 | 3000 | `GET /` |

**Critical**: Inside Docker, services reach each other via container names (`http://nl2sql-service:8000`). Outside Docker, use `localhost` with the host port. The api-gateway's docker-compose env overrides use the container-name URLs.

## Architecture (hard to infer from file structure)

Schema lives in two places — keep them synchronized:
1. **`database/seed.sql`** — the actual DDL + seed data (DROP TABLE IF EXISTS, then CREATE TABLE, then INSERT).
2. **`services/nl2sql-service/core/prompts.py`** → `DATABASE_SCHEMA` — the embedded schema the LLM agents read. Must be manually updated when seed.sql changes.

**There is no migration system.** Schema changes require updating both files and re-seeding.

**No Python type-checker or linter is configured.** Only ESLint exists for the frontend. If you add Python linting/typing tooling, add the commands here.

## Request flow

```
Frontend (3000) → POST /ask → API Gateway (8000)
  → POST /generate-sql → NL2SQL Service (8002)
    Agent 1: Architect (tables, joins, grouping)
    Agent 2: SQL Generator (PostgreSQL SELECT)
    Agent 3: Validator (safety/correctness check)
  → POST /execute → Query Service (8001)
    security.py validation → psycopg2 → Supabase PostgreSQL
  → Gateway logs to query_history.json → returns combined result to frontend
```

## SQL safety

Validation is layered — **do not weaken either layer:**
1. **Validator Agent** (LLM) in `services/nl2sql-service/services/agents/validator_agent.py`
2. **`services/query-service/core/security.py`** — SELECT-only enforcement, forbidden keywords (INSERT/UPDATE/DELETE/DROP/ALTER/TRUNCATE/EXEC), dangerous patterns (semicolons, `--`, `/*`, `xp_`, `LOAD_FILE`, `INTO OUTFILE`)

Modifying one without the other creates a gap.

## Gotchas

- **`database/run_seed.py`** contains hardcoded absolute paths (`/home/traductoan/Seminar_Final/...`). Fix them before running on any other machine.
- **`services/nl2sql-service/.env.example`** contains a real OpenRouter API key. Never commit real keys; this one is already exposed.
- **No `.env.example` for frontend** — only `.env` exists. Required var: `NEXT_PUBLIC_API_URL=http://localhost:8000`.
- **History is file-based**, not a database. Stored as `query_history.json` in the api-gateway container. Path set via `HISTORY_FILE` env var.
- **LLM agents are lazily initialized** on first request, not at startup. LLM temperature is 0.1 for all agents.
- **LLM JSON parsing** strips markdown fences and retries on parse failures (see `core/llm_client.py`). Agents re-prompt the LLM if JSON is invalid.
- **Tests use `sys.path.insert`** to import modules from parent dir. Run pytest from the service root, not the repo root.
- **Docker uses Aliyun PyPI mirrors** for Python packages and **npmmirror** for npm. May cause issues outside Asia.
