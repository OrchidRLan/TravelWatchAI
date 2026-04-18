import streamlit as st
import plotly.graph_objects as go
import numpy as np


def render():
    watches = st.session_state.watches

    # ── Header ───────────────────────────────────────────────────────────────
    col_title, col_btn = st.columns([4, 1])
    with col_title:
        st.markdown('<div class="tw-page-title">Dashboard</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="color:#888; font-size:14px;">You have <b>{len(watches)}</b> active watch routes</div>',
            unsafe_allow_html=True,
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕  Add New Watch", type="primary", use_container_width=True):
            st.session_state.page = "Add New Watch"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Active Watch Route Cards ─────────────────────────────────────────────
    st.markdown('<div class="tw-section-label">Active Watch Routes</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, w in enumerate(watches[:3]):
        badge = (
            '<span class="tw-badge-buy">BUY</span>'
            if w["recommendation"] == "BUY"
            else '<span class="tw-badge-wait">WAIT</span>'
        )
        diff = w["current_price"] - w["target"]
        diff_str = f"+${abs(diff)}" if diff > 0 else f"-${abs(diff)}"
        diff_color = "#e05c3a" if diff > 0 else "#1a9e6e"
        with cols[i]:
            st.markdown(
                f"""
                <div class="tw-card" style="cursor:pointer;">
                    <div style="font-size:13px; color:#888; margin-bottom:6px; font-family: DM Mono, monospace;">
                        {w['origin']} → {w['dest']}
                    </div>
                    <div style="font-size:24px; font-weight:700; color:#0a0a0f; margin-bottom:4px;">
                        ${w['current_price']}
                    </div>
                    <div style="font-size:12px; color:{diff_color}; margin-bottom:10px;">
                        {diff_str} vs target ${w['target']}
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        {badge}
                        <span style="font-size:11px; color:#aaa;">{int(w['confidence']*100)}% conf.</span>
                    </div>
                    <div style="font-size:11px; color:#bbb; margin-top:8px;">
                        {w['dep_date']} · {w['currency']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("View Detail", key=f"view_{w['id']}", use_container_width=True):
                st.session_state.selected_watch_id = w["id"]
                st.session_state.page = "Task Detail"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Summary + Price Trends ────────────────────────────────────────────────
    col_summary, col_chart = st.columns([1, 2])

    with col_summary:
        st.markdown('<div class="tw-section-label">Summary</div>', unsafe_allow_html=True)
        avg_price = int(np.mean([w["current_price"] for w in watches]))
        buy_count = sum(1 for w in watches if w["recommendation"] == "BUY")

        st.markdown(
            f"""
            <div class="tw-card" style="margin-bottom:12px;">
                <div style="font-size:11px; color:#888; margin-bottom:4px;">Routes Tracked</div>
                <div style="font-size:28px; font-weight:700; color:#0a0a0f;">{len(watches)}</div>
            </div>
            <div class="tw-card" style="margin-bottom:12px;">
                <div style="font-size:11px; color:#888; margin-bottom:4px;">Avg. Current Price</div>
                <div style="font-size:28px; font-weight:700; color:#0a0a0f;">${avg_price}</div>
            </div>
            <div class="tw-card">
                <div style="font-size:11px; color:#888; margin-bottom:4px;">Buy Recommendations</div>
                <div style="font-size:28px; font-weight:700; color:#1a9e6e;">{buy_count} / {len(watches)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_chart:
        st.markdown('<div class="tw-section-label">Price Trends (Last 30 Days)</div>', unsafe_allow_html=True)
        days = list(range(30, 0, -1))
        fig = go.Figure()
        colors = ["#4f8ef7", "#e05c3a", "#1a9e6e"]
        for w, color in zip(watches, colors):
            np.random.seed(w["id"])
            prices = w["current_price"] + np.cumsum(np.random.randn(30) * 8)
            prices = np.clip(prices, 100, 600)
            fig.add_trace(go.Scatter(
                x=days, y=prices,
                mode="lines",
                name=f"{w['origin']}→{w['dest']}",
                line=dict(color=color, width=2),
                hovertemplate="Day -%{x}<br>$%{y:.0f}<extra></extra>",
            ))

        fig.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white",
            plot_bgcolor="white",
            legend=dict(font=dict(size=11), orientation="h", y=-0.15),
            xaxis=dict(title="Days Until Departure", gridcolor="#f0f0f5", tickfont=dict(size=11)),
            yaxis=dict(title="Price (USD)", gridcolor="#f0f0f5", tickfont=dict(size=11)),
            font=dict(family="DM Sans"),
        )
        st.plotly_chart(fig, use_container_width=True)
