-- Migration: Add is_exhibitor_pass field to entries table
-- Date: 2025-11-03
-- Purpose: Distinguish exhibitor passes from visitor passes

-- Add the new column with default value False
ALTER TABLE entries
ADD COLUMN is_exhibitor_pass BOOLEAN DEFAULT FALSE NOT NULL;

-- Optional: Set existing entries with both exhibition days to False
-- (They were created before the field existed, so they are visitors)
UPDATE entries
SET is_exhibitor_pass = FALSE
WHERE exhibition_day1 = TRUE AND exhibition_day2 = TRUE;

-- Verification query to check the migration
SELECT
    COUNT(*) as total_entries,
    SUM(CASE WHEN is_exhibitor_pass = TRUE THEN 1 ELSE 0 END) as exhibitors,
    SUM(CASE WHEN is_exhibitor_pass = FALSE THEN 1 ELSE 0 END) as visitors
FROM entries;
