"""
Swavlamban 2025 - Registration System
Main Streamlit Application
"""
import streamlit as st
import sys
import io
import csv
from pathlib import Path
from PIL import Image
import pandas as pd

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Define images directory path
IMAGES_DIR = Path(__file__).parent.parent / "images"

# Import after adding to path
from app.core.database import SessionLocal, init_db
from app.core.security import verify_password, hash_password
from app.models import User

# Page configuration
st.set_page_config(
    page_title="Swavlamban 2025 | Registration System",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, professional UI
st.markdown("""
<style>
    /* Main theme colors - Navy Blue & Gold (Indian Navy colors) */
    :root {
        --primary-color: #1D4E89;
        --secondary-color: #FFD700;
        --background-color: #F5F7FA;
        --text-color: #2C3E50;
    }
    
    /* Hide Streamlit branding and toolbar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    button[kind="header"] {display: none;}
    
    /* Modern card styling */
    .stCard {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1D4E89 0%, #0D2E59 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(29, 78, 137, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .main-header p {
        color: #FFD700;
        font-size: 1.1rem;
        margin-top: 0;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #1D4E89 0%, #0D2E59 100%);
        color: white !important;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(29, 78, 137, 0.4);
        color: white !important;
    }

    .stButton>button:active,
    .stButton>button:focus {
        background: linear-gradient(135deg, #0D2E59 0%, #1D4E89 100%);
        color: white !important;
        box-shadow: 0 2px 6px rgba(29, 78, 137, 0.6);
    }

    /* Fix for primary button type */
    button[kind="primary"] {
        background: linear-gradient(135deg, #1D4E89 0%, #0D2E59 100%) !important;
        color: white !important;
    }

    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2A5FA0 0%, #1D4E89 100%) !important;
        color: white !important;
    }

    button[kind="primary"]:active,
    button[kind="primary"]:focus {
        background: linear-gradient(135deg, #0D2E59 0%, #1D4E89 100%) !important;
        color: white !important;
    }

    /* Tab styling - ensure text is visible when selected */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #1D4E89 !important;
        font-weight: 600;
    }

    /* Prevent flashing cursor/caret globally in non-input elements */
    .stMarkdown, .stRadio, h1, h2, h3, h4, h5, h6, p, div, label, span {
        caret-color: transparent !important;
    }

    /* But allow cursor in actual input fields where user types */
    input[type="text"],
    input[type="email"],
    input[type="number"],
    input[type="password"],
    input[type="tel"],
    textarea,
    [contenteditable="true"] {
        caret-color: auto !important;
    }

    /* Prevent text selection on headers and labels */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    .stRadio label {
        user-select: none !important;
    }

    .stTabs [data-baseweb="tab-list"] button {
        color: #666 !important;
    }

    /* Radio button styling */
    .stRadio label {
        color: #2C3E50 !important;
    }

    /* Checkbox styling */
    .stCheckbox label {
        color: #2C3E50 !important;
    }

    /* Selectbox styling */
    .stSelectbox label {
        color: #2C3E50 !important;
    }

    /* Fix for any selected/active state text */
    *:active, *:focus {
        color: inherit !important;
    }

    /* Input fields */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 2px solid #E5E9F0;
        padding: 10px;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #D4EDDA;
        color: #155724;
        border-radius: 8px;
        padding: 15px;
    }
    
    .stError {
        background-color: #F8D7DA;
        color: #721C24;
        border-radius: 8px;
        padding: 15px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1D4E89 0%, #0D2E59 100%);
    }
    
    /* Metrics styling */
    .metric-card {
        background: white;
        border-left: 4px solid #1D4E89;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'db' not in st.session_state:
        st.session_state.db = SessionLocal()


def login_page():
    """Login page UI"""
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🇮🇳 SWAVLAMBAN 2025</h1>
            <p>Indian Navy | Innovation & Self-Reliance</p>
            <p style="color: white; font-size: 0.9rem; margin-top: 10px;">
                Registration & Pass Management System
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Login form in center
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                help="Organization username provided by TDAC"
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("Login", use_container_width=True)
            with col_b:
                st.form_submit_button("Reset", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    # Authenticate
                    db = SessionLocal()
                    user = db.query(User).filter(User.username == username).first()
                    
                    if user and verify_password(password, user.password_hash):
                        if user.is_active:
                            st.session_state.authenticated = True
                            st.session_state.user = {
                                'username': user.username,
                                'organization': user.organization,
                                'role': user.role,
                                'max_entries': user.max_entries,
                                'allowed_passes': user.allowed_passes
                            }
                            st.success(f"Welcome, {user.organization}!")
                            st.rerun()
                        else:
                            st.error("Your account is inactive. Please contact TDAC.")
                    else:
                        st.error("Invalid username or password")
                    
                    db.close()
        
        # Info section
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; color: #666;">
                <p><strong>Event Dates:</strong> November 25-26, 2025</p>
                <p><strong>Venues:</strong> Manekshaw Centre (Zorawar Hall | Exhibition Hall)</p>
                <p style="font-size: 0.8rem; margin-top: 20px;">
                    For support: 📞 011-26771528 | 📧 niio-tdac@navy.gov.in
                </p>
            </div>
        """, unsafe_allow_html=True)


def main_app():
    """Main application after login"""
    user = st.session_state.user
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: white; border-radius: 10px; margin-bottom: 20px;">
                <h3 style="color: #1D4E89; margin-bottom: 5px;">👤 {user['organization']}</h3>
                <p style="color: #666; font-size: 0.9rem; margin: 0;">@{user['username']}</p>
                <p style="color: #888; font-size: 0.8rem; margin-top: 5px;">Role: {user['role'].upper()}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📋 Navigation")
        
        menu_items = {
            "Dashboard": "📊",
            "Event Information": "ℹ️",
            "My Entries": "📝",
            "Add Entry": "➕",
            "Generate & Email Passes": "🎫",
            "Settings": "⚙️"
        }

        if user['role'] == 'admin':
            menu_items["Admin Panel"] = "👨‍💼"

        # Initialize or get current page from session state
        if 'nav_page' not in st.session_state:
            st.session_state.nav_page = "Dashboard"

        # Get index of current page
        menu_list = list(menu_items.keys())
        current_index = menu_list.index(st.session_state.nav_page) if st.session_state.nav_page in menu_list else 0

        page = st.radio(
            "Go to",
            menu_list,
            index=current_index,
            format_func=lambda x: f"{menu_items[x]} {x}",
            label_visibility="collapsed",
            key="nav_radio"
        )

        # Only update session state if page actually changed (prevents double rerun)
        if page != st.session_state.nav_page:
            st.session_state.nav_page = page
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    
    # Main content area
    st.markdown(f"""
        <div class="main-header" style="padding: 20px;">
            <h1 style="font-size: 1.8rem;">🇮🇳 Swavlamban 2025</h1>
            <p style="font-size: 1rem;">November 25-26, 2025 | Registration System</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Route to different pages
    if page == "Dashboard":
        show_dashboard()
    elif page == "Event Information":
        show_event_information()
    elif page == "My Entries":
        show_my_entries()
    elif page == "Add Entry":
        show_add_entry()
    elif page == "Generate & Email Passes":
        show_generate_passes()
    elif page == "Settings":
        show_settings()
    elif page == "Admin Panel" and user['role'] == 'admin':
        show_admin_panel()


def show_dashboard():
    """Dashboard page"""
    st.markdown("### 📊 Dashboard")

    # Get actual counts from database
    from app.models import Entry
    db = SessionLocal()
    user = st.session_state.user

    # Count entries for this user
    total_entries = db.query(Entry).filter(Entry.username == user['username']).count()

    # Count passes generated (entries where at least one pass_generated flag is True)
    passes_generated = db.query(Entry).filter(
        Entry.username == user['username']
    ).filter(
        (Entry.pass_generated_exhibition_day1 == True) |
        (Entry.pass_generated_exhibition_day2 == True) |
        (Entry.pass_generated_interactive_sessions == True) |
        (Entry.pass_generated_plenary == True)
    ).count()

    remaining = user['max_entries'] - total_entries
    db.close()

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <div class="metric-card">
                <h4 style="color: #666; font-size: 0.9rem; margin: 0;">Total Quota</h4>
                <h2 style="color: #1D4E89; margin: 10px 0;">{}</h2>
            </div>
        """.format(user['max_entries']), unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="metric-card">
                <h4 style="color: #666; font-size: 0.9rem; margin: 0;">Entries Added</h4>
                <h2 style="color: #28A745; margin: 10px 0;">{}</h2>
            </div>
        """.format(total_entries), unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="metric-card">
                <h4 style="color: #666; font-size: 0.9rem; margin: 0;">Remaining</h4>
                <h2 style="color: #FFC107; margin: 10px 0;">{}</h2>
            </div>
        """.format(remaining), unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="metric-card">
                <h4 style="color: #666; font-size: 0.9rem; margin: 0;">Passes Generated</h4>
                <h2 style="color: #17A2B8; margin: 10px 0;">{}</h2>
            </div>
        """.format(passes_generated), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("➕ Add New Entry", use_container_width=True, key="qa_add_entry"):
            st.session_state.nav_page = "Add Entry"
            st.rerun()

    with col2:
        if st.button("📝 View My Entries", use_container_width=True, key="qa_view_entries"):
            st.session_state.nav_page = "My Entries"
            st.rerun()

    with col3:
        if st.button("🎫 Generate & Email Passes", use_container_width=True, key="qa_gen_passes"):
            st.session_state.nav_page = "Generate & Email Passes"
            st.rerun()


def show_event_information():
    """Event Information Hub - All event details in one place"""
    st.markdown("# ℹ️ Event Information Hub")
    st.markdown("*Your complete guide to Swavlamban 2025*")
    st.markdown("---")

    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📍 Venue & Directions", "⏰ Event Schedule", "📋 Guidelines (DOs & DON'Ts)", "📞 Important Info"])

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
        <style>
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
        </style>
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
            st.warning("Venue map not found. Please contact support.")

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

        st.markdown("---")

        # Interactive Sessions Guidelines
        st.markdown("### 🎤 Interactive Sessions Guidelines (Zorawar Hall)")
        dnd_interactive_path = IMAGES_DIR / "DND" / "DND_Interactive.png"
        if dnd_interactive_path.exists():
            st.image(str(dnd_interactive_path), caption="Interactive Sessions - DOs & DON'Ts", use_column_width=True)

        st.markdown("---")

        # Plenary Session Guidelines
        st.markdown("### 🏛️ Plenary Session Guidelines (Zorawar Hall)")
        dnd_plenary_path = IMAGES_DIR / "DND" / "DND_Plenary.png"
        if dnd_plenary_path.exists():
            st.image(str(dnd_plenary_path), caption="Plenary Session - DOs & DON'Ts", use_column_width=True)

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


def show_my_entries():
    """My entries page"""
    st.markdown("### 📝 My Entries")

    user = st.session_state.user
    db = SessionLocal()

    try:
        from app.models import Entry, User

        # Flag to trigger rerun at the end (avoids double flash)
        need_rerun = False

        # Get user object and calculate quota
        user_obj = db.query(User).filter(User.username == user['username']).first()
        entries_count = db.query(Entry).filter(Entry.username == user['username']).count()
        remaining = user_obj.max_entries - entries_count

        entries = db.query(Entry).filter(Entry.username == user['username']).all()

        # Display entries section
        st.info(f"📊 Total Entries: {entries_count} / {user_obj.max_entries} | Remaining: {remaining}")
        st.markdown("---")

        # Existing entries display
        if not entries:
            st.info("No entries yet. Click 'Add Entry' to register attendees.")
        else:
            st.success(f"Total Entries: {len(entries)} / {user['max_entries']}")

            for entry in entries:
                with st.expander(f"👤 {entry.name} - ID: {entry.id}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Email:** {entry.email}")
                        st.write(f"**Phone:** {entry.phone}")
                        st.write(f"**ID Type:** {entry.id_type}")
                        st.write(f"**ID Number:** {entry.id_number}")
                    with col2:
                        # Show pass type (with fallback for entries before migration)
                        is_exhibitor = getattr(entry, 'is_exhibitor_pass', False)
                        pass_type_label = "🏢 Exhibitor Pass" if is_exhibitor else "👤 Visitor Pass"
                        st.write(f"**Pass Type:** {pass_type_label}")

                        st.write("**Passes Selected:**")
                        # Show combined exhibitor pass or individual days
                        if is_exhibitor:
                            st.write("✅ Exhibitor Pass (25-26 Nov)")
                        else:
                            if entry.exhibition_day1:
                                st.write("✅ Exhibition Day 1")
                            if entry.exhibition_day2:
                                st.write("✅ Exhibition Day 2")

                        if entry.interactive_sessions:
                            st.write("✅ Interactive Sessions")
                        if entry.plenary:
                            st.write("✅ Plenary Session")

                    # Edit/Delete actions
                    st.markdown("---")
                    action_col1, action_col2, action_col3 = st.columns([1, 1, 2])

                    with action_col1:
                        if st.button(f"✏️ Edit", key=f"edit_{entry.id}", use_container_width=True):
                            st.session_state[f'editing_{entry.id}'] = True

                    with action_col2:
                        if st.button(f"🗑️ Delete", key=f"delete_{entry.id}", type="secondary", use_container_width=True):
                            st.session_state[f'confirm_delete_{entry.id}'] = True

                    # Delete confirmation
                    if st.session_state.get(f'confirm_delete_{entry.id}', False):
                        st.warning(f"⚠️ Are you sure you want to delete **{entry.name}**? This action cannot be undone!")
                        confirm_col1, confirm_col2 = st.columns(2)
                        with confirm_col1:
                            if st.button(f"✅ Yes, Delete", key=f"confirm_yes_{entry.id}", type="primary", use_container_width=True):
                                try:
                                    db.delete(entry)
                                    db.commit()
                                    st.success(f"✅ Successfully deleted {entry.name}")
                                    # Clean up session state
                                    del st.session_state[f'confirm_delete_{entry.id}']
                                    need_rerun = True
                                except Exception as e:
                                    st.error(f"❌ Error deleting entry: {str(e)}")
                                    db.rollback()
                        with confirm_col2:
                            if st.button(f"❌ Cancel", key=f"confirm_no_{entry.id}", use_container_width=True):
                                del st.session_state[f'confirm_delete_{entry.id}']

                    # Edit form
                    if st.session_state.get(f'editing_{entry.id}', False):
                        st.markdown("---")
                        st.markdown("#### ✏️ Edit Entry")

                        with st.form(key=f"edit_form_{entry.id}"):
                            edit_col1, edit_col2 = st.columns(2)

                            with edit_col1:
                                new_name = st.text_input("Full Name *", value=entry.name)
                                new_phone = st.text_input("Phone *", value=entry.phone)
                                new_email = st.text_input("Email *", value=entry.email)

                            with edit_col2:
                                id_types = ["Aadhaar", "PAN", "Passport", "Driving License", "Voter ID"]
                                current_id_type_index = id_types.index(entry.id_type) if entry.id_type in id_types else 0
                                new_id_type = st.selectbox("ID Type *", id_types, index=current_id_type_index)
                                new_id_number = st.text_input("ID Number *", value=entry.id_number)

                            st.markdown("**Update Passes:**")

                            # Check if this is an exhibitor entry
                            is_exhibitor = getattr(entry, 'is_exhibitor_pass', False)
                            is_admin = user.get('role') == 'admin'

                            if is_exhibitor and not is_admin:
                                # EXHIBITOR ENTRY (Non-Admin): Show exhibitor pass only (read-only)
                                st.info("🏢 This is an Exhibitor entry (Both Days)")
                                new_exhibitor = st.checkbox("🏢 Exhibitor Pass (25-26 Nov)", value=True, disabled=True,
                                                           help="Exhibitor passes cannot be modified to visitor passes")
                                # Set visitor passes to False for exhibitors
                                new_ex1 = False
                                new_ex2 = False
                                new_interactive = False
                                new_plenary = False
                            elif is_exhibitor and is_admin:
                                # EXHIBITOR ENTRY (Admin): Allow editing all passes
                                st.warning("🔓 Admin Mode: You can modify all passes for this exhibitor")
                                pass_col1, pass_col2 = st.columns(2)

                                with pass_col1:
                                    new_ex1 = st.checkbox("🗓️ Exhibition Day 1 - 25 Nov", value=entry.exhibition_day1)
                                    new_ex2 = st.checkbox("🗓️ Exhibition Day 2 - 26 Nov", value=entry.exhibition_day2)

                                with pass_col2:
                                    new_interactive = st.checkbox("🎤 Interactive Sessions (I & II)", value=entry.interactive_sessions)
                                    new_plenary = st.checkbox("🏛️ Plenary Session", value=entry.plenary)
                            else:
                                # VISITOR ENTRY: Show visitor passes
                                pass_col1, pass_col2 = st.columns(2)

                                with pass_col1:
                                    new_ex1 = st.checkbox("🗓️ Exhibition Day 1 - 25 Nov", value=entry.exhibition_day1)
                                    new_ex2 = st.checkbox("🗓️ Exhibition Day 2 - 26 Nov", value=entry.exhibition_day2)

                                with pass_col2:
                                    new_interactive = st.checkbox("🎤 Interactive Sessions (I & II)", value=entry.interactive_sessions)
                                    new_plenary = st.checkbox("🏛️ Plenary Session", value=entry.plenary)

                            form_col1, form_col2 = st.columns(2)
                            with form_col1:
                                submit_edit = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                            with form_col2:
                                cancel_edit = st.form_submit_button("❌ Cancel", use_container_width=True)

                            if submit_edit:
                                try:
                                    # Update entry
                                    entry.name = new_name
                                    entry.phone = new_phone
                                    entry.email = new_email
                                    entry.id_type = new_id_type
                                    entry.id_number = new_id_number
                                    entry.exhibition_day1 = new_ex1
                                    entry.exhibition_day2 = new_ex2
                                    entry.interactive_sessions = new_interactive
                                    entry.plenary = new_plenary

                                    db.commit()
                                    st.success(f"✅ Successfully updated {new_name}")
                                    del st.session_state[f'editing_{entry.id}']
                                    need_rerun = True
                                except Exception as e:
                                    st.error(f"❌ Error updating entry: {str(e)}")
                                    db.rollback()

                            if cancel_edit:
                                del st.session_state[f'editing_{entry.id}']

        # Rerun ONLY if database was modified (avoids double flash on UI-only actions)
        if need_rerun:
            db.close()
            st.rerun()
    finally:
        db.close()


def show_add_entry():
    """Add new entry page"""
    st.markdown("### Add New Entry")

    user = st.session_state.user
    db = SessionLocal()

    try:
        from app.models import Entry, User

        # Check quota per pass type
        user_obj = db.query(User).filter(User.username == user['username']).first()
        all_entries = db.query(Entry).filter(Entry.username == user['username']).all()

        # Count passes used by type (excluding exhibitors)
        ex1_used = sum([1 for e in all_entries if e.exhibition_day1 and not getattr(e, 'is_exhibitor_pass', False)])
        ex2_used = sum([1 for e in all_entries if e.exhibition_day2 and not getattr(e, 'is_exhibitor_pass', False)])
        interactive_used = sum([1 for e in all_entries if e.interactive_sessions])
        plenary_used = sum([1 for e in all_entries if e.plenary])

        # Get quotas with safe fallback for users created before migration
        quota_ex1 = getattr(user_obj, 'quota_ex_day1', 0)
        quota_ex2 = getattr(user_obj, 'quota_ex_day2', 0)
        quota_interactive = getattr(user_obj, 'quota_interactive', 0)
        quota_plenary = getattr(user_obj, 'quota_plenary', 0)

        # Display quota status
        st.markdown("#### 📊 Your Pass Quotas")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            remaining_ex1 = quota_ex1 - ex1_used
            st.metric("Ex Day 1", f"{ex1_used}/{quota_ex1}", delta=f"{remaining_ex1} left", delta_color="normal")
        with col2:
            remaining_ex2 = quota_ex2 - ex2_used
            st.metric("Ex Day 2", f"{ex2_used}/{quota_ex2}", delta=f"{remaining_ex2} left", delta_color="normal")
        with col3:
            remaining_interactive = quota_interactive - interactive_used
            st.metric("Interactive", f"{interactive_used}/{quota_interactive}", delta=f"{remaining_interactive} left", delta_color="normal")
        with col4:
            remaining_plenary = quota_plenary - plenary_used
            st.metric("Plenary", f"{plenary_used}/{quota_plenary}", delta=f"{remaining_plenary} left", delta_color="normal")

        st.markdown("---")

        # INDIVIDUAL ENTRY SECTION

        with st.form("add_entry_form"):
            st.markdown("#### Personal Information")
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Full Name *", placeholder="Enter full name")
                phone = st.text_input("Phone *", placeholder="+91-XXXXXXXXXX")
                email = st.text_input("Email *", placeholder="email@example.com")

            with col2:
                id_type = st.selectbox("ID Type *", ["Aadhaar", "PAN", "Passport", "Driving License", "Voter ID"])
                id_number = st.text_input("ID Number *", placeholder="Enter ID number")

            st.markdown("---")
            st.markdown("#### 🎫 Select Passes")

            # Get user's allowed passes
            allowed_passes = user.get('allowed_passes', {})

            # Filter: Only show passes that this user is allowed to generate
            st.info("Select passes based on your organization's allocation")

            col1, col2 = st.columns(2)

            with col1:
                # Exhibition passes
                if allowed_passes.get('exhibition_day1', False):
                    exhibition_day1 = st.checkbox("🗓️ Exhibition Day 1 - 25 Nov", help="1100-1730 hrs, Exhibition Hall, Manekshaw Centre")
                else:
                    exhibition_day1 = False
                    st.checkbox("🗓️ Exhibition Day 1 - 25 Nov", disabled=True, help="Not available for your organization")

                if allowed_passes.get('exhibition_day2', False):
                    exhibition_day2 = st.checkbox("🗓️ Exhibition Day 2 - 26 Nov", help="1000-1730 hrs, Exhibition Hall, Manekshaw Centre")
                else:
                    exhibition_day2 = False
                    st.checkbox("🗓️ Exhibition Day 2 - 26 Nov", disabled=True, help="Not available for your organization")

            with col2:
                # Interactive sessions (combined as single pass for both panels)
                if allowed_passes.get("interactive_sessions", False):
                    interactive = st.checkbox("🎤 Interactive Sessions (Session I & II)",
                                             help="Interactive Session I: Future & Emerging Tech (1030-1130)\nInteractive Session II: iDEX Ecosystem (1200-1330)")
                    # Set both panels if interactive is selected
                    interactive = interactive
                    interactive = interactive
                else:
                    interactive = False
                    interactive = False
                    interactive = False
                    st.checkbox("🎤 Interactive Sessions (Both Panel Discussions)", disabled=True,
                               help="Not available for your organization")

                # Plenary session
                if allowed_passes.get('plenary', False):
                    plenary = st.checkbox("🏛️ Plenary Session", help="26 Nov, 1530-1615, Zorawar Hall, Manekshaw Centre")
                else:
                    plenary = False
                    st.checkbox("🏛️ Plenary Session", disabled=True, help="Not available for your organization")

            st.markdown("---")
            submitted = st.form_submit_button("✅ Add Entry", use_container_width=True)

            if submitted:
                # Validation
                if not name or not phone or not email or not id_number:
                    st.error("Please fill all required fields!")
                    return

                if not (exhibition_day1 or exhibition_day2 or interactive or interactive or plenary):
                    st.error("Please select at least one pass!")
                    return

                # Check quota for selected passes
                quota_errors = []
                if exhibition_day1 and remaining_ex1 <= 0:
                    quota_errors.append("Exhibition Day 1 quota exhausted")
                if exhibition_day2 and remaining_ex2 <= 0:
                    quota_errors.append("Exhibition Day 2 quota exhausted")
                if interactive and remaining_interactive <= 0:
                    quota_errors.append("Interactive Sessions quota exhausted")
                if plenary and remaining_plenary <= 0:
                    quota_errors.append("Plenary Session quota exhausted")

                if quota_errors:
                    st.error("❌ Quota exceeded:\n" + "\n".join(f"• {err}" for err in quota_errors))
                    st.warning("Please contact admin to increase your quota or select different passes.")
                    return

                # Create entry
                try:
                    new_entry = Entry(
                        username=user['username'],
                        name=name,
                        phone=phone,
                        email=email,
                        id_type=id_type,
                        id_number=id_number,
                        exhibition_day1=exhibition_day1,
                        exhibition_day2=exhibition_day2,
                        interactive_sessions=interactive,
                        plenary=plenary
                    )
                    db.add(new_entry)
                    db.commit()
                    entry_id = new_entry.id
                    db.close()

                    # Show success message and rerun
                    st.success(f"✅ Entry added successfully! Entry ID: {entry_id}")
                    st.info(f"👤 {name} has been registered with {len([x for x in [exhibition_day1, exhibition_day2, interactive or interactive, plenary] if x])} pass(es)")
                    st.balloons()

                    # Wait a moment for user to see the message
                    import time
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    db.rollback()
                    error_msg = str(e)
                    if "UNIQUE constraint failed" in error_msg and "id_number" in error_msg:
                        st.error(f"❌ Error: This {id_type} number ({id_number}) is already registered in the system. Each ID number can only be used once.")
                    elif "UNIQUE constraint failed" in error_msg and "email" in error_msg:
                        st.error(f"❌ Error: This email ({email}) is already registered in the system.")
                    else:
                        st.error(f"❌ Error adding entry: {error_msg}")

        # ==================== BULK UPLOAD SECTION ====================
        st.markdown("---")
        st.markdown("### 📤 Bulk Upload Entries")

        col1, col2 = st.columns(2)

        with col1:
            st.info("""
            **Download CSV Template** → Fill locally → Upload to create entries in bulk!

            Template includes:
            - Pre-configured ID Type dropdown options
            - All required fields (Name, Email, Phone, ID Type, ID Number)
            - Pass selection columns (Exhibition Day 1/2, Interactive, Plenary)
            """)
            # Generate CSV template
            template_data = {
                'Name': ['John Doe', 'Jane Smith', 'Sample Name'],
                'Email': ['john@example.com', 'jane@example.com', 'email@example.com'],
                'Phone': ['9876543210', '9876543211', '9876543212'],
                'ID_Type': ['Aadhaar', 'PAN', 'Passport'],  # One example per row for easier copy-paste
                'ID_Number': ['123456789012', '234567890123', '345678901234'],
                'Exhibition_Day_1': ['Yes', 'No', 'Yes'],
                'Exhibition_Day_2': ['Yes', 'Yes', 'No'],
                'Interactive_Sessions': ['No', 'Yes', 'Yes'],
                'Plenary': ['No', 'Yes', 'No']
            }

            df_template = pd.DataFrame(template_data)
            csv_buffer = io.StringIO()
            df_template.to_csv(csv_buffer, index=False)
            csv_content = csv_buffer.getvalue()

            st.download_button(
                label="📥 Download CSV Template",
                data=csv_buffer.getvalue(),
                file_name=f"swavlamban2025_bulk_entry_template_{user['username']}.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.markdown("""
            **Instructions:**
            1. Download the template CSV
            2. Open in Excel/Google Sheets
            3. Replace sample data with actual attendee details
            4. For ID_Type column: Choose one option (Aadhaar/PAN/Passport/Driving License/Voter ID)
            5. For pass columns: Use "Yes" or "No"
            6. Save and upload below
            """)

        with col2:
            # Calculate total entries and remaining quota
            entries_count = len(all_entries)
            total_quota = quota_ex1 + quota_interactive + quota_plenary
            remaining = total_quota - entries_count

            st.markdown(f"""
            **Current Status:**
            - Total Entries: {entries_count}
            - Total Quota: {total_quota}
            - Remaining: {remaining}
            """)

            # CSV Upload
            uploaded_file = st.file_uploader(
                "📁 Upload Filled CSV",
                type=['csv'],
                help="Upload your filled CSV file with attendee details",
                key="bulk_entry_csv_add_page"
            )

        if uploaded_file is not None:
            try:
                # Read CSV
                df = pd.read_csv(uploaded_file)

                # Validate columns
                required_columns = ['Name', 'Email', 'Phone', 'ID_Type', 'ID_Number',
                                  'Exhibition_Day_1', 'Exhibition_Day_2', 'Interactive_Sessions', 'Plenary']
                missing_columns = [col for col in required_columns if col not in df.columns]

                if missing_columns:
                    st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
                else:
                    # Show preview
                    st.markdown("#### 📋 Preview (First 5 rows)")
                    st.dataframe(df.head(), use_container_width=True)

                    st.info(f"📊 Total entries in CSV: {len(df)} | Remaining quota: {remaining}")

                    if len(df) > remaining:
                        st.error(f"❌ Cannot upload {len(df)} entries. You only have {remaining} slots remaining.")
                    else:
                        if st.button("🚀 Process & Upload Entries", type="primary", use_container_width=True):
                            # Process entries
                            success_count = 0
                            failed_count = 0
                            failed_rows = []

                            progress_bar = st.progress(0)
                            status_text = st.empty()

                            for idx, row in df.iterrows():
                                status_text.text(f"Processing entry {idx + 1}/{len(df)}...")
                                progress_bar.progress((idx + 1) / len(df))

                                try:
                                    # Validate row data
                                    name = str(row['Name']).strip()
                                    email = str(row['Email']).strip()
                                    phone = str(row['Phone']).strip()
                                    id_type = str(row['ID_Type']).strip()
                                    id_number = str(row['ID_Number']).strip()

                                    # Validate required fields
                                    if not name or name == 'nan':
                                        failed_rows.append((idx + 2, "Missing name"))
                                        failed_count += 1
                                        continue

                                    if not email or email == 'nan' or '@' not in email:
                                        failed_rows.append((idx + 2, f"Invalid email: {email}"))
                                        failed_count += 1
                                        continue

                                    if not phone or phone == 'nan' or len(phone) != 10:
                                        failed_rows.append((idx + 2, f"Invalid phone (must be 10 digits): {phone}"))
                                        failed_count += 1
                                        continue

                                    # Validate ID type
                                    valid_id_types = ['Aadhaar', 'PAN', 'Passport', 'Driving License', 'Voter ID']
                                    if id_type not in valid_id_types:
                                        failed_rows.append((idx + 2, f"Invalid ID type: {id_type}"))
                                        failed_count += 1
                                        continue

                                    if not id_number or id_number == 'nan':
                                        failed_rows.append((idx + 2, "Missing ID number"))
                                        failed_count += 1
                                        continue

                                    # Parse pass selections
                                    exhibition_day1 = str(row['Exhibition_Day_1']).strip().lower() == 'yes'
                                    exhibition_day2 = str(row['Exhibition_Day_2']).strip().lower() == 'yes'
                                    interactive_sessions = str(row['Interactive_Sessions']).strip().lower() == 'yes'
                                    plenary = str(row['Plenary']).strip().lower() == 'yes'

                                    # Check if at least one pass is selected
                                    if not (exhibition_day1 or exhibition_day2 or interactive_sessions or plenary):
                                        failed_rows.append((idx + 2, "No passes selected"))
                                        failed_count += 1
                                        continue

                                    # Get user's allowed passes
                                    allowed_passes = user.get('allowed_passes', {})

                                    # Check permissions
                                    if exhibition_day1 and not allowed_passes.get('exhibition_day1', False):
                                        failed_rows.append((idx + 2, "Not allowed to create Exhibition Day 1 passes"))
                                        failed_count += 1
                                        continue

                                    if exhibition_day2 and not allowed_passes.get('exhibition_day2', False):
                                        failed_rows.append((idx + 2, "Not allowed to create Exhibition Day 2 passes"))
                                        failed_count += 1
                                        continue

                                    if interactive_sessions and not allowed_passes.get('interactive_sessions', False):
                                        failed_rows.append((idx + 2, "Not allowed to create Interactive Sessions passes"))
                                        failed_count += 1
                                        continue

                                    if plenary and not allowed_passes.get('plenary', False):
                                        failed_rows.append((idx + 2, "Not allowed to create Plenary passes"))
                                        failed_count += 1
                                        continue

                                    # Create entry
                                    new_entry = Entry(
                                        username=user['username'],
                                        name=name,
                                        phone=phone,
                                        email=email,
                                        id_type=id_type,
                                        id_number=id_number,
                                        exhibition_day1=exhibition_day1,
                                        exhibition_day2=exhibition_day2,
                                        interactive_sessions=interactive_sessions,
                                        plenary=plenary
                                    )
                                    db.add(new_entry)
                                    db.commit()
                                    success_count += 1

                                except Exception as e:
                                    failed_rows.append((idx + 2, str(e)))
                                    failed_count += 1
                                    db.rollback()

                            # Show results
                            status_text.empty()
                            progress_bar.empty()

                            if success_count > 0:
                                st.success(f"✅ Successfully uploaded {success_count} entries!")

                            if failed_count > 0:
                                st.error(f"❌ Failed to upload {failed_count} entries")
                                with st.expander("📋 View Failed Rows"):
                                    for row_num, error in failed_rows:
                                        st.write(f"Row {row_num}: {error}")

                            if success_count > 0:
                                st.rerun()

            except Exception as e:
                st.error(f"❌ Error reading CSV file: {str(e)}")

    finally:
        db.close()


def show_generate_passes():
    """Generate passes page"""
    st.markdown("### 🎫 Generate & Email Passes")

    user = st.session_state.user
    db = SessionLocal()

    try:
        from app.models import Entry
        from app.services.pass_generator import pass_generator
        from app.services.email_service import email_service

        entries = db.query(Entry).filter(Entry.username == user['username']).all()

        if not entries:
            st.info("No entries yet. Add entries first to generate passes.")
            return

        st.info(f"📊 Total Entries: {len(entries)}")

        st.markdown("---")

        # Individual attendee selector
        entry_options = {f"{e.name} (ID: {e.id})": e for e in entries}
        selected_name = st.selectbox("Select Attendee", list(entry_options.keys()))

        if selected_name:
            entry = entry_options[selected_name]

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Attendee Details")
                st.write(f"**Name:** {entry.name}")
                st.write(f"**Email:** {entry.email}")
                st.write(f"**Phone:** {entry.phone}")

            with col2:
                st.markdown("#### Passes Selected")

                # Show pass type (with fallback for entries before migration)
                is_exhibitor = getattr(entry, 'is_exhibitor_pass', False)
                pass_type_label = "🏢 Exhibitor Pass" if is_exhibitor else "👤 Visitor Pass"
                st.write(f"**Pass Type:** {pass_type_label}")
                st.write("")  # Add spacing

                passes_list = []

                # Show combined exhibitor pass or individual days
                if is_exhibitor:
                    st.write("✅ Exhibitor Pass (25-26 Nov)")
                    passes_list.append("exhibition_both_days")
                else:
                    if entry.exhibition_day1:
                        st.write("✅ Exhibition Day 1")
                        passes_list.append("exhibition_day1")
                    if entry.exhibition_day2:
                        st.write("✅ Exhibition Day 2")
                        passes_list.append("exhibition_day2")

                if entry.interactive_sessions:
                    st.write("✅ Interactive Sessions")
                    passes_list.append("interactive")
                if entry.plenary:
                    st.write("✅ Plenary Session")
                    passes_list.append("plenary")

            st.markdown("---")

            # Generate Passes Button
            if st.button("🎫 Generate Passes", use_container_width=True, type="primary"):
                with st.spinner("Generating passes with QR codes..."):
                    try:
                        all_files = pass_generator.generate_passes_for_entry(entry, user['username'])

                        # Separate actual passes from attachments (DND, Event Flow)
                        # Actual passes have pattern: name_id_passtype.png
                        # Attachments have pattern: DND_*.png or EF-*.png
                        actual_passes = [f for f in all_files if not (f.name.startswith('DND_') or f.name.startswith('EF-'))]

                        # Update database flags
                        if entry.exhibition_day1:
                            entry.pass_generated_exhibition_day1 = True
                        if entry.exhibition_day2:
                            entry.pass_generated_exhibition_day2 = True
                        if entry.interactive_sessions:
                            entry.pass_generated_interactive_sessions = True
                            entry.pass_generated_interactive_sessions = True
                        if entry.plenary:
                            entry.pass_generated_plenary = True

                        db.commit()

                        pass_word = "pass" if len(actual_passes) == 1 else "passes"
                        st.success(f"✅ Generated {len(actual_passes)} {pass_word}!")

                        # Store ONLY actual passes in session state for download
                        st.session_state.generated_passes = actual_passes
                        st.session_state.generated_for_entry = entry.id

                    except Exception as e:
                        st.error(f"Error generating passes: {e}")
                        import traceback
                        st.code(traceback.format_exc())

            # Show download buttons if passes were generated
            if 'generated_passes' in st.session_state and st.session_state.get('generated_for_entry') == entry.id:
                st.markdown("### 📥 Download Passes")

                for pass_file in st.session_state.generated_passes:
                    col_name, col_btn = st.columns([3, 1])
                    with col_name:
                        st.write(f"📄 **{pass_file.name}**")
                    with col_btn:
                        with open(pass_file, "rb") as f:
                            st.download_button(
                                label="Download",
                                data=f.read(),
                                file_name=pass_file.name,
                                mime="image/png",
                                key=f"download_{pass_file.name}"
                            )

            st.markdown("---")

            # Email section - Synchronous with spinner
            st.markdown("### 📧 Generate Passes & Send Email")
            st.info(f"📧 Email will be sent to: **{entry.email}**")

            if st.button("📧 Generate Passes & Send Email", use_container_width=True, type="primary", key="individual_email_btn"):
                import time
                import os

                generated_passes = []
                try:
                    with st.spinner("🎫 Generating passes..."):
                        # Generate passes first
                        generated_passes = pass_generator.generate_passes_for_entry(entry, user['username'])
                        time.sleep(0.5)  # Brief pause for visual feedback

                    with st.spinner("💾 Updating database..."):
                        # Update database flags
                        if entry.exhibition_day1:
                            entry.pass_generated_exhibition_day1 = True
                        if entry.exhibition_day2:
                            entry.pass_generated_exhibition_day2 = True
                        if entry.interactive_sessions:
                            entry.pass_generated_interactive_sessions = True
                        if entry.plenary:
                            entry.pass_generated_plenary = True

                        db.commit()
                        time.sleep(0.3)  # Brief pause for visual feedback

                    # Check if exhibitor entry - use correct email template
                    is_exhibitor = getattr(entry, 'is_exhibitor_pass', False)

                    with st.spinner(f"📧 Sending email to {entry.email}..."):
                        start_time = time.time()

                        if is_exhibitor:
                            # EXHIBITOR: Use dedicated exhibitor email template
                            success = email_service.send_exhibitor_bulk_email(
                                recipient_email=entry.email,
                                recipient_name=entry.name,
                                pass_files=generated_passes
                            )
                        else:
                            # VISITOR: Use visitor email template
                            # Determine primary pass type for email template
                            if entry.exhibition_day1:
                                email_type = "exhibition_day1"
                            elif entry.exhibition_day2:
                                email_type = "exhibition_day2"
                            elif entry.interactive_sessions:
                                email_type = "interactive_sessions"
                            elif entry.plenary:
                                email_type = "plenary"
                            else:
                                email_type = "exhibition_day1"

                            success = email_service.send_pass_email(
                                entry.email,
                                entry.name,
                                generated_passes,
                                email_type
                            )
                        duration = time.time() - start_time

                    if success:
                        st.success(f"✅ Email sent successfully to {entry.email} via Mailjet API! (took {duration:.1f}s)")
                        st.balloons()
                    else:
                        st.error("❌ Failed to send email: Email service failed")

                except Exception as e:
                    st.error(f"❌ Failed to send email: {str(e)}")

                finally:
                    # CLEANUP: Delete generated pass files immediately after email sent
                    for pass_file in generated_passes:
                        try:
                            # Only delete QR pass files (not invitation templates)
                            if pass_file.exists() and "generated_passes" in str(pass_file):
                                os.remove(pass_file)
                        except Exception:
                            pass

            st.markdown("---")

            # Bulk Email section (after individual email)
            st.markdown("### 📨 Bulk Email Mode")

            bulk_mode = st.checkbox("📨 Enable Bulk Email Mode", value=False, help="Send passes to multiple attendees at once")

            if bulk_mode:
                st.info("💡 Select multiple attendees below and send all passes in one operation")

                # Pass type filter section
                st.markdown("#### 🎯 Filter by Pass Type")
                st.markdown("Select which pass types to include:")

                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    filter_exhibition_day1 = st.checkbox("Exhibition Day 1", value=True)
                with col2:
                    filter_exhibition_day2 = st.checkbox("Exhibition Day 2", value=True)
                with col3:
                    filter_interactive = st.checkbox("Interactive Sessions", value=True)
                with col4:
                    filter_plenary = st.checkbox("Plenary", value=True)
                with col5:
                    filter_exhibitor = st.checkbox("Exhibitor Passes", value=False, help="Bulk-uploaded exhibitor entries")

                st.markdown("---")

                # Multi-select for bulk operations
                selected_entries = []

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("**Select Attendees:**")
                with col2:
                    select_all = st.checkbox("Select All (filtered)", value=False)

                # Apply pass type filters
                filtered_entries = []
                for bulk_entry in entries:
                    # Check if entry matches filter criteria
                    is_exhibitor_entry = getattr(bulk_entry, 'is_exhibitor_pass', False)

                    # Check if entry has any of the selected pass types
                    has_matching_pass = False

                    if filter_exhibition_day1 and bulk_entry.exhibition_day1:
                        has_matching_pass = True
                    if filter_exhibition_day2 and bulk_entry.exhibition_day2:
                        has_matching_pass = True
                    if filter_interactive and bulk_entry.interactive_sessions:
                        has_matching_pass = True
                    if filter_plenary and bulk_entry.plenary:
                        has_matching_pass = True

                    # Exhibitor pass (only if exhibitor filter is ON)
                    if filter_exhibitor and is_exhibitor_entry:
                        has_matching_pass = True

                    # Skip if no matching passes
                    if not has_matching_pass:
                        continue

                    # Entry passed filters, add to filtered list
                    filtered_entries.append(bulk_entry)

                # Display filtered count
                st.info(f"🔍 Showing {len(filtered_entries)} attendee(s) matching filters (out of {len(entries)} total)")

                for bulk_entry in filtered_entries:
                    passes_info = []
                    if bulk_entry.exhibition_day1: passes_info.append("Ex-1")
                    if bulk_entry.exhibition_day2: passes_info.append("Ex-2")
                    if bulk_entry.interactive_sessions: passes_info.append("Int")
                    if bulk_entry.plenary: passes_info.append("Ple")

                    # Add exhibitor badge if applicable
                    is_exhibitor_entry = getattr(bulk_entry, 'is_exhibitor_pass', False)
                    if is_exhibitor_entry:
                        passes_info.append("🏢 EXHIBITOR")

                    passes_str = ", ".join(passes_info) if passes_info else "No passes selected"

                    is_selected = st.checkbox(
                        f"{bulk_entry.name} - {bulk_entry.email} [{passes_str}]",
                        value=select_all,
                        key=f"bulk_select_{bulk_entry.id}"
                    )

                    if is_selected:
                        selected_entries.append(bulk_entry)

                if selected_entries:
                    st.success(f"✅ Selected {len(selected_entries)} attendee(s)")

                    # ADMIN ONLY: Select which passes to send
                    is_admin = user.get('role') == 'admin'
                    if is_admin:
                        st.markdown("---")
                        st.markdown("#### 🎫 Select Passes to Send (Admin Only)")
                        st.info("💡 Choose which specific passes to generate and send to the selected attendees")

                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            send_ex1 = st.checkbox("📅 Exhibition Day 1", value=True, key="bulk_send_ex1")
                        with col2:
                            send_ex2 = st.checkbox("📅 Exhibition Day 2", value=True, key="bulk_send_ex2")
                        with col3:
                            send_interactive = st.checkbox("🎤 Interactive Sessions", value=True, key="bulk_send_interactive")
                        with col4:
                            send_plenary = st.checkbox("🏛️ Plenary", value=True, key="bulk_send_plenary")

                        # Store selected passes in session state for use during generation
                        st.session_state.bulk_send_passes = {
                            'ex1': send_ex1,
                            'ex2': send_ex2,
                            'interactive': send_interactive,
                            'plenary': send_plenary
                        }

                        if not any([send_ex1, send_ex2, send_interactive, send_plenary]):
                            st.warning("⚠️ Please select at least one pass type to send")
                            return
                    else:
                        # Non-admin: Send all passes
                        st.session_state.bulk_send_passes = None

                    # Time estimation (Mailjet API is 9x faster than SMTP)
                    estimated_time = len(selected_entries) * 10  # 10s per email via Mailjet API
                    estimated_minutes = estimated_time / 60
                    st.info(f"⏱️ Estimated time: ~{estimated_minutes:.1f} minutes ({estimated_time:.0f} seconds) via Mailjet API")

                    # Initialize bulk email session state
                    if 'bulk_email_in_progress' not in st.session_state:
                        st.session_state.bulk_email_in_progress = False
                    if 'bulk_email_processed_ids' not in st.session_state:
                        st.session_state.bulk_email_processed_ids = set()
                    if 'bulk_email_success_count' not in st.session_state:
                        st.session_state.bulk_email_success_count = 0
                    if 'bulk_email_failed_count' not in st.session_state:
                        st.session_state.bulk_email_failed_count = 0
                    if 'bulk_email_start_time' not in st.session_state:
                        st.session_state.bulk_email_start_time = None

                    # Button to start bulk email
                    start_button = st.button("📧 Generate & Send Bulk Emails", use_container_width=True, type="primary", disabled=st.session_state.bulk_email_in_progress)

                    # Button to cancel/reset bulk email
                    if st.session_state.bulk_email_in_progress:
                        if st.button("🛑 Reset Bulk Email Operation", use_container_width=True):
                            st.session_state.bulk_email_in_progress = False
                            st.session_state.bulk_email_processed_ids = set()
                            st.session_state.bulk_email_success_count = 0
                            st.session_state.bulk_email_failed_count = 0
                            st.session_state.bulk_email_start_time = None
                            st.rerun()

                    if start_button or st.session_state.bulk_email_in_progress:
                        import time

                        # Start new operation
                        if not st.session_state.bulk_email_in_progress:
                            st.session_state.bulk_email_in_progress = True
                            st.session_state.bulk_email_processed_ids = set()
                            st.session_state.bulk_email_success_count = 0
                            st.session_state.bulk_email_failed_count = 0
                            st.session_state.bulk_email_start_time = time.time()

                        start_time = st.session_state.bulk_email_start_time

                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        time_text = st.empty()

                        success_count = st.session_state.bulk_email_success_count
                        failed_count = st.session_state.bulk_email_failed_count
                        processed_ids = st.session_state.bulk_email_processed_ids

                        # Filter out already processed entries
                        remaining_entries = [e for e in selected_entries if e.id not in processed_ids]

                        for idx, bulk_entry in enumerate(remaining_entries):
                            # Calculate progress (including already processed entries)
                            total_processed = len(st.session_state.bulk_email_processed_ids)
                            current_position = total_processed + 1

                            # Calculate elapsed and remaining time
                            elapsed = time.time() - start_time
                            avg_time_per_email = elapsed / (total_processed + 1) if total_processed > 0 else 10  # Initial estimate 10s for Mailjet
                            remaining_emails = len(selected_entries) - (total_processed + 1)
                            estimated_remaining = remaining_emails * avg_time_per_email

                            status_text.markdown(f"**📤 Processing {current_position}/{len(selected_entries)}:** {bulk_entry.name}")
                            time_text.info(f"⏱️ Elapsed: {elapsed:.1f}s | Remaining: ~{estimated_remaining:.1f}s | Avg: {avg_time_per_email:.1f}s/email via Mailjet API")

                            generated_passes = []
                            try:
                                # Check if admin has selected specific passes to send
                                send_specific_passes = st.session_state.get('bulk_send_passes')

                                if send_specific_passes:
                                    # ADMIN MODE: Only generate selected passes
                                    # Create a temporary entry copy with only selected passes enabled
                                    from copy import copy
                                    temp_entry = copy(bulk_entry)

                                    # Override pass selections based on admin's choice
                                    temp_entry.exhibition_day1 = bulk_entry.exhibition_day1 and send_specific_passes['ex1']
                                    temp_entry.exhibition_day2 = bulk_entry.exhibition_day2 and send_specific_passes['ex2']
                                    temp_entry.interactive_sessions = bulk_entry.interactive_sessions and send_specific_passes['interactive']
                                    temp_entry.plenary = bulk_entry.plenary and send_specific_passes['plenary']

                                    # Generate only selected passes
                                    generated_passes = pass_generator.generate_passes_for_entry(temp_entry, user['username'])
                                else:
                                    # NON-ADMIN MODE: Generate all passes
                                    generated_passes = pass_generator.generate_passes_for_entry(bulk_entry, user['username'])

                                # Update database flags only for passes that were actually generated
                                if send_specific_passes:
                                    if bulk_entry.exhibition_day1 and send_specific_passes['ex1']:
                                        bulk_entry.pass_generated_exhibition_day1 = True
                                    if bulk_entry.exhibition_day2 and send_specific_passes['ex2']:
                                        bulk_entry.pass_generated_exhibition_day2 = True
                                    if bulk_entry.interactive_sessions and send_specific_passes['interactive']:
                                        bulk_entry.pass_generated_interactive_sessions = True
                                    if bulk_entry.plenary and send_specific_passes['plenary']:
                                        bulk_entry.pass_generated_plenary = True
                                else:
                                    # Update all flags
                                    if bulk_entry.exhibition_day1:
                                        bulk_entry.pass_generated_exhibition_day1 = True
                                    if bulk_entry.exhibition_day2:
                                        bulk_entry.pass_generated_exhibition_day2 = True
                                    if bulk_entry.interactive_sessions:
                                        bulk_entry.pass_generated_interactive_sessions = True
                                    if bulk_entry.plenary:
                                        bulk_entry.pass_generated_plenary = True

                                db.commit()

                                # Send email - use correct template based on entry type
                                is_exhibitor = getattr(bulk_entry, 'is_exhibitor_pass', False)

                                if is_exhibitor:
                                    # EXHIBITOR: Use dedicated exhibitor email template
                                    success = email_service.send_exhibitor_bulk_email(
                                        recipient_email=bulk_entry.email,
                                        recipient_name=bulk_entry.name,
                                        pass_files=generated_passes
                                    )
                                else:
                                    # VISITOR: Use visitor email template
                                    email_type = "exhibition_day1" if bulk_entry.exhibition_day1 else "exhibition_day2"
                                    success = email_service.send_pass_email(
                                        recipient_email=bulk_entry.email,
                                        recipient_name=bulk_entry.name,
                                        pass_files=generated_passes,
                                        pass_type=email_type
                                    )

                                if success:
                                    success_count += 1
                                    st.session_state.bulk_email_success_count += 1
                                else:
                                    failed_count += 1
                                    st.session_state.bulk_email_failed_count += 1

                            except Exception as e:
                                failed_count += 1
                                st.session_state.bulk_email_failed_count += 1
                                st.warning(f"⚠️ Failed for {bulk_entry.name}: {str(e)}")

                            finally:
                                # Mark entry as processed
                                st.session_state.bulk_email_processed_ids.add(bulk_entry.id)
                                processed_ids.add(bulk_entry.id)

                                # CLEANUP: Delete generated pass files immediately after email sent
                                # This prevents disk space issues during bulk operations
                                import os
                                for pass_file in generated_passes:
                                    try:
                                        # Only delete QR pass files (not invitation templates)
                                        if pass_file.exists() and "generated_passes" in str(pass_file):
                                            os.remove(pass_file)
                                    except Exception as cleanup_error:
                                        # Silent fail - cleanup errors shouldn't stop bulk operation
                                        pass

                            # Update progress bar
                            total_processed = len(st.session_state.bulk_email_processed_ids)
                            progress_bar.progress(total_processed / len(selected_entries))

                        # Check if all entries are processed
                        if len(st.session_state.bulk_email_processed_ids) >= len(selected_entries):
                            total_time = time.time() - start_time
                            progress_bar.empty()
                            status_text.empty()
                            time_text.empty()

                            st.success(f"✅ Bulk operation completed in {total_time:.0f} seconds ({total_time/60:.1f} minutes)")
                            if st.session_state.bulk_email_success_count > 0:
                                st.success(f"✅ Successfully sent {st.session_state.bulk_email_success_count} email(s)!")
                            if st.session_state.bulk_email_failed_count > 0:
                                st.error(f"❌ Failed to send {st.session_state.bulk_email_failed_count} email(s)")

                            # Reset session state
                            st.session_state.bulk_email_in_progress = False
                            st.session_state.bulk_email_processed_ids = set()
                            st.session_state.bulk_email_success_count = 0
                            st.session_state.bulk_email_failed_count = 0
                            st.session_state.bulk_email_start_time = None
                        else:
                            # More entries to process, trigger rerun to continue
                            time.sleep(0.1)  # Brief pause before rerun
                            st.rerun()
                else:
                    st.warning("Please select at least one attendee")
    finally:
        db.close()


def show_settings():
    """Settings page - User account management"""
    st.markdown("### ⚙️ Account Settings")

    user = st.session_state.user
    db = SessionLocal()

    try:
        # Get latest user data
        db_user = db.query(User).filter(User.username == user['username']).first()

        # Account Information Section
        st.markdown("#### 📋 Account Information")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            **Username:** {db_user.username}
            **Organization:** {db_user.organization}
            **Role:** {db_user.role.upper()}
            **Account Status:** {'🟢 Active' if db_user.is_active else '🔴 Inactive'}
            """)

        with col2:
            st.markdown(f"""
            **Max Entries:** {db_user.max_entries}
            **Created:** {db_user.created_at.strftime('%Y-%m-%d') if db_user.created_at else 'N/A'}
            **Last Login:** {db_user.last_login.strftime('%Y-%m-%d %H:%M') if db_user.last_login else 'Never'}
            """)

        st.markdown("---")

        # Pass Permissions Section
        st.markdown("#### 🎫 Pass Permissions")
        st.markdown("You are allowed to generate the following pass types:")

        import json
        # allowed_passes is already a dict from SQLAlchemy, no need to parse
        if isinstance(db_user.allowed_passes, str):
            allowed_passes = json.loads(db_user.allowed_passes)
        else:
            allowed_passes = db_user.allowed_passes if db_user.allowed_passes else {}

        cols = st.columns(4)

        # Exhibition Day 1
        with cols[0]:
            if allowed_passes.get('exhibition_day1', False):
                st.success('📅 Exhibition Day 1')
            else:
                st.error('~~📅 Exhibition Day 1~~')

        # Exhibition Day 2
        with cols[1]:
            if allowed_passes.get('exhibition_day2', False):
                st.success('📅 Exhibition Day 2')
            else:
                st.error('~~📅 Exhibition Day 2~~')

        # Interactive Sessions (combined - ONE pass for both sessions)
        with cols[2]:
            has_interactive = allowed_passes.get("interactive_sessions", False)
            if has_interactive:
                st.success('💡 Interactive Sessions')
            else:
                st.error('~~💡 Interactive Sessions~~')

        # Plenary
        with cols[3]:
            if allowed_passes.get('plenary', False):
                st.success('🎤 Plenary')
            else:
                st.error('~~🎤 Plenary~~')

        st.markdown("---")

        # Usage Statistics
        st.markdown("#### 📊 Your Usage Statistics")
        from app.models import Entry

        entries = db.query(Entry).filter(Entry.username == user['username']).all()
        total_entries = len(entries)

        # Count passes generated (number of individuals/entries with at least one pass)
        passes_generated = sum([
            1 for e in entries if (
                e.pass_generated_exhibition_day1 or
                e.pass_generated_exhibition_day2 or
                e.pass_generated_interactive_sessions or
                e.pass_generated_plenary
            )
        ])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Entries", total_entries)
        col2.metric("Quota Remaining", db_user.max_entries - total_entries)
        col3.metric("Passes Generated", passes_generated)
        col4.metric("Usage %", f"{(total_entries/db_user.max_entries*100):.1f}%" if db_user.max_entries > 0 else "0%")

        st.markdown("---")

        # Change Password Section (Future enhancement)
        st.markdown("#### 🔒 Security")
        st.info("🔐 Password change functionality - Contact TDAC to reset password")

    finally:
        db.close()


def show_admin_panel():
    """Admin panel - System monitoring and management"""
    st.markdown("### 👨‍💼 Admin Control Panel")

    user = st.session_state.user

    # Check if user is admin
    if user.get('role') != 'admin':
        st.error("🚫 Access Denied: Admin privileges required")
        return

    db = SessionLocal()

    try:
        from app.models import Entry, User, CheckIn, AuditLog
        from datetime import datetime

        # System Overview
        st.markdown("#### 📊 System Overview")

        # Get statistics
        # Include all users (including admin) who can create entries
        all_users = db.query(User).filter(User.role.in_(['admin', 'user'])).all()
        total_users = len(all_users)
        total_entries = db.query(Entry).count()
        total_quota = sum([u.max_entries for u in all_users])

        # Pass generation stats (count individuals/entries with at least one pass)
        all_entries = db.query(Entry).all()
        passes_generated = sum([
            1 for e in all_entries if (
                e.pass_generated_exhibition_day1 or
                e.pass_generated_exhibition_day2 or
                e.pass_generated_interactive_sessions or
                e.pass_generated_plenary
            )
        ])

        # Display metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Organizations", total_users)
        col2.metric("Total Quota", total_quota)
        col3.metric("Entries Created", total_entries)
        col4.metric("Quota Used", f"{(total_entries/total_quota*100):.1f}%" if total_quota > 0 else "0%")
        col5.metric("Passes Generated", passes_generated)

        st.markdown("---")

        # NIC Mail IP Whitelisting Helper
        st.markdown("#### 🌐 Server IP Address (For NIC Mail Whitelisting)")

        try:
            import requests
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            ip_data = response.json()
            public_ip = ip_data['ip']

            col1, col2 = st.columns([3, 1])
            with col1:
                st.info(f"""
                **Current Server IP Address:** `{public_ip}`

                To enable NIC SMTP email sending from this deployment:
                1. Copy the IP address above
                2. Go to [NIC Mail Security Settings](https://mail.mgovcloud.in)
                3. Click **"Add Allowed IP Address"**
                4. Select **"Add static IP address"**
                5. Enter: `{public_ip}`
                6. Save the settings

                ✅ After whitelisting, NIC SMTP authentication will work!
                """)
            with col2:
                if st.button("🔄 Refresh IP", help="Get current server IP"):
                    st.rerun()

        except Exception as e:
            st.warning(f"⚠️ Could not fetch server IP: {e}")
            st.info("Deploy this app to Streamlit Cloud, then check this section to get the IP address for whitelisting.")

        st.markdown("---")

        # Detailed Statistics by Pass Type
        st.markdown("#### 🎫 Pass Generation Statistics")

        # Row 1: Exhibition passes (visitors separate from exhibitors)
        col1, col2, col3 = st.columns(3)

        with col1:
            # Visitors only - Exhibition Day 1
            visitor_ex1_count = sum([1 for e in all_entries if e.exhibition_day1 and not getattr(e, 'is_exhibitor_pass', False)])
            visitor_ex1_generated = sum([1 for e in all_entries if e.pass_generated_exhibition_day1 and not getattr(e, 'is_exhibitor_pass', False)])
            st.metric("Exhibition Day 1 (Visitors)",
                     visitor_ex1_count,
                     delta=f"{visitor_ex1_generated} generated")

        with col2:
            # Visitors only - Exhibition Day 2
            visitor_ex2_count = sum([1 for e in all_entries if e.exhibition_day2 and not getattr(e, 'is_exhibitor_pass', False)])
            visitor_ex2_generated = sum([1 for e in all_entries if e.pass_generated_exhibition_day2 and not getattr(e, 'is_exhibitor_pass', False)])
            st.metric("Exhibition Day 2 (Visitors)",
                     visitor_ex2_count,
                     delta=f"{visitor_ex2_generated} generated")

        with col3:
            # Exhibitors - Combined pass for both days
            exhibitor_count = sum([1 for e in all_entries if getattr(e, 'is_exhibitor_pass', False)])
            exhibitor_generated = sum([1 for e in all_entries if getattr(e, 'is_exhibitor_pass', False) and e.pass_generated_exhibition_day1])
            st.metric("Exhibitor Passes (Both Days)",
                     exhibitor_count,
                     delta=f"{exhibitor_generated} generated")

        # Row 2: Interactive Sessions and Plenary
        col1, col2, col3 = st.columns(3)

        with col1:
            # Interactive Sessions
            interactive_count = sum([1 for e in all_entries if e.interactive_sessions])
            interactive_generated = sum([1 for e in all_entries if e.pass_generated_interactive_sessions])
            st.metric("Interactive Sessions",
                     interactive_count,
                     delta=f"{interactive_generated} generated")

        with col2:
            # Plenary
            plenary_count = sum([1 for e in all_entries if e.plenary])
            plenary_generated = sum([1 for e in all_entries if e.pass_generated_plenary])
            st.metric("Plenary",
                     plenary_count,
                     delta=f"{plenary_generated} generated")

        with col3:
            # Empty column for alignment
            pass

        st.markdown("---")

        # Organization-wise breakdown
        st.markdown("#### 🏢 Organization-wise Registration Status")

        org_data = []
        for user_obj in all_users:
            user_entries = db.query(Entry).filter(Entry.username == user_obj.username).all()
            entry_count = len(user_entries)

            # Count passes by type
            ex1 = sum([1 for e in user_entries if e.exhibition_day1])
            ex2 = sum([1 for e in user_entries if e.exhibition_day2])
            # Combined Interactive Sessions - ONE pass for both
            interactive = sum([1 for e in user_entries if (e.interactive_sessions)])
            pl = sum([1 for e in user_entries if e.plenary])

            # Calculate total quota from individual pass quotas
            total_quota = user_obj.quota_ex_day1 + user_obj.quota_interactive + user_obj.quota_plenary

            org_data.append({
                'Organization': user_obj.organization,
                'Username': user_obj.username,
                'Quota': total_quota,
                'Entries': entry_count,
                'Remaining': total_quota - entry_count,
                'Usage %': f"{(entry_count/total_quota*100):.1f}%" if total_quota > 0 else "0%",
                'Ex Day 1': ex1,
                'Ex Day 2': ex2,
                'Interactive Sessions': interactive,
                'Plenary': pl,
                'Status': '🟢' if user_obj.is_active else '🔴'
            })

        if org_data:
            df = pd.DataFrame(org_data)
            df = df.sort_values('Entries', ascending=False)
            st.dataframe(df, use_container_width=True, height=400)

            # Export button
            org_csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Organization Report (CSV)",
                data=org_csv,
                file_name=f"swavlamban2025_org_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No organizations registered yet")

        st.markdown("---")

        # All Entries View
        st.markdown("#### 📋 All Registered Entries")

        if all_entries:
            entry_data = []
            for entry in all_entries:
                # Determine entry type based on is_exhibitor_pass field (with fallback)
                # This field is set to True only for bulk uploaded exhibitors
                is_exhibitor = getattr(entry, 'is_exhibitor_pass', False)
                entry_type = "🏢 Exhibitor" if is_exhibitor else "👤 Visitor"

                # Build passes list - exhibitors show combined pass, visitors show individual
                passes_selected = []
                if is_exhibitor:
                    passes_selected.append("Exhibitor Pass")
                else:
                    if entry.exhibition_day1: passes_selected.append("Ex-1")
                    if entry.exhibition_day2: passes_selected.append("Ex-2")
                    if entry.interactive_sessions: passes_selected.append("Interactive")
                    if entry.plenary: passes_selected.append("Plenary")

                entry_data.append({
                    'ID': entry.id,
                    'Name': entry.name,
                    'Organization': db.query(User).filter(User.username == entry.username).first().organization,
                    'Email': entry.email,
                    'Phone': entry.phone,
                    'ID Type': entry.id_type,
                    'Entry Type': entry_type,
                    'Passes': ', '.join(passes_selected),
                    'Created': entry.created_at.strftime('%Y-%m-%d') if entry.created_at else 'N/A'
                })

            entries_df = pd.DataFrame(entry_data)
            st.dataframe(entries_df, use_container_width=True, height=400)

            # Export button
            entries_csv = entries_df.to_csv(index=False)
            st.download_button(
                label="📥 Download All Entries (CSV)",
                data=entries_csv,
                file_name=f"swavlamban2025_all_entries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No entries created yet")

        st.markdown("---")

        # System Health
        st.markdown("#### 💚 System Health")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.success("✅ Database: Online")
            st.info(f"Total Records: {total_entries}")

        with col2:
            import os
            from pathlib import Path

            # Get database file path dynamically
            project_root = Path(__file__).parent.parent
            db_file = project_root / "swavlamban2025.db"

            if db_file.exists():
                db_size = db_file.stat().st_size / 1024  # KB
                st.success(f"✅ Database Size: {db_size:.2f} KB")
            else:
                # Check if using PostgreSQL (Streamlit Cloud)
                import os
                if os.getenv("DB_HOST"):
                    st.success("✅ Database: PostgreSQL (Cloud)")
                else:
                    st.warning("⚠️ Database file not found")

        with col3:
            st.success(f"✅ Active Users: {total_users}")
            st.info(f"Admins: {db.query(User).filter(User.role == 'admin').count()}")

        st.markdown("---")

        # Quick Actions
        st.markdown("#### ⚡ Quick Actions")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("🔄 Refresh Statistics", use_container_width=True):
                st.rerun()

        with col2:
            if st.button("📧 Send Bulk Email", use_container_width=True):
                st.session_state.show_bulk_email = not st.session_state.get('show_bulk_email', False)

        with col3:
            if st.button("📤 Bulk Upload Exhibitors", use_container_width=True):
                st.session_state.show_bulk_exhibitors = not st.session_state.get('show_bulk_exhibitors', False)

        with col4:
            if st.button("👥 Manage Users", use_container_width=True):
                st.session_state.show_manage_users = not st.session_state.get('show_manage_users', False)

        # Get the states (default to False if not set)
        show_bulk_email = st.session_state.get('show_bulk_email', False)
        show_bulk_exhibitors = st.session_state.get('show_bulk_exhibitors', False)
        show_manage_users = st.session_state.get('show_manage_users', False)

        # Bulk Email Feature
        if show_bulk_email:
            st.markdown("---")
            st.markdown("### 📧 Bulk Email Sender")

            # Email filters
            st.markdown("#### 🎯 Select Recipients")

            col1, col2 = st.columns(2)

            with col1:
                email_option = st.radio(
                    "Send to:",
                    ["All Attendees", "By Pass Type", "By Organization", "Custom Selection"],
                    key="email_option"
                )

            with col2:
                if email_option == "By Pass Type":
                    pass_filter = st.multiselect(
                        "Select Pass Types:",
                        ["Exhibition Day 1", "Exhibition Day 2", "Interactive Sessions", "Plenary"],
                        key="pass_filter"
                    )
                elif email_option == "By Organization":
                    org_list = [u.organization for u in all_users]
                    org_filter = st.multiselect("Select Organizations:", org_list, key="org_filter")

            # Get filtered recipients
            recipients = []
            if email_option == "All Attendees":
                recipients = all_entries
            elif email_option == "By Pass Type":
                for entry in all_entries:
                    if "Exhibition Day 1" in pass_filter and entry.exhibition_day1:
                        recipients.append(entry)
                    elif "Exhibition Day 2" in pass_filter and entry.exhibition_day2:
                        recipients.append(entry)
                    elif "Interactive Sessions" in pass_filter and (entry.interactive_sessions):
                        recipients.append(entry)
                    elif "Plenary" in pass_filter and entry.plenary:
                        recipients.append(entry)
                recipients = list(set(recipients))  # Remove duplicates
            elif email_option == "By Organization":
                for entry in all_entries:
                    entry_user = db.query(User).filter(User.username == entry.username).first()
                    if entry_user and entry_user.organization in org_filter:
                        recipients.append(entry)

            st.info(f"📊 Recipients selected: **{len(recipients)}** attendees")

            if recipients:
                # Email composition
                st.markdown("#### ✍️ Compose Email")

                email_subject = st.text_input(
                    "Subject:",
                    value="Important Update - Swavlamban 2025",
                    key="email_subject"
                )

                email_body = st.text_area(
                    "Message:",
                    value="""Dear Attendee,

This is an important update regarding Swavlamban 2025 event.

Event Details:
- Date: November 25-26, 2025
- Venue: Manekshaw Centre (Exhibition Hall & Zorawar Hall)

Please keep your QR code pass ready for entry.

Best regards,
Swavlamban 2025 Team""",
                    height=200,
                    key="email_body"
                )

                include_passes = st.checkbox("Include QR code passes in email", value=False, key="include_passes")

                # Preview
                with st.expander("📋 Preview Email"):
                    st.markdown(f"**Subject:** {email_subject}")
                    st.markdown("**Body:**")
                    st.text(email_body)
                    st.markdown(f"**Recipients:** {len(recipients)}")
                    if include_passes:
                        st.info("✅ QR code passes will be attached")

                # Send button
                if st.button("📤 Send Bulk Email", type="primary", use_container_width=True, key="send_bulk"):
                    with st.spinner(f"Sending emails to {len(recipients)} recipients..."):
                        try:
                            # Import email services
                            from app.core.config import settings
                            from app.services.pass_generator import PassGenerator

                            # Choose email service based on configuration
                            if settings.USE_GMAIL_SMTP:
                                from app.services.gmail_smtp_service import GmailSMTPService
                                email_service = GmailSMTPService()
                                st.info("📧 Using Gmail SMTP (FREE)")
                            else:
                                from app.services.mailbluster_service import MailBlusterService
                                email_service = MailBlusterService()
                                st.info("📧 Using MailBluster")

                            pass_generator = PassGenerator()

                            success_count = 0
                            failed_count = 0

                            progress_bar = st.progress(0)
                            status_text = st.empty()

                            for idx, entry in enumerate(recipients):
                                try:
                                    status_text.text(f"Sending to {entry.email}... ({idx+1}/{len(recipients)})")

                                    # Prepare HTML email content
                                    html_content = f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1D4E89;">Swavlamban 2025</h2>
        <p>Dear {entry.name},</p>
        {email_body.replace(chr(10), '<br>')}
        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd;">
            <p style="color: #666; font-size: 14px;">
                Best regards,<br>
                <strong>Team Swavlamban 2025</strong><br>
                Indian Navy | Innovation & Self-Reliance
            </p>
        </div>
    </div>
</body>
</html>"""

                                    # Generate passes if needed
                                    passes = []
                                    attachments = []
                                    if include_passes:
                                        passes = pass_generator.generate_passes_for_entry(entry, user['username'])

                                        # Prepare attachments based on service type
                                        if settings.USE_GMAIL_SMTP:
                                            # Gmail SMTP uses file paths directly
                                            attachments = passes
                                        else:
                                            # MailBluster uses base64 encoded content
                                            import base64
                                            from pathlib import Path
                                            for pass_file in passes:
                                                if Path(pass_file).exists():
                                                    with open(pass_file, 'rb') as f:
                                                        file_content = base64.b64encode(f.read()).decode('utf-8')
                                                        attachments.append({
                                                            "filename": Path(pass_file).name,
                                                            "content": file_content,
                                                            "type": "image/png"
                                                        })

                                    # Send email using selected service
                                    if settings.USE_GMAIL_SMTP:
                                        # Gmail SMTP service
                                        success = email_service.send_email(
                                            to_email=entry.email,
                                            subject=email_subject,
                                            html_content=html_content,
                                            text_content=email_body,
                                            attachments=attachments if attachments else None
                                        )
                                    else:
                                        # MailBluster service
                                        success = email_service.send_transactional_email(
                                            to_email=entry.email,
                                            subject=email_subject,
                                            html_content=html_content,
                                            text_content=email_body,
                                            attachments=attachments if attachments else None,
                                            from_name="Swavlamban 2025 Team"
                                        )

                                    if success:
                                        success_count += 1
                                    else:
                                        failed_count += 1

                                except Exception as e:
                                    failed_count += 1
                                    st.warning(f"Failed to send to {entry.email}: {str(e)}")

                                # Update progress
                                progress_bar.progress((idx + 1) / len(recipients))

                            progress_bar.empty()
                            status_text.empty()

                            if success_count > 0:
                                st.success(f"✅ Successfully sent {success_count} emails!")
                                st.balloons()
                            if failed_count > 0:
                                st.error(f"❌ Failed to send {failed_count} emails")

                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                            import traceback
                            st.code(traceback.format_exc())

        # Bulk Upload Exhibitors Feature
        if show_bulk_exhibitors:
            st.markdown("---")
            st.markdown("### 📤 Bulk Upload Exhibitors")

            st.info("""
            **Upload a CSV file with exhibitor details** to automatically:
            - Create entries for all exhibitors
            - Generate exhibitor passes (valid for both Exhibition Days)
            - Send passes via email

            **CSV Format Required:**
            - Column 1: Firm Name
            - Column 2: Email Address
            - Column 3: Mobile Number
            - Column 4: Attendee 1 Name
            - Column 5: Attendee 1 Aadhar Number
            - Column 6: Attendee 2 Name
            - Column 7: Attendee 2 Aadhar Number
            - Column 8: Attendee 3 Name
            - Column 9: Attendee 3 Aadhar Number
            - ... (and so on for additional attendees)
            """)

            # CSV Upload
            uploaded_file = st.file_uploader(
                "📁 Upload Exhibitors CSV",
                type=['csv'],
                help="Upload CSV file with exhibitor details",
                key="exhibitor_csv_upload"
            )

            if uploaded_file is not None:
                try:
                    import re
                    from app.services.pass_generator import pass_generator
                    from app.services.email_service import email_service

                    # Read CSV
                    content = uploaded_file.read().decode('utf-8')
                    csv_reader = csv.reader(io.StringIO(content))
                    rows = list(csv_reader)

                    st.success(f"✅ CSV file loaded: {len(rows)} rows found")

                    # Show preview
                    st.markdown("#### 📋 CSV Preview (First 5 rows)")
                    preview_df = pd.DataFrame(rows[:6])  # Header + 5 rows
                    st.dataframe(preview_df, use_container_width=True)

                    # Parse and validate
                    st.markdown("#### 🔍 Parsing Data...")

                    exhibitors = []
                    errors = []

                    # Skip header row
                    for row_num, row in enumerate(rows[1:], start=2):
                        if len(row) < 3:
                            errors.append(f"Row {row_num}: Insufficient columns (need at least 3)")
                            continue

                        firm_name = row[0].strip()
                        email = row[1].strip()
                        mobile = row[2].strip()

                        # Validate email
                        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                        if not re.match(email_pattern, email):
                            errors.append(f"Row {row_num}: Invalid email format: {email}")
                            continue

                        # Validate mobile (10 digits)
                        mobile_clean = re.sub(r'[^\d]', '', mobile)
                        if len(mobile_clean) != 10:
                            errors.append(f"Row {row_num}: Invalid mobile number (need 10 digits): {mobile}")
                            continue

                        # Extract attendees (alternating Name/Aadhar: columns 3,4,5,6,7,8...)
                        # Column 3 (index 3): Attendee 1 Name
                        # Column 4 (index 4): Attendee 1 Aadhar
                        # Column 5 (index 5): Attendee 2 Name
                        # Column 6 (index 6): Attendee 2 Aadhar, etc.
                        attendees = []
                        col_idx = 3  # Start at column 4 (Attendee 1 Name)
                        while col_idx < len(row):
                            attendee_name = row[col_idx].strip() if col_idx < len(row) else ""
                            aadhar_num = row[col_idx + 1].strip() if (col_idx + 1) < len(row) else ""

                            if attendee_name and aadhar_num:
                                # Validate Aadhar (12 digits)
                                aadhar_clean = re.sub(r'[^\d]', '', aadhar_num)
                                if len(aadhar_clean) == 12:
                                    attendees.append({
                                        'name': attendee_name,
                                        'aadhar': aadhar_clean
                                    })
                                else:
                                    errors.append(f"Row {row_num}: Invalid Aadhar for {attendee_name}: {aadhar_num}")

                            col_idx += 2  # Move to next attendee

                        if not attendees:
                            errors.append(f"Row {row_num}: No valid attendees found")
                            continue

                        exhibitors.append({
                            'firm_name': firm_name,
                            'email': email,
                            'mobile': mobile_clean,
                            'attendees': attendees
                        })

                    # Show validation results
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("✅ Valid Exhibitors", len(exhibitors))
                    with col2:
                        st.metric("❌ Errors", len(errors))

                    if errors:
                        with st.expander("⚠️ View Validation Errors"):
                            for error in errors:
                                st.warning(error)

                    # Process button
                    if exhibitors:
                        st.markdown("---")
                        st.markdown(f"**Ready to process {len(exhibitors)} exhibitors**")

                        total_attendees = sum(len(ex['attendees']) for ex in exhibitors)
                        st.info(f"📊 Total attendees across all exhibitors: {total_attendees}")

                        if st.button("🚀 Process All Exhibitors", type="primary", use_container_width=True):
                            st.markdown("### 🔄 Processing Exhibitors...")

                            progress_bar = st.progress(0)
                            status_text = st.empty()

                            success_count = 0
                            failed_count = 0

                            for idx, exhibitor in enumerate(exhibitors):
                                status_text.text(f"Processing {idx + 1}/{len(exhibitors)}: {exhibitor['firm_name']}...")

                                try:
                                    all_passes_for_exhibitor = []
                                    skipped_attendees = []
                                    processed_attendees = 0

                                    # Process each attendee for this exhibitor
                                    for attendee in exhibitor['attendees']:
                                        try:
                                            # Check if Aadhar already exists
                                            existing_entry = db.query(Entry).filter(
                                                Entry.id_number == attendee['aadhar']
                                            ).first()

                                            if existing_entry:
                                                skipped_attendees.append(f"{attendee['name']} (Aadhar: {attendee['aadhar'][:4]}****{attendee['aadhar'][-4:]})")
                                                continue

                                            # Create entry in database
                                            new_entry = Entry(
                                                username=user['username'],  # TDAC admin
                                                name=attendee['name'],
                                                email=exhibitor['email'],  # Exhibitor's email
                                                phone=exhibitor['mobile'],
                                                id_type='Aadhar Card',
                                                id_number=attendee['aadhar'],
                                                # Exhibitor pass - ONLY set is_exhibitor_pass flag
                                                # Do NOT set exhibition_day1/day2 (causes filter issues)
                                                exhibition_day1=False,
                                                exhibition_day2=False,
                                                interactive_sessions=False,
                                                plenary=False,
                                                is_exhibitor_pass=True  # Exhibitor flag for bulk uploads
                                            )

                                            db.add(new_entry)
                                            db.commit()
                                            db.refresh(new_entry)

                                            # Generate exhibitor pass (EP-25n26.png)
                                            generated_passes = pass_generator.generate_passes_for_entry(new_entry, user['username'])
                                            all_passes_for_exhibitor.extend(generated_passes)

                                            # Update database flags
                                            new_entry.pass_generated_exhibition_day1 = True
                                            new_entry.pass_generated_exhibition_day2 = True
                                            db.commit()

                                            processed_attendees += 1

                                        except Exception as attendee_error:
                                            skipped_attendees.append(f"{attendee['name']} (Error: {str(attendee_error)[:50]})")
                                            db.rollback()
                                            continue

                                    # Show warnings for skipped attendees
                                    if skipped_attendees:
                                        st.warning(f"⚠️ {exhibitor['firm_name']}: Skipped {len(skipped_attendees)} attendee(s) - {', '.join(skipped_attendees)}")

                                    # Send email only if at least one attendee was processed
                                    if processed_attendees > 0:
                                        email_success = email_service.send_exhibitor_bulk_email(
                                            recipient_email=exhibitor['email'],
                                            recipient_name=exhibitor['firm_name'],
                                            pass_files=all_passes_for_exhibitor
                                        )

                                        if email_success:
                                            success_count += 1
                                        else:
                                            failed_count += 1
                                            st.warning(f"⚠️ Email failed for {exhibitor['firm_name']}")
                                    else:
                                        failed_count += 1
                                        st.error(f"❌ {exhibitor['firm_name']}: All attendees were duplicates or failed")

                                except Exception as e:
                                    failed_count += 1
                                    st.warning(f"⚠️ Failed for {exhibitor['firm_name']}: {str(e)}")
                                    db.rollback()

                                progress_bar.progress((idx + 1) / len(exhibitors))

                            progress_bar.empty()
                            status_text.empty()

                            st.markdown("---")
                            st.markdown("### 📊 Processing Complete!")

                            col1, col2 = st.columns(2)
                            with col1:
                                st.success(f"✅ Successfully processed: {success_count} exhibitors")
                            with col2:
                                if failed_count > 0:
                                    st.error(f"❌ Failed: {failed_count} exhibitors")

                            st.balloons()

                            if st.button("🔄 Refresh Dashboard"):
                                st.rerun()

                except Exception as e:
                    st.error(f"❌ Error processing CSV: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())

        # Manage Users Feature
        if show_manage_users:
            st.markdown("---")
            st.markdown("### 👥 User Management")

            tab1, tab2, tab3 = st.tabs(["📋 View Users", "➕ Add User", "✏️ Edit User"])

            # Tab 1: View Users
            with tab1:
                st.markdown("#### 👥 All Organizations")

                if all_users:
                    for idx, user_obj in enumerate(all_users):
                        with st.expander(f"{user_obj.organization} (@{user_obj.username})"):
                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.write(f"**Username:** {user_obj.username}")
                                st.write(f"**Organization:** {user_obj.organization}")
                                st.write(f"**Role:** {user_obj.role}")

                            with col2:
                                st.write(f"**Max Entries (Bulk Upload):** {user_obj.max_entries}")
                                st.write("**Pass Quotas:**")
                                # Get quotas with safe fallback
                                quota_ex1 = getattr(user_obj, 'quota_ex_day1', 0)
                                quota_ex2 = getattr(user_obj, 'quota_ex_day2', 0)
                                quota_interactive = getattr(user_obj, 'quota_interactive', 0)
                                quota_plenary = getattr(user_obj, 'quota_plenary', 0)
                                st.write(f"  • Ex Day 1: {quota_ex1}")
                                st.write(f"  • Ex Day 2: {quota_ex2}")
                                st.write(f"  • Interactive: {quota_interactive}")
                                st.write(f"  • Plenary: {quota_plenary}")

                            with col3:
                                st.write(f"**Status:** {'🟢 Active' if user_obj.is_active else '🔴 Inactive'}")
                                st.write(f"**Created:** {user_obj.created_at.strftime('%Y-%m-%d') if user_obj.created_at else 'N/A'}")
                                st.write(f"**Last Login:** {user_obj.last_login.strftime('%Y-%m-%d') if user_obj.last_login else 'Never'}")

                            # Quick actions
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button(f"🔄 Reset Password", key=f"reset_{idx}"):
                                    # Generate random password (8 chars: letters + digits)
                                    import random
                                    import string
                                    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

                                    # Update password
                                    user_obj.password_hash = hash_password(new_password)
                                    db.commit()

                                    st.success(f"✅ Password reset successful for {user_obj.username}!")
                                    st.info(f"**New Password:** `{new_password}`\n\n⚠️ **IMPORTANT:** Copy this password now - it cannot be recovered!")
                                    st.warning(f"Please share this password securely with the user.")
                            with col2:
                                if user_obj.is_active:
                                    if st.button(f"🔴 Deactivate", key=f"deactivate_{idx}"):
                                        user_obj.is_active = False
                                        db.commit()
                                        st.success(f"User {user_obj.username} deactivated")
                                        st.rerun()
                                else:
                                    if st.button(f"🟢 Activate", key=f"activate_{idx}"):
                                        user_obj.is_active = True
                                        db.commit()
                                        st.success(f"User {user_obj.username} activated")
                                        st.rerun()
                else:
                    st.info("No organizations registered yet")

            # Tab 2: Add User
            with tab2:
                print("🟢 TAB 2 (Add User) IS RENDERING")
                st.markdown("#### ➕ Create New Organization Account")

                print("🟢 ABOUT TO CREATE FORM")
                with st.form("add_user_form"):
                    print("🟢 INSIDE FORM BLOCK")
                    col1, col2 = st.columns(2)

                    with col1:
                        new_username = st.text_input("Username*", placeholder="e.g., drdo")
                        new_organization = st.text_input("Organization Name*", placeholder="e.g., DRDO")
                        new_max_entries = st.number_input("Max Entries (Bulk Upload)*", min_value=0, value=0,
                                                         help="For admin bulk upload of exhibitors only")

                    with col2:
                        new_password = st.text_input("Password*", type="password", placeholder="Minimum 8 characters")
                        new_role = st.selectbox("Role*", ["user", "admin", "scanner"])
                        new_active = st.checkbox("Active", value=True)

                    st.markdown("**Pass Quotas (per type):**")
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        new_quota_ex1 = st.number_input("Exhibition Day 1", min_value=0, value=0, key="new_quota_ex1")
                    with col2:
                        new_quota_ex2 = st.number_input("Exhibition Day 2", min_value=0, value=0, key="new_quota_ex2")
                    with col3:
                        new_quota_interactive = st.number_input("Interactive Sessions", min_value=0, value=0, key="new_quota_interactive")
                    with col4:
                        new_quota_plenary = st.number_input("Plenary Session", min_value=0, value=0, key="new_quota_plenary")

                    st.markdown("**Pass Permissions:**")
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        allow_ex1 = st.checkbox("Exhibition Day 1", value=True, key="new_ex1")
                    with col2:
                        allow_ex2 = st.checkbox("Exhibition Day 2", value=True, key="new_ex2")
                    with col3:
                        # Combined Interactive Sessions - ONE pass for both sessions
                        allow_interactive = st.checkbox("Interactive Sessions", value=False, key="new_interactive",
                                                       help="ONE pass for both Session I & II")
                        # Set both panel flags when interactive is checked
                        allow_interactive = allow_interactive
                        allow_interactive = allow_interactive
                    with col4:
                        allow_plenary = st.checkbox("Plenary", value=False, key="new_plenary")

                    submitted = st.form_submit_button("➕ Create User", use_container_width=True, type="primary")

                    if submitted:
                        print(f"🔔 FORM SUBMITTED! Username: {new_username}, Org: {new_organization}")
                        if not new_username or not new_organization or not new_password:
                            print(f"❌ Validation failed: Missing fields")
                            st.error("❌ Please fill all required fields")
                        elif len(new_password) < 8:
                            print(f"❌ Validation failed: Password too short ({len(new_password)} chars)")
                            st.error("❌ Password must be at least 8 characters")
                        else:
                            print(f"✅ Validation passed, attempting to create user")
                            try:
                                # Check if username exists
                                print(f"Checking if username '{new_username}' exists...")
                                existing = db.query(User).filter(User.username == new_username).first()
                                if existing:
                                    print(f"❌ Username already exists")
                                    st.error(f"❌ Username '{new_username}' already exists")
                                else:
                                    # Create new user
                                    allowed_passes_dict = {
                                        "exhibition_day1": allow_ex1,
                                        "exhibition_day2": allow_ex2,
                                        "interactive_sessions": allow_interactive,
                                        "plenary": allow_plenary
                                    }

                                    print(f"Creating user: {new_username}")
                                    print(f"Allowed passes: {allowed_passes_dict}")

                                    new_user = User(
                                        username=new_username,
                                        password_hash=hash_password(new_password),
                                        organization=new_organization,
                                        max_entries=new_max_entries,
                                        quota_ex_day1=new_quota_ex1,
                                        quota_ex_day2=new_quota_ex2,
                                        quota_interactive=new_quota_interactive,
                                        quota_plenary=new_quota_plenary,
                                        role=new_role,
                                        allowed_passes=allowed_passes_dict,
                                        is_active=new_active
                                    )

                                    print(f"User object created: {new_user}")
                                    db.add(new_user)
                                    print(f"User added to session")
                                    db.commit()
                                    print(f"Commit successful")
                                    db.refresh(new_user)  # Ensure user is in DB
                                    print(f"User refreshed from DB")

                                    # Verify user was created
                                    verify_user = db.query(User).filter(User.username == new_username).first()
                                    if verify_user:
                                        st.success(f"✅ User '{new_username}' created successfully!")
                                        st.balloons()
                                        st.info(f"**Credentials:**\nUsername: {new_username}\nPassword: {new_password}\n\n⚠️ Save these credentials - password cannot be recovered!")
                                        # Trigger rerun to refresh user list
                                        import time
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error(f"❌ User created but verification failed - please refresh page")

                            except Exception as e:
                                db.rollback()  # Rollback on error
                                st.error(f"❌ Error creating user: {str(e)}")
                                import traceback
                                st.error(f"Details: {traceback.format_exc()}")

            # Tab 3: Edit User
            with tab3:
                st.markdown("#### ✏️ Edit Organization Account")

                if all_users:
                    edit_user_options = [f"{u.organization} (@{u.username})" for u in all_users]
                    selected_user_str = st.selectbox("Select User to Edit:", edit_user_options)

                    if selected_user_str:
                        # Extract username
                        edit_username = selected_user_str.split("@")[1].rstrip(")")
                        edit_user = db.query(User).filter(User.username == edit_username).first()

                        if edit_user:
                            with st.form("edit_user_form"):
                                st.markdown(f"**Editing: {edit_user.organization}**")

                                col1, col2 = st.columns(2)

                                with col1:
                                    edit_org = st.text_input("Organization Name", value=edit_user.organization)
                                    edit_max = st.number_input("Max Entries (Bulk Upload)", min_value=0, value=edit_user.max_entries,
                                                              help="For admin bulk upload of exhibitors only")
                                    # Password change option
                                    edit_password = st.text_input("New Password (leave blank to keep current)",
                                                                 type="password",
                                                                 placeholder="Enter new password or leave blank",
                                                                 help="Minimum 8 characters. Leave blank to keep existing password.")

                                with col2:
                                    edit_role = st.selectbox("Role", ["user", "admin", "scanner"],
                                                            index=["user", "admin", "scanner"].index(edit_user.role))
                                    edit_active = st.checkbox("Active", value=edit_user.is_active)

                                st.markdown("**Pass Quotas (per type):**")
                                col1, col2, col3, col4 = st.columns(4)

                                with col1:
                                    edit_quota_ex1 = st.number_input("Exhibition Day 1", min_value=0,
                                                                    value=getattr(edit_user, 'quota_ex_day1', 0),
                                                                    key="edit_quota_ex1")
                                with col2:
                                    edit_quota_ex2 = st.number_input("Exhibition Day 2", min_value=0,
                                                                    value=getattr(edit_user, 'quota_ex_day2', 0),
                                                                    key="edit_quota_ex2")
                                with col3:
                                    edit_quota_interactive = st.number_input("Interactive Sessions", min_value=0,
                                                                            value=getattr(edit_user, 'quota_interactive', 0),
                                                                            key="edit_quota_interactive")
                                with col4:
                                    edit_quota_plenary = st.number_input("Plenary Session", min_value=0,
                                                                        value=getattr(edit_user, 'quota_plenary', 0),
                                                                        key="edit_quota_plenary")

                                # Parse current permissions
                                current_perms = edit_user.allowed_passes if edit_user.allowed_passes else {}

                                st.markdown("**Pass Permissions:**")
                                col1, col2, col3, col4 = st.columns(4)

                                with col1:
                                    edit_ex1 = st.checkbox("Exhibition Day 1", value=current_perms.get("exhibition_day1", False), key="edit_ex1")
                                with col2:
                                    edit_ex2 = st.checkbox("Exhibition Day 2", value=current_perms.get("exhibition_day2", False), key="edit_ex2")
                                with col3:
                                    # Combined Interactive Sessions - ONE pass for both sessions
                                    current_interactive = current_perms.get("interactive_sessions", False)
                                    edit_interactive = st.checkbox("Interactive Sessions", value=current_interactive, key="edit_interactive",
                                                                  help="ONE pass for both Session I & II")
                                    # Set both panel flags when interactive is checked
                                    edit_interactive = edit_interactive
                                    edit_interactive = edit_interactive
                                with col4:
                                    edit_plenary = st.checkbox("Plenary", value=current_perms.get("plenary", False), key="edit_plenary")

                                col1, col2 = st.columns(2)

                                with col1:
                                    update_submitted = st.form_submit_button("💾 Update User", use_container_width=True, type="primary")

                                with col2:
                                    delete_submitted = st.form_submit_button("🗑️ Delete User", use_container_width=True)

                                if update_submitted:
                                    try:
                                        # Validate password if provided
                                        if edit_password:
                                            if len(edit_password) < 8:
                                                st.error("❌ Password must be at least 8 characters")
                                                st.stop()
                                            # Update password hash
                                            edit_user.password_hash = hash_password(edit_password)

                                        # Update other fields
                                        edit_user.organization = edit_org
                                        edit_user.max_entries = edit_max
                                        edit_user.quota_ex_day1 = edit_quota_ex1
                                        edit_user.quota_ex_day2 = edit_quota_ex2
                                        edit_user.quota_interactive = edit_quota_interactive
                                        edit_user.quota_plenary = edit_quota_plenary
                                        edit_user.role = edit_role
                                        edit_user.is_active = edit_active
                                        edit_user.allowed_passes = {
                                            "exhibition_day1": edit_ex1,
                                            "exhibition_day2": edit_ex2,
                                            "interactive_sessions": edit_interactive,
                                            "plenary": edit_plenary
                                        }

                                        db.commit()
                                        if edit_password:
                                            st.success(f"✅ User '{edit_username}' updated successfully! Password has been changed.")
                                        else:
                                            st.success(f"✅ User '{edit_username}' updated successfully!")
                                        st.rerun()

                                    except Exception as e:
                                        st.error(f"❌ Error updating user: {str(e)}")

                                if delete_submitted:
                                    st.warning("⚠️ Deleting a user will also delete all their entries!")
                                    confirm_delete = st.checkbox("I understand - Delete this user and all entries")

                                    if confirm_delete:
                                        try:
                                            db.delete(edit_user)
                                            db.commit()
                                            st.success(f"✅ User '{edit_username}' deleted successfully!")
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"❌ Error deleting user: {str(e)}")
                else:
                    st.info("No users available to edit")

    except Exception as e:
        st.error(f"❌ Admin Panel Error: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        print(f"❌ ADMIN PANEL EXCEPTION: {e}")
        print(traceback.format_exc())
    finally:
        db.close()


def ensure_default_admin():
    """Create default admin user if no users exist"""
    from app.core.security import hash_password

    db = SessionLocal()
    try:
        # Check if any users exist
        user_count = db.query(User).count()

        if user_count == 0:
            # Create default admin user
            admin = User(
                username="admin",
                password_hash=hash_password("admin123"),
                organization="TDAC",
                max_entries=999,
                role="admin",
                allowed_passes={
                    "exhibition_day1": True,
                    "exhibition_day2": True,
                    "interactive_sessions": True,
                    "interactive_sessions": True,
                    "plenary": True
                },
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("✅ Created default admin user: admin / admin123")
    except Exception as e:
        db.rollback()
        print(f"⚠️  Error creating default admin: {e}")
    finally:
        db.close()


def main():
    """Main application entry point"""
    # Initialize database
    init_db()

    # Ensure default admin user exists
    ensure_default_admin()

    # Initialize session state
    init_session_state()

    # Show appropriate page
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()


if __name__ == "__main__":
    main()
