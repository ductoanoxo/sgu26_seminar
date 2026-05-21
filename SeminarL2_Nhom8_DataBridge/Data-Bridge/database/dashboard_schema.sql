CREATE SCHEMA IF NOT EXISTS app_private;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS app_private.dashboards (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id text NOT NULL DEFAULT 'public',
  name text NOT NULL,
  description text,
  widgets jsonb NOT NULL DEFAULT '[]'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS dashboards_owner_id_idx
  ON app_private.dashboards (owner_id);

CREATE INDEX IF NOT EXISTS dashboards_updated_at_idx
  ON app_private.dashboards (updated_at DESC);

CREATE OR REPLACE FUNCTION app_private.set_updated_at()
RETURNS trigger AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS dashboards_set_updated_at ON app_private.dashboards;
CREATE TRIGGER dashboards_set_updated_at
BEFORE UPDATE ON app_private.dashboards
FOR EACH ROW EXECUTE PROCEDURE app_private.set_updated_at();
