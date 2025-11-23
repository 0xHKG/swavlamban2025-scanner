# Public Event Information Website - Deployment Guide

## Overview
The public event information website (`event_info_public.py`) is a standalone Streamlit app that provides all event information without requiring authentication. It can be shared publicly with all attendees.

## Features
- ✅ **No Authentication** - Anyone can access
- ✅ **All Event Information** - Venue, Schedule, Guidelines, FAQs
- ✅ **All Images** - Venue maps, Event Flow, DND guidelines
- ✅ **Mobile Responsive** - Works on all devices
- ✅ **FREE to Deploy** - No additional cost on Streamlit Cloud

## What's Included

### 📍 Tab 1: Venue & Directions
- Manekshaw Centre location and address
- Venue map (venue.png)
- Google Maps navigation button
- Metro and car directions
- Parking information
- Arrival instructions

### ⏰ Tab 2: Event Schedule
- Day 1 (25 Nov) - Exhibition schedule table
- Day 2 (26 Nov) - Morning & afternoon sessions
- Interactive Sessions timings (Session I & II)
- Plenary Session details
- Event flow images (EF-25.png, EF-AM26.png, EF-PM26.png)

### 📋 Tab 3: Guidelines (DOs & DONTs)
- Exhibition Hall guidelines (DND_Exhibition.png)
- Interactive Sessions guidelines (DND_Interactive.png)
- Plenary Session guidelines (DND_Plenary.png)

### 📞 Tab 4: Important Information
- Contact details (phone: 011-26771528, email: niio-tdac@navy.gov.in)
- Support hours
- FAQs (What to bring, Entry process, Parking, Lost pass)
- Quick reference guide
- Dress code information

## How to Deploy on Streamlit Cloud

### Step 1: Go to Streamlit Cloud
1. Visit https://share.streamlit.io/
2. Log in with your GitHub account (same account that has the swavlamban2025 repo)

### Step 2: Create New App
1. Click **"New app"** button
2. Select your repository: `0xHKG/swavlamban2025` (or your username)
3. Select branch: `main`
4. **CRITICAL:** Click **"Advanced settings..."** button
5. In **Advanced settings**:
   - **Main file path:** `event_info_public.py`
   - **Requirements file:** `requirements_public.txt` (⚠️ IMPORTANT - Not requirements.txt!)
   - Leave other settings as default
6. **App URL:** Choose a custom URL like:
   - `swavlamban2025-info`
   - `swavlamban-event-info`
   - `swavlamban2025-public`
7. Click **"Deploy!"**

### Why requirements_public.txt?
The public app uses `requirements_public.txt` (minimal dependencies) instead of `requirements.txt` (full dependencies) because:
- ✅ `requirements_public.txt` - Only has Streamlit (no database, no email services)
- ❌ `requirements.txt` - Has PostgreSQL, email services (not needed for public app)
- Using the wrong file will cause deployment to fail with psycopg2 errors!

### Step 3: No Secrets Needed
Unlike the main app, this public app **DOES NOT NEED** any secrets because:
- ❌ No database connection
- ❌ No authentication
- ❌ No email services
- ✅ Just displays static event information

### Step 4: Wait for Deployment
- Deployment takes 2-3 minutes
- You'll see installation logs
- App will automatically start once ready

### Step 5: Get Your Public URL
Once deployed, you'll get a URL like:
- `https://swavlamban2025-info.streamlit.app`
- `https://swavlamban-event-info.streamlit.app`

**Share this URL with all attendees!**

## Two Apps, Same Repo

You'll now have **TWO separate apps** from the same repository:

| App | URL | Purpose | Access |
|-----|-----|---------|--------|
| **Main App** | `swavlamban2025.streamlit.app` | Registration & Pass Management | Login required (Organizations only) |
| **Public Info** | `swavlamban2025-info.streamlit.app` | Event Information Hub | Public (Anyone can access) |

## Use Cases

### Who should access the Public Info website?
- ✅ All registered attendees
- ✅ People interested in the event
- ✅ Organizations planning to attend
- ✅ Anyone needing event details

### What can they do?
- View complete event schedule
- Get venue directions and maps
- Review DOs & DON'Ts guidelines
- Find contact information
- Read FAQs about entry, parking, etc.

### What can't they do?
- ❌ Register for the event (must use main app)
- ❌ Generate passes (must use main app)
- ❌ Access attendee data (must use main app)

## Sharing the Public Website

Once deployed, share the URL via:
- 📧 Email announcements to all registered attendees
- 📱 WhatsApp/SMS
- 🌐 Event website
- 📄 QR code on posters/flyers
- 💌 Include in pass confirmation emails

## Benefits

1. **Reduced Support Queries**
   - All information centralized in one place
   - FAQs answer common questions
   - Contact details clearly visible

2. **Better Attendee Experience**
   - Easy access without login
   - Mobile-friendly design
   - Complete event information

3. **No Cost**
   - FREE deployment on Streamlit Cloud
   - No additional infrastructure needed
   - Reuses existing images and assets

4. **Easy Updates**
   - Update `event_info_public.py` in repo
   - Changes automatically deploy
   - Same repo = single source of truth

## Troubleshooting

### Deployment fails with psycopg2 error?
**Error message:** `Error: pg_config executable not found` or `psycopg2-binary` build failed

**Cause:** You're using `requirements.txt` instead of `requirements_public.txt`

**Solution:**
1. Go to Streamlit Cloud app settings
2. Click "Advanced settings"
3. Change **Requirements file** from `requirements.txt` to `requirements_public.txt`
4. Click "Save" and redeploy

**Why?** The public app doesn't need PostgreSQL database, so it shouldn't install psycopg2!

### Images not loading?
- Check that `backend/images/` directory exists in repo
- Verify image files are committed to Git
- Image paths: `backend/images/venue.png`, `backend/images/EF/`, `backend/images/DND/`

### App won't start?
- Check Streamlit Cloud logs for errors
- Verify `event_info_public.py` is committed to main branch
- Ensure file path is correct: `event_info_public.py` (not `frontend/app.py`)
- Ensure requirements file is: `requirements_public.txt` (not `requirements.txt`)

### Want to customize?
- Edit `event_info_public.py` directly
- Commit and push changes to GitHub
- App will automatically redeploy with updates

## Testing Locally (Optional)

To test the public app on your local machine:

```bash
# Navigate to repo directory
cd "Swavlamban 2025/swavlamban2025"

# Run the public app
streamlit run event_info_public.py
```

Open http://localhost:8501 in your browser to test.

## Support

For questions about deployment:
- Streamlit Cloud docs: https://docs.streamlit.io/streamlit-community-cloud
- GitHub repo: https://github.com/0xHKG/swavlamban2025

---

**Ready to deploy!** Follow the steps above to make your event information publicly accessible. 🚀
