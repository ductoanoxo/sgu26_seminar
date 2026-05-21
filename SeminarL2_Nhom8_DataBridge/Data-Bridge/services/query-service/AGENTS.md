# Query Service Agent Rules

This service executes SQL against Supabase. Security first.

- Never execute SQL without validate_sql; keep validation strict.
- Only allow SELECT or WITH CTE queries; no DDL or DML, no multi-statements.
- **Resource Limits:** Enforce query timeouts (max 30s) and result set limits (max 1000 rows) at the code or DB level.
- **Security Boundaries:** Use a restricted DB role with no access to system tables or cross-database schemas.
- Preserve the readonly database session; do not enable write transactions.
- Maintain forbidden keywords and patterns; extend them if new risks are discovered.
- Keep error messages safe; do not leak credentials or full stack traces in API responses.
- If you change validation or execution logic, update tests in services/query-service/tests.
