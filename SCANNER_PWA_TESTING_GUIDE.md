# Scanner PWA Testing Guide

**Complete guide to test the Scanner PWA with backend API**

---

## 📋 Prerequisites

Before testing, ensure you have:
- Python 3.11+ installed
- Node.js 18+ installed
- Backend dependencies installed
- Frontend dependencies installed (already done)

---

## 🚀 Quick Start Testing

### Step 1: Install Backend Dependencies

```bash
cd /home/user/swavlamban2025
pip3 install -r backend/requirements.txt
```

Or if using the frontend requirements (which includes backend):
```bash
pip3 install -r frontend/requirements.txt
```

### Step 2: Create Scanner User Account

**Option A: Using Python Script (Recommended)**
```bash
python3 create_scanner_user.py
```

**Option B: Using SQL (if Python has issues)**
```bash
# For SQLite
sqlite3 swavlamban2025.db < create_scanner_user.sql

# For PostgreSQL (Supabase)
psql -h db.scvzcvpyvmwzigusdjsl.supabase.co \
     -U postgres \
     -d postgres \
     -f create_scanner_user.sql
```

**Option C: Manual SQL (copy-paste into database tool)**
```sql
INSERT INTO users (
    username, password_hash, organization, max_entries, role,
    quota_ex_day1, quota_ex_day2, quota_interactive, quota_plenary,
    allowed_passes, is_active, created_at
) VALUES (
    'scanner1',
    '$2b$12$LKaGPj7QQYHJvZ9X1.vvnO8wYc3YqN6yJxH0vP6eJ5X7.aKZ5YH2m',
    'Gate Operations', 0, 'scanner',
    0, 0, 0, 0, '{}', 1, datetime('now')
);
```

### Step 3: Start Backend Server

```bash
cd /home/user/swavlamban2025
python3 -m backend.app.main
```

Expected output:
```
🗄️  Using SQLite database: /home/user/swavlamban2025/swavlamban2025.db
✅ Database initialized: sqlite:///swavlamban2025/swavlamban2025.db
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Backend API will be available at: **http://localhost:8000**

### Step 4: Verify Backend API

Open another terminal and test the API:

```bash
# Test root endpoint
curl http://localhost:8000/

# Test health check
curl http://localhost:8000/health

# Test API docs (open in browser)
open http://localhost:8000/docs
```

### Step 5: Start Frontend (Already Running)

The frontend dev server should already be running at:
**http://localhost:3000**

If not, start it:
```bash
cd /home/user/swavlamban2025/scanner-pwa
npm run dev
```

---

## 🧪 Testing the Scanner PWA

### Test Credentials

```
Username: scanner1
Password: scanner123
Gate: Any of the 5 gates
```

### Available Gates:
1. **Gate 1** - Exhibition Day 1 (25 Nov 2025)
2. **Gate 2** - Exhibition Day 2 (26 Nov 2025)
3. **Gate 3** - Interactive Sessions (26 Nov 2025)
4. **Gate 4** - Plenary Session (26 Nov 2025)
5. **Main Entrance** - Date-based validation (all passes)

### Test Flow

#### 1. Test Login
1. Open http://localhost:3000
2. Enter username: `scanner1`
3. Enter password: `scanner123`
4. Select gate: `Gate 1`
5. Click "Login"

**Expected Result:**
- JWT token received
- Redirected to scanner interface
- Gate info displayed in header

#### 2. Test Entry Download
After login, the app should automatically:
- Download all entries from `/api/v1/scanner/entries`
- Store entries in IndexedDB
- Show "Entries synced" message

**Verify in Browser DevTools:**
```javascript
// Open Console and run:
indexedDB.databases().then(console.log)
// Should show "ScannerDB"
```

#### 3. Test QR Scanning
1. Click "Start Scanner" or "Scan QR"
2. Allow camera access
3. Show a test QR code (format: `entryId:passType:signature`)

**Test QR Code Format:**
```
1:exhibition_day1:abc123def456
```

**Expected Result:**
- QR code recognized
- Validation performed locally (offline mode)
- Result displayed (green for success, red for error)
- Entry recorded in pending_scans table

#### 4. Test Offline Mode
1. Disconnect from internet (turn off WiFi)
2. Scan multiple QR codes
3. Check that scans are stored locally

**Verify:**
```javascript
// In Browser Console:
const db = await new Dexie('ScannerDB').open();
const pending = await db.table('pending_scans').toArray();
console.log('Pending scans:', pending);
```

#### 5. Test Sync (Reconnect)
1. Reconnect to internet
2. Wait 5 minutes OR click "Sync Now"
3. Pending scans should upload to backend

**Expected Result:**
- Batch POST to `/api/v1/scanner/checkin/batch`
- Pending scans uploaded
- Database updated
- Counter updates

---

## 🔍 Testing Backend API Directly

### Test with cURL

**1. Login:**
```bash
curl -X POST http://localhost:8000/api/v1/scanner/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "scanner1",
    "password": "scanner123",
    "gate_number": "Gate 1"
  }'
```

Expected response:
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2025-11-06T23:00:00",
  "operator": "scanner1",
  "gate_info": {
    "gate_number": "Gate 1",
    "name": "Gate 1 - Exhibition Day 1",
    "location": "Exhibition Hall",
    "date": "2025-11-25",
    "time": "1100-1730",
    "allowed_passes": ["exhibition_day1", "exhibitor_pass"],
    "session_type": "exhibition_day1"
  }
}
```

**2. Download Entries (use token from login):**
```bash
TOKEN="your-jwt-token-here"

curl -X GET http://localhost:8000/api/v1/scanner/entries \
  -H "Authorization: Bearer $TOKEN"
```

**3. Test Check-in:**
```bash
curl -X POST http://localhost:8000/api/v1/scanner/checkin \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "entry_id": 1,
    "session_type": "exhibition_day1",
    "gate_number": "Gate 1",
    "gate_location": "Exhibition Hall",
    "check_in_time": "2025-11-25T11:30:00",
    "scanner_device_id": "test-device-123",
    "scanner_operator": "scanner1"
  }'
```

**4. Test Batch Upload:**
```bash
curl -X POST http://localhost:8000/api/v1/scanner/checkin/batch \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "checkins": [
      {
        "entry_id": 1,
        "session_type": "exhibition_day1",
        "gate_number": "Gate 1",
        "gate_location": "Exhibition Hall",
        "check_in_time": "2025-11-25T11:30:00",
        "scanner_device_id": "test-device-123",
        "scanner_operator": "scanner1"
      }
    ]
  }'
```

**5. Get Statistics:**
```bash
curl -X GET "http://localhost:8000/api/v1/scanner/stats?gate_number=Gate 1" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📱 Testing on Mobile Devices

### Option 1: Using ngrok (Expose localhost to internet)

```bash
# Install ngrok
npm install -g ngrok

# Expose backend
ngrok http 8000

# Expose frontend
ngrok http 3000
```

Update `.env.development`:
```env
VITE_API_URL=https://your-ngrok-url.ngrok.io/api/v1
```

### Option 2: Deploy to Vercel

```bash
cd scanner-pwa
vercel --prod
```

Configure environment variable on Vercel:
```
VITE_API_URL=https://swavlamban2025.streamlit.app/api/v1
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'sqlalchemy'"
**Solution:**
```bash
pip3 install -r backend/requirements.txt
# OR
pip3 install sqlalchemy passlib bcrypt pyjwt
```

### Issue: "Database locked" (SQLite)
**Solution:**
- Close all database connections
- Restart backend server
- Use PostgreSQL for production

### Issue: "Invalid token" on API calls
**Solution:**
- Token expired (8-hour expiration)
- Login again to get new token
- Check Authorization header format: `Bearer <token>`

### Issue: Camera not working in browser
**Solution:**
- HTTPS required for camera access (or localhost)
- Grant camera permissions in browser
- Check browser compatibility (Chrome/Safari recommended)

### Issue: QR code not scanning
**Solution:**
- Ensure good lighting
- QR code must be in format: `entryId:passType:signature`
- Verify ZXing library loaded correctly

---

## 📊 Verification Checklist

- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 3000
- [ ] Scanner user created in database
- [ ] Login successful with test credentials
- [ ] JWT token received and stored
- [ ] Entries downloaded and stored in IndexedDB
- [ ] QR scanner interface visible
- [ ] Camera access granted
- [ ] Test QR code scans successfully
- [ ] Validation logic works (green/red feedback)
- [ ] Offline scans stored locally
- [ ] Sync uploads pending scans
- [ ] Statistics endpoint returns data

---

## 🎯 Production Deployment Checklist

Before deploying to production:

1. **Create Real Scanner Accounts:**
   ```sql
   INSERT INTO users (username, password_hash, organization, role)
   VALUES ('gate1_scanner', 'hashed_password', 'Gate 1 Operations', 'scanner');
   ```

2. **Update Environment Variables:**
   - Set production API URL in Vercel
   - Configure Supabase database connection
   - Set JWT secret key

3. **Test on Real Devices:**
   - Android phone (Chrome browser)
   - iPhone (Safari browser)
   - Test offline mode thoroughly

4. **Generate Real QR Codes:**
   - Use actual entry IDs from database
   - Include HMAC signatures
   - Test signature verification

5. **Train Scanner Operators:**
   - Login procedure
   - QR scanning workflow
   - Offline mode handling
   - Troubleshooting common issues

---

## 📞 Support

If you encounter issues:

1. Check browser console for errors (F12)
2. Check backend server logs
3. Verify database connection
4. Test API endpoints individually with cURL
5. Check network tab in DevTools

---

**Last Updated:** 2025-11-06
**Status:** Full stack ready for testing
**Next:** Install dependencies → Create user → Test!
