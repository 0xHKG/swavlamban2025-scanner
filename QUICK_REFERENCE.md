# Swavlamban 2025 - Quick Reference Card

## ⏰ Event at a Glance

### Dates
- **Day 1**: November 25, 2025 (Monday)
- **Day 2**: November 26, 2025 (Tuesday)

### Venues
- 🏛️ **Zorawar Hall** - Main sessions
- 🎨 **Exhibition Hall** - Exhibitions
- 🍽️ **Kota House** - Dinner venue

---

## 🎫 3 Pass Types

| Pass | Date/Time | Access |
|------|-----------|--------|
| **Day 1** | Nov 25, 1000-2130 | Exhibition + Industry Interactions + Dinner* |
| **Day 2 Morning** | Nov 26, 0930-1330 | Panel Discussions + Exhibition |
| **Day 2 Plenary** | Nov 26, 1530-1615 | Plenary Session + Hon'ble RM |

*Dinner by invitation only

---

## 🎨 Design Assets Needed

### Logo
- [ ] Update "2024" → "2025"
- [ ] Maintain futuristic military theme

### Pass Templates (3 files)
- [ ] `pass_25nov2025.png` - Day 1
- [ ] `pass_26nov2025_morning.png` - Day 2 Morning
- [ ] `pass_26nov2025_plenary.png` - Day 2 Plenary

### QR Code Specs
- Day 1: 220x220px, Brown on Beige
- Day 2 Morning: 400x400px, Navy Blue on Gray
- Day 2 Plenary: 400x400px, Brown on White

---

## 💻 Tech Stack

### Web App (Registration)
- Streamlit + Python
- PostgreSQL + Redis
- Mailjet (emails)

### Mobile App (Scanner)
- Flutter (Android + iOS)
- QR Scanner
- Offline support

### API
- FastAPI
- JWT authentication
- REST endpoints

---

## 🗄️ Database

### Main Tables
1. `users` - Organizations (54 orgs)
2. `entries` - Attendees (1,500+ expected)
3. `check_ins` - Venue check-ins
4. `scanner_devices` - Mobile scanners (4 gates)
5. `audit_log` - Security audit

---

## 🚪 Gates Setup

### Day 1 (Nov 25)
- **Gate 1**: Exhibition Hall
- **Gate 2**: Kota House (dinner)

### Day 2 (Nov 26)
- **Gate 3**: Zorawar Hall (morning)
- **Gate 4**: Zorawar Hall (plenary)

---

## 📧 Email Templates

3 different emails for each pass type:
1. Day 1 Pass Email
2. Day 2 Morning Pass Email
3. Day 2 Plenary Pass Email

Each includes:
- Event details
- Schedule
- Venue map
- Dos & Don'ts
- QR code pass

---

## 🔐 Security

### Authentication
- ✅ bcrypt password hashing
- ✅ JWT tokens (15-min expiry)
- ✅ Role-based access (User/Admin/Scanner)

### Pass Security
- ✅ Cryptographic HMAC signatures
- ✅ Hashed ID numbers (SHA-256)
- ✅ Time-based validation
- ✅ Duplicate check-in prevention

### Data Protection
- ✅ HTTPS only (TLS 1.3)
- ✅ PostgreSQL encryption
- ✅ Audit logging (all actions)

---

## 📊 Key Features

### Registration System
- ✅ User login (54 organizations)
- ✅ Add attendees (bulk CSV upload)
- ✅ Photo upload (optional)
- ✅ Generate passes (3 types)
- ✅ Email delivery
- ✅ Dinner invitation management
- ✅ Admin dashboard

### Scanner App
- ✅ QR code scanning
- ✅ Real-time verification
- ✅ Offline mode
- ✅ Photo verification
- ✅ Duplicate prevention
- ✅ Gate/session selection
- ✅ Attendance tracking

---

## 📅 Timeline

| Phase | Duration | Key Tasks |
|-------|----------|-----------|
| Design | Week 1-2 | Logo, pass templates, venue maps |
| Registration | Week 3-4 | Build web app |
| Scanner | Week 5-6 | Build mobile app |
| API | Week 6-7 | FastAPI backend |
| Testing | Week 7-8 | Security audit, UAT |
| Deployment | Week 8-9 | Go live |
| Event | Nov 25-26 | Swavlamban 2025 |

---

## ❓ Outstanding Questions

### Critical
1. ❓ Organizations list (54 orgs confirmed?)
2. ❓ Entry quotas per organization
3. ❓ Dinner invitation approval process
4. ❓ Who creates design assets?

### Important
5. ❓ Budget for infrastructure
6. ❓ UAT timeline
7. ❓ Support team during event

---

## 📞 Quick Contacts

- **Documentation**: [CLAUDE.md](CLAUDE.md)
- **Event Details**: [SWAVLAMBAN_2025_CONFIRMED_DETAILS.md](SWAVLAMBAN_2025_CONFIRMED_DETAILS.md)
- **Tech Plan**: [SWAVLAMBAN_2025_PROJECT_PLAN.md](SWAVLAMBAN_2025_PROJECT_PLAN.md)
- **Design Specs**: [IMAGE_ASSETS_ANALYSIS.md](IMAGE_ASSETS_ANALYSIS.md)

---

## 🎯 Success Metrics

- ✅ 1,500+ registrations handled
- ✅ < 2 sec pass generation
- ✅ < 1 sec check-in time
- ✅ 99.9% uptime
- ✅ Zero security breaches

---

## 🚀 Next Steps

1. ✅ Review & approve this plan
2. ⏳ Confirm organizations & quotas
3. ⏳ Update design assets
4. ⏳ Start development (Week 3)

---

**Status**: ✅ Planning Complete
**Last Updated**: 2025-10-18
**Ready to Start**: Awaiting approvals
