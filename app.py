import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from db_connection import engine
import queries as q

st.set_page_config(page_title="Influencer Campaign Dashboard", layout="wide")

# Title
st.title("📊 Influencer Campaign Dashboard")

# Sidebar Filters
with st.sidebar:
    st.header("🔍 Filters")
    selected_brand = st.selectbox("Select Brand", options=q.get_brand_list(engine))
    selected_platform = st.multiselect("Select Platform", options=q.get_platform_list(engine))
    selected_type = st.multiselect("Influencer Type", options=q.get_influencer_type_list(engine))
    date_range = st.date_input("Select Date Range", [])
    show_results = st.button("Show Results")

# Load and Filter Data
data = q.get_main_data(engine, brand=selected_brand, platforms=selected_platform, types=selected_type, dates=date_range)

# KPIs
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Total Spend", f"₹{q.get_total_spend(engine):,.0f}")
kpi2.metric("Total Revenue", f"₹{q.get_total_revenue(engine):,.0f}")
kpi3.metric("ROI", f"{q.get_roi(engine):.2f}")
kpi4.metric("Incremental ROAS", f"{q.get_incremental_roas(engine):.2f}")
kpi5.metric("Total Reach", f"{int(q.get_total_reach(engine).iloc[0]['total_reach']):,}")


# Charts
st.subheader("📈 Performance Overview")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Top 5 Influencers by ROAS")
    roas_df = q.get_top_influencers_by_roas(engine)
    st.bar_chart(roas_df.set_index("influencer_name"))

with col2:
    st.markdown("#### Monthly Spend vs Revenue")
    trend_df = q.get_monthly_trend(engine)
    st.line_chart(trend_df.set_index("month"))

# Detailed Table
st.subheader("📋 Influencer Performance Table")
table_data = q.get_influencer_table(engine)
st.dataframe(table_data, use_container_width=True)

# Optional: Text Insights
st.subheader("💡 Insights")
st.markdown(q.generate_text_insights(engine))
