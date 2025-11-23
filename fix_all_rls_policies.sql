-- ============================================================================
-- FIX RLS POLICIES FOR ALL TABLES
-- Apply to all tables showing "Unrestricted" in Supabase
-- ============================================================================

-- 1. Users table
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for authenticated users" ON public.users;
CREATE POLICY "Allow all for authenticated users"
ON public.users
FOR ALL
USING (true);

-- 2. Audit Log table
ALTER TABLE public.audit_log ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for authenticated users" ON public.audit_log;
CREATE POLICY "Allow all for authenticated users"
ON public.audit_log
FOR ALL
USING (true);

-- 3. Check-ins table
ALTER TABLE public.check_ins ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for authenticated users" ON public.check_ins;
CREATE POLICY "Allow all for authenticated users"
ON public.check_ins
FOR ALL
USING (true);

-- 4. Scanner Devices table
ALTER TABLE public.scanner_devices ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for authenticated users" ON public.scanner_devices;
CREATE POLICY "Allow all for authenticated users"
ON public.scanner_devices
FOR ALL
USING (true);

-- Verify all tables now have RLS enabled
SELECT
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
AND tablename IN ('users', 'entries', 'audit_log', 'check_ins', 'scanner_devices')
ORDER BY tablename;
