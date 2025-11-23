# Swavlamban 2025 - Project Summary

## 📌 Quick Status

**Event**: Swavlamban 2025 - Naval Innovation & Indigenisation Seminar
**Dates**: November 25-26, 2025 (Monday-Tuesday)
**Status**: ✅ Requirements Finalized - Ready for Development

---

## 🎯 What We're Building

### Two Applications

1. **Registration System** (Streamlit Web App)
   - Organizations register attendees
   - Individual registration (visitors) + Bulk upload (exhibitors)
   - Generate 5 types of passes + exhibitor passes
   - Send emails with QR codes
   - Admin dashboard

2. **Scanner App** (Flutter Mobile)
   - Scan QR codes at 4 gates
   - Verify time/venue access
   - Track attendance
   - Works offline

---

## 🎫 Pass Types

### Visitor Passes (Individual Registration)

| # | Pass Type | Date | Time | Venue |
|---|-----------|------|------|-------|
| 1 | Exhibition Day 1 | Nov 25 | 1100-1730 | Exhibition Hall |
| 2 | Exhibition Day 2 | Nov 26 | 1000-1730 | Exhibition Hall |
| 3 | Interactive Sessions | Nov 26 | 1030-1330 | Zorawar Hall |
| 4 | Plenary Session | Nov 26 | 1530-1615 | Zorawar Hall |

### Exhibitor Passes (Bulk Upload)

| # | Pass Type | Date | Time | Venue |
|---|-----------|------|------|-------|
| E1 | Exhibitor Pass (Both Days) | Nov 25-26 | 0930-1730 | Exhibition Hall |

**Key Differences:**
- **Visitors**: Select individual passes, get separate passes for each day
- **Exhibitors**: Bulk uploaded by admin, get 1 combined pass for both days
- **Exhibitor Access**: Stall setup on 24 Nov AM, 3m x 2.5m stalls

**Note**: Dinner invitations handled offline (NOT in this system)

---

## 🚪 4 Scanning Gates

| Gate | Location | Day | Time | Validates |
|------|----------|-----|------|-----------|
| Gate 1 | Exhibition Hall | Nov 25 | 1100-1730 | Exhibition Day 1 |
| Gate 2 | Exhibition Hall | Nov 26 | 1000-1730 | Exhibition Day 2 |
| Gate 3 | Zorawar Hall | Nov 26 | 1030-1330 | Panel I & II |
| Gate 4 | Zorawar Hall | Nov 26 | 1600-1800 | Plenary |

---

## 🎨 Design Assets Required (You Handle)

### To Update Manually
1. Logo: "2024" → "2025"
2. Pass Template 1: Exhibition Day 1
3. Pass Template 2: Exhibition Day 2
4. Pass Template 3: Panel Discussion I (Future & Emerging Tech)
5. Pass Template 4: Panel Discussion II (Boosting iDEX)
6. Pass Template 5: Plenary Session

### Option: Canva Collaboration
- You have source files in Canva
- Can share access if needed for collaboration

---

## 👥 Organizations & Quotas

**Baseline**: 54 organizations from 2024 (see user_data.json)
**Status**: ⏳ Final list to be confirmed later
**Action**: Using 2024 list for now

### Sample Organizations (2024)
- **Military**: Indian Army, IAF, ICG, BSF
- **PSUs**: HAL, BEL, HSL, GSL, GRSE, MDL
- **Academia**: IITD (800 quota), AMITY (200 quota)
- **Think Tanks**: IDSA, CAPS, CLAWS, USI
- **Admin**: TDAC (999 quota - admin account)

---

## 💻 Tech Stack

### Web App
- Streamlit (Python)
- PostgreSQL database
- Redis cache
- Mailjet (emails)
- bcrypt + JWT (security)

### Mobile App
- Flutter (Android + iOS)
- QR scanner
- SQLite (offline)
- Background sync

### API
- FastAPI
- REST endpoints
- Time-based validation

---

## 🗄️ Key Database Tables

1. **users** - 54 organizations with quotas
2. **entries** - Attendee registrations (1,500+ expected)
3. **check_ins** - Gate check-in records
4. **scanner_devices** - 4 mobile scanners
5. **audit_log** - Security audit trail

---

## 📧 Email System

### Visitor Email Templates (5 types)
- Exhibition Day 1 email
- Exhibition Day 2 email
- Interactive Sessions email
- Plenary Session email
- Combined passes email

### Exhibitor Email Template
- Dedicated exhibitor email with stall setup info
- Combined pass for both days
- Special exhibitor invitation card

Each includes:
- QR code pass (PNG)
- Invitation card
- Event program
- Venue map
- Guidelines

---

## 🏢 Exhibitor Bulk Upload Feature

**Admin-Only Feature:**
- CSV bulk upload for exhibitors
- Automatic pass generation (EP-25n26.png)
- Dedicated email template with stall info
- Entry Type tracking (🏢 Exhibitor vs 👤 Visitor)

**CSV Format:**
```csv
organization,name,email,mobile,aadhar
DRDO,John Doe,john@example.com,9876543210,123456789012
```

**Features:**
- Duplicate Aadhar detection
- Batch email sending
- Combined 2-day exhibitor pass
- Special exhibitor invitation (Inv-Exhibitors.png)

**Documentation:** See [EXHIBITOR_BULK_UPLOAD_FEATURE.md](EXHIBITOR_BULK_UPLOAD_FEATURE.md)

---

## 🔐 Security Features

✅ Password hashing (bcrypt)
✅ JWT authentication
✅ QR cryptographic signatures
✅ Time-based access control
✅ Duplicate check-in prevention
✅ Audit logging
✅ HTTPS only

---

## 📊 Expected Scale

- **Organizations**: 54
- **Total Attendees**: 1,500+ (based on 2024: 1,131)
- **Passes Generated**: ~2,000+ (multiple passes per person)
- **Scanning Stations**: 4 gates
- **Event Duration**: 2 days

---

## 📅 Development Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Requirements | Week 0 | ✅ Done |
| Design Assets | Week 1-2 | ⏳ Your action |
| Database Setup | Week 2 | ⏳ Pending |
| Web App Dev | Week 3-4 | ⏳ Pending |
| Mobile App Dev | Week 5-6 | ⏳ Pending |
| API Integration | Week 6-7 | ⏳ Pending |
| Testing | Week 7-8 | ⏳ Pending |
| Deployment | Week 8-9 | ⏳ Pending |
| **Event** | **Nov 25-26** | **Target** |

---

## 📁 Documentation Files

### Main Documents (Start Here)
1. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** ⭐ YOU ARE HERE
2. **[FINAL_REQUIREMENTS.md](FINAL_REQUIREMENTS.md)** - Complete technical requirements
3. **[CLAUDE.md](CLAUDE.md)** - Comprehensive reference
4. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - One-page cheat sheet

### Feature Documentation
5. **[EXHIBITOR_BULK_UPLOAD_FEATURE.md](EXHIBITOR_BULK_UPLOAD_FEATURE.md)** - Exhibitor bulk upload guide
6. **[MIGRATION_EXHIBITOR_FIELD.md](MIGRATION_EXHIBITOR_FIELD.md)** - Database migration for exhibitor field
7. **[MIGRATION_INTERACTIVE_SESSIONS.md](MIGRATION_INTERACTIVE_SESSIONS.md)** - Interactive sessions migration

### Detailed Documents
8. **[SWAVLAMBAN_2025_CONFIRMED_DETAILS.md](SWAVLAMBAN_2025_CONFIRMED_DETAILS.md)** - Event schedule
9. **[IMAGE_ASSETS_ANALYSIS.md](IMAGE_ASSETS_ANALYSIS.md)** - Design specifications
10. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment guide

---

## ✅ Key Clarifications

### What's IN the System:
✅ 4 visitor pass types (Exhibition x2, Interactive Sessions, Plenary)
✅ Exhibitor pass (combined 2-day pass)
✅ Individual registration (visitors)
✅ Bulk CSV upload (exhibitors)
✅ QR code generation
✅ Email delivery (separate templates for visitors/exhibitors)
✅ Scanner app (4 gates)
✅ Offline support
✅ Admin dashboard
✅ Entry Type tracking (Exhibitor vs Visitor)

### What's NOT in the System:
❌ Dinner invitations (handled offline)
❌ Kota House venue
❌ Gate 5 for dinner

---

## 🎯 Next Actions

### Your Actions
1. ⏳ Review [FINAL_REQUIREMENTS.md](FINAL_REQUIREMENTS.md)
2. ⏳ Update design assets (5 pass templates + logo)
   - Manually in Canva OR
   - Share Canva access for collaboration
3. ⏳ **Provide credentials** - See [CREDENTIALS_SETUP.md](CREDENTIALS_SETUP.md)
   - Mailjet API keys (from 2024)
   - GitHub PAT (from 2024)
   - Email sender address
4. ⏳ Confirm final organizations & quotas (when ready)
5. ⏳ Approve to start development

### My Actions (After Your Approval)
1. ⏳ Setup development environment
2. ⏳ Create database schema
3. ⏳ Build registration UI
4. ⏳ Implement pass generation (using your templates)
5. ⏳ Build scanner app
6. ⏳ Testing & deployment

---

## 💡 Important Notes

### Design Assets
- You'll handle manually (no rush for me)
- I need final PNG templates before pass generation
- Logo can be updated anytime

### Organizations List
- Using 2024 baseline for now (54 orgs)
- Can be updated anytime in database
- No blocker for development

### Flexible Approach
- Multiple passes per person allowed
- Users select which passes they want
- Each pass generated independently

---

## 🚀 Ready to Start?

### Prerequisites Checklist
- [x] Requirements finalized
- [x] Event schedule confirmed
- [x] Pass types defined (5 types)
- [x] Gate configuration (4 gates)
- [x] Tech stack decided
- [x] Database schema designed
- [ ] Design assets updated (your action)
- [ ] Final org list (can update later)

### Can Start Development Now?
✅ **YES** - All technical requirements are clear!
⏳ Just need your design assets for final pass generation

---

## 📞 Questions?

If anything is unclear:
- Check **[FINAL_REQUIREMENTS.md](FINAL_REQUIREMENTS.md)** for technical details
- Check **[CLAUDE.md](CLAUDE.md)** for complete reference
- Ask me any questions!

---

## 🎉 Summary

✅ **Planning**: 100% complete
✅ **Requirements**: Fully documented
⏳ **Design Assets**: Your action (Canva)
⏳ **Development**: Ready to start (after assets)
🎯 **Target Event**: November 25-26, 2025

---

**Status**: ✅ Fully Functional - Exhibitor Feature Deployed
**Last Updated**: 2025-11-03
**Latest Feature**: Exhibitor Bulk Upload (See [EXHIBITOR_BULK_UPLOAD_FEATURE.md](EXHIBITOR_BULK_UPLOAD_FEATURE.md))
**Event Date**: November 25-26, 2025
