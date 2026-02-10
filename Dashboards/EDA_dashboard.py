import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from streamlit_option_menu import option_menu


st.set_page_config(
    page_title="Tourism EDA Dashboard",
    layout="wide"
)


@st.cache_data
def load_data():
    return pd.read_csv("Tourism_Final_Master_Analytical.csv")

df = load_data()

### side bar
with st.sidebar:
    selected = option_menu(
        menu_title="EDA Navigation",
        options=["Dashboard", "EDA Summary"],
        icons=["bar-chart-line", "clipboard-data"],
        menu_icon="cast",
        default_index=0
    )


if selected == "Dashboard":

    st.title("📊 Tourism Experience Analytics – EDA Dashboard")
    st.markdown("Interactive exploration of traveler behavior and attraction trends")

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

    filtered_df = df[
        (df["Traveler_Home_Continent"].isin(selected_continent)) &
        (df["Year_of_Visit"].isin(selected_year))
    ]

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Visits", filtered_df.shape[0])
    col2.metric("Unique Travelers", filtered_df["UserId"].nunique())
    col3.metric("Attractions", filtered_df["AttractionId"].nunique())
    col4.metric("Avg Rating", round(filtered_df["User_Rating"].mean(), 2))

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


elif selected == "EDA Summary":
    st.title("🧠 EDA Summary & Key Takeaways")

    st.markdown("""
    ### 📌 Data Overview
    - This dataset contains individual tourist visit records.
    - It includes traveler details, attraction details, and visit information.
    - All required tables were merged into one final dataset for easy analysis.

    ### 🌍 Travel Behavior Patterns
    - Most tourists are coming from limited regions, not evenly distributed.
    - Different traveler groups like family, friends, and business prefer different attractions.
    - Season and month have some impact, but they do not directly decide satisfaction.

    ### ⭐ Rating Insights
    - Ratings are not directly related to numeric values in a straight way.
    - Tourist satisfaction depends more on visit type, location, and attraction category.
    - Context matters more than just numbers.

    ### 🔍 Correlation Understanding
    - Numerical columns show very low linear correlation.
    - There is no multicollinearity issue in the dataset.
    - Because of this, linear models are not the best choice.

    ### 🤖 Model Decision Logic
    - Tree-based models can capture complex patterns better.
    - Models like Random Forest, XGBoost, LightGBM, and CatBoost are suitable.
    - Recommendation system works based on user and attraction interaction history.

    ### 💡 Business Impact
    - Helps in customer segmentation and personalization.
    - Can be used for targeted marketing and recommendations.
    - Supports better decision-making for tourism platforms.
    """)
