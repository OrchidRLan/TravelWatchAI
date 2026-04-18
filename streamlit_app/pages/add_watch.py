import streamlit as st
from datetime import date, timedelta

CURRENCIES = ["USD", "EUR", "GBP", "JPY", "KRW", "CAD", "AUD", "CHF", "CNY", "INR",
              "SGD", "HKD", "MXN", "BRL", "SEK", "NOK", "DKK", "NZD", "ZAR", "AED"]

IATA_CODES = ["JFK", "LAX", "ORD", "LGA", "EWR", "SFO", "MIA", "ATL", "DFW",
              "BOS", "SEA", "DEN", "LHR", "CDG", "AMS", "NRT", "ICN", "SIN",
              "HKG", "DXB", "SYD", "YYZ", "GRU", "MEX", "FCO", "BCN", "MUC"]


def render():
    col_title, col_btn = st.columns([4, 1])
    with col_title:
        st.markdown('<div class="tw-page-title">Add New Watch</div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="color:#888; font-size:14px;">Track a new route and get Buy/Wait recommendations</div>',
            unsafe_allow_html=True,
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="tw-section-label">Origin</div>', unsafe_allow_html=True)
            origin = st.selectbox(
                "Origin Airport (IATA)",
                options=IATA_CODES,
                index=0,
                label_visibility="collapsed",
            )
        with col2:
            st.markdown('<div class="tw-section-label">Destination</div>', unsafe_allow_html=True)
            dest = st.selectbox(
                "Destination Airport (IATA)",
                options=IATA_CODES,
                index=1,
                label_visibility="collapsed",
            )

        st.markdown("<br>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="tw-section-label">Departure Date</div>', unsafe_allow_html=True)
            dep_date = st.date_input(
                "Departure Date",
                value=date.today() + timedelta(days=30),
                min_value=date.today(),
                label_visibility="collapsed",
            )
        with col4:
            st.markdown('<div class="tw-section-label">Return / Arrival Date</div>', unsafe_allow_html=True)
            arr_date = st.date_input(
                "Arrival Date",
                value=date.today() + timedelta(days=37),
                min_value=date.today(),
                label_visibility="collapsed",
            )

        st.markdown("<br>", unsafe_allow_html=True)
        col5, col6 = st.columns(2)
        with col5:
            st.markdown('<div class="tw-section-label">Target Price</div>', unsafe_allow_html=True)
            target_price = st.number_input(
                "Target Price",
                min_value=50,
                max_value=10000,
                value=300,
                step=10,
                label_visibility="collapsed",
            )
        with col6:
            st.markdown('<div class="tw-section-label">Currency</div>', unsafe_allow_html=True)
            currency = st.selectbox(
                "Currency",
                options=CURRENCIES,
                index=0,
                label_visibility="collapsed",
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="tw-section-label">Notifications</div>', unsafe_allow_html=True)
        col7, col8 = st.columns(2)
        with col7:
            email_notif = st.toggle("Email Notifications", value=st.session_state.email_notif)
        with col8:
            whatsapp_notif = st.toggle("WhatsApp Notifications", value=False)

        st.markdown("<br>", unsafe_allow_html=True)

        col_cancel, col_submit = st.columns([3, 1])
        with col_cancel:
            if st.button("Cancel", use_container_width=True):
                st.session_state.page = "Dashboard"
                st.rerun()
        with col_submit:
            if st.button("🚀  Start Watching", type="primary", use_container_width=True):
                if origin == dest:
                    st.error("Origin and destination cannot be the same.")
                elif dep_date >= arr_date:
                    st.error("Arrival date must be after departure date.")
                else:
                    import numpy as np
                    new_id = max(w["id"] for w in st.session_state.watches) + 1 if st.session_state.watches else 1
                    np.random.seed(new_id)
                    current_price = int(target_price * np.random.uniform(0.85, 1.2))
                    rec = "BUY" if current_price <= target_price * 1.05 else "WAIT"
                    st.session_state.watches.append({
                        "id": new_id,
                        "origin": origin,
                        "dest": dest,
                        "dep_date": str(dep_date),
                        "arr_date": str(arr_date),
                        "target": target_price,
                        "currency": currency,
                        "current_price": current_price,
                        "recommendation": rec,
                        "confidence": round(np.random.uniform(0.65, 0.92), 2),
                    })
                    st.success(f"✅ Now watching {origin} → {dest}!")
                    st.session_state.page = "Dashboard"
                    st.rerun()
