# Swavlamban 2025 - Design Assets Status

**Last Updated**: 2025-10-19
**Status**: ✅ ALL DESIGN ASSETS COMPLETE AND APPROVED

---

## 📊 Complete Inventory

### ✅ HIGH PRIORITY - COMPLETE (6 files)

| # | File | Location | Size | Purpose | Status |
|---|------|----------|------|---------|--------|
| 1 | logo.png | `/images/` | 6912 x 3456 | Event branding | ✅ Verified correct (2025) |
| 2 | EP-25.png | `/images/Passes/` | 1999 x 825 | Exhibition Day 1 pass | ✅ Ready |
| 3 | EP-26.png | `/images/Passes/` | 1999 x 825 | Exhibition Day 2 pass | ✅ Ready |
| 4 | EP-25n26.png | `/images/Passes/` | 1999 x 823 | Exhibitor both-day pass | ✅ Ready |
| 5 | EP-INTERACTIVE.png | `/images/Passes/` | 1999 x 826 | Panel discussions pass | ✅ Ready |
| 6 | EP-PLENARY.png | `/images/Passes/` | 1999 x 825 | Plenary session pass | ✅ Ready |

### ✅ MEDIUM PRIORITY - COMPLETE (3 files)

| # | File | Location | Size | Purpose | Status |
|---|------|----------|------|---------|--------|
| 7 | EF-25.png | `/images/EF/` | 2000 x 1428 | Event Flow Day 1 | ✅ Verified correct |
| 8 | EF-AM26.png | `/images/EF/` | 2000 x 1428 | Event Flow Day 2 AM | ✅ Verified correct |
| 9 | EF-PM26.png | `/images/EF/` | 2000 x 1428 | Event Flow Day 2 PM | ✅ Verified correct |

### ⚠️ PLACEHOLDER FILES - TO BE UPDATED LATER

| # | Folder/File | Count | Status | Notes |
|---|-------------|-------|--------|-------|
| 10-13 | **DND/** (Dos & Don'ts) | 4 files | ⚠️ **PLACEHOLDER** | **CRITICAL**: Venue guidelines - user will update content later |
| - | Guidelines PDFs | 4 files | ⏳ Pending | Email attachments |
| - | Venue maps | 3 files | ⏳ Optional | Nice to have |

**🚨 CRITICAL**: DND folder contains 4 placeholder images for venue Dos & Don'ts guidelines:
- `DND_Exhibition_25.png` - Exhibition Hall dos/don'ts (Day 1)
- `DND_Exhibition_26.png` - Exhibition Hall dos/don'ts (Day 2)
- `DND_interactive.png` - Zorawar Hall dos/don'ts (Panel Discussions)
- `DND_Plenary.png` - Zorawar Hall dos/don'ts (Plenary Session)

**⚠️ MUST use exact filenames in code** - user will replace image content later (no code changes needed).
See [DND_IMAGES_CRITICAL_NOTE.md](DND_IMAGES_CRITICAL_NOTE.md) for full details.

---

## 🎯 Pass Structure (APPROVED)

### User-Confirmed Pass Types:

1. **Exhibition Visitor Passes** (2 types):
   - Day 1 only (25 Nov) → EP-25.png
   - Day 2 only (26 Nov) → EP-26.png

2. **Exhibitor Pass** (1 type):
   - Both days 25 & 26 Nov → EP-25n26.png

3. **Interactive Sessions Pass** (1 type):
   - Covers BOTH Panel I & Panel II → EP-INTERACTIVE.png
   - Rationale: Only 30-min gap between panels, attendees likely to attend both

4. **Plenary Session Pass** (1 type):
   - VIP session (26 Nov) → EP-PLENARY.png

**Total**: 5 pass templates ✅

---

## 🔍 Verification Summary

### Logo Analysis (logo.png)
- ✅ Shows "SWAVLAMBAN-2025" (correct year)
- ✅ Official branding: MoD, Defence Production, Indian Navy, SIDM, iDEX
- ✅ Taglines in English and Hindi
- ✅ Naval imagery (aircraft carriers, warships)
- ℹ️ Dimensions flexible - will adjust per UI requirements
- **Status**: Ready to use

### Event Flow Documents (EF folder)
- ✅ EF-25.png: Day 1 schedule - 100% match with CLAUDE.md
- ✅ EF-AM26.png: Day 2 morning schedule - 100% match
- ✅ EF-PM26.png: Day 2 plenary schedule - 100% match
- **Purpose**: Email attachments showing event schedule
- **Status**: All correct, ready to use

### Pass Templates (Passes folder)
- ✅ All 5 passes professionally designed
- ✅ Consistent branding (Indian Navy, iDEX, SIDM)
- ✅ Left-side blank space for QR codes (as specified)
- ✅ Elegant ornamental borders
- ✅ Clear date labeling
- ✅ Color differentiation (beige for exhibition/plenary, navy blue for interactive)
- **Status**: Production ready

---

## 🎨 Design Specifications

### Pass Design Features

**Common Elements:**
- Header: "NAVAL INNOVATION & INDIGENISATION ORGANISATION (NIIO) SEMINAR"
- Logos: Indian Navy crest (center), iDEX (right), SIDM (far right)
- QR Code Space: Left side, vertically centered, ~300-400px wide
- Decorative borders: Ornamental brown/gold or silver
- Background: Naval ship imagery (faint)

**Color Schemes:**
- **Exhibition & Plenary**: Cream/beige background, brown/gold borders and text
- **Interactive Sessions**: Navy blue background, white text, silver borders

**Typography:**
- Main title: Large serif font
- Pass type: Bold sans-serif
- Dates: Red accent color for emphasis

---

## 🗄️ Database Mapping

### Registration UI → Database → Pass File

```
USER SELECTS           DATABASE FLAGS                    PASS GENERATED
--------------------------------------------------------------------------------
Exhibition Day 1    → exhibition_day1 = true          → EP-25.png
Exhibition Day 2    → exhibition_day2 = true          → EP-26.png
Exhibitor Pass      → exhibition_day1 = true          → EP-25n26.png
                      exhibition_day2 = true
Panel Discussions   → panel1_emerging_tech = true     → EP-INTERACTIVE.png
                      panel2_idex = true
Plenary Session     → plenary = true                  → EP-PLENARY.png
```

### QR Code Implementation

**QR Code Placement:**
- Position: Left side of pass, vertically centered
- Reserved space: ~300-400px width
- Background: Blank/white area
- When generating passes, overlay QR code on this reserved area

**QR Code Data (JSON format):**
```json
{
  "event": "SWAVLAMBAN_2025",
  "entry_id": 12345,
  "name": "Attendee Name",
  "organization": "Organization Name",
  "id_type": "Aadhaar",
  "id_number_hash": "sha256_hash",
  "pass_type": "exhibition_day1",
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

## 📧 Email Templates Mapping

### Email 1: Exhibition Day 1 Pass
**Attachments:**
- EP-25.png (with attendee QR code)
- EF-25.png (Event Flow Day 1)
- **DND_Exhibition_25.png** ⚠️ (Dos/Don'ts - placeholder, update later)
- Guidelines PDF
- Venue map

### Email 2: Exhibition Day 2 Pass
**Attachments:**
- EP-26.png (with attendee QR code)
- EF-AM26.png (Event Flow Day 2 AM)
- EF-PM26.png (Event Flow Day 2 PM)
- **DND_Exhibition_26.png** ⚠️ (Dos/Don'ts - placeholder, update later)
- Guidelines PDF
- Venue map

### Email 3: Exhibitor Pass (Both Days)
**Attachments:**
- EP-25n26.png (with attendee QR code)
- EF-25.png (Event Flow Day 1)
- EF-AM26.png (Event Flow Day 2 AM)
- EF-PM26.png (Event Flow Day 2 PM)
- **DND_Exhibition_25.png** ⚠️ (Day 1 Dos/Don'ts)
- **DND_Exhibition_26.png** ⚠️ (Day 2 Dos/Don'ts)
- Exhibitor guidelines
- Venue map

### Email 4: Interactive Sessions Pass
**Attachments:**
- EP-INTERACTIVE.png (with attendee QR code)
- EF-AM26.png (Panel discussions schedule)
- **DND_interactive.png** ⚠️ (Zorawar Hall Dos/Don'ts - placeholder)
- Session guidelines
- Venue map (Zorawar Hall)

### Email 5: Plenary Session Pass
**Attachments:**
- EP-PLENARY.png (with attendee QR code)
- EF-PM26.png (Plenary schedule)
- **DND_Plenary.png** ⚠️ (Zorawar Hall VIP Dos/Don'ts - placeholder)
- VIP guidelines
- Venue map (Zorawar Hall)

---

## 🚪 Gate Configuration

### Gate 1: Exhibition Hall - Day 1 (25 Nov)
- **Validates**: EP-25.png, EP-25n26.png
- **Time**: 1100 - 1730 hrs
- **Database check**: `exhibition_day1 = true`

### Gate 2: Exhibition Hall - Day 2 (26 Nov)
- **Validates**: EP-26.png, EP-25n26.png
- **Time**: 1000 - 1730 hrs
- **Database check**: `exhibition_day2 = true`

### Gate 3: Zorawar Hall - Panel Discussions (26 Nov)
- **Validates**: EP-INTERACTIVE.png
- **Time**: 1030 - 1330 hrs
- **Database check**: `panel1_emerging_tech = true OR panel2_idex = true`
- **Time-based**: Panel I (1030-1130), Panel II (1200-1330)

### Gate 4: Zorawar Hall - Plenary Session (26 Nov)
- **Validates**: EP-PLENARY.png
- **Time**: 1600 - 1800 hrs
- **Database check**: `plenary = true`
- **Special**: VIP security clearance

---

## ✅ Completion Checklist

### Design Assets
- [x] Logo verified (shows 2025)
- [x] Event Flow documents (3 files) verified against schedule
- [x] Pass templates (5 files) created and approved
- [x] QR code placement reserved on all passes
- [x] Color schemes finalized
- [x] Branding consistent across all materials

### Documentation
- [x] Image analysis report created
- [x] Pass templates analysis completed
- [x] User-approved pass structure documented
- [x] Database mapping defined
- [x] Email templates mapped
- [x] Gate configuration specified

### Ready for Development
- [x] All required design assets present
- [x] Pass structure finalized and approved
- [x] Technical specifications documented
- [x] Database schema aligned with passes
- [x] QR code format defined

---

## 🎯 Next Phase: Development

### Immediate Next Steps:

1. **Backend Development**:
   - Set up PostgreSQL database (schema in CLAUDE.md)
   - Implement FastAPI endpoints
   - QR code generation logic
   - Pass overlay system (QR on template)
   - Email service integration (Mailjet)

2. **Frontend Development**:
   - Streamlit registration UI
   - User login system
   - Pass selection interface
   - Bulk CSV upload
   - Admin dashboard

3. **Mobile App Development**:
   - Flutter scanner app
   - QR code scanning
   - Offline mode with SQLite
   - Gate configuration
   - Time-based validation

4. **Integration**:
   - API connection between web and mobile
   - Email delivery testing
   - QR code scanning testing
   - Database synchronization

---

## 📝 Notes

### Important Decisions Made:

1. **Exhibitor vs Visitor Distinction**: Recognized that exhibitors need both days to operate booths, hence EP-25n26.png
2. **Combined Panel Pass**: Practical decision that attendees will likely attend both panels (30-min gap)
3. **Standardized Dimensions**: All passes ~2000x825px for consistency (easier to maintain)
4. **QR Code Left Placement**: Confirmed by user, space reserved on all templates

### Outstanding Items:

1. **Guidelines PDFs**: 4 files needed for email attachments (not critical for MVP)
2. **Venue Maps**: 3 files optional (nice to have)
3. **DND Folder**: To be updated by user at later date

### Credentials Still Needed:

- Mailjet API key and secret (from 2024 or new account)
- GitHub PAT (optional - for database backups)
- Email sender address
- Database credentials (generate new)
- Redis credentials (generate new)
- JWT secret key (generate new)

---

## 🎉 Summary

**STATUS**: ✅ **ALL CRITICAL DESIGN ASSETS COMPLETE**

All high-priority design assets are ready for the registration system:
- ✅ 1 logo
- ✅ 5 pass templates (user-approved structure)
- ✅ 3 event flow documents

**Total**: 9 design files complete and verified

**The project is READY to proceed to development phase.**

---

**Document Version**: 1.0
**Status**: Complete
**Date**: 2025-10-19
**Next Phase**: Backend + Frontend Development
