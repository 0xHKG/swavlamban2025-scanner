"""
Swavlamban 2025 - Public Event Information
A public-facing website providing all essential event information
No authentication required - Accessible to everyone
"""

import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Swavlamban 2025 - Event Information",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main container styling */
    .main {
        background: #ffffff;
    }

    /* Header styling - Navy blue background with WHITE text */
    .main-header {
        background: linear-gradient(135deg, #1D4E89 0%, #0D2E59 100%);
        color: white !important;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .main-header * {
        color: white !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background: #e9ecef;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        color: #1D4E89 !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1D4E89 0%, #0D2E59 100%);
    }

    .stTabs [aria-selected="true"] * {
        color: white !important;
    }

    /* Button styling */
    .nav-button {
        background: linear-gradient(135deg, #1D4E89 0%, #0D2E59 100%);
        color: white !important;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
        margin: 10px 0;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s;
    }
    .nav-button:hover {
        background: linear-gradient(135deg, #2563a8 0%, #1D4E89 100%);
        color: white !important;
        box-shadow: 0 4px 8px rgba(29, 78, 137, 0.4);
    }
    .nav-button:active, .nav-button:focus {
        background: linear-gradient(135deg, #0D2E59 0%, #1D4E89 100%);
        color: white !important;
        box-shadow: 0 2px 6px rgba(29, 78, 137, 0.6);
    }

    /* Info box styling */
    .stAlert {
        border-radius: 10px;
    }

    /* Dataframe styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Define paths to images (correct path in repo)
IMAGES_DIR = Path(__file__).parent / "images"

# Main header
st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 2.5rem; margin: 0;">🇮🇳 Swavlamban 2025</h1>
        <p style="font-size: 1.2rem; margin: 10px 0 0 0;">Indian Navy's Flagship Seminar on Innovation & Self-Reliance</p>
        <p style="font-size: 1rem; margin: 5px 0 0 0; opacity: 0.9;">25-26 November 2025 | Manekshaw Centre, New Delhi</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("# ℹ️ Event Information Hub")
st.markdown("*Your complete guide to Swavlamban 2025 - All essential information in one place*")
st.markdown("---")

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs([
    "📍 Venue & Directions",
    "⏰ Event Schedule",
    "📋 Guidelines (DOs & DON'Ts)",
    "📞 Important Info"
])

# TAB 1: Venue & Directions
with tab1:
    st.markdown("## 📍 Venue Information")

    # Venue details
    st.markdown("""
    ### Manekshaw Centre
    **Address:** H4QW+2MW, Khyber Lines, Delhi Cantonment, New Delhi, Delhi 110010

    The event will be held across two main venues within Manekshaw Centre:
    - **Zorawar Hall** - Main sessions (Interactive Sessions, Plenary)
    - **Exhibition Hall** - Industry exhibitions and booths
    """)

    # Navigation button with proper styling
    st.markdown("""
    <a href="https://www.google.com/maps/dir/?api=1&destination=28.586103304500742,77.14529897550334" target="_blank" style="text-decoration: none;">
        <button class="nav-button">
            📍 Open in Google Maps / Navigate
        </button>
    </a>
    """, unsafe_allow_html=True)

    st.info("💡 **Tip:** Click the button above to open navigation in your device's default maps app (Google Maps, Apple Maps, etc.)")

    # Venue map
    st.markdown("### 🗺️ Venue Map")
    venue_map_path = IMAGES_DIR / "venue.png"
    if venue_map_path.exists():
        st.image(str(venue_map_path), caption="Manekshaw Centre - Venue Layout", use_column_width=True)
    else:
        st.warning("Venue map will be available soon.")

    st.markdown("---")

    # Directions
    st.markdown("### 🚗 How to Reach")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **By Metro:**
        - Nearest Metro Station: **Dhaula Kuan** (Airport Express Line)
        - Distance: ~3 km from metro station
        - Auto/taxi available from station

        **By Car:**
        - Well connected via Ring Road
        - Use GPS: **H4QW+2MW** or click navigation button above
        - Ample parking available on premises
        """)

    with col2:
        st.markdown("""
        **Important Notes:**
        - ⏰ Please arrive 30 minutes before your session
        - 🎫 Keep your QR pass ready for scanning
        - 🪪 Valid Government ID required
        - 🚫 Security check at entrance
        """)

# TAB 2: Event Schedule
with tab2:
    st.markdown("## ⏰ Complete Event Schedule")

    # Day 1
    st.markdown("### Day 1 - Monday, 25 November 2025")
    st.markdown("**Venue: Exhibition Hall, Manekshaw Centre**")

    schedule_day1 = {
        "Time": ["1100 hrs", "1100 - 1730 hrs"],
        "Event": ["Gates Open", "Exhibition Open"],
        "Description": ["Entry begins for registered attendees", "Industry booths, innovation displays, networking"]
    }
    st.dataframe(schedule_day1, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Day 2
    st.markdown("### Day 2 - Tuesday, 26 November 2025")

    # Morning Session
    st.markdown("#### 🌅 Morning Sessions")
    st.markdown("**Venue: Exhibition Hall & Zorawar Hall, Manekshaw Centre**")

    schedule_day2_am = {
        "Time": ["1000 hrs", "1000 - 1730 hrs", "1030 - 1130 hrs", "1200 - 1330 hrs"],
        "Event": ["Gates Open", "Exhibition Open (Day 2)", "Interactive Session I", "Interactive Session II"],
        "Venue": ["Exhibition Hall", "Exhibition Hall", "Zorawar Hall", "Zorawar Hall"],
        "Description": ["Entry begins", "Continued exhibition", "Future & Emerging Technologies", "Boosting iDEX Ecosystem"]
    }
    st.dataframe(schedule_day2_am, use_container_width=True, hide_index=True)

    st.markdown("#### 🌆 Afternoon Session")
    st.markdown("**Venue: Zorawar Hall, Manekshaw Centre**")

    schedule_day2_pm = {
        "Time": ["1500 hrs", "1530 - 1615 hrs"],
        "Event": ["Gates Open", "Plenary Session"],
        "Description": ["Entry for Plenary Session", "CNS Welcome Address | Address by Chief Guest | Release of Books/Documents/MoUs | Discussions on Innovation & Self-reliance"]
    }
    st.dataframe(schedule_day2_pm, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Event Flow Images
    st.markdown("### 📊 Detailed Event Flow")

    col1, col2, col3 = st.columns(3)

    with col1:
        ef_25_path = IMAGES_DIR / "EF" / "EF-25.png"
        if ef_25_path.exists():
            st.image(str(ef_25_path), caption="25 Nov - Day 1 Schedule", use_column_width=True)
        else:
            st.info("Event Flow for 25 Nov will be available soon.")

    with col2:
        ef_am26_path = IMAGES_DIR / "EF" / "EF-AM26.png"
        if ef_am26_path.exists():
            st.image(str(ef_am26_path), caption="26 Nov - Morning Schedule", use_column_width=True)
        else:
            st.info("Event Flow for 26 Nov AM will be available soon.")

    with col3:
        ef_pm26_path = IMAGES_DIR / "EF" / "EF-PM26.png"
        if ef_pm26_path.exists():
            st.image(str(ef_pm26_path), caption="26 Nov - Afternoon Schedule", use_column_width=True)
        else:
            st.info("Event Flow for 26 Nov PM will be available soon.")

# TAB 3: Guidelines
with tab3:
    st.markdown("## 📋 Event Guidelines - DOs & DON'Ts")

    st.info("⚠️ Please review the guidelines carefully for a smooth event experience")

    # Exhibition Guidelines
    st.markdown("### 🏛️ Exhibition Hall Guidelines")
    dnd_exhibition_path = IMAGES_DIR / "DND" / "DND_Exhibition.png"
    if dnd_exhibition_path.exists():
        st.image(str(dnd_exhibition_path), caption="Exhibition Hall - DOs & DON'Ts", use_column_width=True)
    else:
        st.warning("Exhibition guidelines will be available soon.")

    st.markdown("---")

    # Interactive Sessions Guidelines
    st.markdown("### 🎤 Interactive Sessions Guidelines (Zorawar Hall)")
    dnd_interactive_path = IMAGES_DIR / "DND" / "DND_Interactive.png"
    if dnd_interactive_path.exists():
        st.image(str(dnd_interactive_path), caption="Interactive Sessions - DOs & DON'Ts", use_column_width=True)
    else:
        st.warning("Interactive Sessions guidelines will be available soon.")

    st.markdown("---")

    # Plenary Session Guidelines
    st.markdown("### 🏛️ Plenary Session Guidelines (Zorawar Hall)")
    dnd_plenary_path = IMAGES_DIR / "DND" / "DND_Plenary.png"
    if dnd_plenary_path.exists():
        st.image(str(dnd_plenary_path), caption="Plenary Session - DOs & DON'Ts", use_column_width=True)
    else:
        st.warning("Plenary Session guidelines will be available soon.")

# TAB 4: Important Information
with tab4:
    st.markdown("## 📞 Important Contacts & Information")

    # Support Contact
    st.markdown("### 💬 Event Support")
    st.info("""
    **Phone:** 011-26771528
    **Email:** niio-tdac@navy.gov.in
    **Support Hours:** 0900 - 1730 hrs (Mon-Fri)

    For urgent queries during the event, please approach the Help Desk at the venue.
    """)

    st.markdown("---")

    # FAQs
    st.markdown("### ❓ Frequently Asked Questions (FAQs)")

    with st.expander("🎫 What do I need to bring?"):
        st.markdown("""
        **Essential Items:**
        - QR Pass (printed or on mobile device)
        - Valid Government ID (Aadhar/PAN/Driving License/Passport)

        **Optional:**
        - Pen and notepad for sessions
        - Business cards for networking
        - Mobile charger/power bank
        - Water bottle (allowed in exhibition area)
        """)

    with st.expander("🚪 How does entry work?"):
        st.markdown("""
        **Entry Process:**
        1. Arrive at the designated gate (see venue map)
        2. Show your QR pass to security
        3. Pass will be scanned and verified
        4. Show matching Government ID
        5. Proceed to your session/exhibition area

        **Note:** Each pass is valid only for the specified session(s) and date(s).
        """)

    with st.expander("🅿️ Where can I park?"):
        st.markdown("""
        **Parking Information:**
        - Designated parking area marked on venue map (magenta area)
        - Free parking for all registered attendees
        - Limited spaces - carpooling encouraged
        - Security check at parking entrance
        - Follow parking attendant instructions
        """)

    with st.expander("❓ What if I lose my pass?"):
        st.markdown("""
        **Lost Pass Protocol:**
        1. Contact event support immediately: niio-tdac@navy.gov.in
        2. Visit the Help Desk at venue entrance
        3. Present your Government ID for verification
        4. Your entry details will be verified from the system
        5. Temporary entry may be granted after verification

        **Tip:** Save your QR pass in multiple places (email, phone, cloud).
        """)

    st.markdown("---")

    # Quick Reference
    st.markdown("### 📌 Quick Reference")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Dates:**
        - Day 1: 25 November 2025 (Monday)
        - Day 2: 26 November 2025 (Tuesday)

        **Venue:**
        - Manekshaw Centre, Delhi Cantt

        **Dress Code:**
        - Business formal / Smart casual
        - Plenary Session: Formal attire mandatory
        """)

    with col2:
        st.markdown("""
        **Timings:**
        - Exhibition: 1100-1730 hrs (Day 1), 1000-1730 hrs (Day 2)
        - Interactive Sessions: 1030-1130, 1200-1330 hrs (Day 2)
        - Plenary: 1530-1615 hrs (Day 2)

        **Support:**
        - Phone: 011-26771528
        - Email: niio-tdac@navy.gov.in
        - Help Desk: At venue
        """)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 20px; background: white; border-radius: 10px; margin-top: 30px;">
        <p style="color: #666; margin: 0;">
            <strong>Swavlamban 2025</strong> - Indian Navy's Flagship Seminar on Innovation & Self-Reliance
        </p>
        <p style="color: #999; margin: 5px 0 0 0; font-size: 0.9rem;">
            Organized by Naval Innovation & Indigenisation Organisation (NIIO) - TDAC
        </p>
    </div>
""", unsafe_allow_html=True)
