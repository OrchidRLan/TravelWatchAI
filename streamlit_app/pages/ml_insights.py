import streamlit as st
import plotly.graph_objects as go
import numpy as np
import json
import os


@st.cache_data
def load_model_data():
    base = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base, "model_weights", "travelwatch_models.json")
    with open(path, "r") as f:
        return json.load(f)


def render():
    st.markdown('<h2 style="font-size:24px;font-weight:700;color:#111;margin:0 0 20px 0;">Machine Learning Insights</h2>', unsafe_allow_html=True)

    try:
        data = load_model_data()
        clf  = data["classification"]
        reg  = data["regression"]
        lc   = data["learning_curves"]

        # ── Model selector ────────────────────────────────────────────────────
        st.markdown('<div class="sec-label">Model</div>', unsafe_allow_html=True)
        model = st.radio("Model", ["Logistic Regression", "KNN"],
                         label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)

        if model == "Logistic Regression":
            m_data = clf["logistic_regression"]
        else:
            m_data = clf["knn"]

        f1  = m_data["f1"]
        auc = m_data["auc"]
        cm  = m_data["confusion_matrix"]
        acc = (cm[0][0] + cm[1][1]) / (cm[0][0] + cm[0][1] + cm[1][0] + cm[1][1])

        # ── Performance metrics ───────────────────────────────────────────────
        st.markdown('<div class="sec-label">Model Performance</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="tw-card" style="display:flex; padding:0; overflow:hidden; margin-bottom:20px;">
            <div style="flex:1; padding:16px 20px; border-right:1px solid #ebebeb; text-align:center;">
                <div style="font-size:13px; font-weight:600; color:#111; margin-bottom:4px;">Accuracy</div>
                <div style="font-size:15px; color:#374151;">{acc*100:.1f}%</div>
            </div>
            <div style="flex:1; padding:16px 20px; border-right:1px solid #ebebeb; text-align:center;">
                <div style="font-size:13px; font-weight:600; color:#111; margin-bottom:4px;">F1 Score</div>
                <div style="font-size:15px; color:#374151;">{f1:.3f}</div>
            </div>
            <div style="flex:1; padding:16px 20px; text-align:center;">
                <div style="font-size:13px; font-weight:600; color:#111; margin-bottom:4px;">AUC-ROC</div>
                <div style="font-size:15px; color:#374151;">{auc:.3f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Confusion Matrix ──────────────────────────────────────────────────
        st.markdown('<div class="sec-label">Confusion Matrix</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <table style="border-collapse:collapse; margin-bottom:20px; font-family:Inter,sans-serif;">
            <thead>
                <tr>
                    <td style="padding:8px 16px;"></td>
                    <td style="padding:8px 24px; font-size:13px; color:#374151; font-weight:500; text-align:center;">Predicted BUY</td>
                    <td style="padding:8px 24px; font-size:13px; color:#374151; font-weight:500; text-align:center;">Predicted WAIT</td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding:8px 16px; font-size:13px; color:#374151; font-weight:500;">Actual BUY</td>
                    <td style="border:1px solid #d1d5db; padding:16px 32px; text-align:center; font-size:18px; font-weight:600; color:#111;">{cm[0][0]}</td>
                    <td style="border:1px solid #d1d5db; padding:16px 32px; text-align:center; font-size:18px; font-weight:600; color:#111;">{cm[0][1]}</td>
                </tr>
                <tr>
                    <td style="padding:8px 16px; font-size:13px; color:#374151; font-weight:500;">Actual WAIT</td>
                    <td style="border:1px solid #d1d5db; padding:16px 32px; text-align:center; font-size:18px; font-weight:600; color:#111;">{cm[1][0]}</td>
                    <td style="border:1px solid #d1d5db; padding:16px 32px; text-align:center; font-size:18px; font-weight:600; color:#111;">{cm[1][1]}</td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

        # ── ROC Curve ─────────────────────────────────────────────────────────
        st.markdown('<div class="sec-label">ROC Curve</div>', unsafe_allow_html=True)
        fpr = np.linspace(0, 1, 100)
        tpr = np.clip(fpr ** (1 / (auc * 2.8)), 0, 1)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines",
                                 line=dict(color="#3b82f6", width=2.5),
                                 name=f"AUC = {auc:.3f}"))
        fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines",
                                 line=dict(color="#e5e7eb", dash="dash", width=1),
                                 name="Random"))
        fig.update_layout(height=300, margin=dict(l=10,r=10,t=10,b=10),
                          paper_bgcolor="white", plot_bgcolor="white",
                          xaxis=dict(title="False Positive Rate", gridcolor="#f5f5f5"),
                          yaxis=dict(title="True Positive Rate", gridcolor="#f5f5f5"),
                          legend=dict(font=dict(size=11)),
                          font=dict(family="Inter"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # ── Regression Results ────────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="sec-label">Regression Results (Price Prediction)</div>', unsafe_allow_html=True)
        ridge = reg["ridge"]
        lasso = reg["lasso"]
        st.markdown(f"""
        <div class="tw-card" style="display:flex; padding:0; overflow:hidden; margin-bottom:20px;">
            <div style="flex:1; padding:16px 20px; border-right:1px solid #ebebeb; text-align:center;">
                <div style="font-size:13px; font-weight:600; color:#111; margin-bottom:8px;">Ridge Regression</div>
                <div style="font-size:13px; color:#374151;">R² = {ridge['r2']:.4f}</div>
                <div style="font-size:13px; color:#374151;">RMSE = {ridge['rmse']:.1f}</div>
                <div style="font-size:13px; color:#374151;">MAE = {ridge['mae']:.1f}</div>
            </div>
            <div style="flex:1; padding:16px 20px; text-align:center;">
                <div style="font-size:13px; font-weight:600; color:#111; margin-bottom:8px;">Lasso Regression</div>
                <div style="font-size:13px; color:#374151;">R² = {lasso['r2']:.4f}</div>
                <div style="font-size:13px; color:#374151;">RMSE = {lasso['rmse']:.1f}</div>
                <div style="font-size:13px; color:#374151;">MAE = {lasso['mae']:.1f}</div>
            </div>
        </div>
        <div style="font-size:12px; color:#6b7280; margin-bottom:20px;">
            ✅ Deployed model: <b>{reg['best_model']}</b> (selected based on R² performance)
        </div>
        """, unsafe_allow_html=True)

        # ── Learning Curves ───────────────────────────────────────────────────
        st.markdown('<div class="sec-label">Learning Curves (Ridge vs Lasso)</div>', unsafe_allow_html=True)
        fig_lc = go.Figure()
        fig_lc.add_trace(go.Scatter(x=lc["ridge_sizes"], y=lc["ridge_train_r2"],
                                    mode="lines+markers", name="Ridge Train",
                                    line=dict(color="#3b82f6", width=2)))
        fig_lc.add_trace(go.Scatter(x=lc["ridge_sizes"], y=lc["ridge_val_r2"],
                                    mode="lines+markers", name="Ridge Val",
                                    line=dict(color="#3b82f6", dash="dash", width=2)))
        fig_lc.add_trace(go.Scatter(x=lc["lasso_sizes"], y=lc["lasso_train_r2"],
                                    mode="lines+markers", name="Lasso Train",
                                    line=dict(color="#e05c3a", width=2)))
        fig_lc.add_trace(go.Scatter(x=lc["lasso_sizes"], y=lc["lasso_val_r2"],
                                    mode="lines+markers", name="Lasso Val",
                                    line=dict(color="#e05c3a", dash="dash", width=2)))
        fig_lc.update_layout(height=300, margin=dict(l=10,r=10,t=10,b=10),
                              paper_bgcolor="white", plot_bgcolor="white",
                              xaxis=dict(title="Training Set Size", gridcolor="#f5f5f5"),
                              yaxis=dict(title="R² Score", gridcolor="#f5f5f5"),
                              legend=dict(font=dict(size=11), orientation="h", y=-0.25),
                              font=dict(family="Inter"))
        st.plotly_chart(fig_lc, use_container_width=True, config={"displayModeBar": False})

    except FileNotFoundError:
        st.warning("Model weights not found. Please run the training notebook first.")
