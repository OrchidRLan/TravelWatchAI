import streamlit as st

CURRENCIES = ["USD", "EUR", "GBP", "JPY", "KRW", "CAD", "AUD", "CHF", "CNY", "INR"]


def render():
    st.markdown('<h2 style="font-size:24px;font-weight:700;color:#111;margin:0 0 24px 0;">Settings</h2>', unsafe_allow_html=True)

    # ── Currency ──────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Currency</div>', unsafe_allow_html=True)
    currency = st.selectbox("Currency", CURRENCIES,
                            index=CURRENCIES.index(st.session_state.currency),
                            label_visibility="collapsed")
    st.session_state.currency = currency

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Notifications ─────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Notifications</div>', unsafe_allow_html=True)
    st.markdown('<div class="tw-card" style="margin-bottom:16px;">', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div style="font-size:14px; font-weight:500; color:#111; padding:6px 0;">Price Drop Alerts</div>', unsafe_allow_html=True)
    with col2:
        price_alert = st.selectbox("Price Drop Alerts", ["On", "Off"],
                                   index=0 if st.session_state.price_alert == "On" else 1,
                                   key="pa_sel", label_visibility="collapsed")
    st.session_state.price_alert = price_alert

    col3, col4 = st.columns([3, 1])
    with col3:
        st.markdown('<div style="font-size:14px; font-weight:500; color:#111; padding:6px 0;">Email Notifications</div>', unsafe_allow_html=True)
    with col4:
        email_notif = st.selectbox("Email Notifications", ["On", "Off"],
                                   index=0 if st.session_state.email_notif == "On" else 1,
                                   key="en_sel", label_visibility="collapsed")
    st.session_state.email_notif = email_notif
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Account ───────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Account</div>', unsafe_allow_html=True)
    email = st.text_input("Email", value=st.session_state.user_email,
                          placeholder="your@email.com", label_visibility="collapsed")

    st.markdown("<br><br>", unsafe_allow_html=True)

    col_save, col_logout = st.columns([5, 1])
    with col_save:
        if st.button("Save Settings", type="primary"):
            st.session_state.user_email = email
            st.success("Saved!")
    with col_logout:
        if st.button("Log Out", use_container_width=True):
            st.warning("Logged out.")
