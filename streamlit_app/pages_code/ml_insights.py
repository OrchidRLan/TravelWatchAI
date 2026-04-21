import streamlit as st
import plotly.graph_objects as go
import numpy as np


def _metrics(model):
    if model == "Logistic Regression":
        return dict(accuracy=82, f1=0.76, auc=0.81, cm=[[50, 10], [5, 35]])
    else:
        return dict(accuracy=77, f1=0.72, auc=0.78, cm=[[44, 16], [9, 31]])


def render():
    st.markdown('<h2 style="font-size:24px;font-weight:700;color:#111;margin:0 0 20px 0;">Machine Learning Insights</h2>', unsafe_allow_html=True)

    # ── Model selector ────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Model</div>', unsafe_allow_html=True)
    model = st.radio("Model", ["Logistic Regression", "KNN"],
                     label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    m = _metrics(model)

    # ── Model Performance row ─────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Model Performance</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="tw-card" style="display:flex; padding:0; overflow:hidden; margin-bottom:20px;">
        <div style="flex:1; padding:16px 20px; border-right:1px solid #ebebeb; text-align:center;">
            <div style="font-size:13px; font-weight:600; color:#111; margin-bottom:4px;">Accuracy</div>
            <div style="font-size:15px; color:#374151;">{m['accuracy']}%</div>
        </div>
        <div style="flex:1; padding:16px 20px; border-right:1px solid #ebebeb; text-align:center;">
            <div style="font-size:13px; font-weight:600; color:#111; margin-bottom:4px;">F1 Score</div>
            <div style="font-size:15px; color:#374151;">{m['f1']:.2f}</div>
        </div>
        <div style="flex:1; padding:16px 20px; text-align:center;">
            <div style="font-size:13px; font-weight:600; color:#111; margin-bottom:4px;">AUC-ROC</div>
            <div style="font-size:15px; color:#374151;">{m['auc']:.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Confusion Matrix ──────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Confusion Matrix</div>', unsafe_allow_html=True)
    cm = m["cm"]

    # Simple HTML table styled like the figma
    st.markdown(f"""
    <table style="border-collapse: collapse; margin-bottom: 20px; font-family: Inter, sans-serif;">
        <thead>
            <tr>
                <td style="padding:8px 16px;"></td>
                <td style="padding:8px 24px; font-size:13px; color:#374151; font-weight:500; text-align:center;">Predicted</td>
                <td style="padding:8px 24px; font-size:13px; color:#374151; font-weight:500; text-align:center;">Not Predicted</td>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="padding:8px 16px; font-size:13px; color:#374151; font-weight:500;">Actual</td>
                <td style="border:1px solid #d1d5db; padding:16px 32px; text-align:center;
                    font-size:18px; font-weight:600; color:#111;">{cm[0][0]}</td>
                <td style="border:1px solid #d1d5db; padding:16px 32px; text-align:center;
                    font-size:18px; font-weight:600; color:#111;">{cm[0][1]}</td>
            </tr>
            <tr>
                <td style="padding:8px 16px; font-size:13px; color:#374151; font-weight:500;">Not</td>
                <td style="border:1px solid #d1d5db; padding:16px 32px; text-align:center;
                    font-size:18px; font-weight:600; color:#111;">{cm[1][0]}</td>
                <td style="border:1px solid #d1d5db; padding:16px 32px; text-align:center;
                    font-size:18px; font-weight:600; color:#111;">{cm[1][1]}</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # ── ROC Curve ─────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">ROC Curve</div>', unsafe_allow_html=True)
    fpr = np.linspace(0, 1, 100)
    tpr = np.clip(fpr ** (1 / (m["auc"] * 2.8)), 0, 1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr, mode="lines",
        line=dict(color="#3b82f6", width=2.5),
        name=f"AUC = {m['auc']:.2f}",
    ))
    fig.add_trace(go.Scatter(
        x=[0,1], y=[0,1], mode="lines",
        line=dict(color="#e5e7eb", dash="dash", width=1),
        name="Random",
    ))
    fig.update_layout(
        height=300, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(title="False Positive Rate", gridcolor="#f5f5f5", tickfont=dict(size=10)),
        yaxis=dict(title="True Positive Rate", gridcolor="#f5f5f5", tickfont=dict(size=10)),
        legend=dict(font=dict(size=11)),
        font=dict(family="Inter"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
