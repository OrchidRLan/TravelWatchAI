import streamlit as st
import plotly.graph_objects as go
import numpy as np


def render():
    watches = st.session_state.watches

    st.markdown('<div class="tw-page-title">Compare Routes</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#888; font-size:14px; margin-bottom:20px;">Side-by-side price comparison across your watched routes</div>',
        unsafe_allow_html=True,
    )

    if len(watches) < 2:
        st.info("Add at least 2 watch routes to compare.")
        if st.button("➕ Add New Watch"):
            st.session_state.page = "Add New Watch"
            st.rerun()
        return

    display = watches[:3]
    n = len(display)
    cols = st.columns(n)
    colors = ["#4f8ef7", "#e05c3a", "#1a9e6e"]

    # ── Route name headers ────────────────────────────────────────────────────
    st.markdown('<div class="tw-section-label">Routes</div>', unsafe_allow_html=True)
    cols = st.columns(n)
    for i, w in enumerate(display):
        with cols[i]:
            st.markdown(
                f"""
                <div class="tw-card" style="border-top: 3px solid {colors[i]};">
                    <div style="font-size:11px;color:#888;">ROUTE {i+1}</div>
                    <div style="font-size:18px;font-weight:700;font-family:DM Mono,monospace;margin-top:4px;">
                        {w['origin']} → {w['dest']}
                    </div>
                    <div style="font-size:11px;color:#aaa;margin-top:2px;">{w['dep_date']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Price charts ──────────────────────────────────────────────────────────
    st.markdown('<div class="tw-section-label">Price Trends</div>', unsafe_allow_html=True)
    cols = st.columns(n)
    for i, w in enumerate(display):
        with cols[i]:
            np.random.seed(w["id"] * 13)
            days = list(range(30, 0, -1))
            prices = w["current_price"] + np.cumsum(np.random.randn(30) * 9)
            prices = np.clip(prices, 80, 700)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=days, y=prices, mode="lines",
                line=dict(color=colors[i], width=2),
                fill="tozeroy", fillcolor=f"rgba{tuple(list(int(colors[i].lstrip('#')[j:j+2], 16) for j in (0,2,4)) + [0.08])}",
                hovertemplate="Day -%{x}<br>$%{y:.0f}<extra></extra>",
            ))
            fig.add_hline(y=w["target"], line_dash="dot", line_color="#999",
                          annotation_text="target")
            fig.update_layout(
                height=180, margin=dict(l=4, r=4, t=4, b=4),
                paper_bgcolor="white", plot_bgcolor="white",
                xaxis=dict(gridcolor="#f5f5f5", showticklabels=False),
                yaxis=dict(gridcolor="#f5f5f5", tickfont=dict(size=10)),
                showlegend=False, font=dict(family="DM Sans"),
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── Stats rows ────────────────────────────────────────────────────────────
    for label, key, prefix in [
        ("Current Price", "current_price", "$"),
        ("Target Price", "target", "$"),
    ]:
        st.markdown(f'<div class="tw-section-label">{label}</div>', unsafe_allow_html=True)
        cols = st.columns(n)
        for i, w in enumerate(display):
            with cols[i]:
                val = w[key]
                is_best = key == "current_price" and val == min(x[key] for x in display)
                color = "#1a9e6e" if is_best else "#0a0a0f"
                st.markdown(
                    f"""
                    <div class="tw-card" style="margin-bottom:8px;">
                        <div style="font-size:22px;font-weight:700;color:{color};">{prefix}{val}</div>
                        {"<div style='font-size:10px;color:#1a9e6e;margin-top:2px;'>✓ Lowest</div>" if is_best else ""}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ── Insight row ───────────────────────────────────────────────────────────
    st.markdown('<div class="tw-section-label">ML Insight</div>', unsafe_allow_html=True)
    cols = st.columns(n)
    for i, w in enumerate(display):
        with cols[i]:
            badge = (
                '<span class="tw-badge-buy">BUY</span>'
                if w["recommendation"] == "BUY"
                else '<span class="tw-badge-wait">WAIT</span>'
            )
            st.markdown(
                f"""
                <div class="tw-card">
                    {badge}
                    <div style="font-size:11px;color:#aaa;margin-top:8px;">
                        {int(w['confidence']*100)}% confidence
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
