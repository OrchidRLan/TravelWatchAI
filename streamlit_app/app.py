import streamlit as st

st.set_page_config(
    page_title="TravelWatch AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Hide default nav */
[data-testid="stSidebarNav"] { display: none; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #f0f0f0;
    padding-top: 0;
}
[data-testid="stSidebar"] > div:first-child { padding: 0; }

/* Remove default padding */
.block-container { padding: 2rem 2.5rem 2rem 2.5rem !important; }

/* Main background */
[data-testid="stAppViewContainer"] { background: #f5f5f5; }
[data-testid="stAppViewContainer"] > .main { background: #f5f5f5; }

/* Main content white card */
.main-content {
    background: #ffffff;
    border-radius: 16px;
    padding: 32px 36px;
    min-height: 90vh;
}

/* Cards */
.tw-card {
    background: #ffffff;
    border: 1px solid #ebebeb;
    border-radius: 12px;
    padding: 18px 20px;
}
.tw-card-sm {
    background: #ffffff;
    border: 1px solid #ebebeb;
    border-radius: 10px;
    padding: 12px 16px;
}

/* Badges */
.badge-buy {
    background: #1a56db;
    color: #fff;
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}
.badge-wait {
    background: #6b7280;
    color: #fff;
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

/* Section label */
.sec-label {
    font-size: 12px;
    color: #9ca3af;
    margin-bottom: 6px;
    font-weight: 500;
}

/* Nav item active */
.nav-active {
    background: #f3f4f6;
    border-radius: 8px;
    font-weight: 600;
}

/* Button overrides */
.stButton > button {
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
}
.stButton > button[kind="primary"] {
    background: #1a56db;
    border: none;
    color: white;
}

/* Input fields */
.stSelectbox > div, .stTextInput > div, .stDateInput > div, .stNumberInput > div {
    border-radius: 8px;
}

/* Radio buttons */
div[data-testid="stRadio"] > div {
    border: 1px solid #ebebeb;
    border-radius: 10px;
    padding: 8px 12px;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "watches" not in st.session_state:
    st.session_state.watches = [
        {"id": 1, "origin": "NYC", "dest": "LAX",
         "dep_date": "May 12, 2026", "arr_date": "May 23, 2026",
         "target": 300, "currency": "USD", "current_price": 348,
         "recommendation": "WAIT", "confidence": 72, "change_pct": 1.3, "change_dir": "up"},
        {"id": 2, "origin": "SFO", "dest": "Tokyo",
         "dep_date": "Jun 1, 2026", "arr_date": "Jun 15, 2026",
         "target": 650, "currency": "USD", "current_price": 780,
         "recommendation": "WAIT", "confidence": 72, "change_pct": 0.9, "change_dir": "up"},
        {"id": 3, "origin": "NYC", "dest": "London",
         "dep_date": "Jul 4, 2026", "arr_date": "Jul 18, 2026",
         "target": 550, "currency": "USD", "current_price": 512,
         "recommendation": "BUY", "confidence": 68, "change_pct": 1.2, "change_dir": "down"},
    ]
if "selected_watch_id" not in st.session_state:
    st.session_state.selected_watch_id = 1
if "currency" not in st.session_state:
    st.session_state.currency = "USD"
if "email_notif" not in st.session_state:
    st.session_state.email_notif = "On"
if "price_alert" not in st.session_state:
    st.session_state.price_alert = "On"
if "user_email" not in st.session_state:
    st.session_state.user_email = "lp346@cornell.edu"
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div style='padding: 28px 20px 20px 20px; border-bottom: 1px solid #f0f0f0;'>
        <div style='display:flex; align-items:center; gap:8px;'>
            <span style='font-size:22px;'>🪁</span>
            <span style='font-size:17px; font-weight:700; color:#111;'>TravelWatch AI</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='padding: 16px 12px 8px 12px;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px; font-weight:600; color:#9ca3af; letter-spacing:0.08em; margin-bottom:8px;'>MENU</div>", unsafe_allow_html=True)

    pages = [("🏠", "Dashboard"), ("📄", "Compare"), ("📊", "ML Insights")]
    for icon, pg in pages:
        active = st.session_state.page == pg
        if st.button(
            f"{icon}  {pg}",
            key=f"nav_{pg}",
            use_container_width=True,
            type="secondary",
        ):
            st.session_state.page = pg
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Settings + User profile at bottom
    st.markdown("<div style='position:absolute; bottom:0; left:0; right:0; padding:16px 12px; border-top:1px solid #f0f0f0;'>", unsafe_allow_html=True)
    if st.button("⚙️  Settings", key="nav_Settings", use_container_width=True):
        st.session_state.page = "Settings"
        st.rerun()

    st.markdown(f"""
    <div style='background:#f9f9f9; border:1px solid #ebebeb; border-radius:10px;
                padding:10px 12px; margin-top:8px; display:flex; align-items:center; gap:10px;'>
        <div style='width:32px; height:32px; background:#e05c3a; border-radius:8px;
                    display:flex; align-items:center; justify-content:center;
                    color:white; font-weight:700; font-size:13px;'>L</div>
        <div>
            <div style='font-size:13px; font-weight:600; color:#111;'>Lena Park</div>
            <div style='font-size:11px; color:#9ca3af;'>{st.session_state.user_email}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Page router ───────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "Dashboard":
    from pages_code.dashboard import render
elif page == "Add New Watch":
    from pages_code.add_watch import render
elif page == "Task Detail":
    from pages_code.task_detail import render
elif page == "Compare":
    from pages_code.compare import render
elif page == "ML Insights":
    from pages_code.ml_insights import render
elif page == "Settings":
    from pages_code.settings import render

render()
