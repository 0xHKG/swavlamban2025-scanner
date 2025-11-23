# Database Migration: Consolidate Panel1/Panel2 → Interactive Sessions

## Problem
Currently the database has separate columns for `panel1_emerging_tech` and `panel2_idex`, but there should be only ONE pass for both sessions called `interactive_sessions`.

## Solution - Database Migration Steps

### Step 1: Add New Column (in Supabase SQL Editor)

```sql
-- Add the new interactive_sessions column
ALTER TABLE public.entries
ADD COLUMN interactive_sessions BOOLEAN DEFAULT FALSE;

-- Migrate existing data: Set TRUE if either panel1 OR panel2 is TRUE
UPDATE public.entries
SET interactive_sessions = (panel1_emerging_tech OR panel2_idex);

-- Add the tracking column
ALTER TABLE public.entries
ADD COLUMN pass_generated_interactive_sessions BOOLEAN DEFAULT FALSE;

-- Migrate tracking: Set TRUE if either panel tracking is TRUE
UPDATE public.entries
SET pass_generated_interactive_sessions = (pass_generated_panel1 OR pass_generated_panel2);
```

### Step 2: Verify Migration (Check Before Dropping)

```sql
-- Verify the migration worked correctly
SELECT
    id,
    name,
    panel1_emerging_tech,
    panel2_idex,
    interactive_sessions,
    pass_generated_panel1,
    pass_generated_panel2,
    pass_generated_interactive_sessions
FROM public.entries
WHERE panel1_emerging_tech = TRUE OR panel2_idex = TRUE OR interactive_sessions = TRUE;
```

Expected result: `interactive_sessions` should be TRUE whenever panel1 OR panel2 is TRUE.

### Step 3: Drop Old Columns (AFTER VERIFYING)

```sql
-- Drop the old panel columns
ALTER TABLE public.entries
DROP COLUMN panel1_emerging_tech,
DROP COLUMN panel2_idex,
DROP COLUMN pass_generated_panel1,
DROP COLUMN pass_generated_panel2;
```

### Step 4: Update Python Model

Update `backend/app/models/entry.py`:

```python
# BEFORE (Lines 37-38, 44-45):
panel1_emerging_tech = Column(Boolean, default=False)
panel2_idex = Column(Boolean, default=False)
pass_generated_panel1 = Column(Boolean, default=False)
pass_generated_panel2 = Column(Boolean, default=False)

# AFTER (Single column):
interactive_sessions = Column(Boolean, default=False)  # EP-INTERACTIVE.png
pass_generated_interactive_sessions = Column(Boolean, default=False)
```

### Step 5: Update All Code References

Files to update:
- `backend/app/models/entry.py` - Model definition
- `backend/app/schemas/entry.py` - Schema definition
- `frontend/app.py` - All UI references to panel1/panel2
- `backend/app/services/pass_generator.py` - Pass generation logic

### Step 6: Fix RLS (Row Level Security) Policies

The Supabase errors show RLS is enabled but no policies exist. Add policies:

```sql
-- Enable RLS on entries table (already enabled based on error)
-- ALTER TABLE public.entries ENABLE ROW LEVEL SECURITY;

-- Policy: Allow all operations for now (can restrict later)
CREATE POLICY "Allow all for authenticated users"
ON public.entries
FOR ALL
USING (true);

-- Apply same to other tables showing RLS errors
CREATE POLICY "Allow all for authenticated users"
ON public.users
FOR ALL
USING (true);

CREATE POLICY "Allow all for authenticated users"
ON public.scanner_devices
FOR ALL
USING (true);

CREATE POLICY "Allow all for authenticated users"
ON public.audit_log
FOR ALL
USING (true);

CREATE POLICY "Allow all for authenticated users"
ON public.check_ins
FOR ALL
USING (true);
```

## Rollback Plan

If something goes wrong:

```sql
-- Restore old columns
ALTER TABLE public.entries
ADD COLUMN panel1_emerging_tech BOOLEAN DEFAULT FALSE,
ADD COLUMN panel2_idex BOOLEAN DEFAULT FALSE,
ADD COLUMN pass_generated_panel1 BOOLEAN DEFAULT FALSE,
ADD COLUMN pass_generated_panel2 BOOLEAN DEFAULT FALSE;

-- Restore data from interactive_sessions
UPDATE public.entries
SET panel1_emerging_tech = interactive_sessions;

-- Drop new column
ALTER TABLE public.entries
DROP COLUMN interactive_sessions,
DROP COLUMN pass_generated_interactive_sessions;
```

## Testing Checklist

After migration:
- [ ] Create new entry with interactive_sessions checked
- [ ] Generate pass - should create EP-INTERACTIVE.png
- [ ] Verify old entries with panel1/panel2 now show interactive_sessions
- [ ] Check email sending includes interactive sessions pass
- [ ] Verify statistics show correct count

---

**DO NOT proceed with Step 3 (dropping columns) until Step 2 verification is complete!**
