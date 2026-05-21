-- ============================================
-- NL2SQL - Connection Management Schema
-- Description: Tables for dynamic database connections and user access control
-- ============================================

-- Create schema if not exists
CREATE SCHEMA IF NOT EXISTS app_private;

-- Bảng lưu connection configurations
CREATE TABLE IF NOT EXISTS app_private.connections (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id      uuid NOT NULL,                    -- ID từ auth.users
  name          text NOT NULL,
  db_type       text NOT NULL DEFAULT 'postgresql',
  host          text NOT NULL,
  port          integer NOT NULL DEFAULT 5432,
  database_name text NOT NULL,
  username      text NOT NULL,
  password_enc  text NOT NULL,                    -- Mã hóa Fernet
  ssl_enabled   boolean NOT NULL DEFAULT true,
  is_active     boolean NOT NULL DEFAULT true,
  schema_cache  jsonb DEFAULT '[]'::jsonb,
  settings      jsonb DEFAULT '{"timeout_ms": 30000, "max_rows": 500}'::jsonb,
  created_at    timestamptz NOT NULL DEFAULT now(),
  updated_at    timestamptz NOT NULL DEFAULT now()
);

-- Bảng phân quyền user
CREATE TABLE IF NOT EXISTS app_private.connection_members (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  connection_id uuid NOT NULL REFERENCES app_private.connections(id) ON DELETE CASCADE,
  user_id       uuid NOT NULL,                    -- ID người được share
  role          text NOT NULL DEFAULT 'viewer',   -- 'admin' | 'viewer'
  granted_by    uuid NOT NULL,
  created_at    timestamptz NOT NULL DEFAULT now(),
  UNIQUE (connection_id, user_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_connections_owner ON app_private.connections(owner_id);
CREATE INDEX IF NOT EXISTS idx_conn_members_user ON app_private.connection_members(user_id);
CREATE INDEX IF NOT EXISTS idx_conn_members_conn ON app_private.connection_members(connection_id);
