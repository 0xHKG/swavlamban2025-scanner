# Swavlamban 2025 - Complete Project Plan

## Project Overview

Building TWO integrated applications for Swavlamban 2025:
1. **Registration & Pass Management System** (Web - Streamlit)
2. **QR Scanner & Check-in System** (Mobile - Flutter)

---

## Architecture: Option C (Hybrid Approach)

### App 1: Registration System (Streamlit)
- **Tech**: Streamlit + Python
- **Database**: PostgreSQL (upgraded from SQLite)
- **Features**: User management, pass generation, email delivery, admin dashboard

### App 2: Scanner App (Flutter)
- **Tech**: Flutter (Android + iOS)
- **Features**: QR scanning, offline support, check-in tracking, real-time sync
- **Database**: Shared PostgreSQL + local SQLite for offline

### Shared Components
- **API Layer**: FastAPI (for Flutter app communication)
- **Database**: PostgreSQL with proper indexing
- **Cache**: Redis for session management

---

## Image Assets Analysis (2024 Edition)

### Homepage Logo
**File**: `logo.png` (2000x1428px, 6MB)

**Description from Vision AI**:
- **Main Title**: "SWAYAM LAMBAN" in large white sans-serif font
- **Year**: "2024" in yellow font below title
- **Design Theme**: Futuristic military/defense
- **Visual Elements**:
  - Fighter jet (left)
  - Tank (center)
  - Spacecraft/satellite (right)
  - Complex network of lines and dots (radar/tech theme)
- **Color Palette**:
  - Blue background (tech theme)
  - White text (main title)
  - Yellow accents (year, highlights)
  - Gray (military equipment)
- **Style**: Video game/military promotional poster aesthetic

### Pass Templates

#### 1. October 28 Pass (`28.png`)
- **Size**: 1280x526px (103KB)
- **Format**: Landscape pass
- **QR Code**:
  - **Position**: Left side, 60px margin, vertically centered
  - **Size**: 220x220px
  - **Colors**: Brown (#8B4513) on Beige (#F5DEB3)

#### 2. Interactive Session - Oct 29 AM (`AM29.png`)
- **Size**: 2000x826px (827KB)
- **Format**: Landscape pass
- **QR Code**:
  - **Position**: Left side, 60px margin, vertically centered
  - **Size**: 400x400px
  - **Colors**: Navy Blue (#1D4E89) on Gray (#D3D3D3)

#### 3. Plenary Session - Oct 29 PM (`PM29.png`)
- **Size**: 2000x826px (1.2MB)
- **Format**: Landscape pass
- **QR Code**:
  - **Position**: Left side, 60px margin, vertically centered
  - **Size**: 400x400px
  - **Colors**: Brown (#8B4513) on White (#FFFFFF)

### Supporting Documents (Email Attachments)
- `DND-28.png` - DOs & DON'Ts guidelines for Oct 28
- `DND-Forenoon.png` - Guidelines for morning session
- `DND-Plenary.png` - Guidelines for plenary session
- `EF-AM29.png` - Event flow for morning session
- `EF-PM29.png` - Event flow for plenary session

---

## Design Requirements for 2025

### Logo Updates Needed
- Change "2024" → **"2025"**
- Consider updated military equipment if new tech showcased
- Maintain: Futuristic theme, blue/white/yellow color scheme
- Possibly add: Indian Navy emblem prominence

### Pass Template Updates (✅ CONFIRMED)

#### Template 1: Day 1 - 25 November 2025
- **Title**: "SWAVLAMBAN 2025 - DAY 1"
- **Date**: "25 November 2025 (Monday)"
- **Subtitle**: "Exhibition & Industry Interactions"
- **Time**: "1000 - 2130 hrs"
- **Venues**: "Exhibition Hall | Kota House"
- **Special Note**: "Dinner by Invitation Only"
- **QR Code**: 220x220px, Brown (#8B4513) on Beige (#F5DEB3)

#### Template 2: Day 2 Morning - 26 November 2025
- **Title**: "SWAVLAMBAN 2025 - DAY 2 MORNING"
- **Date**: "26 November 2025 (Tuesday)"
- **Subtitle**: "Panel Discussions"
- **Time**: "0930 - 1330 hrs"
- **Venue**: "Zorawar Hall"
- **Sessions Listed**:
  - Inaugural Session
  - Panel I: Future & Emerging Technologies
  - Panel II: Boosting iDEX Ecosystem
- **QR Code**: 400x400px, Navy Blue (#1D4E89) on Gray (#D3D3D3)

#### Template 3: Day 2 Plenary - 26 November 2025
- **Title**: "SWAVLAMBAN 2025 - PLENARY SESSION"
- **Date**: "26 November 2025 (Tuesday)"
- **Subtitle**: "Innovation & Self-reliance"
- **Time**: "1530 - 1615 hrs"
- **Venue**: "Zorawar Hall"
- **Highlights**:
  - Hon'ble RM Address
  - CNS Welcome & VCNS Vote of Thanks
  - Release of Books/Documents/MoUs
- **QR Code**: 400x400px, Brown (#8B4513) on White (#FFFFFF)

**Design Improvements**:
- Maintain QR code positions and sizes (proven layout)
- Consider: Adding photo space for enhanced security
- Optional: Holographic/watermark elements for authenticity
- Add venue icons for quick identification

### Branding Consistency
- **Colors**: Navy blue, white, yellow (Indian Navy colors)
- **Typography**: Sans-serif, bold, modern
- **Elements**: Tech/radar patterns, defense equipment silhouettes
- **Logos**: Indian Navy, NIIO, Government of India emblems

---

## Database Schema Updates

### Existing Table (2024)
```sql
CREATE TABLE entries (
    username TEXT,
    name TEXT,
    phone TEXT,
    email TEXT,
    id_type TEXT,
    id_number TEXT,
    pass_28oct BOOLEAN,
    pass_interactive BOOLEAN,
    pass_plenary BOOLEAN
);
```

### New Tables for 2025

#### 1. Enhanced Entries Table
```sql
CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    id_type TEXT NOT NULL,
    id_number TEXT NOT NULL UNIQUE,
    photo_url TEXT,  -- NEW: For photo verification
    pass_28oct BOOLEAN DEFAULT FALSE,
    pass_interactive BOOLEAN DEFAULT FALSE,
    pass_plenary BOOLEAN DEFAULT FALSE,
    pass_generated_28oct BOOLEAN DEFAULT FALSE,
    pass_generated_interactive BOOLEAN DEFAULT FALSE,
    pass_generated_plenary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (username) REFERENCES users(username)
);

CREATE INDEX idx_username ON entries(username);
CREATE INDEX idx_id_number ON entries(id_number);
CREATE INDEX idx_email ON entries(email);
```

#### 2. Check-ins Table (NEW for Scanner App)
```sql
CREATE TABLE check_ins (
    id SERIAL PRIMARY KEY,
    entry_id INTEGER NOT NULL,
    session_type TEXT NOT NULL,  -- '28_oct', 'interactive', 'plenary'
    check_in_time TIMESTAMP DEFAULT NOW(),
    gate_number TEXT,
    scanner_device_id TEXT,
    scanner_operator TEXT,
    verification_status TEXT DEFAULT 'verified',  -- 'verified', 'manual', 'flagged'
    notes TEXT,
    FOREIGN KEY (entry_id) REFERENCES entries(id)
);

CREATE INDEX idx_entry_id ON check_ins(entry_id);
CREATE INDEX idx_check_in_time ON check_ins(check_in_time);
CREATE INDEX idx_session_type ON check_ins(session_type);
```

#### 3. Users Table (Enhanced)
```sql
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,  -- bcrypt hashed
    organization TEXT NOT NULL,
    max_entries INTEGER NOT NULL,
    role TEXT DEFAULT 'user',  -- 'user', 'admin', 'scanner'
    allowed_passes JSONB,  -- {"28_oct": true, "interactive": false, ...}
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);
```

#### 4. Scanner Devices Table (NEW)
```sql
CREATE TABLE scanner_devices (
    device_id TEXT PRIMARY KEY,
    device_name TEXT NOT NULL,
    gate_number TEXT,
    operator_username TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    last_sync TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 5. Audit Log Table (NEW)
```sql
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    username TEXT,
    action TEXT NOT NULL,  -- 'login', 'add_entry', 'generate_pass', 'check_in', etc.
    table_name TEXT,
    record_id INTEGER,
    changes JSONB,
    ip_address TEXT,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_username_audit ON audit_log(username);
CREATE INDEX idx_timestamp_audit ON audit_log(timestamp);
CREATE INDEX idx_action_audit ON audit_log(action);
```

---

## QR Code Data Structure

### 2024 Format
```
Name: [Full Name]
ID Type: [Aadhaar/PAN/DL]
ID Number: [XXXX-XXXX-XXXX]
Pass Type: [28 Oct 24 / Interactive Session - 29 Oct 24 / ...]
```

### 2025 Enhanced Format (JSON-based)
```json
{
  "entry_id": 12345,
  "name": "Full Name",
  "id_type": "Aadhaar",
  "id_number_hash": "sha256_hash",
  "pass_type": "28_oct_25",
  "issued_at": "2025-10-15T10:30:00Z",
  "signature": "cryptographic_signature"
}
```

**Benefits**:
- Faster scanning (structured data)
- Security (signature verification)
- Privacy (hashed ID numbers)
- Fraud prevention (timestamp + signature)

---

## Features Breakdown

### Registration System (Streamlit App)

#### Security Improvements
- ✅ **Password hashing** (bcrypt)
- ✅ **JWT authentication** with refresh tokens
- ✅ **Environment variables** for secrets
- ✅ **Role-based access control** (RBAC)
- ✅ **Audit logging** for all actions
- ✅ **HTTPS enforcement**

#### UI/UX Enhancements
- 🎨 Modern dashboard with charts
- 🎨 Responsive design (mobile/tablet)
- 🎨 Dark mode support
- 🎨 Real-time validation
- 🎨 Progress indicators
- 🎨 Drag-and-drop CSV upload

#### New Features
- 📋 Bulk import (CSV/Excel)
- 📋 Advanced search & filtering
- 📋 Pass revocation
- 📋 Email template customization
- 📋 SMS notifications (optional)
- 📋 Photo upload for passes
- 📋 Duplicate detection
- 📋 Multi-language (Hindi/English)
- 📋 Export reports (PDF, Excel)
- 📋 Real-time analytics dashboard

### Scanner App (Flutter Mobile)

#### Core Features
- 📱 **QR Code Scanning** (camera-based)
- 📱 **Manual Entry** (if QR damaged)
- 📱 **Real-time Verification** against database
- 📱 **Offline Mode** with sync queue
- 📱 **Photo Verification** (compare with ID)
- 📱 **Duplicate Check-in Prevention**
- 📱 **Multi-gate Support**

#### User Interface
- 🎯 Large scan button
- 🎯 Success/failure visual + audio feedback
- 🎯 Attendee details display
- 🎯 Real-time attendance counter
- 🎯 Search by name/org
- 🎯 Manual override for admins

#### Admin Features
- 👤 Scanner operator login
- 👤 Session selection (28 Oct / Interactive / Plenary)
- 👤 Gate number assignment
- 👤 Export attendance reports
- 👤 Flag suspicious activity
- 👤 Manual entry approval

---

## API Endpoints (FastAPI)

### Authentication
```
POST   /api/auth/login
POST   /api/auth/refresh
POST   /api/auth/logout
```

### Registration (Web App)
```
GET    /api/entries
POST   /api/entries
PUT    /api/entries/{id}
DELETE /api/entries/{id}
POST   /api/entries/bulk-upload
GET    /api/entries/export
```

### Check-in (Scanner App)
```
POST   /api/check-in/verify-qr
POST   /api/check-in/manual
GET    /api/check-in/stats
GET    /api/check-in/attendance
POST   /api/check-in/sync
```

### Admin
```
GET    /api/admin/dashboard
GET    /api/admin/users
GET    /api/admin/audit-log
POST   /api/admin/revoke-pass
GET    /api/admin/reports
```

---

## Deployment Plan

### Registration System
- **Platform**: Streamlit Cloud / AWS / DigitalOcean
- **Requirements**:
  - PostgreSQL database
  - Redis instance
  - Email service (Mailjet/SendGrid)
  - File storage (S3/local)

### Scanner App
- **Platform**: Google Play Store + Apple App Store
- **Requirements**:
  - API endpoint (FastAPI backend)
  - SSL certificate
  - Push notification service (Firebase)

### Infrastructure
```
┌─────────────────┐
│  Web Browser    │ → Streamlit App (Registration)
└─────────────────┘
         ↓
┌─────────────────┐
│  FastAPI        │ → REST API
└─────────────────┘
         ↓
┌─────────────────┐
│  PostgreSQL     │ → Shared Database
│  Redis          │ → Session Cache
└─────────────────┘
         ↑
┌─────────────────┐
│  Flutter App    │ → Scanner (Android/iOS)
└─────────────────┘
```

---

## Timeline Estimate

### Phase 1: Design & Setup (Week 1-2)
- [ ] Update logo and pass templates (2024 → 2025)
- [ ] Finalize dates and sessions
- [ ] Setup PostgreSQL + Redis
- [ ] Design API architecture

### Phase 2: Registration System (Week 3-4)
- [ ] Implement security improvements (bcrypt, JWT)
- [ ] Build new UI with modern dashboard
- [ ] Add bulk upload functionality
- [ ] Implement photo upload
- [ ] Email/SMS notification system

### Phase 3: Scanner App (Week 5-6)
- [ ] Flutter app setup
- [ ] QR scanner implementation
- [ ] Offline mode with SQLite
- [ ] Photo verification
- [ ] Admin controls

### Phase 4: Testing & Integration (Week 7)
- [ ] End-to-end testing
- [ ] Security audit
- [ ] Performance testing
- [ ] User acceptance testing

### Phase 5: Deployment (Week 8)
- [ ] Deploy web app
- [ ] Publish mobile apps
- [ ] Training for operators
- [ ] Documentation

---

## Security Considerations

### Data Protection
- ✅ ID numbers hashed in QR codes
- ✅ Passwords bcrypt-hashed (12 rounds)
- ✅ JWT tokens with 15-min expiry
- ✅ HTTPS only (no HTTP)
- ✅ SQL injection prevention (parameterized queries)
- ✅ Rate limiting on API endpoints

### Fraud Prevention
- ✅ Cryptographic signatures on passes
- ✅ Duplicate check-in prevention
- ✅ Photo verification (optional)
- ✅ Timestamp validation
- ✅ Audit trail for all actions

### Privacy
- ✅ GDPR/data protection compliance
- ✅ Minimal data collection
- ✅ Encrypted data at rest
- ✅ Encrypted data in transit

---

## ✅ CONFIRMED EVENT DETAILS

### Event Dates (CONFIRMED)
- **Day 1**: November 25, 2025 (Monday)
- **Day 2**: November 26, 2025 (Tuesday)
- **Venue**: Zorawar Hall, Exhibition Hall, Kota House

### Session Structure (UPDATED)

#### Day 1 - November 25, 2025
- **Time**: 1000 - 2130 hrs
- **Focus**: Exhibition & Industry Interactions
- **Key Events**:
  - Exhibition Inauguration by CNS (1000-1100)
  - Exhibition Open (1100 onwards)
  - Industry Interactions (1430-1715)
  - Swavlamban Dinner by invitation (1915-2130) - Kota House
- **Venues**: Exhibition Hall, Kota House

#### Day 2 Morning - November 26, 2025
- **Time**: 0930 - 1330 hrs
- **Focus**: Panel Discussions
- **Key Events**:
  - Registration (0930-1000)
  - Inaugural Session (1000-1030)
  - Panel Discussion I: Future & Emerging Technologies (1030-1130)
  - Tea Break (1130-1200)
  - Panel Discussion II: Boosting iDEX Ecosystem (1200-1330)
- **Venue**: Zorawar Hall

#### Day 2 Plenary - November 26, 2025
- **Time**: 1530 - 1615 hrs
- **Focus**: Innovation & Self-reliance
- **Key Events**:
  - Welcome Address by CNS
  - Discussions on Innovation & Self-reliance
  - Felicitations & Release of Books/Documents/MoUs
  - Hon'ble RM Address
  - Vote of Thanks by VCNS
  - Note: Exact sub-timing breakdown to be confirmed
- **Venue**: Zorawar Hall

### Scanning Stations (CONFIRMED)
**Day 1 (25 Nov)**:
- Gate 1: Exhibition Hall Main Entrance
- Gate 2: Kota House (Dinner venue - invitation only)

**Day 2 (26 Nov)**:
- Gate 3: Zorawar Hall - Morning Sessions
- Gate 4: Zorawar Hall - Plenary Session (VIP security)

### Major Changes from 2024
1. **Dates**: October → November (28-29 Oct → 25-26 Nov)
2. **Day**: Weekend → Weekday (Sat-Sun → Mon-Tue)
3. **New Addition**: Swavlamban Dinner (Day 1 evening)
4. **Session Names**: "Interactive Session" → "Panel Discussions" (2 sessions)
5. **Venue Names**: Confirmed specific halls

### Outstanding Questions
1. **Organizations**: Same 54 orgs or updated list?
2. **Quotas**: Entry limits per organization?
3. **Dinner Invitations**: Who approves? How many max?
4. **Budget**: Infrastructure budget constraints?
5. **Timeline**: When should system be ready for testing?
6. **Design Assets**: Who will update logo/pass templates?

---

## Next Steps

1. **Approve this plan** and architecture
2. **Provide 2025 event details** (dates, sessions, orgs)
3. **Update image assets** (logo, pass templates)
4. **Start development** following hybrid approach

Ready to start building! 🚀

---

## File Structure (Proposed)

```
swav-registration-2025/
├── backend/
│   ├── fastapi_app/
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── models.py
│   │   ├── routes/
│   │   ├── database.py
│   │   └── utils.py
│   └── requirements.txt
│
├── frontend/
│   ├── streamlit_app/
│   │   ├── app.py
│   │   ├── pages/
│   │   ├── components/
│   │   └── config.py
│   └── requirements.txt
│
├── mobile/
│   ├── flutter_scanner/
│   │   ├── lib/
│   │   │   ├── main.dart
│   │   │   ├── screens/
│   │   │   ├── services/
│   │   │   └── models/
│   │   ├── pubspec.yaml
│   │   └── android/
│   │   └── ios/
│
├── assets/
│   ├── images/
│   │   ├── logo.png (2025 version)
│   │   ├── 28oct25.png
│   │   ├── AM29oct25.png
│   │   └── PM29oct25.png
│   └── fonts/
│
├── database/
│   ├── schema.sql
│   ├── migrations/
│   └── seed_data.sql
│
├── docs/
│   ├── API.md
│   ├── USER_GUIDE.md
│   └── DEPLOYMENT.md
│
└── docker-compose.yml
```
