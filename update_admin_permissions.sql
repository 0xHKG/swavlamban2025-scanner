-- ============================================================================
-- UPDATE ADMIN USER PERMISSIONS
-- Fix allowed_passes to use interactive_sessions instead of panel1/panel2
-- ============================================================================

-- Update all users who had panel1 or panel2 permissions
-- Set interactive_sessions to true if either was true

UPDATE public.users
SET allowed_passes = jsonb_set(
    jsonb_set(
        allowed_passes::jsonb,
        '{interactive_sessions}',
        'true'::jsonb
    ),
    '{panel1_emerging_tech}',
    'null'::jsonb
)::json
WHERE allowed_passes::jsonb ? 'panel1_emerging_tech'
   OR allowed_passes::jsonb ? 'panel2_idex';

-- Remove the old panel keys
UPDATE public.users
SET allowed_passes = (allowed_passes::jsonb - 'panel1_emerging_tech' - 'panel2_idex')::json
WHERE allowed_passes::jsonb ? 'panel1_emerging_tech'
   OR allowed_passes::jsonb ? 'panel2_idex';

-- Verify the update
SELECT
    username,
    organization,
    role,
    allowed_passes
FROM public.users
ORDER BY username;
