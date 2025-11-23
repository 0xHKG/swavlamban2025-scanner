-- Fix exhibitor entries: Remove exhibition_day1 and exhibition_day2 flags
-- This ensures exhibitors are ONLY identified by is_exhibitor_pass flag
-- Run this on production database to fix existing 103 exhibitor entries

-- Update all exhibitors to remove exhibition pass flags
UPDATE entries
SET
    exhibition_day1 = false,
    exhibition_day2 = false,
    updated_at = NOW()
WHERE
    is_exhibitor_pass = true
    AND interactive_sessions = false
    AND plenary = false;

-- Verification query: Count updated entries
SELECT
    COUNT(*) as updated_exhibitors,
    'Pure exhibitors with exhibition flags removed' as description
FROM entries
WHERE
    is_exhibitor_pass = true
    AND interactive_sessions = false
    AND plenary = false
    AND exhibition_day1 = false
    AND exhibition_day2 = false;

-- Show exhibitors with extra passes (should NOT be updated)
SELECT
    id,
    name,
    email,
    exhibition_day1,
    exhibition_day2,
    interactive_sessions,
    plenary,
    is_exhibitor_pass
FROM entries
WHERE
    is_exhibitor_pass = true
    AND (interactive_sessions = true OR plenary = true)
ORDER BY name;
