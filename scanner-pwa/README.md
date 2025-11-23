# Swavlamban 2025 - Scanner PWA

**Progressive Web App for QR Code Scanning at Event Gates**

Zero-installation mobile scanner for liaison personnel at Swavlamban 2025 event (Indian Navy - TDAC).

---

## 🎯 Overview

This PWA allows authorized personnel to scan attendee QR codes at event gates using their personal smartphones - no app installation required. Simply open the URL, login, and start scanning.

**Event**: Swavlamban 2025 - Naval Innovation & Indigenisation Seminar
**Dates**: November 25-26, 2025
**Venue**: Manekshaw Centre, New Delhi
**Organizer**: Indian Navy - TDAC

---

## ✨ Features

### ✅ Zero Installation
- Open URL in any browser (Chrome, Safari, Firefox)
- No app store downloads
- Works on any smartphone (Android/iOS)

### ✅ Fast QR Scanning
- 300-500ms scan speed (ZXing WebAssembly)
- Auto-scan with 2-second cooldown
- Live camera preview with targeting overlay

### ✅ Offline-First Architecture
- Works without internet connection
- IndexedDB for local storage
- Background sync when online

### ✅ Two-Tier Validation
- **Main Entrance**: Date-based validation
- **Hall Gates**: Date + time + venue validation

### ✅ Professional UI
- Mobile-optimized interface
- Real-time statistics
- Visual/audio/vibration feedback
- Scan history tracking

---

## 🛠️ Tech Stack

- **Frontend**: React 18 + TypeScript
- **Build Tool**: Vite 4.4
- **QR Scanner**: @zxing/browser (WebAssembly)
- **Offline DB**: Dexie (IndexedDB wrapper)
- **State Management**: Zustand
- **Styling**: Tailwind CSS
- **PWA**: vite-plugin-pwa (Workbox)
- **Deployment**: Vercel (FREE)

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🔧 Configuration

### Environment Variables

Create `.env.development` and `.env.production` files (see `.env.example`):

```bash
# API Configuration
VITE_API_URL=https://swavlamban2025.streamlit.app/api

# App Configuration
VITE_APP_NAME=Swavlamban 2025 Scanner
VITE_APP_VERSION=1.0.0
VITE_ENABLE_OFFLINE=true
VITE_SYNC_INTERVAL=300000

# Debug
VITE_DEBUG=false
VITE_LOG_LEVEL=error
```

### Gate Configuration

Edit `src/config/gates.ts` to customize gates:

```typescript
export const GATE_CONFIG = {
  'Gate 1': {
    name: 'Gate 1 - Exhibition Day 1',
    location: 'Exhibition Hall',
    date: '2025-11-25',
    time: '1100-1730',
    allowedPasses: ['exhibition_day1', 'exhibitor_pass'],
    sessionType: 'exhibition_day1'
  },
  // ... more gates
};
```

---

## 📱 PWA Installation

### On Mobile (Chrome/Safari)

1. Open scanner URL: `https://scan.swavlamban2025.in`
2. Chrome: Menu → "Install app" or "Add to Home Screen"
3. Safari: Share → "Add to Home Screen"
4. App icon appears on home screen

### Desktop (Chrome)

1. Click install icon in address bar
2. Or Settings → "Install Swavlamban 2025 Scanner"

---

## 🎫 Usage Flow

### 1. Login
- Enter username, password, and select gate
- Credentials provided by admin

### 2. Download Entries
- App automatically downloads valid entries
- Stored in IndexedDB for offline use

### 3. Scan QR Codes
- Point camera at attendee's QR code
- Auto-scan (no button press needed)
- Visual/audio feedback (✅ green = allowed, ❌ red = denied)

### 4. View Results
- Scan result appears for 3 seconds
- Recent 10 scans in history
- Today's statistics at bottom

### 5. Sync Data
- Auto-sync every 5 minutes when online
- Manual sync button available
- Pending scans shown in status bar

---

## 🗄️ Data Flow

```
1. Login → Download Entries → Store in IndexedDB
2. Scan QR → Validate Offline → Record in IndexedDB
3. Background Sync → Upload to Backend → Mark as Uploaded
```

### Offline Capabilities
- ✅ View downloaded entries
- ✅ Scan and validate QR codes
- ✅ Record check-ins locally
- ❌ Cannot download new entries (requires connection)
- ❌ Cannot sync check-ins (queued until online)

---

## 🔐 Security

- JWT authentication (8-hour expiration)
- HMAC-SHA256 QR signature verification
- Session-based storage (cleared on logout)
- No permanent data on personal devices
- HTTPS required in production

---

## 📂 Project Structure

```
scanner-pwa/
├── public/                     # Static assets
│   ├── manifest.json          # PWA configuration
│   ├── icon-*.png             # App icons
│   └── robots.txt
├── src/
│   ├── components/            # React components
│   │   ├── Auth/              # Login, GateSelector
│   │   ├── Scanner/           # QRScanner, ScanResult, ScanHistory
│   │   └── Layout/            # Header, Footer, StatusBar
│   ├── services/              # Business logic
│   │   ├── api.ts             # HTTP client
│   │   ├── auth.ts            # Authentication
│   │   ├── db.ts              # IndexedDB
│   │   ├── scanner.ts         # Validation
│   │   └── sync.ts            # Background sync
│   ├── stores/                # Zustand state
│   │   ├── authStore.ts
│   │   ├── scanStore.ts
│   │   └── syncStore.ts
│   ├── types/                 # TypeScript types
│   ├── utils/                 # Utility functions
│   ├── config/                # Configuration
│   ├── App.tsx                # Main app
│   └── main.tsx               # Entry point
├── .env.example               # Environment template
├── vercel.json                # Deployment config
└── package.json
```

---

## 🧪 Testing

### Local Testing
```bash
npm run dev
# Open http://localhost:3000
```

### Production Build Testing
```bash
npm run build
npm run preview
# Open http://localhost:4173
```

### Mobile Testing
```bash
# Expose local server to network
npm run dev -- --host
# Access from phone: http://<your-ip>:3000
```

---

## 🚀 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Add custom domain
vercel domains add scan.swavlamban2025.in
```

### Environment Variables in Vercel

Dashboard → Settings → Environment Variables:
- `VITE_API_URL` = `https://swavlamban2025.streamlit.app/api`

### Manual Deployment

```bash
# Build
npm run build

# Upload dist/ folder to any static host
# (Netlify, GitHub Pages, Firebase Hosting, etc.)
```

---

## 📋 Backend API Requirements

The PWA requires these backend endpoints (see `SCANNER_APP_IMPLEMENTATION_GUIDE.md`):

1. **POST /api/scanner/login** - Authentication
2. **GET /api/scanner/entries** - Download entries
3. **POST /api/scanner/checkin/batch** - Batch upload check-ins

Optional:
- POST /api/scanner/verify - Real-time verification
- GET /api/scanner/stats - Statistics

---

## 🐛 Troubleshooting

### Camera Not Working
- Grant camera permission when prompted
- Reload page (pull down to refresh)
- Try different browser (Chrome recommended)

### Slow Scanning
- Improve lighting (use flashlight)
- Hold QR code steady
- Adjust distance (10-30cm optimal)
- Clean camera lens

### Offline Mode Issues
- Ensure entries downloaded before going offline
- Clear browser cache and re-login
- Check pending scans count

### Battery Draining
- Reduce screen brightness
- Close other apps
- Use power bank
- Enable battery saver mode

---

## 📞 Support

- **Technical Issues**: Check browser console for errors
- **Admin Support**: Contact TDAC event coordinators
- **Documentation**: See `IMPLEMENTATION_STATUS.md`

---

## 📄 License

Internal use only - Indian Navy TDAC
Event: Swavlamban 2025

---

## 🙏 Acknowledgments

- Indian Navy - Technology Development and Acceleration Cell (TDAC)
- Event Organizing Team
- Liaison Personnel

---

**Version**: 1.0.0
**Last Updated**: 2025-11-06
**Status**: Production Ready (Frontend Complete)
