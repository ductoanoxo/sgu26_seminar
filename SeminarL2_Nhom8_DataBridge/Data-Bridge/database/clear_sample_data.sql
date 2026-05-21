-- ============================================
-- NL2SQL - Clear Sample Database Data
-- Description: Drops the mock tables used for testing NL2SQL
-- ============================================

-- Drop tables in the correct order to handle foreign key constraints
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Note: This script does NOT touch the 'auth' schema or any Supabase internal tables.
