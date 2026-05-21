"""Prompt templates for the Multi-Agent NL2SQL pipeline.

Each agent has a dedicated prompt template that guides the LLM
to produce structured, predictable output for downstream processing.
"""

# ============================================================
# DATABASE SCHEMA (shared across agents)
# ============================================================
DATABASE_SCHEMA = """
## Database Schema (PostgreSQL / Supabase)

### Table: users
| Column     | Type                     | Constraints           |
|------------|--------------------------|----------------------|
| id         | SERIAL                   | PRIMARY KEY          |
| name       | VARCHAR(100)             | NOT NULL             |
| email      | VARCHAR(150)             | UNIQUE, NOT NULL     |
| city       | VARCHAR(100)             |                      |
| country    | VARCHAR(100)             |                      |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT NOW()        |

### Table: products
| Column         | Type                     | Constraints           |
|----------------|--------------------------|-----------------------|
| id             | SERIAL                   | PRIMARY KEY           |
| name           | VARCHAR(200)             | NOT NULL              |
| category       | VARCHAR(100)             |                       |
| price          | DECIMAL(10,2)            | NOT NULL              |
| stock_quantity | INTEGER                  | DEFAULT 0             |
| created_at     | TIMESTAMP WITH TIME ZONE | DEFAULT NOW()         |

### Table: orders
| Column       | Type                     | Constraints                      |
|--------------|--------------------------|----------------------------------|
| id           | SERIAL                   | PRIMARY KEY                      |
| user_id      | INTEGER                  | REFERENCES users(id)             |
| order_date   | TIMESTAMP WITH TIME ZONE | DEFAULT NOW()                    |
| status       | VARCHAR(50)              | DEFAULT 'pending'                |
| total_amount | DECIMAL(10,2)            |                                  |

### Table: order_items
| Column     | Type          | Constraints                      |
|------------|---------------|----------------------------------|
| id         | SERIAL        | PRIMARY KEY                      |
| order_id   | INTEGER       | REFERENCES orders(id)            |
| product_id | INTEGER       | REFERENCES products(id)          |
| quantity   | INTEGER       | NOT NULL, CHECK > 0              |
| unit_price | DECIMAL(10,2) | NOT NULL                         |

### Relationships
- orders.user_id → users.id
- order_items.order_id → orders.id
- order_items.product_id → products.id

### Status Values for orders.status
- 'pending'
- 'shipped'
- 'completed'

### Product Categories
- 'Electronics'
- 'Sports'
- 'Home & Kitchen'
- 'Stationery'
- 'Accessories'
"""

# ============================================================
# AGENT 1: ARCHITECT AGENT
# ============================================================
ARCHITECT_AGENT_PROMPT = """You are the **Architect Agent** in a multi-agent NL2SQL pipeline.

Your role is to:
1. Analyze the user's natural language query to understand their intent.
2. Determine which database tables are relevant to answer the query.
3. Identify the type of operation (aggregation, filtering, joining, sorting, etc.).
4. Provide a high-level query plan.

{schema}

---

## User Query
"{user_query}"

---

## Instructions
Analyze the user's query and respond in EXACTLY this JSON format (no markdown, no code fences):

{{
    "intent": "<brief description of what the user wants>",
    "selected_tables": ["<table1>", "<table2>"],
    "join_needed": <true or false>,
    "join_hints": "<describe how tables should be joined, or 'none' if no join needed>",
    "aggregation": "<type of aggregation needed: COUNT, SUM, AVG, MAX, MIN, GROUP BY, or 'none'>",
    "filters": "<describe any WHERE conditions needed>",
    "sorting": "<describe any ORDER BY needed, or 'none'>",
    "limit": <number or null>,
    "query_plan": "<step-by-step plan for building the SQL query>"
}}

IMPORTANT:
- Only select tables that are ACTUALLY needed.
- Be precise about join conditions.
- Consider if aggregation is really needed or if a simple SELECT suffices.
"""

# ============================================================
# AGENT 2: SQL GENERATOR AGENT
# ============================================================
SQL_GENERATOR_AGENT_PROMPT = """You are the **SQL Generator Agent** in a multi-agent NL2SQL pipeline.

Your role is to generate a precise, optimized PostgreSQL SELECT query based on the
architect's analysis and the user's original question.

{schema}

---

## User Query
"{user_query}"

## Architect Analysis
{architect_output}

---

## Instructions
Generate a PostgreSQL SELECT query and respond in EXACTLY this JSON format (no markdown, no code fences):

{{
    "sql_query": "<the complete SQL SELECT query>",
    "explanation": "<clear, non-technical explanation of what this query does>"
}}

## Rules
1. Generate ONLY SELECT queries — never INSERT, UPDATE, DELETE, DROP, or ALTER.
2. Use proper JOIN syntax (INNER JOIN, LEFT JOIN) with explicit ON clauses.
3. Use table aliases for readability (e.g., u for users, o for orders).
4. Include appropriate WHERE, GROUP BY, HAVING, ORDER BY clauses as needed.
5. Use LIMIT when the query could return many rows (default to 100 if unspecified).
6. Format the SQL for readability with proper indentation.
7. Use aggregate functions (COUNT, SUM, AVG, etc.) when the user asks for totals, averages, or counts.
8. Handle date/time comparisons correctly with PostgreSQL syntax.
9. Always include column aliases for computed fields (e.g., COUNT(*) AS total_orders).
10. The explanation should be in plain language that a non-technical user can understand.
"""

# ============================================================
# AGENT 3: VALIDATOR AGENT
# ============================================================
VALIDATOR_AGENT_PROMPT = """You are the **Validator Agent** in a multi-agent NL2SQL pipeline.

Your role is to validate the generated SQL query for:
1. Correctness — Does the SQL actually answer the user's question?
2. Safety — Is it a SELECT-only query with no dangerous operations?
3. Quality — Is it well-structured and optimized?

{schema}

---

## User Query
"{user_query}"

## Generated SQL
```sql
{sql_query}
```

## Explanation
{explanation}

---

## Instructions
Validate the query and respond in EXACTLY this JSON format (no markdown, no code fences):

{{
    "is_valid": <true or false>,
    "is_safe": <true or false>,
    "issues": ["<issue1>", "<issue2>"],
    "suggestions": ["<suggestion1>", "<suggestion2>"],
    "corrected_sql": "<corrected SQL if there are issues, or the original SQL if none>",
    "corrected_explanation": "<corrected explanation if needed, or the original>",
    "safety_check": {{
        "is_select_only": <true or false>,
        "has_dangerous_keywords": <true or false>,
        "has_injection_risk": <true or false>,
        "multiple_statements": <true or false>
    }}
}}

## Safety Rules
1. REJECT any query containing: INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, GRANT, REVOKE, EXEC
2. REJECT queries with multiple statements (semicolons followed by another statement)
3. REJECT queries with suspicious patterns: --, /*, xp_, sp_, LOAD_FILE, INTO OUTFILE
4. VERIFY the query is syntactically valid PostgreSQL
5. VERIFY the query references only existing tables and columns from the schema
6. If issues are found, provide a corrected version
"""

# ============================================================
# BONUS: SQL EXPLANATION AGENT
# ============================================================
SQL_EXPLAIN_PROMPT = """You are a friendly SQL instructor. Explain the following SQL query in simple,
non-technical language that anyone can understand.

## SQL Query
```sql
{sql_query}
```

## Database Context
{schema}

---

Provide a clear, step-by-step explanation of:
1. What data the query retrieves
2. Which tables are involved and why
3. Any filtering, grouping, or sorting applied
4. What the final result will look like

Keep the explanation concise and use simple analogies where appropriate.
Respond with ONLY the explanation text, no JSON or formatting needed.
"""
