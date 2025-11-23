# Exhibitor Bulk Upload Feature

## Overview

The Exhibitor Bulk Upload feature allows administrators to bulk register exhibitors for Swavlamban 2025 using a CSV file. Exhibitors receive special combined passes for both exhibition days (25-26 Nov) with dedicated email templates and invitation cards.

---

## Key Differences: Exhibitors vs Visitors

| Feature | Exhibitors | Visitors |
|---------|-----------|----------|
| **Pass Type** | 1 combined pass (EP-25n26.png) | 2 separate passes (EP-25.png + EP-26.png) |
| **Invitation** | Inv-Exhibitors.png | Day-specific invitations (Inv-25.png, Inv-26.png) |
| **Registration** | Bulk CSV upload (Admin only) | Individual registration |
| **Access** | Both exhibition days | Choose specific days |
| **Stall Setup** | Yes (24 Nov AM, 3m x 2.5m) | No |
| **Day 1 Timing** | 0930-1730 hrs | 1100-1730 hrs |
| **Display** | "Exhibitor Pass (25-26 Nov)" | "Exhibition Day 1", "Exhibition Day 2" |
| **Entry Type** | 🏢 Exhibitor | 👤 Visitor |

---

## Admin Access

The bulk upload feature is **ADMIN-ONLY** and available in:
- **Admin Panel** → **Bulk Actions** section
- **Bulk Generate & Email Passes**

### CSV Format

Required columns:
```csv
organization,name,email,mobile,aadhar
DRDO,John Doe,john@example.com,9876543210,123456789012
HAL,Jane Smith,jane@example.com,9876543211,123456789013
```

**Column Requirements:**
- `organization`: Organization name (any string)
- `name`: Full name of attendee
- `email`: Valid email address
- `mobile`: 10-digit phone number
- `aadhar`: 12-digit Aadhar number (unique identifier)

**Important Notes:**
- First row MUST be header row (will be skipped)
- Duplicate Aadhar numbers are automatically skipped
- All fields are required
- Email validation is performed
- Phone must be exactly 10 digits

---

## Technical Implementation

### Database Schema

**New Field Added to Entry Model:**
```python
# backend/app/models/entry.py
is_exhibitor_pass = Column(Boolean, default=False)
```

**Purpose:** Distinguishes exhibitor passes from visitor passes regardless of who created the entry.

**Values:**
- `True` = Exhibitor (bulk uploaded, gets combined pass)
- `False` = Visitor (individual registration, gets separate passes)

### Entry Creation Logic

**Bulk Upload (Admin Panel):**
```python
new_entry = Entry(
    username=user['username'],
    name=attendee['name'],
    email=exhibitor['email'],
    phone=exhibitor['mobile'],
    id_type='Aadhar Card',
    id_number=attendee['aadhar'],
    exhibition_day1=True,        # Both days enabled
    exhibition_day2=True,        # Both days enabled
    interactive_sessions=False,  # Exhibitors don't attend sessions
    plenary=False,               # Exhibitors don't attend plenary
    is_exhibitor_pass=True       # ✅ Exhibitor flag
)
```

**Individual Registration:**
```python
new_entry = Entry(
    # ... other fields ...
    exhibition_day1=user_selected,
    exhibition_day2=user_selected,
    interactive_sessions=user_selected,
    plenary=user_selected,
    is_exhibitor_pass=False     # ✅ Visitor (default)
)
```

### Pass Generation Logic

**File:** `backend/app/services/pass_generator.py`

```python
def determine_passes_needed(self, entry: Entry) -> List[tuple]:
    """Determine which pass files are needed for this entry"""
    passes = []

    # Check if exhibitor - gets COMBINED pass
    if entry.is_exhibitor:
        passes.append(("exhibition_both_days",
                      self.PASS_TEMPLATES["exhibition_both_days_exhibitor"]))
    else:
        # Visitor - gets SEPARATE passes for each day
        if entry.exhibition_day1:
            passes.append(("exhibition_day1",
                          self.PASS_TEMPLATES["exhibition_day1_visitor"]))
        if entry.exhibition_day2:
            passes.append(("exhibition_day2",
                          self.PASS_TEMPLATES["exhibition_day2_visitor"]))

    # Sessions (visitors only - exhibitors don't attend)
    if entry.interactive_sessions:
        passes.append(("interactive_sessions",
                      self.PASS_TEMPLATES["interactive_sessions"]))
    if entry.plenary:
        passes.append(("plenary",
                      self.PASS_TEMPLATES["plenary"]))

    return passes
```

### Invitation Attachments Logic

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
            if inv_file.exists():
                attachments.append(inv_file)
        if entry.exhibition_day2:
            inv_file = invitation_dir / "Inv-26.png"
            if inv_file.exists():
                attachments.append(inv_file)

    return attachments
```

---

## Email Templates

### Exhibitor Email Template

**File:** `backend/app/services/email_service.py` → `send_exhibitor_bulk_email()`

**Subject:** `Swavlamban 2025 - Exhibitor Pass{es} Generated`

**Key Content:**

```
EVENT DETAILS:
• Dates: 25-26 November 2025
• Time: Day 1: 0930-1730 hrs | Day 2: 1000-1730 hrs
• Venue: Exhibition Hall, Manekshaw Centre
• Note: Please arrive by 0930 hrs on Day 1 for inauguration at 1000 hrs

STALL SETUP:
• Venue will be available for stall setup on AM 24 Nov 25
• Dimensions of stalls: 3m X 2.5m

EXHIBITOR ACCESS:
• Full access to Exhibition Hall on both days
• Booth setup and operations
• Industry interactions

ATTACHMENTS:
✅ Event Pass with QR Code (for entry gate scanning)
✅ Invitation Card

IMPORTANT INFORMATION:
• PRINT or SHOW the QR code pass at entry gates
• Valid Aadhar Card required for entry
• Security clearance mandatory for all attendees

EVENT INFORMATION:
For complete event details, visit https://swavlamban2025-info.streamlit.app
```

**Differences from Visitor Email:**
- ✅ Includes stall setup information
- ✅ Day 1 timing starts at 0930 hrs (not 1100 hrs)
- ✅ Mentions inauguration at 1000 hrs
- ✅ Stall dimensions specified
- ✅ "Invitation Card" instead of "Invitation Image"
- ✅ Aadhar Card explicitly required (not generic "photo ID")
- ✅ Links to public event info site (not login portal)
- ❌ No session timing instructions
- ❌ No login instructions

---

## UI Display

### Entry Type Column

**Location:** Admin Panel → Bulk Generate & Email Passes

**Display Logic:**
```python
# Determine entry type based on is_exhibitor_pass field
is_exhibitor = getattr(entry, 'is_exhibitor_pass', False)
entry_type = "🏢 Exhibitor" if is_exhibitor else "👤 Visitor"
```

**Safe Fallback:** Uses `getattr()` with `False` default for entries created before migration.

### Passes Selected Display

**Location 1: My Entries Section**

**Code:** `frontend/app.py` (Lines 810-823)

```python
st.write("**Passes Selected:**")

# Show combined exhibitor pass or individual days
if is_exhibitor:
    st.write("✅ Exhibitor Pass (25-26 Nov)")
else:
    if entry.exhibition_day1:
        st.write("✅ Exhibition Day 1")
    if entry.exhibition_day2:
        st.write("✅ Exhibition Day 2")

if entry.interactive_sessions:
    st.write("✅ Interactive Sessions")
if entry.plenary:
    st.write("✅ Plenary Session")
```

**Location 2: Generate & Email Passes Section**

**Code:** `frontend/app.py` (Lines 1327-1344)

```python
passes_list = []

# Show combined exhibitor pass or individual days
if is_exhibitor:
    st.write("✅ Exhibitor Pass (25-26 Nov)")
    passes_list.append("exhibition_both_days")
else:
    if entry.exhibition_day1:
        st.write("✅ Exhibition Day 1")
        passes_list.append("exhibition_day1")
    if entry.exhibition_day2:
        st.write("✅ Exhibition Day 2")
        passes_list.append("exhibition_day2")
```

**Display Examples:**

**Exhibitor:**
```
Passes Selected:
✅ Exhibitor Pass (25-26 Nov)
```

**Visitor:**
```
Passes Selected:
✅ Exhibition Day 1
✅ Exhibition Day 2
✅ Interactive Sessions
```

---

## QR Code Generation

### Session Details

**File:** `backend/app/services/pass_generator.py` → `SESSION_DETAILS`

```python
"exhibition_both_days": {
    "name": "Exhibition - 25 & 26 Nov",
    "date": "2025-11-25 to 2025-11-26",
    "time_start": "0930",
    "time_end": "1730",
    "venue": "Exhibition Hall, Manekshaw Centre"
},
"exhibition_both_days_exhibitor": {
    "name": "Exhibition - 25 & 26 Nov",
    "date": "2025-11-25 to 2025-11-26",
    "time_start": "0930",
    "time_end": "1730",
    "venue": "Exhibition Hall, Manekshaw Centre"
}
```

**QR Code Data:**
```json
{
  "entry_id": "12345",
  "name": "John Doe",
  "organization": "DRDO",
  "session_type": "exhibition_both_days",
  "date": "2025-11-25 to 2025-11-26",
  "time": "0930-1730",
  "venue": "Exhibition Hall, Manekshaw Centre",
  "id_number": "1234****9012"
}
```

---

## Error Handling

### Duplicate Aadhar Detection

**Code:** `frontend/app.py` (Lines 2312-2329)

```python
# Check if Aadhar already exists
existing_entry = db.query(Entry).filter(
    Entry.id_number == attendee['aadhar']
).first()

if existing_entry:
    skipped_attendees.append(
        f"{attendee['name']} (Aadhar: {attendee['aadhar'][:4]}****{attendee['aadhar'][-4:]})"
    )
    continue  # Skip and continue with next attendee
```

**Behavior:**
- Skips duplicate entries instead of failing entire batch
- Displays list of skipped attendees after upload
- Continues processing remaining attendees

### CSV Validation

**Checks Performed:**
1. File format validation (CSV)
2. Required columns present
3. Email format validation
4. Phone number format (10 digits)
5. Aadhar format (12 digits)
6. No empty required fields

---

## Testing Checklist

After deploying the exhibitor feature:

- [ ] Upload CSV with exhibitors
- [ ] Verify exhibitors show "🏢 Exhibitor" in Entry Type column
- [ ] Generate passes - verify EP-25n26.png created (not EP-25.png + EP-26.png)
- [ ] Verify Inv-Exhibitors.png attached to email
- [ ] Check email content includes stall setup info
- [ ] Verify Day 1 timing shows 0930-1730 hrs
- [ ] Check "Passes Selected" shows "Exhibitor Pass (25-26 Nov)"
- [ ] Test duplicate Aadhar detection
- [ ] Scan QR code - verify venue shows correctly
- [ ] Test individual visitor registration still works
- [ ] Verify admin can create both exhibitor and visitor passes

---

## Files Modified

### Backend Files

1. **backend/app/models/entry.py**
   - Added `is_exhibitor_pass = Column(Boolean, default=False)`
   - Updated `is_exhibitor` property to read from database field

2. **backend/app/services/pass_generator.py**
   - Updated `determine_passes_needed()` to check `entry.is_exhibitor`
   - Added "exhibition_both_days" to SESSION_DETAILS
   - Updated `get_additional_attachments()` for exhibitor invitations

3. **backend/app/services/email_service.py**
   - Created `send_exhibitor_bulk_email()` function
   - Dedicated exhibitor email template

### Frontend Files

4. **frontend/app.py**
   - Fixed CSV variable shadowing (line 1839)
   - Set `is_exhibitor_pass=True` in bulk upload (lines 2331-2345)
   - Added Entry Type column display (lines 1863-1878)
   - Updated Passes Selected display in My Entries (lines 810-823)
   - Updated Passes Selected display in Generate Passes (lines 1327-1344)
   - Duplicate Aadhar handling (lines 2312-2329)
   - Changed calendar icon from 📅 to ⏰ (line 127)

### Database Migration

5. **run_migration.py**
   - Migration script to add `is_exhibitor_pass` column

6. **DATABASE_MIGRATION_ADD_EXHIBITOR_FIELD.sql**
   - SQL migration for Supabase

---

## Design Assets Required

### Pass Templates

**Exhibitor Pass:**
- `backend/app/images/Passes/EP-25n26.png` - Combined 2-day exhibitor pass

**Visitor Passes:**
- `backend/app/images/Passes/EP-25.png` - Exhibition Day 1
- `backend/app/images/Passes/EP-26.png` - Exhibition Day 2

### Invitations

**Exhibitor Invitation:**
- `backend/app/images/Invitation/Inv-Exhibitors.png` - Special exhibitor invitation

**Visitor Invitations:**
- `backend/app/images/Invitation/Inv-25.png` - Day 1 invitation
- `backend/app/images/Invitation/Inv-26.png` - Day 2 invitation

---

## Future Enhancements

Potential improvements:

1. **CSV Template Download**
   - Provide downloadable CSV template with sample data

2. **Bulk Edit**
   - Allow editing exhibitor details after upload

3. **Organization Grouping**
   - Group exhibitors by organization in admin view

4. **Stall Assignment**
   - Assign stall numbers to exhibitors

5. **Badge Printing**
   - Physical badge generation for exhibitors

6. **Check-in Reports**
   - Separate analytics for exhibitors vs visitors

---

## Troubleshooting

### Issue: Entry Type shows all as exhibitors

**Cause:** Old logic checked both exhibition days instead of database field

**Solution:** Updated to use `entry.is_exhibitor_pass` field

### Issue: AttributeError 'is_exhibitor_pass'

**Cause:** App using cached Entry model before database migration

**Solution:**
1. Run database migration
2. Restart Streamlit app
3. Use safe fallback: `getattr(entry, 'is_exhibitor_pass', False)`

### Issue: QR code missing venue

**Cause:** SESSION_DETAILS missing "exhibition_both_days" key

**Solution:** Added "exhibition_both_days" entry to SESSION_DETAILS

### Issue: CSV upload fails with AttributeError

**Cause:** Variable `csv` shadowing module import

**Solution:** Renamed to `org_csv = df.to_csv(index=False)`

### Issue: Wrong passes displayed for exhibitors

**Cause:** Display logic didn't check exhibitor flag

**Solution:** Added conditional display - show "Exhibitor Pass (25-26 Nov)" if `is_exhibitor`

---

## Security Considerations

1. **Admin-Only Access**
   - Bulk upload restricted to admin role
   - Regular users cannot bulk upload

2. **Duplicate Prevention**
   - Aadhar number uniqueness check
   - Prevents duplicate registrations

3. **Data Validation**
   - Email format validation
   - Phone number validation
   - Aadhar number validation

4. **Audit Trail**
   - All bulk uploads logged with admin username
   - Timestamp of creation

---

## Support

For issues or questions:
- **Technical Documentation:** See [MIGRATION_EXHIBITOR_FIELD.md](MIGRATION_EXHIBITOR_FIELD.md)
- **Database Schema:** See [backend/app/models/entry.py](backend/app/models/entry.py)
- **Pass Generation:** See [backend/app/services/pass_generator.py](backend/app/services/pass_generator.py)
- **Email Service:** See [backend/app/services/email_service.py](backend/app/services/email_service.py)

---

**Feature Status:** ✅ Fully Functional
**Last Updated:** 2025-11-03
**Migration Required:** Yes (see [MIGRATION_EXHIBITOR_FIELD.md](MIGRATION_EXHIBITOR_FIELD.md))
