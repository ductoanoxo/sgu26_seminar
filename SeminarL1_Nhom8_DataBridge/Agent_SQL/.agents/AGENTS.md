# Project Global Agent Rules

These rules apply to all components and agents working on the Agent_SQL project.

- **Unified Tech Stack:** Use FastAPI for backend services and Next.js (App Router) for frontend. Use Supabase for database and authentication.
- **Testing Standard:** Every major logic change or bug fix MUST include corresponding unit or integration tests. Reference `docs/project_infras.md` for test locations.
- **Data Privacy:** Never hardcode secrets. Never log user-sensitive data (PII) or full database connection strings.
- **Consistency:** Maintain the distinction between NL2SQL (AI generation) and Query (execution) services. Do not merge their responsibilities.
- **Error Handling:** Use centralized error mapping to provide user-friendly messages while keeping technical logs detailed for developers.
- **Documentation:** Update `docs/` and local `AGENTS.md` files when architectural patterns or security protocols change.
