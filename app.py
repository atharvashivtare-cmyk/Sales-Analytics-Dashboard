import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Analytics Dashboard")
st.markdown("### Analyze your sales data with interactive visualizations")

st.sidebar.header("📂 Upload Data")

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/sales_data.csv")

st.sidebar.header("🎛 Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories))
]

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = len(filtered_df)
total_products = filtered_df["Product"].nunique()

st.header("📈 Dashboard Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Sales", f"₹{total_sales:,}")
c2.metric("📈 Total Profit", f"₹{total_profit:,}")
c3.metric("🛒 Orders", total_orders)
c4.metric("📦 Products", total_products)

st.divider()

st.subheader("📋 Sales Data")
st.dataframe(filtered_df, use_container_width=True)

left, right = st.columns(2)

with left:
    sales_region = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        sales_region,
        x="Region",
        y="Sales",
        color="Region",
        title="Sales by Region",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    sales_category = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        sales_category,
        values="Sales",
        names="Category",
        hole=0.45,
        title="Sales by Category"
    )

    st.plotly_chart(fig2, use_container_width=True)