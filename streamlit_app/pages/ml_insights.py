import streamlit as st
import plotly.graph_objects as go
import numpy as np


def _mock_metrics(model: str):
    """Return deterministic mock metrics for demo."""
    if model == "Logistic Regression":
        return dict(accuracy=0.81, f1=0.78, auc=0.84,
                    cm=[[312, 48], [61, 279]])
    else:  # KNN
        return dict(accuracy=0.77, f1=0.74, auc=0.80,
                    cm=[[298, 62], [74, 266]])


def render():
    st.markdown('<div class="tw-page-title">Machine Learning Insights</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#888; font-size:14px; margin-bottom:20px;">Explore offline model evaluation results</div>',
        unsafe_allow_html=True,
    )

    # ── Model selector ────────────────────────────────────────────────────────
    st.markdown('<div class="tw-section-label">Model</div>', unsafe_allow_html=True)
    model = st.radio(
        "Select model",
        options=["Logistic Regression", "KNN"],
        horizontal=True,
        label_visibility="collapsed",
    )

    metrics = _mock_metrics(model)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Performance metrics ───────────────────────────────────────────────────
    st.markdown('<div class="tw-section-label">Model Performance</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""<div class="tw-card" style="text-align:center;">
                <div style="font-size:11px;color:#888;">ACCURACY</div>
                <div style="font-size:32px;font-weight:700;color:#4f8ef7;">{metrics['accuracy']*100:.1f}%</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class="tw-card" style="text-align:center;">
                <div style="font-size:11px;color:#888;">F1 SCORE</div>
                <div style="font-size:32px;font-weight:700;color:#4f8ef7;">{metrics['f1']:.3f}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""<div class="tw-card" style="text-align:center;">
                <div style="font-size:11px;color:#888;">AUC-ROC</div>
                <div style="font-size:32px;font-weight:700;color:#4f8ef7;">{metrics['auc']:.3f}</div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_cm, col_roc = st.columns(2)

    # ── Confusion Matrix ──────────────────────────────────────────────────────
    with col_cm:
        st.markdown('<div class="tw-section-label">Confusion Matrix</div>', unsafe_allow_html=True)
        cm = metrics["cm"]
        labels = ["Predicted Buy", "Predicted Wait"]
        fig_cm = go.Figure(go.Heatmap(
            z=cm,
            x=labels, y=["Actual Buy", "Actual Wait"],
            colorscale=[[0, "#f0f4ff"], [1, "#4f8ef7"]],
            text=[[str(v) for v in row] for row in cm],
            texttemplate="%{text}",
            textfont=dict(size=20, color="white"),
            showscale=False,
        ))
        fig_cm.update_layout(
            height=260, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(side="top", tickfont=dict(size=11)),
            yaxis=dict(tickfont=dict(size=11)),
            font=dict(family="DM Sans"),
        )
        st.plotly_chart(fig_cm, use_container_width=True)

    # ── ROC Curve ─────────────────────────────────────────────────────────────
    with col_roc:
        st.markdown('<div class="tw-section-label">ROC Curve</div>', unsafe_allow_html=True)
        np.random.seed(42 if model == "Logistic Regression" else 7)
        fpr = np.linspace(0, 1, 100)
        auc_val = metrics["auc"]
        tpr = np.clip(fpr ** (1 / (auc_val * 3)), 0, 1)

        fig_roc = go.Figure()
        fig_roc.add_trace(go.Scatter(
            x=fpr, y=tpr, mode="lines",
            line=dict(color="#4f8ef7", width=2.5),
            name=f"AUC = {auc_val:.3f}",
        ))
        fig_roc.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1], mode="lines",
            line=dict(color="#ddd", dash="dash", width=1),
            name="Random",
        ))
        fig_roc.update_layout(
            height=260, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(title="FPR", gridcolor="#f0f0f5"),
            yaxis=dict(title="TPR", gridcolor="#f0f0f5"),
            legend=dict(font=dict(size=11)),
            font=dict(family="DM Sans"),
        )
        st.plotly_chart(fig_roc, use_container_width=True)

    # ── Learning Curves (Regression) ──────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="tw-section-label">Regression Learning Curves (Ridge vs Lasso)</div>', unsafe_allow_html=True)
    sizes = [1000, 5000, 10000, 50000, 100000, 200000, 300000]
    np.random.seed(1)
    ridge_train = [0.91 - 0.01 * i + np.random.randn() * 0.005 for i in range(7)]
    ridge_val = [0.75 + 0.02 * i + np.random.randn() * 0.005 for i in range(7)]
    lasso_train = [0.89 - 0.01 * i + np.random.randn() * 0.005 for i in range(7)]
    lasso_val = [0.73 + 0.018 * i + np.random.randn() * 0.005 for i in range(7)]

    fig_lc = go.Figure()
    fig_lc.add_trace(go.Scatter(x=sizes, y=ridge_train, mode="lines+markers",
                                name="Ridge Train", line=dict(color="#4f8ef7", width=2)))
    fig_lc.add_trace(go.Scatter(x=sizes, y=ridge_val, mode="lines+markers",
                                name="Ridge Val", line=dict(color="#4f8ef7", dash="dash", width=2)))
    fig_lc.add_trace(go.Scatter(x=sizes, y=lasso_train, mode="lines+markers",
                                name="Lasso Train", line=dict(color="#e05c3a", width=2)))
    fig_lc.add_trace(go.Scatter(x=sizes, y=lasso_val, mode="lines+markers",
                                name="Lasso Val", line=dict(color="#e05c3a", dash="dash", width=2)))
    fig_lc.update_layout(
        height=300, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(title="Training Set Size", gridcolor="#f0f0f5", type="log"),
        yaxis=dict(title="R² Score", gridcolor="#f0f0f5", range=[0.6, 1.0]),
        legend=dict(font=dict(size=11), orientation="h", y=-0.2),
        font=dict(family="DM Sans"),
    )
    st.plotly_chart(fig_lc, use_container_width=True)
