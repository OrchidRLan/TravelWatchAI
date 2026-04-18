import streamlit as st

CURRENCIES = ["USD", "EUR", "GBP", "JPY", "KRW", "CAD", "AUD", "CHF", "CNY", "INR",
              "SGD", "HKD", "MXN", "BRL", "SEK", "NOK", "DKK", "NZD", "ZAR", "AED"]


def render():
    st.markdown('<div class="tw-page-title">Settings</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#888; font-size:14px; margin-bottom:24px;">Manage your preferences and account</div>',
        unsafe_allow_html=True,
    )

    # ── Currency ──────────────────────────────────────────────────────────────
    st.markdown("### Currency")
    st.markdown('<div class="tw-section-label">Default Currency</div>', unsafe_allow_html=True)
    currency = st.selectbox(
        "Currency",
        options=CURRENCIES,
        index=CURRENCIES.index(st.session_state.currency),
        label_visibility="collapsed",
    )
    st.session_state.currency = currency

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Notifications ─────────────────────────────────────────────────────────
    st.markdown("### Notifications")
    st.markdown(
        '<div class="tw-card" style="margin-bottom:16px;">',
        unsafe_allow_html=True,
    )
    price_alert = st.toggle("Price Drop Alerts", value=st.session_state.price_alert)
    st.session_state.price_alert = price_alert
    email_notif = st.toggle("Email Notifications", value=st.session_state.email_notif)
    st.session_state.email_notif = email_notif
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Account ───────────────────────────────────────────────────────────────
    st.markdown("### Account")
    st.markdown('<div class="tw-section-label">Email Address</div>', unsafe_allow_html=True)
    email = st.text_input(
        "Email",
        value=st.session_state.user_email,
        placeholder="you@example.com",
        label_visibility="collapsed",
    )

    col_save, col_logout = st.columns([4, 1])
    with col_save:
        if st.button("💾  Save Settings", type="primary", use_container_width=True):
            st.session_state.user_email = email
            st.success("Settings saved!")
    with col_logout:
        if st.button("Logout", use_container_width=True):
            st.warning("Logout clicked — implement auth flow here.")
