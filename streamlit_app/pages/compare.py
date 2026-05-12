import streamlit as st
import plotly.graph_objects as go
import numpy as np


def render():
    watches = st.session_state.watches

    st.markdown('<h2 style="font-size:24px;font-weight:700;color:#111;margin:0 0 20px 0;">Compare Routes</h2>', unsafe_allow_html=True)

    if len(watches) < 2:
        st.info("Add at least 2 routes to compare.")
        if st.button("➕ Add New Watch"):
            st.session_state.page = "Add New Watch"
            st.rerun()
        return

    display = watches[:3]
    n = len(display)

    # ── Route dropdown selectors ──────────────────────────────────────────────
    all_labels = [f"{w['origin']} - {w['dest']}" for w in watches]
    cols = st.columns(n)
    selected_watches = []
    for i in range(n):
        with cols[i]:
            default = display[i]
            idx = next((j for j, w in enumerate(watches) if w["id"] == default["id"]), 0)
            chosen = st.selectbox(f"Route {i+1}", all_labels, index=idx,
                                  key=f"compare_sel_{i}", label_visibility="collapsed")
            chosen_w = next(w for w in watches if f"{w['origin']} - {w['dest']}" == chosen)
            selected_watches.append(chosen_w)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Mini charts ───────────────────────────────────────────────────────────
    chart_styles = [
        ("rgba(239,68,68,0.8)", "rgba(239,68,68,0.12)", "dot"),
        ("rgba(34,197,94,0.9)", "rgba(34,197,94,0.2)", "solid"),
        ("rgba(239,68,68,0.8)", "rgba(239,68,68,0.12)", "dot"),
    ]
    cols = st.columns(n)
    for i, w in enumerate(selected_watches):
        with cols[i]:
            np.random.seed(w["id"] * 13)
            x = ["10/1","10/9","10/18","10/27"]
            prices = w["current_price"] + np.cumsum(np.random.randn(4) * 60)
            prices = np.clip(prices, 100, 1200)
            lc, fc, dash = chart_styles[i % 3]

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x, y=prices, mode="lines",
                line=dict(color=lc, width=2, dash=dash),
                fill="tozeroy", fillcolor=fc,
            ))
            fig.update_layout(
                height=160, margin=dict(l=0, r=0, t=0, b=20),
                paper_bgcolor="white", plot_bgcolor="white",
                showlegend=False,
                xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#9ca3af"), tickvals=x),
                yaxis=dict(showgrid=False, visible=False),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Stats ─────────────────────────────────────────────────────────────────
    cols = st.columns(n)
    for i, w in enumerate(selected_watches):
        with cols[i]:
            st.markdown(f"""
            <div style="margin-bottom:4px;">
                <div class="sec-label">Current Price</div>
                <div style="font-size:22px; font-weight:700; color:#111; margin-bottom:12px;">${w['current_price']}</div>
                <div class="sec-label">Target Price</div>
                <div style="font-size:22px; font-weight:700; color:#111; margin-bottom:12px;">${w['target']}</div>
                <div class="sec-label">Insight</div>
                <div style="font-size:18px; font-weight:700; color:#111;">
                    {'Buy' if w['recommendation']=='BUY' else 'Wait'}
                </div>
            </div>
            """, unsafe_allow_html=True)
