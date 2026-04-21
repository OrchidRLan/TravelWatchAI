import streamlit as st

st.set_page_config(
    page_title="TravelWatch AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Inactive sidebar buttons */
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] .stButton > button p,
[data-testid="stSidebar"] .stButton > button span,
[data-testid="stSidebar"] .stButton > button div {
    color: #1e3a8a !important;
}

/* Active sidebar button */
[data-testid="stSidebar"] .stButton > button[kind="primary"],
[data-testid="stSidebar"] .stButton > button[kind="primary"] p,
[data-testid="stSidebar"] .stButton > button[kind="primary"] span,
[data-testid="stSidebar"] .stButton > button[kind="primary"] div {
    color: #ffffff !important;
}

/* Hide default Streamlit nav */
[data-testid="stSidebarNav"] { display: none; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0a0a0f;
    border-right: 1px solid #1e1e2e;
}
[data-testid="stSidebar"] * { color: #e2e2e8 !important; }

/* Main background */
[data-testid="stAppViewContainer"] {
    background: #f7f7fb;
}

/* Button text ONLY */
.stButton > button {
    color: #1e3a8a !important;
}          
/* Metric cards */
.tw-card {
    background: #ffffff;
    border: 1px solid #e8e8f0;
    border-radius: 14px;
    padding: 20px 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.tw-card-dark {
    background: #0a0a0f;
    border: 1px solid #1e1e2e;
    border-radius: 14px;
    padding: 20px 24px;
    color: #e2e2e8;
}
.tw-badge-buy {
    background: #d4f7e7;
    color: #0a6640;
    border-radius: 999px;
    padding: 4px 14px;
    font-weight: 600;
    font-size: 13px;
    display: inline-block;
}
.tw-badge-wait {
    background: #fde8d8;
    color: #7a3010;
    border-radius: 999px;
    padding: 4px 14px;
    font-weight: 600;
    font-size: 13px;
    display: inline-block;
}
.tw-page-title {
    font-size: 26px;
    font-weight: 700;
    color: #0a0a0f;
    margin-bottom: 6px;
}
.tw-section-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 6px;
}
.tw-route-card {
    background: #fff;
    border: 1px solid #e8e8f0;
    border-radius: 12px;
    padding: 18px 20px;
    cursor: pointer;
    transition: box-shadow 0.2s;
}
.tw-route-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.08); }

</style>
""", unsafe_allow_html=True)

# ── Session state defaults ───────────────────────────────────────────────────
if "watches" not in st.session_state:
    st.session_state.watches = [
        {"id": 1, "origin": "JFK", "dest": "LAX", "dep_date": "2026-05-10",
         "arr_date": "2026-05-17", "target": 300, "currency": "USD",
         "current_price": 287, "recommendation": "BUY", "confidence": 0.82},
        {"id": 2, "origin": "LGA", "dest": "ORD", "dep_date": "2026-06-01",
         "arr_date": "2026-06-08", "target": 180, "currency": "USD",
         "current_price": 210, "recommendation": "WAIT", "confidence": 0.71},
        {"id": 3, "origin": "EWR", "dest": "MIA", "dep_date": "2026-06-15",
         "arr_date": "2026-06-22", "target": 220, "currency": "USD",
         "current_price": 198, "recommendation": "BUY", "confidence": 0.76},
    ]
if "selected_watch_id" not in st.session_state:
    st.session_state.selected_watch_id = 1
if "currency" not in st.session_state:
    st.session_state.currency = "USD"
if "email_notif" not in st.session_state:
    st.session_state.email_notif = True
if "price_alert" not in st.session_state:
    st.session_state.price_alert = True
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 28px 0;'>
        <div style='font-size:22px; font-weight:700; letter-spacing:-0.5px; color:#fff;'>
            ✈ TravelWatch
        </div>
        <div style='font-size:11px; color:#555; margin-top:2px; font-family: DM Mono, monospace;'>
            AI Price Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    pages = ["Dashboard", "Add New Watch", "Task Detail", "Compare", "ML Insights", "Settings"]
    icons = ["⬛", "➕", "📋", "⚖️", "🧠", "⚙️"]

    for icon, pg in zip(icons, pages):
        active = st.session_state.page == pg
        if st.button(
            f"{icon}  {pg}",
            key=f"nav_{pg}",
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            st.session_state.page = pg
            st.rerun()

    st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:12px; color:#555; padding: 8px 0;'>
        <div style='color:#888; margin-bottom:4px;'>Signed in as</div>
        <div style='color:#ccc;'>{st.session_state.user_email or 'user@example.com'}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Page router ──────────────────────────────────────────────────────────────
page = st.session_state.page

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from pages import dashboard, task_detail, add_watch, compare, ml_insights, settings

if page == "Dashboard":
    dashboard.render()
elif page == "Task Detail":
    task_detail.render()
elif page == "Add New Watch":
    add_watch.render()
elif page == "Compare":
    compare.render()
elif page == "ML Insights":
    ml_insights.render()
elif page == "Settings":
    settings.render()

dashboard.render()
