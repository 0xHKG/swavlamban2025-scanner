# Swavlamban 2025 - Registration & Pass Management System

**Indian Navy's Naval Innovation & Indigenisation Organisation (NIIO) Seminar**

**Event Dates**: November 25-26, 2025
**Venue**: Manekshaw Centre (Exhibition Hall & Zorawar Hall)

---

## 🎯 Project Overview

Comprehensive registration and access control system for Swavlamban 2025, comprising:

1. **Web Registration System** (Streamlit + FastAPI)
2. **Mobile Scanner App** (Flutter)
3. **Admin Dashboard** (Streamlit)

### Key Features

- ✅ Multi-organization registration management
- ✅ QR code-based digital passes (5 types)
- ✅ Email delivery with event materials
- ✅ Mobile scanning with offline support
- ✅ Real-time analytics and reporting
- ✅ Time-based access validation
- ✅ Venue-specific gate control

---

## 🏗️ Architecture

```
┌─────────────────┐
│  Web Browsers   │ ──▶ Registration System (Streamlit)
└─────────────────┘
        │
        ▼
┌─────────────────┐
│  FastAPI        │ ──▶ REST API Layer
└─────────────────┘
        │
        ▼
┌─────────────────┐
│  PostgreSQL     │ ──▶ Database
│  Redis          │ ──▶ Cache/Sessions
└─────────────────┘
        ▲
        │
┌─────────────────┐
│  Flutter Mobile │ ──▶ Scanner App
└─────────────────┘
```

---

## 🎫 Pass Types

| Pass | Event | Date | Venue | File |
|------|-------|------|-------|------|
| Exhibition Day 1 | Exhibition viewing | 25 Nov | Exhibition Hall | EP-25.png |
| Exhibition Day 2 | Exhibition viewing | 26 Nov | Exhibition Hall | EP-26.png |
| Exhibitor Pass | Booth operation | 25-26 Nov | Exhibition Hall | EP-25n26.png |
| Interactive Sessions | Panel Discussions I & II | 26 Nov | Zorawar Hall | EP-INTERACTIVE.png |
| Plenary Session | VIP session with Hon'ble RM | 26 Nov | Zorawar Hall | EP-PLENARY.png |

---

## 🚀 Quick Start

See [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for detailed setup instructions.

---

## 📚 Documentation

- **[CLAUDE.md](CLAUDE.md)** - Complete project documentation
- **[DESIGN_ASSETS_STATUS.md](DESIGN_ASSETS_STATUS.md)** - Asset inventory
- **[DND_IMAGES_CRITICAL_NOTE.md](DND_IMAGES_CRITICAL_NOTE.md)** - DND images guide

---

## 📞 Support

**Technical Support**: support@swavlamban2025.in

---

**Built for Indian Navy's Swavlamban 2025**
