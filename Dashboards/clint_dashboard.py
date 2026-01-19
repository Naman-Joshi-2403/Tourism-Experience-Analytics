import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

# =================================================
# PROJECT ROOT & ENV
# =================================================
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

ENV_PATH = os.path.join(PROJECT_ROOT, "dev.env")
load_dotenv(ENV_PATH)

APP_TITLE = os.getenv("APP_TITLE")
MASTER_DATA_PATH = os.getenv("MASTER_DATA_PATH")

DATA_PATH = os.path.join(PROJECT_ROOT, MASTER_DATA_PATH)

# =================================================
# STREAMLIT CONFIG
# =================================================
st.set_page_config(page_title=f"{APP_TITLE} – For Travelers", layout="wide")
st.title(f"{APP_TITLE} – Traveler Portal")

# =================================================
# LOAD DATA
# =================================================
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

# =================================================
# TOP MENU
# =================================================
selected_page = option_menu(
    menu_title=None,
    options=["Find Attractions", "My Preferences"],
    icons=["map", "heart"],
    orientation="horizontal"
)

# =================================================
# SIDEBAR – USER INPUTS
# =================================================
with st.sidebar:
    st.header("🌍 Your Travel Preferences")

    travel_month = st.selectbox("Month of Travel", list(range(1, 13)))

    attraction_category = st.selectbox(
        "Preferred Attraction Type",
        sorted(df["Attraction_Category"].dropna().unique())
    )

    destination_region = st.selectbox(
        "Preferred Region",
        sorted(df["Destination_Region_Name"].dropna().unique())
    )

    traveler_group = st.selectbox(
        "You are traveling with",
        sorted(df["Traveler_Group_Type"].dropna().unique())
    )

# =================================================
# PAGE 1: FIND ATTRACTIONS
# =================================================
if selected_page == "Find Attractions":

    st.subheader("🎯 Recommended Attractions For You")

    filtered = df[
        (df["Attraction_Category"] == attraction_category) &
        (df["Destination_Region_Name"] == destination_region) &
        (df["Traveler_Group_Type"] == traveler_group)
    ]

    if filtered.empty:
        st.warning("No exact matches found. Showing popular alternatives.")
        filtered = df[
            (df["Destination_Region_Name"] == destination_region)
        ]

    top_attractions = (
        filtered
        .groupby("Attraction_Name")["User_Rating"]
        .mean()
        .sort_values(ascending=False)
        .head(6)
        .reset_index()
    )

    if top_attractions.empty:
        st.info("Not enough data to recommend yet.")
    else:
        cols = st.columns(3)
        for idx, row in top_attractions.iterrows():
            with cols[idx % 3]:
                st.markdown(f"### 📍 {row['Attraction_Name']}")
                st.write(f"⭐ Avg Rating: {row['User_Rating']:.2f}")
                st.write(f"Category: {attraction_category}")
                st.write(f"Region: {destination_region}")

# =================================================
# PAGE 2: MY PREFERENCES
# =================================================
if selected_page == "My Preferences":

    st.subheader("💖 Your Travel Profile")

    st.write("Based on your inputs:")

    st.success(f"""
    • You prefer **{attraction_category}**  
    • You like traveling in **{destination_region}**  
    • You travel with **{traveler_group}**  
    • You plan to travel in month **{travel_month}**
    """)

    similar_users = df[
        (df["Attraction_Category"] == attraction_category) &
        (df["Traveler_Group_Type"] == traveler_group)
    ]

    if not similar_users.empty:
        best_region = (
            similar_users
            .groupby("Destination_Region_Name")["User_Rating"]
            .mean()
            .idxmax()
        )

        st.info(f"People like you enjoyed trips most in: **{best_region}**")
    else:
        st.info("Not enough similar users yet to analyze.")
