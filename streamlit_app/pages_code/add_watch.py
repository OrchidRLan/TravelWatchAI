import streamlit as st
from datetime import date, timedelta
import numpy as np

CURRENCIES = ["USD", "EUR", "GBP", "JPY", "KRW", "CAD", "AUD", "CHF", "CNY", "INR",
              "SGD", "HKD", "MXN", "BRL", "SEK", "NOK", "DKK", "NZD", "ZAR", "AED"]

CITIES = ["NYC", "LAX", "SFO", "Chicago", "Miami", "London", "Tokyo", "Paris",
          "Seoul", "Sydney", "Dubai", "Singapore", "Toronto", "Amsterdam", "Barcelona"]


def render():
    # ── Header ────────────────────────────────────────────────────────────────
    col_title, col_btn = st.columns([5, 1])
    with col_title:
        back_col, title_col = st.columns([1, 10])
        with back_col:
            if st.button("←", key="back_btn"):
                st.session_state.page = "Dashboard"
                st.rerun()
        with title_col:
            st.markdown('<h2 style="font-size:24px;font-weight:700;color:#111;margin:0;">Add New Watch</h2>', unsafe_allow_html=True)
    with col_btn:
        start_btn = st.button("Start Watching", type="primary", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Form fields ───────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Origin <span style="color:#ef4444;">*</span></div>', unsafe_allow_html=True)
    origin = st.selectbox("Origin", options=CITIES, index=0,
                          placeholder="Select Origin...", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Destination <span style="color:#ef4444;">*</span></div>', unsafe_allow_html=True)
    dest = st.selectbox("Destination", options=CITIES, index=1,
                        placeholder="Select Destination...", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Departure Date <span style="color:#ef4444;">*</span></div>', unsafe_allow_html=True)
    dep_date = st.date_input("Departure Date", value=date.today() + timedelta(days=30),
                             min_value=date.today(), label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Arrival Date <span style="color:#ef4444;">*</span></div>', unsafe_allow_html=True)
    arr_date = st.date_input("Arrival Date", value=date.today() + timedelta(days=37),
                             min_value=date.today(), label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Target Price <span style="color:#ef4444;">*</span></div>', unsafe_allow_html=True)
    target_price = st.number_input("Target Price", min_value=50, max_value=10000,
                                   value=300, step=10, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Currency <span style="color:#ef4444;">*</span></div>', unsafe_allow_html=True)
    currency = st.selectbox("Currency", options=CURRENCIES, index=0,
                            placeholder="Select Currency", label_visibility="collapsed")

    # ── Submit ────────────────────────────────────────────────────────────────
    if start_btn:
        if origin == dest:
            st.error("Origin and destination cannot be the same.")
        elif dep_date >= arr_date:
            st.error("Arrival date must be after departure date.")
        else:
            np.random.seed(len(st.session_state.watches) + 10)
            new_id = max(w["id"] for w in st.session_state.watches) + 1
            current_price = int(target_price * np.random.uniform(0.85, 1.25))
            rec = "BUY" if current_price <= target_price * 1.05 else "WAIT"
            change_dir = "down" if rec == "BUY" else "up"
            st.session_state.watches.append({
                "id": new_id,
                "origin": origin, "dest": dest,
                "dep_date": str(dep_date), "arr_date": str(arr_date),
                "target": target_price, "currency": currency,
                "current_price": current_price,
                "recommendation": rec,
                "confidence": int(np.random.uniform(60, 90)),
                "change_pct": round(np.random.uniform(0.5, 2.5), 1),
                "change_dir": change_dir,
            })
            st.success(f"✅ Now watching {origin} → {dest}!")
            st.session_state.page = "Dashboard"
            st.rerun()
