import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from streamlit_option_menu import option_menu

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="Tourism EDA Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("Tourism_Final_Master_Analytical.csv")

df = load_data()

# ---------------------------------------------------
# Sidebar Navigation ONLY
# ---------------------------------------------------
with st.sidebar:
    selected = option_menu(
        menu_title="EDA Navigation",
        options=["Dashboard", "EDA Summary"],
        icons=["bar-chart-line", "clipboard-data"],
        menu_icon="cast",
        default_index=0
    )

# ===================================================
# 1️⃣ DASHBOARD TAB (WITH FILTERS)
# ===================================================
if selected == "Dashboard":

    st.title("📊 Tourism Experience Analytics – EDA Dashboard")
    st.markdown("Interactive exploration of traveler behavior and attraction trends")

    # ---------------- Filters (INSIDE DASHBOARD) ----------------
    st.subheader("🔎 Dashboard Filters")

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        selected_continent = st.multiselect(
            "Select Continent",
            options=df["Traveler_Home_Continent"].dropna().unique(),
            default=df["Traveler_Home_Continent"].dropna().unique()
        )

    with col_f2:
        selected_year = st.multiselect(
            "Select Year",
            options=sorted(df["Year_of_Visit"].dropna().unique()),
            default=sorted(df["Year_of_Visit"].dropna().unique())
        )

    # Apply filters
    filtered_df = df[
        (df["Traveler_Home_Continent"].isin(selected_continent)) &
        (df["Year_of_Visit"].isin(selected_year))
    ]

    st.markdown("---")

    # ---------------- KPI Section ----------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Visits", filtered_df.shape[0])
    col2.metric("Unique Travelers", filtered_df["UserId"].nunique())
    col3.metric("Attractions", filtered_df["AttractionId"].nunique())
    col4.metric("Avg Rating", round(filtered_df["User_Rating"].mean(), 2))

    # ---------------- Visuals ----------------
    st.subheader("🌍 Travelers by Continent")
    fig1, ax1 = plt.subplots()
    filtered_df["Traveler_Home_Continent"].value_counts().plot(kind="bar", ax=ax1)
    st.pyplot(fig1)

    st.subheader("🏝️ Popular Attraction Categories")
    fig2, ax2 = plt.subplots()
    filtered_df["Attraction_Category"].value_counts().head(10).plot(kind="barh", ax=ax2)
    st.pyplot(fig2)

    st.subheader("⭐ Rating Distribution")
    fig3, ax3 = plt.subplots()
    sns.histplot(filtered_df["User_Rating"], bins=10, kde=True, ax=ax3)
    st.pyplot(fig3)

    st.subheader("👨‍👩‍👧‍👦 Avg Rating by Visit Mode")
    avg_rating = filtered_df.groupby("Traveler_Group_Type")["User_Rating"].mean()
    fig4, ax4 = plt.subplots()
    avg_rating.plot(kind="bar", ax=ax4)
    st.pyplot(fig4)

    st.subheader("📆 Monthly Travel Trend")
    monthly_trend = filtered_df["Month_of_Visit"].value_counts().sort_index()
    fig5, ax5 = plt.subplots()
    monthly_trend.plot(kind="line", marker="o", ax=ax5)
    st.pyplot(fig5)

    # ---------------- Correlation Heatmap ----------------
    st.subheader("🔥 Correlation Heatmap")

    numerical_cols = [
        "Year_of_Visit",
        "Month_of_Visit",
        "User_Rating",
        "UserId",
        "AttractionId"
    ]

    corr = filtered_df[numerical_cols].corr()

    fig6, ax6 = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax6)
    st.pyplot(fig6)

# ===================================================
# 2️⃣ EDA SUMMARY TAB (NO FILTERS)
# ===================================================
elif selected == "EDA Summary":

    st.title("🧠 EDA Summar y & Key Takeaways")

    st.markdown("""
    ### 📌 Data Overview
    - Dataset represents individual tourist visits with enriched traveler and attraction attributes.
    - A consolidated analytical table enables efficient EDA and modeling.

    ### 🌍 Key Behavioral Patterns
    - Tourism demand shows strong regional concentration.
    - Attraction preferences vary significantly by traveler group.
    - Seasonal trends exist but do not linearly drive satisfaction.

    ### ⭐ Rating Insights
    - Ratings are not linearly correlated with numeric features.
    - Satisfaction is driven by **non-linear interactions** and categorical context.

    ### 🔥 Correlation Interpretation
    - Low linear correlation confirms the absence of multicollinearity.
    - Identifier columns are excluded from modeling.
    - Tree-based and ensemble models are justified.

    ### 🤖 Modeling Decisions
    - Preference for Random Forest, XGBoost, LightGBM, CatBoost.
    - Recommendation systems rely on user–item interaction patterns.

    ### 💡 Business Impact
    - Enables personalization, segmentation, and targeted marketing.
    - Supports data-driven tourism strategy and experience optimization.
    """)
 