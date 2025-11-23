-- ============================================================================
-- RECREATE ENTRIES TABLE WITH INTERACTIVE_SESSIONS
-- This will DELETE ALL existing data and create a clean table
-- ============================================================================

-- WARNING: This drops the entire entries table and ALL data!
-- Make sure you have a backup if needed

-- Drop the table (cascades to dependent tables)
DROP TABLE IF EXISTS public.entries CASCADE;

-- Create fresh entries table with correct structure
CREATE TABLE public.entries (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL REFERENCES public.users(username) ON DELETE CASCADE,

    -- Personal information
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    id_type VARCHAR(50) NOT NULL,
    id_number VARCHAR(100) NOT NULL UNIQUE,
    photo_url VARCHAR(500),

    -- Pass allocation (4 types - NO panel1/panel2)
    exhibition_day1 BOOLEAN DEFAULT FALSE,
    exhibition_day2 BOOLEAN DEFAULT FALSE,
    interactive_sessions BOOLEAN DEFAULT FALSE,
    plenary BOOLEAN DEFAULT FALSE,

    -- Pass generation tracking
    pass_generated_exhibition_day1 BOOLEAN DEFAULT FALSE,
    pass_generated_exhibition_day2 BOOLEAN DEFAULT FALSE,
    pass_generated_interactive_sessions BOOLEAN DEFAULT FALSE,
    pass_generated_plenary BOOLEAN DEFAULT FALSE,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_entries_username ON public.entries(username);
CREATE INDEX idx_entries_email ON public.entries(email);
CREATE INDEX idx_entries_id_number ON public.entries(id_number);

-- Enable RLS
ALTER TABLE public.entries ENABLE ROW LEVEL SECURITY;

-- Create RLS policy
CREATE POLICY "Allow all for authenticated users"
ON public.entries
FOR ALL
USING (true);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_entries_updated_at
    BEFORE UPDATE ON public.entries
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Success message
SELECT 'Table public.entries recreated successfully!' AS status;
