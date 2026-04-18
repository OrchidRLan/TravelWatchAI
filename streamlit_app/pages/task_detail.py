import streamlit as st
import plotly.graph_objects as go
import numpy as np


def render():
    watches = st.session_state.watches
    watch_id = st.session_state.selected_watch_id
    w = next((x for x in watches if x["id"] == watch_id), watches[0] if watches else None)

    if not w:
        st.warning("No watch selected.")
        return

    # ── Header ────────────────────────────────────────────────────────────────
    col_title, col_del, col_edit, col_book = st.columns([3, 1, 1, 1])
    with col_title:
        st.markdown(
            f'<div class="tw-page-title">{w["origin"]} → {w["dest"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="color:#888; font-size:13px; font-family: DM Mono, monospace;">'
            f'Dep: {w["dep_date"]}  ·  Ret: {w["arr_date"]}</div>',
            unsafe_allow_html=True,
        )
    with col_del:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑 Delete", use_container_width=True):
            st.session_state.watches = [x for x in watches if x["id"] != watch_id]
            st.session_state.page = "Dashboard"
            st.rerun()
    with col_edit:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("✏️ Edit", use_container_width=True)
    with col_book:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("📗 Book Now", type="primary", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Route Info ────────────────────────────────────────────────────────────
    st.markdown('<div class="tw-section-label">Route Info</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="tw-card" style="margin-bottom:16px;">
            <div style="display:flex; gap:32px; flex-wrap:wrap;">
                <div><span style="color:#888;font-size:11px;">FROM</span><br>
                    <span style="font-size:20px;font-weight:700;font-family:DM Mono,monospace;">{w['origin']}</span>
                </div>
                <div style="align-self:center;font-size:20px;color:#bbb;">→</div>
                <div><span style="color:#888;font-size:11px;">TO</span><br>
                    <span style="font-size:20px;font-weight:700;font-family:DM Mono,monospace;">{w['dest']}</span>
                </div>
                <div><span style="color:#888;font-size:11px;">DEPARTURE</span><br>
                    <span style="font-size:15px;font-weight:600;">{w['dep_date']}</span>
                </div>
                <div><span style="color:#888;font-size:11px;">RETURN</span><br>
                    <span style="font-size:15px;font-weight:600;">{w['arr_date']}</span>
                </div>
                <div><span style="color:#888;font-size:11px;">CURRENCY</span><br>
                    <span style="font-size:15px;font-weight:600;">{w['currency']}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Price Cards ───────────────────────────────────────────────────────────
    col_cur, col_tgt = st.columns(2)
    diff = w["current_price"] - w["target"]
    diff_color = "#e05c3a" if diff > 0 else "#1a9e6e"
    diff_label = f"${abs(diff)} above target" if diff > 0 else f"${abs(diff)} below target 🎉"

    with col_cur:
        st.markdown(
            f"""
            <div class="tw-card">
                <div style="font-size:11px;color:#888;margin-bottom:6px;">CURRENT PRICE</div>
                <div style="font-size:36px;font-weight:700;color:#0a0a0f;">${w['current_price']}</div>
                <div style="font-size:12px;color:{diff_color};margin-top:4px;">{diff_label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_tgt:
        st.markdown(
            f"""
            <div class="tw-card">
                <div style="font-size:11px;color:#888;margin-bottom:6px;">TARGET PRICE</div>
                <div style="font-size:36px;font-weight:700;color:#0a0a0f;">${w['target']}</div>
                <div style="font-size:12px;color:#aaa;margin-top:4px;">Alert when price ≤ target</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Recommendation ────────────────────────────────────────────────────────
    st.markdown('<div class="tw-section-label">ML Recommendation</div>', unsafe_allow_html=True)
    badge = (
        '<span class="tw-badge-buy" style="font-size:16px;padding:8px 22px;">✅ BUY NOW</span>'
        if w["recommendation"] == "BUY"
        else '<span class="tw-badge-wait" style="font-size:16px;padding:8px 22px;">⏳ WAIT</span>'
    )
    rec_text = (
        "Price is at or below your target. Our model recommends purchasing now."
        if w["recommendation"] == "BUY"
        else "Price is above your target. Our model predicts prices may drop. Hold off."
    )
    st.markdown(
        f"""
        <div class="tw-card" style="margin-bottom:16px; display:flex; align-items:center; gap:24px;">
            {badge}
            <div>
                <div style="font-weight:600; color:#0a0a0f;">{rec_text}</div>
                <div style="font-size:12px; color:#aaa; margin-top:4px;">
                    Confidence: {int(w['confidence']*100)}% · Logistic Regression model
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Price Trend Chart ─────────────────────────────────────────────────────
    st.markdown('<div class="tw-section-label">Price History (30 Days)</div>', unsafe_allow_html=True)
    np.random.seed(w["id"] * 7)
    days = list(range(30, 0, -1))
    prices = w["current_price"] + np.cumsum(np.random.randn(30) * 10)
    prices = np.clip(prices, 100, 800)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days, y=prices, mode="lines+markers",
        line=dict(color="#4f8ef7", width=2.5),
        marker=dict(size=4),
        name="Price",
        hovertemplate="Day -%{x}<br>$%{y:.0f}<extra></extra>",
    ))
    fig.add_hline(
        y=w["target"], line_dash="dash", line_color="#1a9e6e",
        annotation_text=f"Target ${w['target']}", annotation_position="right",
    )
    fig.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(title="Days Until Departure", gridcolor="#f0f0f5", autorange="reversed"),
        yaxis=dict(title=f"Price ({w['currency']})", gridcolor="#f0f0f5"),
        font=dict(family="DM Sans"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Watch selector ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="tw-section-label">Switch Route</div>', unsafe_allow_html=True)
    options = {f"{x['origin']} → {x['dest']}": x["id"] for x in watches}
    selected_label = st.selectbox(
        "Select route", list(options.keys()),
        index=list(options.values()).index(watch_id),
        label_visibility="collapsed",
    )
    if options[selected_label] != watch_id:
        st.session_state.selected_watch_id = options[selected_label]
        st.rerun()
