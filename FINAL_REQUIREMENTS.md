# Swavlamban 2025 - Final Requirements (Updated)

## ✅ Clarifications Received (2025-10-18)

### 1. Dinner Invitations - OFFLINE ONLY
- ❌ **NOT part of online registration system**
- ✅ Handled separately offline
- ✅ No dinner invitation flag in database
- ✅ No dinner mentions on website/passes

### 2. Online Registration Scope (5 Pass Types)

#### Exhibition Passes (2 passes)
1. **Exhibition Day 1** - November 25, 2025
2. **Exhibition Day 2** - November 26, 2025

#### Session Passes (3 passes)
3. **Panel Discussion I** - Future & Emerging Technologies (Nov 26, 1030-1130)
4. **Panel Discussion II** - Boosting iDEX Ecosystem (Nov 26, 1200-1330)
5. **Plenary Session** - Innovation & Self-reliance (Nov 26, 1530-1615)

### 3. Design Assets
- ✅ You will modify all images manually
- ✅ Option: Connect via Canva for collaboration
- ✅ Source files available in Canva
- ⏳ Waiting for your updates

### 4. Organizations & Quotas
- ✅ Use 2024 list as baseline (54 organizations)
- ⏳ Final list to be updated later
- ⏳ Quotas to be confirmed later

---

## 🎫 Updated Pass Types (5 Passes)

### Pass 1: Exhibition Day 1 (25 Nov 2025)
**Access**: Exhibition Hall only
**Time**: 1100 - 1730 hrs
**Activities**:
- Exhibition viewing
- Industry booths
- Innovation displays

**Design Specs**:
```
Title: "SWAVLAMBAN 2025 - EXHIBITION DAY 1"
Date: "25 November 2025 (Monday)"
Time: "1100 - 1730 hrs"
Venue: "Exhibition Hall"

QR Code:
- Size: 220 x 220 px
- Position: Left (60px margin, centered)
- Colors: Brown (#8B4513) on Beige (#F5DEB3)
```

---

### Pass 2: Exhibition Day 2 (26 Nov 2025)
**Access**: Exhibition Hall only
**Time**: 1000 - 1730 hrs
**Activities**:
- Exhibition viewing
- Industry booths
- Innovation displays

**Design Specs**:
```
Title: "SWAVLAMBAN 2025 - EXHIBITION DAY 2"
Date: "26 November 2025 (Tuesday)"
Time: "1000 - 1730 hrs"
Venue: "Exhibition Hall"

QR Code:
- Size: 220 x 220 px
- Position: Left (60px margin, centered)
- Colors: Blue (#1D4E89) on Gray (#D3D3D3)
```

---

### Pass 3: Panel Discussion I (26 Nov 2025)
**Access**: Zorawar Hall
**Time**: 1030 - 1130 hrs
**Topic**: Future & Emerging Technologies

**Design Specs**:
```
Title: "SWAVLAMBAN 2025 - PANEL DISCUSSION I"
Date: "26 November 2025 (Tuesday)"
Topic: "Future & Emerging Technologies"
Time: "1030 - 1130 hrs"
Venue: "Zorawar Hall"

QR Code:
- Size: 400 x 400 px
- Position: Left (60px margin, centered)
- Colors: Navy Blue (#1D4E89) on Gray (#D3D3D3)
```

---

### Pass 4: Panel Discussion II (26 Nov 2025)
**Access**: Zorawar Hall
**Time**: 1200 - 1330 hrs
**Topic**: Boosting iDEX Ecosystem

**Design Specs**:
```
Title: "SWAVLAMBAN 2025 - PANEL DISCUSSION II"
Date: "26 November 2025 (Tuesday)"
Topic: "Boosting iDEX Ecosystem"
Time: "1200 - 1330 hrs"
Venue: "Zorawar Hall"

QR Code:
- Size: 400 x 400 px
- Position: Left (60px margin, centered)
- Colors: Green (#2E7D32) on Light Green (#C8E6C9)
```

---

### Pass 5: Plenary Session (26 Nov 2025)
**Access**: Zorawar Hall
**Time**: 1530 - 1615 hrs
**Highlights**: Hon'ble RM Address, Book Releases

**Design Specs**:
```
Title: "SWAVLAMBAN 2025 - PLENARY SESSION"
Date: "26 November 2025 (Tuesday)"
Subtitle: "Innovation & Self-reliance"
Time: "1530 - 1615 hrs"
Venue: "Zorawar Hall"
Highlights:
  • Hon'ble Raksha Mantri Address
  • Release of Books/Documents/MoUs

QR Code:
- Size: 400 x 400 px
- Position: Left (60px margin, centered)
- Colors: Brown (#8B4513) on White (#FFFFFF)
```

---

## 🗄️ Updated Database Schema

### Entries Table (Revised)
```sql
CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    id_type TEXT NOT NULL,
    id_number TEXT NOT NULL UNIQUE,
    photo_url TEXT,

    -- Pass allocation (5 types - boolean flags)
    pass_exhibition_day1 BOOLEAN DEFAULT FALSE,
    pass_exhibition_day2 BOOLEAN DEFAULT FALSE,
    pass_panel1_emerging_tech BOOLEAN DEFAULT FALSE,
    pass_panel2_idex BOOLEAN DEFAULT FALSE,
    pass_plenary BOOLEAN DEFAULT FALSE,

    -- Pass generation tracking
    pass_generated_exhibition_day1 BOOLEAN DEFAULT FALSE,
    pass_generated_exhibition_day2 BOOLEAN DEFAULT FALSE,
    pass_generated_panel1 BOOLEAN DEFAULT FALSE,
    pass_generated_panel2 BOOLEAN DEFAULT FALSE,
    pass_generated_plenary BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    FOREIGN KEY (username) REFERENCES users(username)
);

CREATE INDEX idx_username ON entries(username);
CREATE INDEX idx_id_number ON entries(id_number);
CREATE INDEX idx_email ON entries(email);
```

### Users Table (Updated)
```sql
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,
    organization TEXT NOT NULL,
    max_entries INTEGER NOT NULL,
    role TEXT DEFAULT 'user',

    -- Allowed passes per organization (5 types)
    allowed_passes JSONB,
    -- Example: {
    --   "exhibition_day1": true,
    --   "exhibition_day2": true,
    --   "panel1_emerging_tech": false,
    --   "panel2_idex": true,
    --   "plenary": false
    -- }

    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);
```

### Check-ins Table (Updated)
```sql
CREATE TABLE check_ins (
    id SERIAL PRIMARY KEY,
    entry_id INTEGER NOT NULL,
    session_type TEXT NOT NULL,
    -- 'exhibition_day1', 'exhibition_day2',
    -- 'panel1_emerging_tech', 'panel2_idex', 'plenary'

    session_name TEXT,
    check_in_time TIMESTAMP DEFAULT NOW(),
    gate_number TEXT,
    gate_location TEXT,
    scanner_device_id TEXT,
    scanner_operator TEXT,
    verification_status TEXT DEFAULT 'verified',
    notes TEXT,

    FOREIGN KEY (entry_id) REFERENCES entries(id)
);

CREATE INDEX idx_entry_id ON check_ins(entry_id);
CREATE INDEX idx_session_type ON check_ins(session_type);
CREATE INDEX idx_check_in_time ON check_ins(check_in_time);
```

---

## 🚪 Updated Gate Configuration

### Day 1 - November 25, 2025

#### Gate 1: Exhibition Hall
- **Location**: Exhibition Hall Main Entrance
- **Time**: 1100 - 1730 hrs
- **Validates**: `exhibition_day1` passes only
- **Capacity**: 500-800 persons

---

### Day 2 - November 26, 2025

#### Gate 2: Exhibition Hall
- **Location**: Exhibition Hall Main Entrance
- **Time**: 1000 - 1730 hrs
- **Validates**: `exhibition_day2` passes only
- **Capacity**: 500-800 persons

#### Gate 3: Zorawar Hall - Panel Discussions
- **Location**: Zorawar Hall Entrance
- **Time**: 1030 - 1330 hrs
- **Validates**:
  - `panel1_emerging_tech` passes (1030-1130)
  - `panel2_idex` passes (1200-1330)
- **Capacity**: 300-500 persons
- **Note**: Time-based validation required

#### Gate 4: Zorawar Hall - Plenary Session
- **Location**: Zorawar Hall Entrance
- **Time**: 1600 - 1800 hrs
- **Validates**: `plenary` passes only
- **Capacity**: 300-500 persons
- **Special**: VIP security clearance

---

## 🔐 Updated QR Code Format

### JSON Structure (5 Pass Types)
```json
{
  "event": "SWAVLAMBAN_2025",
  "entry_id": 12345,
  "name": "Full Name",
  "organization": "Organization Name",
  "id_type": "Aadhaar",
  "id_number_hash": "sha256_hash",
  "pass_type": "exhibition_day1",
  // Options: "exhibition_day1", "exhibition_day2",
  //          "panel1_emerging_tech", "panel2_idex", "plenary"

  "valid_date": "2025-11-25",
  "valid_time_start": "1100",
  "valid_time_end": "1730",
  "venue": "Exhibition Hall",
  "issued_at": "2025-11-15T10:30:00Z",
  "issued_by": "username",
  "signature": "hmac_sha256_signature",
  "version": "2.0"
}
```

---

## 📧 Updated Email Templates (5 Types)

### Email 1: Exhibition Day 1 Pass
```
Subject: Swavlamban 2025 - Exhibition Pass (Day 1 - 25 November)

Dear [Name],

Your exhibition pass for Swavlamban 2025 - Day 1 has been generated.

EVENT DETAILS:
- Date: 25 November 2025 (Monday)
- Time: 1100 - 1730 hrs
- Venue: Exhibition Hall

ACCESS:
• Exhibition viewing
• Industry booths and stalls
• Innovation displays
• Technology demonstrations

IMPORTANT INSTRUCTIONS:
1. Carry valid government-issued photo ID
2. Display QR code at entrance
3. No photography without permission
4. Follow security protocols

ATTACHMENTS:
- Your Exhibition Pass (QR Code)
- Event Program
- Venue Map
- Guidelines

For support: support@swavlamban2025.in

Regards,
Swavlamban 2025 Organizing Committee
```

### Email 2: Exhibition Day 2 Pass
(Similar to Day 1, with updated date: 26 November 2025, Time: 1000-1730)

### Email 3: Panel Discussion I Pass
```
Subject: Swavlamban 2025 - Panel Discussion I (26 November)

Dear [Name],

Your pass for Panel Discussion I has been generated.

SESSION DETAILS:
- Date: 26 November 2025 (Tuesday)
- Time: 1030 - 1130 hrs
- Venue: Zorawar Hall
- Topic: Future & Emerging Technologies

IMPORTANT:
• Please arrive by 1020 hrs
• Seating is limited
• Late entry may not be permitted
• Formal dress code required

[Similar attachments and instructions]
```

### Email 4: Panel Discussion II Pass
(Similar to Panel I, with Topic: Boosting iDEX Ecosystem, Time: 1200-1330)

### Email 5: Plenary Session Pass
```
Subject: Swavlamban 2025 - Plenary Session (26 November)

Dear [Name],

Your pass for the Plenary Session has been generated.

SESSION DETAILS:
- Date: 26 November 2025 (Tuesday)
- Time: 1530 - 1615 hrs (Gates open at 1500)
- Venue: Zorawar Hall

HIGHLIGHTS:
• Address by Hon'ble Raksha Mantri
• CNS Welcome Address
• Release of Books/Documents/MoUs
• VCNS Vote of Thanks

SPECIAL NOTES:
• Please be seated by 1620 hrs
• Formal dress code mandatory
• Security clearance required
• Photography restricted

[Similar attachments and instructions]
```

---

## 🎨 Registration Form UI (Updated)

### Pass Selection Interface
```
┌─────────────────────────────────────────────────────┐
│  SWAVLAMBAN 2025 - REGISTRATION                     │
│                                                     │
│  Organization: [Organization Name]                 │
│  Quota: [Used: 45 / Total: 150 / Remaining: 105]  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  ATTENDEE DETAILS                                   │
│  Name:        [_____________________________]       │
│  Phone:       [_____________________________]       │
│  Email:       [_____________________________]       │
│  ID Type:     [Aadhaar ▼]                          │
│  ID Number:   [_____________________________]       │
│  Photo:       [Upload Photo] (Optional)            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  SELECT PASSES (Choose one or more)                 │
│                                                     │
│  EXHIBITION PASSES                                  │
│  □ Day 1 - 25 Nov (1100-1730) | Exhibition Hall   │
│  □ Day 2 - 26 Nov (1000-1730) | Exhibition Hall   │
│                                                     │
│  SESSION PASSES (Day 2 - 26 Nov)                   │
│  □ Panel Discussion I (1030-1130)                  │
│     Topic: Future & Emerging Technologies          │
│     Venue: Zorawar Hall                            │
│                                                     │
│  □ Panel Discussion II (1200-1330)                 │
│     Topic: Boosting iDEX Ecosystem                 │
│     Venue: Zorawar Hall                            │
│                                                     │
│  □ Plenary Session (1530-1615)                     │
│     Includes: Hon'ble RM Address                   │
│     Venue: Zorawar Hall                            │
└─────────────────────────────────────────────────────┘

            [Submit Registration]  [Clear Form]
```

---

## 📊 Scanner App - Session Configuration

### Session Validation Logic
```python
# Pseudo-code for scanner validation

if pass_type == "exhibition_day1":
    if current_date == "2025-11-25" and "1100" <= current_time <= "1730":
        if gate_location == "Exhibition Hall":
            ALLOW_ENTRY()
    else:
        REJECT("Invalid time or venue")

elif pass_type == "exhibition_day2":
    if current_date == "2025-11-26" and "1000" <= current_time <= "1730":
        if gate_location == "Exhibition Hall":
            ALLOW_ENTRY()
    else:
        REJECT("Invalid time or venue")

elif pass_type == "panel1_emerging_tech":
    if current_date == "2025-11-26" and "1020" <= current_time <= "1130":
        if gate_location == "Zorawar Hall":
            ALLOW_ENTRY()
    else:
        REJECT("Panel Discussion I: 1030-1130 only")

elif pass_type == "panel2_idex":
    if current_date == "2025-11-26" and "1150" <= current_time <= "1330":
        if gate_location == "Zorawar Hall":
            ALLOW_ENTRY()
    else:
        REJECT("Panel Discussion II: 1200-1330 only")

elif pass_type == "plenary":
    if current_date == "2025-11-26" and "1500" <= current_time <= "1615":
        if gate_location == "Zorawar Hall":
            ALLOW_ENTRY()
    else:
        REJECT("Plenary Session: 1530-1615 only")
```

---

## 🎯 Key Differences from Original Plan

### ❌ Removed Features
1. **Dinner Invitation System**
   - No dinner_invitation flag in database
   - No dinner mentions on passes
   - No Kota House venue in scanner app
   - No Gate 2 for dinner venue

2. **Combined Passes**
   - No "Day 1 Full Access" pass
   - No "Day 2 Morning Combined" pass

### ✅ Added Features
1. **Separate Exhibition Passes**
   - Day 1 exhibition (standalone)
   - Day 2 exhibition (standalone)

2. **Individual Session Passes**
   - Panel Discussion I (separate pass)
   - Panel Discussion II (separate pass)
   - Plenary Session (separate pass)

3. **Flexible Access**
   - Users can select multiple passes
   - Independent pass generation
   - Granular access control

---

## 📋 Development Checklist (Updated)

### Phase 1: Design Assets (You handle manually)
- [ ] Logo: Update "2024" → "2025"
- [ ] Pass Template 1: Exhibition Day 1
- [ ] Pass Template 2: Exhibition Day 2
- [ ] Pass Template 3: Panel Discussion I
- [ ] Pass Template 4: Panel Discussion II
- [ ] Pass Template 5: Plenary Session
- [ ] Supporting documents (guidelines, maps)

### Phase 2: Database Setup
- [ ] Create PostgreSQL database
- [ ] Implement updated schema (5 pass types)
- [ ] Remove dinner_invitation field
- [ ] Import 2024 organizations list
- [ ] Setup Redis cache

### Phase 3: Registration System (Web)
- [ ] Update pass selection UI (5 checkboxes)
- [ ] Remove dinner invitation logic
- [ ] Update email templates (5 types)
- [ ] Implement pass generation (5 templates)
- [ ] Update admin dashboard

### Phase 4: Scanner App (Mobile)
- [ ] Update gate configuration (4 gates, not 5)
- [ ] Implement time-based validation
- [ ] Remove Kota House venue
- [ ] Update session types (5 types)
- [ ] Test offline mode

### Phase 5: Testing
- [ ] Test all 5 pass types
- [ ] Test time-based access control
- [ ] Verify email templates
- [ ] Test scanner at different times
- [ ] Load testing

---

## ⏱️ Timeline (Unchanged)
- **Phase 1-2**: Week 1-2 (Design + Setup)
- **Phase 3-4**: Week 3-6 (Development)
- **Phase 5**: Week 7-8 (Testing)
- **Deployment**: Week 8-9
- **Event**: November 25-26, 2025

---

## 📞 Next Steps

### Immediate Actions
1. ✅ Review this updated requirements document
2. ⏳ You: Update design assets (5 pass templates + logo)
   - Option: Share Canva link for collaboration
3. ⏳ Confirm final organizations list & quotas
4. ⏳ Approve to start development

### Development Start
Once design assets are ready:
- Setup development environment
- Create database schema
- Build registration UI
- Implement pass generation
- Build scanner app

---

**Document Status**: ✅ Updated with clarifications
**Last Updated**: 2025-10-18
**Next Review**: After design assets delivery
**Ready for**: Design asset creation & development start
