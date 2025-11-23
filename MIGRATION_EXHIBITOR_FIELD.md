# Database Migration: Add Exhibitor Field

## Problem

The Entry model needs a way to distinguish exhibitor passes from visitor passes. Previously, the system had no explicit field to mark exhibitor passes, which caused:

1. Incorrect pass generation (visitors with both days got exhibitor passes)
2. Wrong Entry Type classification
3. Incorrect email templates being sent
4. Wrong invitation attachments

## Solution - Database Migration Steps

### Step 1: Add New Column (in Supabase SQL Editor)

```sql
-- Add the new column with default value False
ALTER TABLE entries
ADD COLUMN IF NOT EXISTS is_exhibitor_pass BOOLEAN DEFAULT FALSE NOT NULL;

-- Set all existing entries to False (they are visitors)
UPDATE entries
SET is_exhibitor_pass = FALSE
WHERE is_exhibitor_pass IS NULL;
```

**What this does:**
- Adds `is_exhibitor_pass` column to entries table
- Sets default value to `FALSE` (visitor)
- Updates all existing entries to `FALSE` (all existing entries are visitors)

### Step 2: Verify Migration (Check Before Proceeding)

```sql
-- Verify the migration worked correctly
SELECT
    id,
    name,
    email,
    exhibition_day1,
    exhibition_day2,
    is_exhibitor_pass
FROM entries
WHERE exhibition_day1 = TRUE OR exhibition_day2 = TRUE
LIMIT 10;
```

**Expected result:**
- All existing entries should have `is_exhibitor_pass = FALSE`
- Column should exist in all rows

### Step 3: Update Python Model

Update `backend/app/models/entry.py`:

```python
# ADD after line 39 (after exhibition_day2):
# Exhibitor flag - for bulk uploaded exhibitors (gets combined pass EP-25n26.png)
is_exhibitor_pass = Column(Boolean, default=False)  # True = Exhibitor, False = Visitor
```

**What this does:**
- Adds the field to the SQLAlchemy model
- Sets default value to `False` for new entries
- Allows bulk upload to set `True` for exhibitors

### Step 4: Update is_exhibitor Property

Update `backend/app/models/entry.py` (around line 60):

```python
# BEFORE:
@property
def is_exhibitor(self) -> bool:
    """Check if this is an exhibitor pass (both exhibition days)"""
    return self.exhibition_day1 and self.exhibition_day2

# AFTER:
@property
def is_exhibitor(self) -> bool:
    """Check if this is an exhibitor pass (from bulk upload)"""
    return self.is_exhibitor_pass
```

**What this does:**
- Changes logic from checking both days to checking database field
- Prevents incorrect classification of visitors with both days
- Allows admin to create both visitor and exhibitor passes

### Step 5: Run Python Migration Script

**File:** `run_migration.py`

```python
from sqlalchemy import create_engine, text
from backend.app.database import DATABASE_URL

engine = create_engine(DATABASE_URL)

def run_migration():
    """Add is_exhibitor_pass column to entries table"""
    print("Starting database migration...")

    with engine.connect() as conn:
        try:
            # Add the new column
            conn.execute(text("""
                ALTER TABLE entries
                ADD COLUMN IF NOT EXISTS is_exhibitor_pass BOOLEAN DEFAULT FALSE NOT NULL;
            """))
            conn.commit()
            print("✅ Column added successfully")

            # Set all existing entries to False (they are visitors)
            result = conn.execute(text("""
                UPDATE entries
                SET is_exhibitor_pass = FALSE
                WHERE is_exhibitor_pass IS NULL OR is_exhibitor_pass = FALSE;
            """))
            conn.commit()
            print(f"✅ Updated {result.rowcount} existing entries")

            print("✅ Migration completed successfully!")
            return True

        except Exception as e:
            print(f"❌ Migration failed: {e}")
            conn.rollback()
            return False

if __name__ == "__main__":
    run_migration()
```

**Run the script:**
```bash
cd /path/to/swavlamban2025
python run_migration.py
```

**Expected output:**
```
Starting database migration...
✅ Column added successfully
✅ Updated 15 existing entries
✅ Migration completed successfully!
```

### Step 6: Update All Code References

**Files to update:**

#### 1. `backend/app/models/entry.py`
- ✅ Added `is_exhibitor_pass` field (Step 3)
- ✅ Updated `is_exhibitor` property (Step 4)

#### 2. `frontend/app.py`

**Bulk Upload - Set Exhibitor Flag (Lines ~2340):**
```python
new_entry = Entry(
    username=user['username'],
    name=attendee['name'],
    email=exhibitor['email'],
    phone=exhibitor['mobile'],
    id_type='Aadhar Card',
    id_number=attendee['aadhar'],
    exhibition_day1=True,
    exhibition_day2=True,
    interactive_sessions=False,
    plenary=False,
    is_exhibitor_pass=True  # ✅ SET TRUE for exhibitors
)
```

**Entry Type Display (Lines ~1870):**
```python
# Determine entry type based on is_exhibitor_pass field (with fallback)
is_exhibitor = getattr(entry, 'is_exhibitor_pass', False)
entry_type = "🏢 Exhibitor" if is_exhibitor else "👤 Visitor"
```

**Passes Selected Display (Lines ~815, ~1330):**
```python
# Show combined exhibitor pass or individual days
if is_exhibitor:
    st.write("✅ Exhibitor Pass (25-26 Nov)")
else:
    if entry.exhibition_day1:
        st.write("✅ Exhibition Day 1")
    if entry.exhibition_day2:
        st.write("✅ Exhibition Day 2")
```

#### 3. `backend/app/services/pass_generator.py`

**Pass Generation Logic (Lines ~165):**
```python
def determine_passes_needed(self, entry: Entry) -> List[tuple]:
    """Determine which pass files are needed for this entry"""
    passes = []

    # Check if exhibitor (both exhibition days) - gets combined pass
    if entry.is_exhibitor:
        passes.append(("exhibition_both_days",
                      self.PASS_TEMPLATES["exhibition_both_days_exhibitor"]))
    else:
        # Visitor - gets separate passes for each day
        if entry.exhibition_day1:
            passes.append(("exhibition_day1",
                          self.PASS_TEMPLATES["exhibition_day1_visitor"]))
        if entry.exhibition_day2:
            passes.append(("exhibition_day2",
                          self.PASS_TEMPLATES["exhibition_day2_visitor"]))

    return passes
```

**Invitation Attachments (Lines ~190):**
```python
def get_additional_attachments(self, entry: Entry) -> List[Path]:
    attachments = []
    invitation_dir = self.images_dir / "Invitation"

    # EXHIBITORS - Special exhibitor invitation
    if entry.is_exhibitor:
        inv_file = invitation_dir / "Inv-Exhibitors.png"
        if inv_file.exists():
            attachments.append(inv_file)
    else:
        # VISITORS - Day-specific invitations
        if entry.exhibition_day1:
            inv_file = invitation_dir / "Inv-25.png"
            # ... visitor logic
```

### Step 7: Restart Application

**Important:** After migration, restart the Streamlit app:

```bash
# Stop the current app (Ctrl+C if running locally)
streamlit run frontend/app.py
```

**Or** redeploy on Streamlit Cloud if deployed.

**Why restart is needed:**
- Streamlit caches the database connection and model definitions
- Must reload to pick up new column
- Otherwise will get `AttributeError: 'Entry' object has no attribute 'is_exhibitor_pass'`

---

## Rollback Plan

If something goes wrong:

```sql
-- Remove the column
ALTER TABLE entries
DROP COLUMN IF EXISTS is_exhibitor_pass;
```

**Revert Python Model:**
```python
# Remove from backend/app/models/entry.py:
# is_exhibitor_pass = Column(Boolean, default=False)

# Revert is_exhibitor property:
@property
def is_exhibitor(self) -> bool:
    """Check if this is an exhibitor pass (both exhibition days)"""
    return self.exhibition_day1 and self.exhibition_day2
```

---

## Testing Checklist

After migration:

### Database Tests
- [ ] Column exists: `SELECT is_exhibitor_pass FROM entries LIMIT 1;`
- [ ] All existing entries are `FALSE`: `SELECT COUNT(*) FROM entries WHERE is_exhibitor_pass = TRUE;` (should be 0)
- [ ] New entries default to `FALSE`

### Application Tests
- [ ] App restarts without errors
- [ ] Create new visitor entry - `is_exhibitor_pass` should be `FALSE`
- [ ] Bulk upload exhibitors - `is_exhibitor_pass` should be `TRUE`
- [ ] Entry Type shows "🏢 Exhibitor" for bulk uploaded entries
- [ ] Entry Type shows "👤 Visitor" for individual registrations
- [ ] Exhibitors get EP-25n26.png (1 combined pass)
- [ ] Visitors get EP-25.png + EP-26.png (2 separate passes)
- [ ] Exhibitors get Inv-Exhibitors.png invitation
- [ ] Visitors get Inv-25.png and/or Inv-26.png invitations
- [ ] "Passes Selected" shows "Exhibitor Pass (25-26 Nov)" for exhibitors
- [ ] "Passes Selected" shows "Exhibition Day 1" + "Exhibition Day 2" for visitors
- [ ] QR code scan shows correct venue for exhibitor passes

---

## Safe Attribute Access Pattern

**Problem:** During transition period, some code may try to access `is_exhibitor_pass` before migration or app restart.

**Solution:** Use `getattr()` with fallback:

```python
# Safe access with default value False
is_exhibitor = getattr(entry, 'is_exhibitor_pass', False)
```

**Where used:**
- Entry Type display in frontend
- Any code that accesses the field directly (not through property)

**Why this works:**
- If field doesn't exist, returns `False` (visitor)
- Prevents `AttributeError`
- Allows graceful degradation during transition

---

## Migration Timeline

| Step | Action | Estimated Time |
|------|--------|----------------|
| 1 | Run SQL migration in Supabase | 1 minute |
| 2 | Verify migration | 2 minutes |
| 3 | Update Python model | 1 minute |
| 4 | Update is_exhibitor property | 1 minute |
| 5 | Run Python migration script | 2 minutes |
| 6 | Update code references | Already done |
| 7 | Restart application | 1 minute |
| 8 | Testing | 10 minutes |
| **Total** | | **~20 minutes** |

---

## Database Schema Changes

### Before Migration

```sql
CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    phone VARCHAR NOT NULL,
    id_type VARCHAR NOT NULL,
    id_number VARCHAR NOT NULL UNIQUE,
    exhibition_day1 BOOLEAN DEFAULT FALSE,
    exhibition_day2 BOOLEAN DEFAULT FALSE,
    interactive_sessions BOOLEAN DEFAULT FALSE,
    plenary BOOLEAN DEFAULT FALSE,
    -- ... other fields
);
```

### After Migration

```sql
CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    phone VARCHAR NOT NULL,
    id_type VARCHAR NOT NULL,
    id_number VARCHAR NOT NULL UNIQUE,
    exhibition_day1 BOOLEAN DEFAULT FALSE,
    exhibition_day2 BOOLEAN DEFAULT FALSE,
    interactive_sessions BOOLEAN DEFAULT FALSE,
    plenary BOOLEAN DEFAULT FALSE,
    is_exhibitor_pass BOOLEAN DEFAULT FALSE NOT NULL,  -- ✅ NEW FIELD
    -- ... other fields
);
```

---

## Common Issues and Solutions

### Issue 1: AttributeError after migration

**Error:**
```
AttributeError: 'Entry' object has no attribute 'is_exhibitor_pass'
```

**Cause:** App not restarted after model update

**Solution:**
1. Restart Streamlit app
2. Clear browser cache
3. Verify migration ran successfully

### Issue 2: All entries showing as visitors

**Cause:** Bulk upload not setting `is_exhibitor_pass=True`

**Solution:** Check bulk upload code sets the field:
```python
is_exhibitor_pass=True  # Must be in Entry() constructor
```

### Issue 3: Migration script fails

**Error:**
```
ERROR: column "is_exhibitor_pass" already exists
```

**Cause:** Column already added in previous attempt

**Solution:** Migration uses `IF NOT EXISTS` - safe to re-run

### Issue 4: Supabase connection error

**Error:**
```
ERROR: could not connect to database
```

**Cause:** DATABASE_URL not set or incorrect

**Solution:**
1. Check `.env` file has correct `DATABASE_URL`
2. Verify Supabase credentials
3. Test connection: `psql $DATABASE_URL`

---

## Files Created/Modified

### New Files
1. `run_migration.py` - Python migration script
2. `DATABASE_MIGRATION_ADD_EXHIBITOR_FIELD.sql` - SQL migration script
3. `MIGRATION_EXHIBITOR_FIELD.md` - This documentation

### Modified Files
1. `backend/app/models/entry.py` - Added field and updated property
2. `frontend/app.py` - Bulk upload, display logic
3. `backend/app/services/pass_generator.py` - Pass generation logic
4. `backend/app/services/email_service.py` - Email templates

---

## Success Criteria

Migration is successful when:

✅ Database column exists and has correct type (BOOLEAN)
✅ All existing entries have `is_exhibitor_pass = FALSE`
✅ New exhibitor uploads have `is_exhibitor_pass = TRUE`
✅ New visitor registrations have `is_exhibitor_pass = FALSE`
✅ Exhibitors get 1 combined pass (EP-25n26.png)
✅ Visitors get separate passes (EP-25.png + EP-26.png)
✅ Entry Type displays correctly (🏢 Exhibitor vs 👤 Visitor)
✅ Passes Selected displays correctly
✅ QR codes scan correctly with venue information
✅ Email templates use correct content and attachments
✅ No AttributeErrors in application logs

---

## References

- **Feature Documentation:** [EXHIBITOR_BULK_UPLOAD_FEATURE.md](EXHIBITOR_BULK_UPLOAD_FEATURE.md)
- **Entry Model:** [backend/app/models/entry.py](backend/app/models/entry.py)
- **Pass Generator:** [backend/app/services/pass_generator.py](backend/app/services/pass_generator.py)
- **Email Service:** [backend/app/services/email_service.py](backend/app/services/email_service.py)
- **Similar Migration:** [MIGRATION_INTERACTIVE_SESSIONS.md](MIGRATION_INTERACTIVE_SESSIONS.md)

---

**Migration Status:** ✅ Completed
**Last Updated:** 2025-11-03
**Migration Date:** 2025-11-03
**Tested:** ✅ Yes
**Deployed:** ✅ Yes
