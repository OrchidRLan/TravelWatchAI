import streamlit as st
import plotly.graph_objects as go
import numpy as np


def mini_chart(watch, color_up="#ef4444", color_down="#22c55e"):
    np.random.seed(watch["id"] * 3)
    x = ["10/1","10/9","10/18","10/27"]
    prices = watch["current_price"] + np.cumsum(np.random.randn(4) * 30)
    prices = np.clip(prices, 100, 1200)
    is_down = watch["change_dir"] == "down"
    line_color = color_down if is_down else color_up
    fill_color = "rgba(34,197,94,0.15)" if is_down else "rgba(239,68,68,0.12)"

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=prices, mode="lines",
        line=dict(color=line_color, width=1.5, dash="dot" if not is_down else "solid"),
        fill="tozeroy", fillcolor=fill_color,
    ))
    fig.update_layout(
        height=90, margin=dict(l=0, r=0, t=0, b=20),
        paper_bgcolor="white", plot_bgcolor="white",
        showlegend=False,
        xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#9ca3af"), tickvals=x),
        yaxis=dict(showgrid=False, visible=False),
    )
    return fig


def render():
    watches = st.session_state.watches

    # ── Header ────────────────────────────────────────────────────────────────
    col_title, col_btn = st.columns([5, 1])
    with col_title:
        st.markdown('<h2 style="font-size:24px;font-weight:700;color:#111;margin:0;">Dashboard</h2>', unsafe_allow_html=True)
    with col_btn:
        if st.button("＋  Add New Watch", type="primary", use_container_width=True):
            st.session_state.page = "Add New Watch"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Route Cards ───────────────────────────────────────────────────────────
    see_all_col = st.columns([6, 1])
    with see_all_col[1]:
        st.markdown('<div style="text-align:right; color:#9ca3af; font-size:13px; padding-top:4px;">See All</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for i, w in enumerate(watches[:3]):
        badge = f'<span class="badge-{"buy" if w["recommendation"]=="BUY" else "wait"}">{w["recommendation"]} ({w["confidence"]}%)</span>'
        arrow = "↑" if w["change_dir"] == "up" else "↓"
        change_color = "#ef4444" if w["change_dir"] == "up" else "#22c55e"
        change_text = f"{arrow} {w['change_pct']}% {'Up' if w['change_dir']=='up' else 'Down'} from past week"

        with cols[i]:
            st.markdown(f"""
            <div class="tw-card" style="padding:20px;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
                    <div style="font-size:17px; font-weight:700; color:#111;">{w['origin']} - {w['dest']}</div>
                    {badge}
                </div>
                <div style="font-size:12px; color:{change_color}; margin-bottom:12px; font-weight:500;">
                    {change_text}
                </div>
                <div style="display:flex; gap:24px; margin-bottom:4px;">
                    <div>
                        <span style="font-size:12px; color:#9ca3af;">Current</span>
                        <span style="font-size:15px; font-weight:700; color:#111; margin-left:8px;">${w['current_price']}</span>
                    </div>
                </div>
                <div style="display:flex; gap:24px; margin-bottom:8px;">
                    <div>
                        <span style="font-size:12px; color:#9ca3af;">Target</span>
                        <span style="font-size:15px; font-weight:700; color:#111; margin-left:8px;">${w['target']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(mini_chart(w), use_container_width=True, config={"displayModeBar": False})
            if st.button("View Detail", key=f"view_{w['id']}", use_container_width=True):
                st.session_state.selected_watch_id = w["id"]
                st.session_state.page = "Task Detail"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Summary + Price Trends ────────────────────────────────────────────────
    col_sum, col_chart = st.columns([1, 2])

    with col_sum:
        dropping = sum(1 for w in watches if w["change_dir"] == "up")
        buy_count = sum(1 for w in watches if w["recommendation"] == "BUY")

        for label, val, icon_bg, icon in [
            ("Currently Tracking", f"{len(watches)} Routes", "#d1fae5", "📈"),
            ("Routes Dropping", f"{dropping} Route{'s' if dropping != 1 else ''}", "#fee2e2", "🕐"),
            ("Buy Recommendations", f"{buy_count} Route{'s' if buy_count != 1 else ''}", "#fef9c3", "📦"),
        ]:
            st.markdown(f"""
            <div class="tw-card" style="display:flex; justify-content:space-between;
                 align-items:center; margin-bottom:12px; padding:16px 20px;">
                <div>
                    <div style="font-size:12px; color:#9ca3af; margin-bottom:4px;">{label}</div>
                    <div style="font-size:20px; font-weight:700; color:#111;">{val}</div>
                </div>
                <div style="width:44px; height:44px; background:{icon_bg}; border-radius:50%;
                     display:flex; align-items:center; justify-content:center; font-size:20px;">
                    {icon}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_chart:
        # Month selector
        col_ct, col_dd = st.columns([3, 1])
        with col_ct:
            st.markdown('<div style="font-size:18px; font-weight:700; color:#111; padding-top:4px;">Price Trends Chart</div>', unsafe_allow_html=True)
        with col_dd:
            month = st.selectbox("Month", ["October", "November", "December"], label_visibility="collapsed")

        fig = go.Figure()
        colors = [
            ("rgba(239,68,68,0.7)", "rgba(239,68,68,0.15)"),
            ("rgba(167,139,250,0.7)", "rgba(167,139,250,0.15)"),
            ("rgba(59,130,246,0.7)", "rgba(59,130,246,0.15)"),
        ]
        days = [f"10/{d}" for d in [1,4,7,10,13,16,19,22,25,27]]
        for w, (line_c, fill_c) in zip(watches, colors):
            np.random.seed(w["id"] * 11)
            prices = w["current_price"] + np.cumsum(np.random.randn(10) * 80)
            prices = np.clip(prices, 150, 1000)
            fig.add_trace(go.Scatter(
                x=days, y=prices, mode="lines",
                name=f"{w['origin']} - {w['dest']}",
                line=dict(color=line_c, width=2),
                fill="tozeroy", fillcolor=fill_c,
                hovertemplate="%{x}<br>$%{y:.0f}<extra></extra>",
            ))
        fig.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white", plot_bgcolor="white",
            legend=dict(orientation="h", y=-0.25, font=dict(size=11)),
            xaxis=dict(gridcolor="#f5f5f5", tickfont=dict(size=10)),
            yaxis=dict(gridcolor="#f5f5f5", tickprefix="$", tickfont=dict(size=10)),
            font=dict(family="Inter"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
