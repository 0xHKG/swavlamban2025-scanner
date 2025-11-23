-- ================================================================
-- Database Migration: Add Separate Quotas for Each Pass Type
-- ================================================================
--
-- This migration adds individual quota columns for each pass type
-- to allow organizations to have different quotas per pass type.
--
-- Example: Organization A can have:
--   - 5 Exhibition Day 1 passes
--   - 1 Exhibition Day 2 pass
--   - 13 Interactive Sessions passes
--   - 15 Plenary Session passes
--
-- Run this in Supabase SQL Editor if you prefer manual migration
-- ================================================================

-- Step 1: Add new quota columns
ALTER TABLE users
ADD COLUMN IF NOT EXISTS quota_ex_day1 INTEGER DEFAULT 0 NOT NULL;

ALTER TABLE users
ADD COLUMN IF NOT EXISTS quota_ex_day2 INTEGER DEFAULT 0 NOT NULL;

ALTER TABLE users
ADD COLUMN IF NOT EXISTS quota_interactive INTEGER DEFAULT 0 NOT NULL;

ALTER TABLE users
ADD COLUMN IF NOT EXISTS quota_plenary INTEGER DEFAULT 0 NOT NULL;

-- Step 2: Initialize existing users with 0 for all new quotas
UPDATE users
SET quota_ex_day1 = 0,
    quota_ex_day2 = 0,
    quota_interactive = 0,
    quota_plenary = 0
WHERE quota_ex_day1 IS NULL
   OR quota_ex_day2 IS NULL
   OR quota_interactive IS NULL
   OR quota_plenary IS NULL;

-- Step 3: Verify the migration
SELECT username, organization, max_entries, quota_ex_day1, quota_ex_day2, quota_interactive, quota_plenary
FROM users
LIMIT 10;

-- ================================================================
-- NEXT STEPS:
-- ================================================================
-- 1. Restart your Streamlit app
-- 2. Go to Admin Panel → User Management
-- 3. Edit each organization to set their pass quotas
-- 4. Users will now be checked against separate quotas when adding entries
-- ================================================================
