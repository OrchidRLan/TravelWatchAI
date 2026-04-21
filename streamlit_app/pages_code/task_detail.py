import streamlit as st
import plotly.graph_objects as go
import numpy as np


def render():
    watches = st.session_state.watches
    watch_id = st.session_state.selected_watch_id
    w = next((x for x in watches if x["id"] == watch_id), watches[0])

    # ── Header ────────────────────────────────────────────────────────────────
    col_back, col_title, col_del, col_edit, col_book = st.columns([0.3, 3, 1, 1, 1])
    with col_back:
        if st.button("←"):
            st.session_state.page = "Dashboard"
            st.rerun()
    with col_title:
        st.markdown(f'<h2 style="font-size:22px;font-weight:700;color:#111;margin:0;">Route Details ({w["origin"]} - {w["dest"]})</h2>', unsafe_allow_html=True)
    with col_del:
        if st.button("Delete Watch", use_container_width=True):
            st.session_state.watches = [x for x in watches if x["id"] != watch_id]
            st.session_state.page = "Dashboard"
            st.rerun()
    with col_edit:
        st.button("Edit Watch", use_container_width=True)
    with col_book:
        st.button("Book Now", type="primary", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Route Info ────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Route Info</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="tw-card-sm" style="margin-bottom:16px;">
        <span style="font-weight:600; color:#111;">{w['origin']} - {w['dest']}</span>
        <span style="color:#9ca3af; font-size:13px;"> (Depart {w['dep_date']} - Arrive {w['arr_date']})</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Current / Target Price ────────────────────────────────────────────────
    col_cur, col_tgt = st.columns(2)
    with col_cur:
        st.markdown('<div class="sec-label">Current Price</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="tw-card-sm" style="margin-bottom:16px;">
            <span style="font-size:18px; font-weight:700; color:#111;">${w['current_price']}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_tgt:
        st.markdown('<div class="sec-label">Target Price</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="tw-card-sm" style="margin-bottom:16px;">
            <span style="font-size:18px; font-weight:700; color:#111;">${w['target']}</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Recommendation ────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Recommendation</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="tw-card-sm" style="margin-bottom:20px;">
        <span style="font-weight:600; color:#111;">{w['recommendation'].capitalize()}</span>
        <span style="color:#9ca3af; font-size:13px;"> ({w['confidence']}% Confidence)</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Price Trend Chart ─────────────────────────────────────────────────────
    col_ct, col_dd = st.columns([4, 1])
    with col_ct:
        st.markdown('<div style="font-size:18px; font-weight:700; color:#111; margin-bottom:8px;">Price Trend Chart</div>', unsafe_allow_html=True)
    with col_dd:
        st.selectbox("Range", ["Last 30 days", "Last 7 days", "Last 90 days"],
                     label_visibility="collapsed")

    np.random.seed(w["id"] * 7)
    dates = [f"10/{d}" for d in [1,4,7,10,13,16,19,22,25,27,31,"11/3"]]
    prices = w["current_price"] + np.cumsum(np.random.randn(12) * 80)
    prices = np.clip(prices, 150, 1100)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=prices, mode="lines+markers",
        line=dict(color="#3b82f6", width=2),
        marker=dict(size=5, color="#3b82f6"),
        fill="tozeroy", fillcolor="rgba(59,130,246,0.08)",
        hovertemplate="%{x}<br>$%{y:.0f}<extra></extra>",
    ))
    fig.update_layout(
        height=320, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(gridcolor="#f5f5f5", tickfont=dict(size=10, color="#9ca3af")),
        yaxis=dict(gridcolor="#f5f5f5", tickprefix="$", tickfont=dict(size=10, color="#9ca3af"),
                   range=[0, max(prices) * 1.15]),
        font=dict(family="Inter"),
        showlegend=False,
    )

    st.markdown('<div class="tw-card" style="padding:20px;">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Switch route ──────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Switch Route</div>', unsafe_allow_html=True)
    options = {f"{x['origin']} - {x['dest']}": x["id"] for x in watches}
    selected = st.selectbox("Route", list(options.keys()),
                            index=list(options.values()).index(watch_id),
                            label_visibility="collapsed")
    if options[selected] != watch_id:
        st.session_state.selected_watch_id = options[selected]
        st.rerun()
