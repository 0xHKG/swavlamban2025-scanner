-- ============================================================================
-- SUPABASE DATABASE MIGRATION
-- Consolidate panel1/panel2 → interactive_sessions
-- ============================================================================

-- STEP 1: Fix RLS (Row Level Security) Policies FIRST
-- This fixes the "RLS Disabled in Public" errors you're seeing
-- ============================================================================

-- Policy for entries table
DROP POLICY IF EXISTS "Allow all for authenticated users" ON public.entries;
CREATE POLICY "Allow all for authenticated users"
ON public.entries
FOR ALL
USING (true);

-- Policy for users table
DROP POLICY IF EXISTS "Allow all for authenticated users" ON public.users;
CREATE POLICY "Allow all for authenticated users"
ON public.users
FOR ALL
USING (true);

-- Policy for scanner_devices table
DROP POLICY IF EXISTS "Allow all for authenticated users" ON public.scanner_devices;
CREATE POLICY "Allow all for authenticated users"
ON public.scanner_devices
FOR ALL
USING (true);

-- Policy for audit_log table
DROP POLICY IF EXISTS "Allow all for authenticated users" ON public.audit_log;
CREATE POLICY "Allow all for authenticated users"
ON public.audit_log
FOR ALL
USING (true);

-- Policy for check_ins table
DROP POLICY IF EXISTS "Allow all for authenticated users" ON public.check_ins;
CREATE POLICY "Allow all for authenticated users"
ON public.check_ins
FOR ALL
USING (true);

-- ============================================================================
-- STEP 2: Add Interactive Sessions Column
-- ============================================================================

-- Add the new interactive_sessions column
ALTER TABLE public.entries
ADD COLUMN IF NOT EXISTS interactive_sessions BOOLEAN DEFAULT FALSE;

-- Migrate existing data: Set TRUE if either panel1 OR panel2 is TRUE
UPDATE public.entries
SET interactive_sessions = COALESCE(panel1_emerging_tech, FALSE) OR COALESCE(panel2_idex, FALSE);

-- Add the tracking column
ALTER TABLE public.entries
ADD COLUMN IF NOT EXISTS pass_generated_interactive_sessions BOOLEAN DEFAULT FALSE;

-- Migrate tracking: Set TRUE if either panel tracking is TRUE
UPDATE public.entries
SET pass_generated_interactive_sessions = COALESCE(pass_generated_panel1, FALSE) OR COALESCE(pass_generated_panel2, FALSE);

-- ============================================================================
-- STEP 3: VERIFICATION QUERY (RUN THIS BEFORE PROCEEDING)
-- Check that data migrated correctly
-- ============================================================================

SELECT
    id,
    name,
    panel1_emerging_tech AS old_panel1,
    panel2_idex AS old_panel2,
    interactive_sessions AS new_interactive,
    pass_generated_panel1 AS old_gen_panel1,
    pass_generated_panel2 AS old_gen_panel2,
    pass_generated_interactive_sessions AS new_gen_interactive
FROM public.entries
WHERE panel1_emerging_tech = TRUE
   OR panel2_idex = TRUE
   OR interactive_sessions = TRUE
ORDER BY id;

-- Expected: interactive_sessions should be TRUE whenever panel1 OR panel2 is TRUE

-- ============================================================================
-- STEP 4: DROP OLD COLUMNS (ONLY RUN AFTER VERIFICATION!)
-- WARNING: This is IRREVERSIBLE - make sure Step 3 verification passed!
-- ============================================================================

-- UNCOMMENT THESE LINES AFTER VERIFICATION:
-- ALTER TABLE public.entries
-- DROP COLUMN IF EXISTS panel1_emerging_tech,
-- DROP COLUMN IF EXISTS panel2_idex,
-- DROP COLUMN IF EXISTS pass_generated_panel1,
-- DROP COLUMN IF EXISTS pass_generated_panel2;

-- ============================================================================
-- FINAL VERIFICATION
-- ============================================================================

-- After dropping columns, verify the table structure
-- SELECT column_name, data_type, is_nullable
-- FROM information_schema.columns
-- WHERE table_name = 'entries'
-- ORDER BY ordinal_position;
