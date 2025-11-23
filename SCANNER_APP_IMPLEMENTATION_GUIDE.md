# Scanner App Implementation Guide

**For Claude Code Web Development**

This document provides complete implementation details for building the Swavlamban 2025 Scanner Progressive Web App (PWA).

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Dependencies](#dependencies)
5. [API Specification](#api-specification)
6. [Database Schema](#database-schema)
7. [Component Architecture](#component-architecture)
8. [Implementation Steps](#implementation-steps)
9. [Local Development](#local-development)
10. [Deployment](#deployment)

---

## 📌 Project Overview

**Goal**: Build a Progressive Web App that allows liaison personnel to scan QR codes at event gates using their personal smartphones, with zero installation required.

**Key Features**:
- Zero installation (web-based)
- Fast QR scanning (300-500ms)
- Two-tier validation (main entrance + hall gates)
- Offline-first architecture
- Works on any modern smartphone

**Backend**: Existing FastAPI backend (already deployed)
**Frontend**: New React PWA (to be built)
**Deployment**: Vercel (free)

---

## 🛠️ Technology Stack

### Frontend PWA
```json
{
  "framework": "React 18.2.0",
  "language": "TypeScript 5.0",
  "qr-scanner": "@zxing/browser 0.1.1",
  "offline-db": "dexie 3.2.4",
  "state": "zustand 4.4.0",
  "ui": "tailwind 3.3.0",
  "build": "vite 4.4.0",
  "pwa": "vite-plugin-pwa 0.16.0"
}
```

### Backend API (Existing)
```json
{
  "framework": "FastAPI",
  "database": "PostgreSQL (Supabase)",
  "auth": "JWT",
  "hosting": "Streamlit Cloud"
}
```

---

## 📁 Project Structure

```
scanner-pwa/
├── public/
│   ├── manifest.json              # PWA manifest
│   ├── icon-192.png               # App icon 192x192
│   ├── icon-512.png               # App icon 512x512
│   ├── apple-touch-icon.png       # iOS icon
│   └── robots.txt
├── src/
│   ├── components/                # React components
│   │   ├── Auth/
│   │   │   ├── LoginForm.tsx      # Login screen
│   │   │   └── GateSelector.tsx   # Select gate number
│   │   ├── Scanner/
│   │   │   ├── QRScanner.tsx      # Camera + QR detection
│   │   │   ├── ScanResult.tsx     # Show scan result (success/fail)
│   │   │   └── ScanHistory.tsx    # Recent scans list
│   │   ├── Layout/
│   │   │   ├── Header.tsx         # Top bar (gate, operator, status)
│   │   │   ├── Footer.tsx         # Bottom stats + controls
│   │   │   └── StatusBar.tsx      # Online/offline indicator
│   │   └── Settings/
│   │       ├── SettingsPanel.tsx  # Scanner settings
│   │       └── SyncControl.tsx    # Manual sync button
│   ├── services/                  # Business logic
│   │   ├── api.ts                 # API client (fetch wrapper)
│   │   ├── auth.ts                # Authentication service
│   │   ├── scanner.ts             # Scan validation logic
│   │   ├── sync.ts                # Background sync
│   │   └── db.ts                  # IndexedDB wrapper
│   ├── stores/                    # State management
│   │   ├── authStore.ts           # Auth state (token, user, gate)
│   │   ├── scanStore.ts           # Scan state (history, stats)
│   │   └── syncStore.ts           # Sync state (online, pending)
│   ├── hooks/                     # Custom React hooks
│   │   ├── useQRScanner.ts        # QR scanner hook
│   │   ├── useValidation.ts       # Validation logic hook
│   │   ├── useOffline.ts          # Offline detection
│   │   └── useSync.ts             # Background sync hook
│   ├── types/                     # TypeScript types
│   │   ├── api.types.ts           # API request/response types
│   │   ├── entry.types.ts         # Entry/Pass types
│   │   ├── scan.types.ts          # Scan record types
│   │   └── gate.types.ts          # Gate configuration types
│   ├── utils/                     # Utility functions
│   │   ├── validation.ts          # Date/time validation
│   │   ├── crypto.ts              # HMAC signature verification
│   │   ├── datetime.ts            # Date/time helpers
│   │   └── feedback.ts            # Visual/audio feedback
│   ├── config/                    # Configuration
│   │   ├── gates.ts               # Gate configuration data
│   │   └── constants.ts           # App constants
│   ├── App.tsx                    # Main app component
│   ├── main.tsx                   # Entry point
│   ├── sw.ts                      # Service worker
│   └── index.css                  # Global styles
├── .env.development               # Dev environment vars
├── .env.production                # Prod environment vars
├── package.json                   # Dependencies
├── tsconfig.json                  # TypeScript config
├── vite.config.ts                 # Vite config
├── tailwind.config.js             # Tailwind config
└── vercel.json                    # Vercel deployment config
```

---

## 📦 Dependencies

### package.json

```json
{
  "name": "swavlamban-scanner",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@zxing/browser": "^0.1.1",
    "@zxing/library": "^0.20.0",
    "dexie": "^3.2.4",
    "dexie-react-hooks": "^1.1.7",
    "zustand": "^4.4.0",
    "date-fns": "^2.30.0",
    "clsx": "^2.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.0.0",
    "typescript": "^5.0.0",
    "vite": "^4.4.0",
    "vite-plugin-pwa": "^0.16.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.27",
    "eslint": "^8.45.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0"
  }
}
```

### vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['icon-192.png', 'icon-512.png', 'apple-touch-icon.png'],
      manifest: {
        name: 'Swavlamban 2025 Scanner',
        short_name: 'Scanner',
        description: 'QR Code Scanner for Swavlamban 2025 Event',
        theme_color: '#1f2937',
        background_color: '#ffffff',
        display: 'standalone',
        orientation: 'portrait',
        icons: [
          {
            src: 'icon-192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'icon-512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/.*\.supabase\.co\/.*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              expiration: {
                maxEntries: 100,
                maxAgeSeconds: 60 * 60 // 1 hour
              },
              networkTimeoutSeconds: 10
            }
          }
        ]
      }
    })
  ],
  server: {
    port: 3000,
    host: true
  }
});
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### tailwind.config.js

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
      },
      animation: {
        'pulse-success': 'pulse 0.5s cubic-bezier(0.4, 0, 0.6, 1)',
        'pulse-error': 'pulse 0.5s cubic-bezier(0.4, 0, 0.6, 1)',
      }
    },
  },
  plugins: [],
}
```

---

## 🌐 API Specification

### Base URL
```
Development: http://localhost:8000/api
Production: https://swavlamban2025.streamlit.app/api
```

### Authentication
All API requests (except login) require JWT token in header:
```
Authorization: Bearer <jwt_token>
```

---

### 1. Scanner Login

**Endpoint**: `POST /scanner/login`

**Request**:
```json
{
  "username": "gate1_scanner",
  "password": "SecurePassword123",
  "gate_number": "Gate 1"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2025-11-25T20:00:00Z",
  "gate_info": {
    "gate_number": "Gate 1",
    "gate_location": "Exhibition Hall",
    "session_type": "exhibition_day1",
    "operator": "gate1_scanner"
  }
}
```

**Response** (401 Unauthorized):
```json
{
  "success": false,
  "error": "Invalid credentials"
}
```

---

### 2. Download Valid Entries (for offline)

**Endpoint**: `GET /scanner/entries`

**Headers**:
```
Authorization: Bearer <token>
```

**Query Parameters**:
- `gate_number`: string (optional, filters by gate)
- `date`: string (YYYY-MM-DD, optional, filters by date)

**Response** (200 OK):
```json
{
  "success": true,
  "count": 1543,
  "entries": [
    {
      "entry_id": 1,
      "name": "Dr. Rashi Mehrotra",
      "organization": "TDAC",
      "mobile": "9876543210",
      "qr_signature": "a3f7b9c2e1d4f8a6b5c9e2f1a4b8c3d7",
      "passes": {
        "exhibition_day1": true,
        "exhibition_day2": true,
        "interactive_sessions": false,
        "plenary": true
      }
    },
    {
      "entry_id": 2,
      "name": "Col. Ashok Kumar",
      "organization": "Indian Army",
      "mobile": "9876543211",
      "qr_signature": "b4g8c0d3f2e5g9b7c6d0f3b5c4e8d9e4",
      "passes": {
        "exhibition_day1": false,
        "exhibition_day2": true,
        "interactive_sessions": true,
        "plenary": false
      }
    }
    // ... more entries
  ]
}
```

---

### 3. Verify QR Code (online validation)

**Endpoint**: `POST /scanner/verify`

**Headers**:
```
Authorization: Bearer <token>
```

**Request**:
```json
{
  "qr_data": "1:exhibition_day1:a3f7b9c2e1d4f8a6b5c9e2f1a4b8c3d7",
  "gate_number": "Gate 1",
  "scan_time": "2025-11-25T11:30:00Z"
}
```

**Response** (200 OK - Allowed):
```json
{
  "success": true,
  "allowed": true,
  "entry": {
    "entry_id": 1,
    "name": "Dr. Rashi Mehrotra",
    "organization": "TDAC",
    "pass_type": "exhibition_day1"
  },
  "message": "Welcome to Exhibition"
}
```

**Response** (200 OK - Rejected):
```json
{
  "success": true,
  "allowed": false,
  "reason": "This pass is for Day 2 (26 Nov)",
  "entry": {
    "entry_id": 1,
    "name": "Dr. Rashi Mehrotra",
    "organization": "TDAC"
  }
}
```

**Response** (400 Bad Request):
```json
{
  "success": false,
  "error": "Invalid QR code format"
}
```

---

### 4. Submit Check-In (record entry)

**Endpoint**: `POST /scanner/checkin`

**Headers**:
```
Authorization: Bearer <token>
```

**Request**:
```json
{
  "entry_id": 1,
  "session_type": "exhibition_day1",
  "session_name": "Exhibition Day 1",
  "gate_number": "Gate 1",
  "gate_location": "Exhibition Hall",
  "scanner_device_id": "samsung-a50-abc123",
  "scanner_operator": "gate1_scanner",
  "check_in_time": "2025-11-25T11:30:00Z",
  "verification_status": "verified",
  "notes": null
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "checkin_id": 4521,
  "message": "Check-in recorded successfully"
}
```

**Response** (409 Conflict - Duplicate):
```json
{
  "success": false,
  "error": "Duplicate check-in detected",
  "previous_checkin": {
    "time": "2025-11-25T11:25:00Z",
    "gate": "Gate 1"
  }
}
```

---

### 5. Batch Submit Check-Ins (offline sync)

**Endpoint**: `POST /scanner/checkin/batch`

**Headers**:
```
Authorization: Bearer <token>
```

**Request**:
```json
{
  "checkins": [
    {
      "entry_id": 1,
      "session_type": "exhibition_day1",
      "gate_number": "Gate 1",
      "check_in_time": "2025-11-25T11:30:00Z",
      "scanner_device_id": "samsung-a50-abc123",
      "scanner_operator": "gate1_scanner"
    },
    {
      "entry_id": 2,
      "session_type": "exhibition_day1",
      "gate_number": "Gate 1",
      "check_in_time": "2025-11-25T11:31:00Z",
      "scanner_device_id": "samsung-a50-abc123",
      "scanner_operator": "gate1_scanner"
    }
    // ... more check-ins
  ]
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "total": 25,
  "created": 23,
  "duplicates": 2,
  "errors": 0,
  "message": "Batch upload complete"
}
```

---

### 6. Get Scanner Stats

**Endpoint**: `GET /scanner/stats`

**Headers**:
```
Authorization: Bearer <token>
```

**Query Parameters**:
- `gate_number`: string (optional)
- `date`: string (YYYY-MM-DD, optional)

**Response** (200 OK):
```json
{
  "success": true,
  "stats": {
    "total_scans": 245,
    "successful": 240,
    "rejected": 5,
    "success_rate": 97.96,
    "last_sync": "2025-11-25T11:45:00Z",
    "by_hour": [
      { "hour": "11", "count": 120 },
      { "hour": "12", "count": 125 }
    ]
  }
}
```

---

### 7. Register Scanner Device

**Endpoint**: `POST /scanner/device/register`

**Headers**:
```
Authorization: Bearer <token>
```

**Request**:
```json
{
  "device_id": "samsung-a50-abc123",
  "device_name": "Samsung Galaxy A50",
  "gate_number": "Gate 1",
  "gate_location": "Exhibition Hall",
  "operator_username": "gate1_scanner"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Device registered successfully"
}
```

---

### 8. Heartbeat / Keep Alive

**Endpoint**: `POST /scanner/heartbeat`

**Headers**:
```
Authorization: Bearer <token>
```

**Request**:
```json
{
  "device_id": "samsung-a50-abc123",
  "gate_number": "Gate 1",
  "battery_level": 85,
  "is_online": true
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "server_time": "2025-11-25T11:30:00Z",
  "should_sync": true
}
```

---

## 🗄️ Database Schema

### Backend Tables (Existing PostgreSQL)

#### entries
```sql
CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    mobile VARCHAR(20),
    aadhar VARCHAR(12) UNIQUE,
    organization VARCHAR(255),

    -- Pass flags
    exhibition_day1 BOOLEAN DEFAULT FALSE,
    exhibition_day2 BOOLEAN DEFAULT FALSE,
    interactive_sessions BOOLEAN DEFAULT FALSE,
    plenary BOOLEAN DEFAULT FALSE,
    is_exhibitor_pass BOOLEAN DEFAULT FALSE,

    -- QR Signature (HMAC-SHA256)
    qr_signature_ex1 VARCHAR(64),
    qr_signature_ex2 VARCHAR(64),
    qr_signature_interactive VARCHAR(64),
    qr_signature_plenary VARCHAR(64),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### check_ins
```sql
CREATE TABLE check_ins (
    id SERIAL PRIMARY KEY,
    entry_id INTEGER REFERENCES entries(id) ON DELETE CASCADE,

    session_type VARCHAR(50) NOT NULL,  -- 'exhibition_day1', 'exhibition_day2', etc.
    session_name VARCHAR(255),

    check_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    gate_number VARCHAR(50),
    gate_location VARCHAR(255),

    scanner_device_id VARCHAR(100),
    scanner_operator VARCHAR(100),

    verification_status VARCHAR(50) DEFAULT 'verified',
    notes TEXT,

    INDEX idx_entry_id (entry_id),
    INDEX idx_session_type (session_type),
    INDEX idx_check_in_time (check_in_time)
);
```

#### scanner_devices
```sql
CREATE TABLE scanner_devices (
    device_id VARCHAR(100) PRIMARY KEY,
    device_name VARCHAR(255) NOT NULL,

    gate_number VARCHAR(50),
    gate_location VARCHAR(255),

    operator_username VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,

    last_sync TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Frontend Database (IndexedDB)

#### Schema Definition (Dexie.js)

```typescript
// src/services/db.ts
import Dexie, { Table } from 'dexie';

export interface Entry {
  entry_id: number;
  name: string;
  organization: string;
  mobile: string;
  qr_signature: string;
  passes: {
    exhibition_day1: boolean;
    exhibition_day2: boolean;
    interactive_sessions: boolean;
    plenary: boolean;
  };
  synced_at: Date;
}

export interface PendingScan {
  id?: number;
  entry_id: number;
  session_type: string;
  gate_number: string;
  gate_location: string;
  check_in_time: Date;
  scanner_device_id: string;
  scanner_operator: string;
  uploaded: boolean;
  created_at: Date;
}

export class ScannerDB extends Dexie {
  entries!: Table<Entry, number>;
  pending_scans!: Table<PendingScan, number>;

  constructor() {
    super('ScannerDB');
    this.version(1).stores({
      entries: 'entry_id, qr_signature, organization',
      pending_scans: '++id, entry_id, uploaded, check_in_time'
    });
  }
}

export const db = new ScannerDB();
```

---

## 🏗️ Component Architecture

### 1. LoginForm Component

**Purpose**: Authenticate scanner operator

**File**: `src/components/Auth/LoginForm.tsx`

```typescript
import { useState } from 'react';
import { useAuthStore } from '@/stores/authStore';
import { login } from '@/services/auth';

export function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const setAuth = useAuthStore(state => state.setAuth);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await login(username, password);
      setAuth(response.token, response.gate_info);
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-lg p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold text-center mb-6">
          Swavlamban 2025 Scanner
        </h1>

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
}
```

**Props**: None
**State**:
- `username`, `password` (form inputs)
- `loading` (submission state)
- `error` (error message)

---

### 2. GateSelector Component

**Purpose**: Select gate number after login

**File**: `src/components/Auth/GateSelector.tsx`

```typescript
import { useState } from 'react';
import { useAuthStore } from '@/stores/authStore';
import { GATE_CONFIG } from '@/config/gates';

export function GateSelector() {
  const [selectedGate, setSelectedGate] = useState('');
  const setGate = useAuthStore(state => state.setGate);

  const handleSelect = () => {
    if (selectedGate) {
      setGate(selectedGate);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-lg p-8 w-full max-w-md">
        <h2 className="text-xl font-bold mb-6">Select Your Gate</h2>

        <div className="space-y-3 mb-6">
          {Object.entries(GATE_CONFIG).map(([key, gate]) => (
            <button
              key={key}
              onClick={() => setSelectedGate(key)}
              className={`w-full p-4 border-2 rounded-lg text-left transition ${
                selectedGate === key
                  ? 'border-blue-600 bg-blue-50'
                  : 'border-gray-300 hover:border-blue-400'
              }`}
            >
              <div className="font-semibold">{gate.name}</div>
              <div className="text-sm text-gray-600">{gate.location}</div>
              <div className="text-xs text-gray-500">{gate.time}</div>
            </button>
          ))}
        </div>

        <button
          onClick={handleSelect}
          disabled={!selectedGate}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50"
        >
          Continue
        </button>
      </div>
    </div>
  );
}
```

**Props**: None
**State**: `selectedGate`

---

### 3. QRScanner Component

**Purpose**: Main scanner interface with camera

**File**: `src/components/Scanner/QRScanner.tsx`

```typescript
import { useEffect, useRef, useState } from 'react';
import { BrowserMultiFormatReader } from '@zxing/browser';
import { useScanStore } from '@/stores/scanStore';
import { useAuthStore } from '@/stores/authStore';
import { validateScan } from '@/services/scanner';
import { playFeedback } from '@/utils/feedback';

export function QRScanner() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [scanning, setScanning] = useState(false);
  const [lastScan, setLastScan] = useState<string | null>(null);

  const gateNumber = useAuthStore(state => state.gateNumber);
  const addScan = useScanStore(state => state.addScan);

  useEffect(() => {
    const codeReader = new BrowserMultiFormatReader();

    const startScanning = async () => {
      try {
        await codeReader.decodeFromVideoDevice(
          undefined, // Auto-select camera
          videoRef.current!,
          async (result, error) => {
            if (result) {
              const qrData = result.getText();

              // Prevent duplicate scans (2-second cooldown)
              if (qrData === lastScan) return;
              setLastScan(qrData);
              setTimeout(() => setLastScan(null), 2000);

              // Validate and record
              const scanResult = await validateScan(qrData, gateNumber);
              addScan(scanResult);

              // Visual/audio feedback
              playFeedback(scanResult.allowed);
            }
          }
        );

        setScanning(true);
      } catch (err) {
        console.error('Camera error:', err);
      }
    };

    startScanning();

    return () => {
      codeReader.reset();
    };
  }, [gateNumber, lastScan, addScan]);

  return (
    <div className="relative w-full h-96 bg-black rounded-lg overflow-hidden">
      <video
        ref={videoRef}
        className="w-full h-full object-cover"
        autoPlay
        playsInline
      />

      {!scanning && (
        <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white">
          <div className="text-center">
            <div className="text-xl mb-2">Starting camera...</div>
            <div className="text-sm">Please grant camera permission</div>
          </div>
        </div>
      )}

      {/* Scanner overlay */}
      <div className="absolute inset-0 border-4 border-blue-500 opacity-50 pointer-events-none">
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 border-4 border-white" />
      </div>
    </div>
  );
}
```

**Props**: None
**State**:
- `scanning` (camera active status)
- `lastScan` (prevent duplicate scans)

**Refs**: `videoRef` (video element for camera)

---

### 4. ScanResult Component

**Purpose**: Show scan result feedback

**File**: `src/components/Scanner/ScanResult.tsx`

```typescript
import { useEffect, useState } from 'react';
import { ScanRecord } from '@/types/scan.types';

interface Props {
  scan: ScanRecord | null;
}

export function ScanResult({ scan }: Props) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (scan) {
      setVisible(true);
      const timer = setTimeout(() => setVisible(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [scan]);

  if (!scan || !visible) return null;

  return (
    <div className={`p-4 rounded-lg mb-4 ${
      scan.allowed ? 'bg-green-100 border-green-500' : 'bg-red-100 border-red-500'
    } border-2`}>
      <div className="flex items-center justify-between mb-2">
        <div className="text-2xl">
          {scan.allowed ? '✅' : '❌'}
        </div>
        <div className="text-sm text-gray-600">
          {new Date(scan.scan_time).toLocaleTimeString()}
        </div>
      </div>

      <div className="font-semibold text-lg">{scan.name}</div>
      <div className="text-sm text-gray-700">{scan.organization}</div>
      <div className="text-sm text-gray-600">{scan.pass_type}</div>

      <div className={`mt-2 font-semibold ${
        scan.allowed ? 'text-green-700' : 'text-red-700'
      }`}>
        {scan.allowed ? scan.message : scan.reason}
      </div>
    </div>
  );
}
```

**Props**:
- `scan`: ScanRecord | null (current scan result)

---

### 5. Header Component

**Purpose**: Top bar with gate info and status

**File**: `src/components/Layout/Header.tsx`

```typescript
import { useAuthStore } from '@/stores/authStore';
import { useSyncStore } from '@/stores/syncStore';
import { useEffect, useState } from 'react';

export function Header() {
  const { gateNumber, operator } = useAuthStore();
  const isOnline = useSyncStore(state => state.isOnline);
  const [battery, setBattery] = useState(100);

  useEffect(() => {
    // Get battery level
    if ('getBattery' in navigator) {
      (navigator as any).getBattery().then((battery: any) => {
        setBattery(Math.round(battery.level * 100));
        battery.addEventListener('levelchange', () => {
          setBattery(Math.round(battery.level * 100));
        });
      });
    }
  }, []);

  return (
    <div className="bg-gray-800 text-white p-4">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-xl font-bold">🎫 Swavlamban 2025</div>
          <div className="text-sm">{gateNumber} • {operator}</div>
        </div>

        <div className="flex items-center gap-4 text-sm">
          <div className={`flex items-center gap-1 ${
            isOnline ? 'text-green-400' : 'text-red-400'
          }`}>
            <span>{isOnline ? '📶' : '📵'}</span>
            <span>{isOnline ? 'Online' : 'Offline'}</span>
          </div>

          <div className="flex items-center gap-1">
            <span>🔋</span>
            <span>{battery}%</span>
          </div>
        </div>
      </div>
    </div>
  );
}
```

**Props**: None
**State**: `battery` (battery level)

---

### 6. Footer Component

**Purpose**: Bottom bar with stats and controls

**File**: `src/components/Layout/Footer.tsx`

```typescript
import { useScanStore } from '@/stores/scanStore';
import { useAuthStore } from '@/stores/authStore';
import { useSync } from '@/hooks/useSync';

export function Footer() {
  const stats = useScanStore(state => state.stats);
  const logout = useAuthStore(state => state.logout);
  const { syncNow, syncing } = useSync();

  const successRate = stats.total > 0
    ? ((stats.successful / stats.total) * 100).toFixed(1)
    : 0;

  return (
    <div className="bg-gray-100 border-t p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="text-sm">
          <span className="font-semibold">Today:</span> {stats.total} scans
        </div>
        <div className="text-sm">
          <span className="font-semibold">Success:</span> {successRate}%
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2">
        <button className="px-4 py-2 bg-white border rounded-lg text-sm hover:bg-gray-50">
          ⚙️ Settings
        </button>

        <button
          onClick={syncNow}
          disabled={syncing}
          className="px-4 py-2 bg-white border rounded-lg text-sm hover:bg-gray-50 disabled:opacity-50"
        >
          {syncing ? '⏳' : '🔄'} Sync
        </button>

        <button
          onClick={logout}
          className="px-4 py-2 bg-red-500 text-white rounded-lg text-sm hover:bg-red-600"
        >
          🚪 Logout
        </button>
      </div>
    </div>
  );
}
```

**Props**: None

---

## 🔧 Implementation Steps

### Phase 1: Project Setup (Day 1)

**Step 1.1: Create React Project**

```bash
npm create vite@latest scanner-pwa -- --template react-ts
cd scanner-pwa
```

**Step 1.2: Install Dependencies**

```bash
npm install react react-dom @zxing/browser @zxing/library dexie dexie-react-hooks zustand date-fns clsx
npm install -D @types/react @types/react-dom @vitejs/plugin-react typescript vite vite-plugin-pwa tailwindcss autoprefixer postcss eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser
```

**Step 1.3: Initialize Tailwind**

```bash
npx tailwindcss init -p
```

**Step 1.4: Create Project Structure**

```bash
mkdir -p src/{components/{Auth,Scanner,Layout,Settings},services,stores,hooks,types,utils,config}
```

---

### Phase 2: Backend API (Day 2-3)

**Step 2.1: Create API Endpoints**

Create file: `backend/app/api/scanner.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import jwt

from ..core.database import get_db
from ..core.security import verify_password, create_access_token
from ..models.entry import Entry
from ..models.checkin import CheckIn
from ..models.scanner_device import ScannerDevice
from ..schemas.scanner import (
    ScannerLoginRequest,
    ScannerLoginResponse,
    CheckInCreate,
    CheckInBatch
)

router = APIRouter(prefix="/scanner", tags=["scanner"])

@router.post("/login", response_model=ScannerLoginResponse)
def scanner_login(request: ScannerLoginRequest, db: Session = Depends(get_db)):
    """Login for scanner operators"""
    # Verify credentials (use scanner-specific users)
    # Create JWT token
    # Return token + gate info
    pass

@router.get("/entries")
def get_entries(db: Session = Depends(get_db), token: str = Depends(verify_token)):
    """Download all valid entries for offline use"""
    entries = db.query(Entry).all()
    return {
        "success": True,
        "count": len(entries),
        "entries": [format_entry(e) for e in entries]
    }

@router.post("/checkin")
def create_checkin(checkin: CheckInCreate, db: Session = Depends(get_db)):
    """Record a single check-in"""
    # Check for duplicates
    # Create check-in record
    # Return success
    pass

@router.post("/checkin/batch")
def batch_checkin(batch: CheckInBatch, db: Session = Depends(get_db)):
    """Batch upload check-ins (offline sync)"""
    # Process multiple check-ins
    # Handle duplicates gracefully
    # Return summary
    pass
```

**Step 2.2: Create Schema Definitions**

Create file: `backend/app/schemas/scanner.py`

```python
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ScannerLoginRequest(BaseModel):
    username: str
    password: str
    gate_number: str

class ScannerLoginResponse(BaseModel):
    success: bool
    token: str
    expires_at: datetime
    gate_info: dict

class CheckInCreate(BaseModel):
    entry_id: int
    session_type: str
    gate_number: str
    gate_location: str
    check_in_time: datetime
    scanner_device_id: str
    scanner_operator: str

class CheckInBatch(BaseModel):
    checkins: List[CheckInCreate]
```

**Step 2.3: Add Routes to Main App**

In `backend/app/main.py`:

```python
from .api import scanner

app.include_router(scanner.router, prefix="/api")
```

---

### Phase 3: Frontend Core (Day 4-5)

**Step 3.1: Setup Configuration**

Create file: `src/config/gates.ts`

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
  'Gate 2': {
    name: 'Gate 2 - Exhibition Day 2',
    location: 'Exhibition Hall',
    date: '2025-11-26',
    time: '1000-1730',
    allowedPasses: ['exhibition_day2', 'exhibitor_pass'],
    sessionType: 'exhibition_day2'
  },
  'Gate 3': {
    name: 'Gate 3 - Interactive Sessions',
    location: 'Zorawar Hall',
    date: '2025-11-26',
    time: '1020-1330',
    allowedPasses: ['interactive_sessions'],
    sessionType: 'interactive_sessions'
  },
  'Gate 4': {
    name: 'Gate 4 - Plenary Session',
    location: 'Zorawar Hall',
    date: '2025-11-26',
    time: '1500-1615',
    allowedPasses: ['plenary'],
    sessionType: 'plenary'
  },
  'Main Entrance': {
    name: 'Main Entrance',
    location: 'Manekshaw Centre',
    tier: 1,
    allowedPasses: [] // All passes (date-specific)
  }
} as const;
```

**Step 3.2: Create Type Definitions**

Create file: `src/types/scan.types.ts`

```typescript
export interface ScanRecord {
  id?: number;
  entry_id: number;
  name: string;
  organization: string;
  pass_type: string;
  gate_number: string;
  scan_time: Date;
  allowed: boolean;
  reason?: string;
  message?: string;
  uploaded: boolean;
}

export interface ScanStats {
  total: number;
  successful: number;
  rejected: number;
}
```

**Step 3.3: Create API Service**

Create file: `src/services/api.ts`

```typescript
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export async function apiCall(
  endpoint: string,
  options: RequestInit = {}
): Promise<any> {
  const token = sessionStorage.getItem('scanner_token');

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'API request failed');
  }

  return response.json();
}
```

**Step 3.4: Create Auth Service**

Create file: `src/services/auth.ts`

```typescript
import { apiCall } from './api';

export async function login(username: string, password: string, gateNumber: string) {
  const response = await apiCall('/scanner/login', {
    method: 'POST',
    body: JSON.stringify({ username, password, gate_number: gateNumber })
  });

  sessionStorage.setItem('scanner_token', response.token);
  return response;
}

export function logout() {
  sessionStorage.clear();
  window.location.reload();
}
```

**Step 3.5: Create IndexedDB Service**

Create file: `src/services/db.ts`

```typescript
import Dexie, { Table } from 'dexie';

export interface Entry {
  entry_id: number;
  name: string;
  organization: string;
  mobile: string;
  qr_signature: string;
  passes: {
    exhibition_day1: boolean;
    exhibition_day2: boolean;
    interactive_sessions: boolean;
    plenary: boolean;
  };
}

export interface PendingScan {
  id?: number;
  entry_id: number;
  session_type: string;
  gate_number: string;
  check_in_time: Date;
  uploaded: boolean;
}

export class ScannerDB extends Dexie {
  entries!: Table<Entry, number>;
  pending_scans!: Table<PendingScan, number>;

  constructor() {
    super('ScannerDB');
    this.version(1).stores({
      entries: 'entry_id, qr_signature',
      pending_scans: '++id, uploaded'
    });
  }
}

export const db = new ScannerDB();
```

---

### Phase 4: State Management (Day 6)

**Step 4.1: Create Auth Store**

Create file: `src/stores/authStore.ts`

```typescript
import { create } from 'zustand';

interface AuthState {
  token: string | null;
  gateNumber: string | null;
  operator: string | null;
  setAuth: (token: string, gateInfo: any) => void;
  setGate: (gate: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: sessionStorage.getItem('scanner_token'),
  gateNumber: sessionStorage.getItem('gate_number'),
  operator: sessionStorage.getItem('operator'),

  setAuth: (token, gateInfo) => {
    sessionStorage.setItem('scanner_token', token);
    sessionStorage.setItem('operator', gateInfo.operator);
    set({ token, operator: gateInfo.operator });
  },

  setGate: (gate) => {
    sessionStorage.setItem('gate_number', gate);
    set({ gateNumber: gate });
  },

  logout: () => {
    sessionStorage.clear();
    set({ token: null, gateNumber: null, operator: null });
    window.location.reload();
  }
}));
```

**Step 4.2: Create Scan Store**

Create file: `src/stores/scanStore.ts`

```typescript
import { create } from 'zustand';
import { ScanRecord, ScanStats } from '@/types/scan.types';

interface ScanState {
  recentScans: ScanRecord[];
  stats: ScanStats;
  addScan: (scan: ScanRecord) => void;
  clearScans: () => void;
}

export const useScanStore = create<ScanState>((set) => ({
  recentScans: [],
  stats: { total: 0, successful: 0, rejected: 0 },

  addScan: (scan) => set((state) => {
    const newScans = [scan, ...state.recentScans].slice(0, 10);
    const newStats = {
      total: state.stats.total + 1,
      successful: scan.allowed ? state.stats.successful + 1 : state.stats.successful,
      rejected: !scan.allowed ? state.stats.rejected + 1 : state.stats.rejected
    };

    return {
      recentScans: newScans,
      stats: newStats
    };
  }),

  clearScans: () => set({ recentScans: [], stats: { total: 0, successful: 0, rejected: 0 } })
}));
```

---

### Phase 5: Validation Logic (Day 7)

**Step 5.1: Create Validation Utils**

Create file: `src/utils/validation.ts`

```typescript
import { format, isAfter, isBefore, parse } from 'date-fns';

export function validateDateTime(
  currentDate: Date,
  currentTime: string,
  allowedDate: string,
  timeRange: string
): { valid: boolean; reason?: string } {
  // Check date
  const dateStr = format(currentDate, 'yyyy-MM-dd');
  if (dateStr !== allowedDate) {
    return { valid: false, reason: 'Wrong date for this pass' };
  }

  // Check time range
  const [startTime, endTime] = timeRange.split('-');
  if (currentTime < startTime || currentTime > endTime) {
    return { valid: false, reason: `Gates open ${timeRange}` };
  }

  return { valid: true };
}

export function parseQRData(qrString: string): {
  entry_id: number;
  pass_type: string;
  signature: string;
} | null {
  const parts = qrString.split(':');
  if (parts.length !== 3) return null;

  return {
    entry_id: parseInt(parts[0]),
    pass_type: parts[1],
    signature: parts[2]
  };
}
```

**Step 5.2: Create Scanner Service**

Create file: `src/services/scanner.ts`

```typescript
import { db } from './db';
import { parseQRData } from '@/utils/validation';
import { GATE_CONFIG } from '@/config/gates';
import { ScanRecord } from '@/types/scan.types';

export async function validateScan(
  qrData: string,
  gateNumber: string
): Promise<ScanRecord> {
  // Parse QR code
  const parsed = parseQRData(qrData);
  if (!parsed) {
    return createErrorResult('Invalid QR code format');
  }

  // Find entry in offline database
  const entry = await db.entries
    .where('entry_id')
    .equals(parsed.entry_id)
    .first();

  if (!entry) {
    return createErrorResult('Entry not found');
  }

  // Verify signature
  if (entry.qr_signature !== parsed.signature) {
    return createErrorResult('Invalid QR signature');
  }

  // Get gate config
  const gate = GATE_CONFIG[gateNumber];
  if (!gate) {
    return createErrorResult('Invalid gate');
  }

  // Check if pass type is allowed at this gate
  if (!gate.allowedPasses.includes(parsed.pass_type)) {
    return createErrorResult('Wrong pass for this gate');
  }

  // Check date/time (simplified)
  const now = new Date();
  const currentDate = format(now, 'yyyy-MM-dd');
  const currentTime = format(now, 'HHmm');

  if (currentDate !== gate.date) {
    return createErrorResult('Wrong date for this pass');
  }

  // Record scan in pending queue
  await db.pending_scans.add({
    entry_id: entry.entry_id,
    session_type: gate.sessionType,
    gate_number: gateNumber,
    check_in_time: now,
    uploaded: false
  });

  // Return success
  return {
    entry_id: entry.entry_id,
    name: entry.name,
    organization: entry.organization,
    pass_type: parsed.pass_type,
    gate_number: gateNumber,
    scan_time: now,
    allowed: true,
    message: 'Entry granted',
    uploaded: false
  };
}

function createErrorResult(reason: string): ScanRecord {
  return {
    entry_id: 0,
    name: 'Unknown',
    organization: 'Unknown',
    pass_type: 'unknown',
    gate_number: '',
    scan_time: new Date(),
    allowed: false,
    reason,
    uploaded: false
  };
}
```

---

### Phase 6: UI Components (Day 8-9)

Implement all components listed in the Component Architecture section above.

---

### Phase 7: Offline Sync (Day 10)

**Step 7.1: Create Sync Hook**

Create file: `src/hooks/useSync.ts`

```typescript
import { useEffect, useState } from 'react';
import { db } from '@/services/db';
import { apiCall } from '@/services/api';
import { useSyncStore } from '@/stores/syncStore';

export function useSync() {
  const [syncing, setSyncing] = useState(false);
  const setOnline = useSyncStore(state => state.setOnline);

  // Detect online/offline
  useEffect(() => {
    const updateOnlineStatus = () => {
      setOnline(navigator.onLine);
    };

    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);

    return () => {
      window.removeEventListener('online', updateOnlineStatus);
      window.removeEventListener('offline', updateOnlineStatus);
    };
  }, [setOnline]);

  // Auto-sync every 5 minutes
  useEffect(() => {
    const interval = setInterval(() => {
      if (navigator.onLine) {
        syncPendingScans();
      }
    }, 5 * 60 * 1000);

    return () => clearInterval(interval);
  }, []);

  const syncPendingScans = async () => {
    if (syncing) return;

    setSyncing(true);
    try {
      // Get pending scans
      const pending = await db.pending_scans
        .where('uploaded')
        .equals(false)
        .toArray();

      if (pending.length === 0) return;

      // Upload batch
      const response = await apiCall('/scanner/checkin/batch', {
        method: 'POST',
        body: JSON.stringify({ checkins: pending })
      });

      // Mark as uploaded
      await db.pending_scans
        .where('uploaded')
        .equals(false)
        .modify({ uploaded: true });

      console.log('Sync complete:', response);
    } catch (error) {
      console.error('Sync failed:', error);
    } finally {
      setSyncing(false);
    }
  };

  return {
    syncNow: syncPendingScans,
    syncing
  };
}
```

---

### Phase 8: Testing (Day 11-12)

**Test Checklist**:
- [ ] Login works on Android/iOS
- [ ] Camera activates correctly
- [ ] QR scanning detects codes
- [ ] Validation logic works correctly
- [ ] Offline mode stores data
- [ ] Background sync uploads data
- [ ] Battery usage acceptable
- [ ] Works on 5+ different devices

---

### Phase 9: Deployment (Day 13)

**Step 9.1: Build for Production**

```bash
npm run build
```

**Step 9.2: Deploy to Vercel**

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Add custom domain
vercel domains add scan.swavlamban2025.in
```

**Step 9.3: Configure Environment Variables**

In Vercel dashboard, add:
```
VITE_API_URL=https://swavlamban2025.streamlit.app/api
```

---

## 🚀 Local Development

### Setup Instructions

```bash
# 1. Clone repository
git clone https://github.com/0xHKG/swavlamban2025.git
cd swavlamban2025

# 2. Setup scanner PWA
cd scanner-pwa
npm install

# 3. Create .env.development
cat > .env.development << EOF
VITE_API_URL=http://localhost:8000/api
EOF

# 4. Run development server
npm run dev

# 5. Open browser
# Navigate to: http://localhost:3000
```

### Testing Without Backend

Create mock API server:

```typescript
// src/services/mockApi.ts
export const mockEntries = [
  {
    entry_id: 1,
    name: "Dr. Rashi Mehrotra",
    organization: "TDAC",
    mobile: "9876543210",
    qr_signature: "a3f7b9c2e1d4f8a6b5c9e2f1a4b8c3d7",
    passes: {
      exhibition_day1: true,
      exhibition_day2: true,
      interactive_sessions: false,
      plenary: true
    }
  }
];

export async function mockLogin() {
  return {
    token: 'mock-jwt-token',
    gate_info: {
      gate_number: 'Gate 1',
      operator: 'test_user'
    }
  };
}
```

---

## 📱 Deployment

### Vercel Deployment

**vercel.json**:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

### Custom Domain Setup

1. Add domain in Vercel dashboard
2. Update DNS records:
   ```
   Type: CNAME
   Name: scan
   Value: cname.vercel-dns.com
   ```
3. Wait for SSL certificate (auto)

---

## ✅ Success Criteria

**Functionality**:
- ✅ Login works
- ✅ Camera activates
- ✅ QR scanning works
- ✅ Validation correct
- ✅ Offline mode functional
- ✅ Sync works

**Performance**:
- ✅ Scan < 500ms
- ✅ Validation < 100ms
- ✅ No bottlenecks

**Compatibility**:
- ✅ Works on Android 8+
- ✅ Works on iOS 11.3+
- ✅ Works offline

---

## 📞 Support

**Technical Issues**:
- Check browser console for errors
- Verify camera permissions granted
- Test internet connectivity
- Clear browser cache if needed

**Backend Integration**:
- Ensure backend API is deployed
- Verify CORS settings allow PWA domain
- Check JWT token expiration
- Test API endpoints with Postman

---

**Document Version**: 1.0
**Last Updated**: 2025-11-06
**Status**: Ready for Implementation
**Next Step**: Begin Phase 1 - Project Setup
