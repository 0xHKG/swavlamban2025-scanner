# Swavlamban 2025 - Confirmed Event Details

## Official Event Information

### Event Dates
- **Day 1**: November 25, 2025 (Monday)
- **Day 2**: November 26, 2025 (Tuesday)
- **Venue**: Zorawar Hall (main sessions), Exhibition Hall, Kota House (dinner)

---

## Event Structure Analysis

### Three Pass Types Required

#### Pass Type 1: Day 1 - Full Day Access (25 Nov 2025)
**Schedule**: 1000 - 2130 hrs
**Activities**:
- Exhibition Inauguration & Walkaround by CNS (1000-1100)
- Tea & Refreshments (1100-1130)
- Exhibition Open for all (1100 onwards)
- Industry Interactions (1430-1715):
  - Industry with Nodal Officers
  - Presentation to NAs/DAs
  - Industry with VCs
- Swavlamban Dinner by invitation (1915-2130) - Kota House

**Venues**: Exhibition Hall, Kota House
**Access Level**: Full day + dinner (by invitation)

---

#### Pass Type 2: Day 2 - Morning Sessions (26 Nov 2025)
**Schedule**: 0930 - 1330 hrs
**Activities**:
- Registration (0930-1000)
- Inaugural Session (1000-1030) - Zorawar Hall
- Panel Discussion I: Future and Emerging Technologies (1030-1130) - Zorawar Hall
- Tea Break (1130-1200)
- Panel Discussion II: Boosting iDEX Ecosystem (1200-1330) - Zorawar Hall

**Venue**: Zorawar Hall (main)
**Access Level**: Morning sessions only

---

#### Pass Type 3: Day 2 - Plenary Session (26 Nov 2025)
**Schedule**: 1530 - 1615 hrs
**Activities**:
- Welcome address by CNS (1625-1630)
- Discussions on 'Innovation & Self-reliance' (1630-1715)
- Felicitations and Release of Books/Documents/MoUs (1715-1732)
- Hon'ble RM Address (1732-1752)
- Vote of Thanks by VCNS (1752-1755)
- Tea and Departure (1755 onwards)

**Venue**: Zorawar Hall
**Access Level**: Plenary session only

---

## Exhibition Schedule

### Open Hours:
- **Day 1 (25 Nov)**: 1100 - 1730 hrs
- **Day 2 (26 Nov)**: 1000 - 1730 hrs

### Special Events:
- **Exhibition Inauguration**: 1000-1100 (Day 1) by Chief of Naval Staff
- **Hon'ble RM Visit**: 1600-1620 (Day 2)

---

## Key Differences from 2024

### Date Changes
| Item | 2024 | 2025 |
|------|------|------|
| Month | October | **November** |
| Day 1 | October 28 | **November 25** |
| Day 2 | October 29 | **November 26** |
| Day of Week | Sat-Sun | **Mon-Tue** |

### Session Structure Changes
| Aspect | 2024 | 2025 |
|--------|------|------|
| Day 1 Focus | Exhibition + General | Exhibition + Industry Interactions |
| Day 2 Morning | Interactive Session | Panel Discussions (2 sessions) |
| Day 2 Afternoon | Plenary Session | Plenary Session (similar) |
| New Addition | - | **Swavlamban Dinner (Day 1)** |

### Venue Updates
- **Main Hall**: Zorawar Hall (confirmed)
- **Exhibition**: Exhibition Hall (confirmed)
- **Dinner**: Kota House (new venue for 2025)

---

## Pass Requirements Matrix

### Day 1 Pass (25 Nov 2025)
- Exhibition access (1100-1730)
- Industry interaction sessions (1430-1715)
- Swavlamban Dinner access (1915-2130) - **by invitation only**

**Target Attendees**:
- Industry representatives
- Startups and MSMEs
- Nodal Officers
- Naval Advisors (NAs) / Defence Advisors (DAs)
- Venture Capitalists
- Selected invitees for dinner

### Day 2 Morning Pass (26 Nov 2025)
- Registration area access (0930-1000)
- Inaugural Session (1000-1030)
- Panel Discussion I: Future & Emerging Technologies (1030-1130)
- Tea Break (1130-1200)
- Panel Discussion II: Boosting iDEX Ecosystem (1200-1330)
- Lunch break and Exhibition visit (1330-1530)

**Target Attendees**:
- Academia
- Think tanks
- Policy makers
- Industry participants
- Students and researchers

### Day 2 Plenary Pass (26 Nov 2025)
- Gates open (1500)
- Plenary Session (1530-1615):
  - CNS welcome address
  - Innovation & Self-reliance discussions
  - Book/Document/MoU releases
  - Hon'ble RM address
  - VCNS vote of thanks
- Tea and departure (post-event)

**Target Attendees**:
- Senior government officials
- Military leadership
- VIPs and dignitaries
- Key industry partners
- Media

---

## Updated Pass Template Specifications

### Pass 1: Day 1 - 25 November 2025
```
File name: pass_25nov2025.png
Title: "SWAVLAMBAN 2025 - DAY 1"
Date: "25 November 2025"
Subtitle: "Exhibition & Industry Interactions"
Venues: "Exhibition Hall | Kota House"
Time: "1000 - 2130 hrs"
Special Note: "Dinner by Invitation Only"

QR Code Config:
- Position: Left (60px margin, centered vertically)
- Size: 220x220px
- Colors: Brown (#8B4513) on Beige (#F5DEB3)
```

### Pass 2: Day 2 Morning - 26 November 2025
```
File name: pass_26nov2025_morning.png
Title: "SWAVLAMBAN 2025 - DAY 2 MORNING"
Date: "26 November 2025"
Subtitle: "Panel Discussions"
Sessions:
  - "Inaugural Session (1000-1030)"
  - "Panel I: Future & Emerging Technologies (1030-1130)"
  - "Panel II: Boosting iDEX Ecosystem (1200-1330)"
Venue: "Zorawar Hall"
Time: "0930 - 1330 hrs"

QR Code Config:
- Position: Left (60px margin, centered vertically)
- Size: 400x400px
- Colors: Navy Blue (#1D4E89) on Gray (#D3D3D3)
```

### Pass 3: Day 2 Plenary - 26 November 2025
```
File name: pass_26nov2025_plenary.png
Title: "SWAVLAMBAN 2025 - PLENARY SESSION"
Date: "26 November 2025"
Subtitle: "Innovation & Self-reliance"
Highlights:
  - "Hon'ble RM Address"
  - "CNS Welcome & VCNS Vote of Thanks"
  - "Release of Books/Documents/MoUs"
Venue: "Zorawar Hall"
Time: "1530 - 1615 hrs"

QR Code Config:
- Position: Left (60px margin, centered vertically)
- Size: 400x400px
- Colors: Brown (#8B4513) on White (#FFFFFF)
```

---

## Database Schema Updates

### Updated Pass Type Enum
```sql
CREATE TYPE pass_type AS ENUM (
    'day1_25nov',           -- Full Day 1 access
    'day2_morning_26nov',   -- Morning sessions
    'day2_plenary_26nov'    -- Plenary session
);
```

### Entries Table (Updated)
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

    -- Pass allocation (boolean flags)
    pass_day1 BOOLEAN DEFAULT FALSE,
    pass_day2_morning BOOLEAN DEFAULT FALSE,
    pass_day2_plenary BOOLEAN DEFAULT FALSE,

    -- Dinner invitation (special access)
    dinner_invitation BOOLEAN DEFAULT FALSE,

    -- Pass generation tracking
    pass_generated_day1 BOOLEAN DEFAULT FALSE,
    pass_generated_day2_morning BOOLEAN DEFAULT FALSE,
    pass_generated_day2_plenary BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (username) REFERENCES users(username)
);
```

### Check-ins Table (Updated)
```sql
CREATE TABLE check_ins (
    id SERIAL PRIMARY KEY,
    entry_id INTEGER NOT NULL,
    session_type TEXT NOT NULL,  -- 'day1_25nov', 'day2_morning_26nov', 'day2_plenary_26nov'
    session_name TEXT,           -- 'Exhibition', 'Panel Discussion I', 'Plenary', etc.
    check_in_time TIMESTAMP DEFAULT NOW(),
    gate_number TEXT,
    gate_location TEXT,          -- 'Exhibition Hall', 'Zorawar Hall', 'Kota House'
    scanner_device_id TEXT,
    scanner_operator TEXT,
    verification_status TEXT DEFAULT 'verified',
    notes TEXT,
    FOREIGN KEY (entry_id) REFERENCES entries(id)
);
```

---

## QR Code Data Format (2025)

### Enhanced JSON Structure
```json
{
  "event": "SWAVLAMBAN_2025",
  "entry_id": 12345,
  "name": "Full Name",
  "organization": "Organization Name",
  "id_type": "Aadhaar",
  "id_number_hash": "sha256_hash_of_id",
  "pass_type": "day1_25nov",
  "access_level": {
    "exhibition": true,
    "industry_sessions": true,
    "dinner": false
  },
  "valid_date": "2025-11-25",
  "valid_time_start": "1000",
  "valid_time_end": "2130",
  "venues": ["Exhibition Hall", "Kota House"],
  "issued_at": "2025-11-15T10:30:00Z",
  "issued_by": "username",
  "signature": "cryptographic_hmac_signature",
  "version": "2.0"
}
```

---

## User Interface Updates Needed

### Registration Form - Pass Selection
```
Pass Selection for [Organization Name]:

□ Day 1 - 25 November 2025 (Exhibition & Industry Interactions)
  Time: 1000 - 2130 hrs | Venues: Exhibition Hall, Kota House
  ☑ Include Dinner Invitation (by approval only)

□ Day 2 Morning - 26 November 2025 (Panel Discussions)
  Time: 0930 - 1330 hrs | Venue: Zorawar Hall
  Sessions: Inaugural, Panel I (Emerging Tech), Panel II (iDEX)

□ Day 2 Plenary - 26 November 2025 (Plenary Session)
  Time: 1530 - 1615 hrs | Venue: Zorawar Hall
  Includes: Hon'ble RM Address, Book/MoU Releases

Attendee Details:
- Name: [_______________]
- Phone: [_______________]
- Email: [_______________]
- ID Type: [Aadhaar ▼]
- ID Number: [_______________]
- Photo Upload: [Choose File]
```

---

## Email Templates (Updated)

### Day 1 Pass Email
```
Subject: Swavlamban 2025 - Day 1 Pass (25 November 2025)

Dear [Name],

Your entry pass for Swavlamban 2025 - Day 1 has been generated successfully.

Event Details:
- Date: 25 November 2025 (Monday)
- Time: 1000 - 2130 hrs
- Venues: Exhibition Hall, Kota House

Schedule Highlights:
• Exhibition Inauguration by CNS (1000-1100)
• Exhibition Open (1100 onwards)
• Industry Interactions (1430-1715)
• Swavlamban Dinner [if invited] (1915-2130)

Important Instructions:
1. Carry a valid government-issued photo ID
2. Arrive 15 minutes before your scheduled session
3. Display QR code pass at all entry points
4. Follow security protocols

Attachments:
- Your Entry Pass (QR Code)
- Event Program
- Dos and Don'ts Guidelines
- Venue Map

For queries: support@swavlamban2025.in

Regards,
Swavlamban 2025 Organizing Committee
```

### Day 2 Morning Pass Email
```
Subject: Swavlamban 2025 - Day 2 Morning Sessions (26 November 2025)

Dear [Name],

Your entry pass for Swavlamban 2025 - Day 2 Morning Sessions has been generated.

Event Details:
- Date: 26 November 2025 (Tuesday)
- Time: 0930 - 1330 hrs
- Venue: Zorawar Hall

Session Schedule:
• 0930-1000: Registration
• 1000-1030: Inaugural Session
• 1030-1130: Panel Discussion I - Future & Emerging Technologies
• 1130-1200: Tea Break
• 1200-1330: Panel Discussion II - Boosting iDEX Ecosystem

Exhibition Access:
You may visit the exhibition during lunch break (1330-1530)

[Rest of email similar to Day 1]
```

### Day 2 Plenary Pass Email
```
Subject: Swavlamban 2025 - Plenary Session (26 November 2025)

Dear [Name],

Your entry pass for Swavlamban 2025 - Plenary Session has been generated.

Event Details:
- Date: 26 November 2025 (Tuesday)
- Time: 1530 - 1615 hrs (Gates open at 1500)
- Venue: Zorawar Hall

Session Highlights:
• Welcome Address by Chief of Naval Staff
• Discussions on 'Innovation & Self-reliance'
• Release of Books, Documents, and MoUs
• Address by Hon'ble Raksha Mantri
• Vote of Thanks by Vice Chief of Naval Staff

Special Notes:
- Plenary session begins sharp at 1530
- Please be seated by 1525
- Formal dress code required

[Rest of email similar to Day 1]
```

---

## Supporting Documents to Create

### 1. Event Program Document
- Full schedule for both days
- Speaker bios
- Panel discussion topics and moderators
- Exhibition layout map

### 2. Dos and Don'ts Guidelines (Updated)
- Day 1 specific guidelines
- Day 2 morning session guidelines
- Day 2 plenary session guidelines (VIP protocol)
- Photography/video recording rules
- Security clearance requirements

### 3. Venue Maps
- Zorawar Hall seating plan
- Exhibition Hall layout
- Kota House location (for dinner)
- Parking and transport information

---

## Scanner App Session Configuration

### Gate Setup for Day 1 (25 Nov 2025)
```
Gate 1: Exhibition Hall Main Entrance
- Validates: day1_25nov passes
- Time: 1000 - 1730 hrs
- Capacity tracking: Yes

Gate 2: Kota House (Dinner Venue)
- Validates: day1_25nov passes + dinner_invitation=true
- Time: 1915 - 2130 hrs
- Capacity tracking: Yes
- Special: Check invitation flag
```

### Gate Setup for Day 2 (26 Nov 2025)
```
Gate 3: Zorawar Hall - Morning Sessions
- Validates: day2_morning_26nov passes
- Time: 0930 - 1330 hrs
- Sessions: Registration, Inaugural, Panel Discussions

Gate 4: Zorawar Hall - Plenary Session
- Validates: day2_plenary_26nov passes
- Time: 1600 - 1800 hrs
- Special: VIP protocol, early seating required
- Alert: RM security clearance
```

---

## Key Action Items

### Design Updates Required
- [ ] Update logo: "2024" → "2025"
- [ ] Create Day 1 pass template (25 Nov 2025)
- [ ] Create Day 2 Morning pass template (26 Nov 2025)
- [ ] Create Day 2 Plenary pass template (26 Nov 2025)
- [ ] Update Dos & Don'ts documents (3 versions)
- [ ] Create Event Program document with full schedule
- [ ] Design venue maps (Zorawar Hall, Exhibition Hall, Kota House)

### Development Updates Required
- [ ] Update database schema (pass types, session names)
- [ ] Update QR code generation (new JSON format)
- [ ] Add "dinner invitation" flag in registration form
- [ ] Update email templates (3 versions)
- [ ] Configure scanner app (4 gates, 2 days)
- [ ] Add session-specific validation logic
- [ ] Update admin dashboard (new statistics)

### Testing Requirements
- [ ] Test pass generation for all 3 types
- [ ] Verify dinner invitation flag works correctly
- [ ] Test scanner app at different gates/times
- [ ] Validate QR codes with new data format
- [ ] Test email delivery with new templates
- [ ] Verify venue-specific access control

---

## Timeline (Revised)

### Immediate (Week 1)
- Finalize organization list and quotas
- Update all design assets (logo, passes, documents)
- Confirm dinner invitation list

### Development (Week 2-6)
- Implement database changes
- Update web app UI
- Build/update scanner app
- Create email templates

### Testing (Week 7-8)
- End-to-end testing
- Security audit
- Operator training

### Deployment (Week 9)
- Go-live for registrations
- Final testing with actual data

### Event (Week 10+)
- November 25-26, 2025

---

## Important Notes

### Special Access Controls

1. **Dinner Invitation**:
   - Separate flag from Day 1 pass
   - Requires approval (admin only)
   - Scanner at Kota House must validate both pass + invitation

2. **Exhibition Access**:
   - Day 1 pass holders: Full access (1100-1730)
   - Day 2 morning pass holders: Lunch break access (1330-1530)
   - Day 2 plenary pass holders: No separate exhibition access (unless combined pass)

3. **VIP Protocol**:
   - Hon'ble RM visit: 1600-1620 (Day 2)
   - CNS, VCNS, and senior officials
   - Special security clearance required
   - Early seating for plenary session

### Capacity Planning
```
Estimated Capacity:
- Exhibition Hall: 500-800 persons
- Zorawar Hall: 300-500 persons
- Kota House Dinner: 200-300 persons (by invitation)

Gate Staffing:
- Day 1: 2 gates (Exhibition + Dinner venue)
- Day 2 Morning: 1 gate (Zorawar Hall)
- Day 2 Plenary: 1 gate (Zorawar Hall - VIP security)
```

---

**Document Status**: ✅ Confirmed from official program
**Last Updated**: 2025-10-18
**Source**: Draft Programme - Swavlamban 2025
