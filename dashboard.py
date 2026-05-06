from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"


@st.cache_data
def load_scorecard() -> pd.DataFrame:
    path = OUTPUT_DIR / "scorecard_results.csv"
    return pd.read_csv(path)


def format_pct(val: float) -> str:
    return f"{val:.2f}%"


def format_days(val: float) -> str:
    return f"{val:.1f}d"


st.set_page_config(page_title="Supplier Scorecard Dashboard", page_icon="📋", layout="wide")
st.title("📋 Supplier Performance Scorecard")
st.caption("Supplier KPI summary: OTD, lead time, quality, savings, compliance")

df = load_scorecard()
df_sorted = df.sort_values("weighted_score", ascending=False)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Suppliers", f"{len(df)}")
c2.metric("Avg Weighted Score", f"{df['weighted_score'].mean():.2f}")
c3.metric("Best OTD Rate", f"{df['otd_rate'].max():.1f}%")
c4.metric("Best Compliance", f"{df['compliance_rate'].max():.1f}%")
c5.metric("Best Savings", f"{df['avg_savings_pct'].max():.2f}%")

st.divider()
st.subheader("Overall Scorecard Ranking")

display_df = df_sorted[["Supplier", "otd_rate", "avg_lead_time_days", "defect_rate_pct", "avg_savings_pct", "compliance_rate", "weighted_score"]].copy()
display_df.columns = ["Supplier", "OTD %", "Lead Time (days)", "Defect %", "Savings %", "Compliance %", "Score"]

st.dataframe(
    display_df,
    use_container_width=True
)

st.divider()
st.subheader("1) Weighted Score Ranking")

fig_score = df_sorted[["Supplier", "weighted_score"]].copy()
st.bar_chart(fig_score.set_index("Supplier")["weighted_score"], use_container_width=True)

st.divider()
st.subheader("2) On-Time Delivery Rate")

fig_otd = df_sorted[["Supplier", "otd_rate"]].copy()
st.bar_chart(fig_otd.set_index("Supplier")["otd_rate"], use_container_width=True)

left, right = st.columns([1, 1])
with left:
    st.metric("Highest OTD", df_sorted.iloc[0]["Supplier"], f"{df_sorted.iloc[0]['otd_rate']:.1f}%")
with right:
    st.metric("Lowest OTD", df_sorted.iloc[-1]["Supplier"], f"{df_sorted.iloc[-1]['otd_rate']:.1f}%")

st.divider()
st.subheader("3) Lead Time Performance")

fig_lt = df_sorted[["Supplier", "avg_lead_time_days"]].copy()
st.bar_chart(fig_lt.set_index("Supplier")["avg_lead_time_days"], use_container_width=True)

left, right = st.columns([1, 1])
with left:
    st.metric("Fastest", df_sorted.loc[df_sorted["avg_lead_time_days"].idxmin()]["Supplier"], 
              f"{df_sorted['avg_lead_time_days'].min():.1f} days")
with right:
    st.metric("Slowest", df_sorted.loc[df_sorted["avg_lead_time_days"].idxmax()]["Supplier"], 
              f"{df_sorted['avg_lead_time_days'].max():.1f} days")

st.divider()
st.subheader("4) Quality: Defect Rate")

fig_defect = df_sorted[["Supplier", "defect_rate_pct"]].copy()
st.bar_chart(fig_defect.set_index("Supplier")["defect_rate_pct"], use_container_width=True)

left, right = st.columns([1, 1])
with left:
    st.metric("Best Quality", df_sorted.loc[df_sorted["defect_rate_pct"].idxmin()]["Supplier"], 
              f"{df_sorted['defect_rate_pct'].min():.2f}%")
with right:
    st.metric("Worst Quality", df_sorted.loc[df_sorted["defect_rate_pct"].idxmax()]["Supplier"], 
              f"{df_sorted['defect_rate_pct'].max():.2f}%")

st.divider()
st.subheader("5) Cost Savings")

fig_savings = df_sorted[["Supplier", "avg_savings_pct"]].copy()
st.bar_chart(fig_savings.set_index("Supplier")["avg_savings_pct"], use_container_width=True)

left, right = st.columns([1, 1])
with left:
    st.metric("Highest Savings", df_sorted.loc[df_sorted["avg_savings_pct"].idxmax()]["Supplier"], 
              f"{df_sorted['avg_savings_pct'].max():.2f}%")
with right:
    st.metric("Lowest Savings", df_sorted.loc[df_sorted["avg_savings_pct"].idxmin()]["Supplier"], 
              f"{df_sorted['avg_savings_pct'].min():.2f}%")

st.divider()
st.subheader("6) Compliance Rate")

fig_compliance = df_sorted[["Supplier", "compliance_rate"]].copy()
st.bar_chart(fig_compliance.set_index("Supplier")["compliance_rate"], use_container_width=True)

left, right = st.columns([1, 1])
with left:
    st.metric("Best Compliance", df_sorted.loc[df_sorted["compliance_rate"].idxmax()]["Supplier"], 
              f"{df_sorted['compliance_rate'].max():.1f}%")
with right:
    st.metric("Worst Compliance", df_sorted.loc[df_sorted["compliance_rate"].idxmin()]["Supplier"], 
              f"{df_sorted['compliance_rate'].min():.1f}%")

st.divider()
st.subheader("Multi-Metric Comparison")

st.markdown("**Normalized view (0-100 scale)** of all KPIs for easy side-by-side comparison:")

normalized = df_sorted[["Supplier"]].copy()
normalized["OTD %"] = df_sorted["otd_rate"]
normalized["Quality (100 - Defect %)"] = 100 - df_sorted["defect_rate_pct"]
normalized["Compliance %"] = df_sorted["compliance_rate"]
normalized["Savings %"] = df_sorted["avg_savings_pct"]
normalized["Lead Time Efficiency"] = 100 - (df_sorted["avg_lead_time_days"] / df_sorted["avg_lead_time_days"].max() * 100)

st.bar_chart(normalized.set_index("Supplier"), use_container_width=True)

st.divider()
with st.expander("View raw scorecard data"):
    st.dataframe(df.sort_values("weighted_score", ascending=False), use_container_width=True)
