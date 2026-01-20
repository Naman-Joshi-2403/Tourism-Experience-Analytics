import streamlit as st
import pandas as pd
import joblib
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

###### Load envirnment variabel #######
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

ENV_PATH = os.path.join(PROJECT_ROOT, "dev.env")
if not os.path.exists(ENV_PATH):
    raise FileNotFoundError(f"dev.env not found at: {ENV_PATH}")

load_dotenv(ENV_PATH)

APP_TITLE = os.getenv("APP_TITLE")
MASTER_DATA_PATH = os.getenv("MASTER_DATA_PATH")
RATING_MODEL_PATH = os.getenv("RATING_MODEL_PATH")
VISIT_MODE_MODEL_PATH = os.getenv("VISIT_MODE_MODEL_PATH")


DATA_PATH = os.path.join(PROJECT_ROOT, MASTER_DATA_PATH)
RATING_MODEL_PATH = os.path.join(PROJECT_ROOT, RATING_MODEL_PATH)
VISIT_MODE_MODEL_PATH = os.path.join(PROJECT_ROOT, VISIT_MODE_MODEL_PATH)

# raw data load
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

################## Streamlit app config ##################
st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)
st.caption("Organization Intelligence Dashboard")


########## nav bar #############
selected_dashboard = option_menu(
    menu_title="Organization Dashboards",
    options=[
        "Trip Quality Validator",
        "Visit Mode Intelligence"
    ],
    icons=["star-fill", "people-fill"],
    menu_icon="building",
    default_index=0,
    orientation="horizontal"
)

############### side bad filters ###############
with st.sidebar:
    st.subheader("🗓️ Travel Planning Inputs")

    CURRENT_YEAR = 2026
    MAX_YEAR = CURRENT_YEAR + 5

    year = st.selectbox(
        "Year of Travel",
        list(range(CURRENT_YEAR, MAX_YEAR + 1))
    )

    month = st.selectbox(
        "Month of Travel",
        list(range(1, 13))
    )

    attraction_category = st.selectbox(
        "Attraction Category",
        sorted(df["Attraction_Category"].dropna().unique())
    )

    destination_region = st.selectbox(
        "Destination Region",
        sorted(df["Destination_Region_Name"].dropna().unique())
    )



############# Load Models ######################


@st.cache_resource
def load_rating_artifacts():
    return joblib.load(RATING_MODEL_PATH)

@st.cache_resource
def load_visit_mode_model():
    return joblib.load(VISIT_MODE_MODEL_PATH)


# rating model load 
rating_artifacts = load_rating_artifacts()
rating_pipeline = rating_artifacts["model"]
region_frequency_map = rating_artifacts["region_frequency_map"]

# Visit mode model load
# visit_mode_model = load_visit_mode_model()


########## Travel quality validator ########################
if selected_dashboard == "Trip Quality Validator":

    st.subheader("⭐ Trip Quality Validator")
    st.write(
        "Predict expected customer satisfaction **before** finalizing a trip package."
    )

    traveler_group = st.selectbox(
        "Traveler Group Type",
        sorted(df["Traveler_Group_Type"].dropna().unique())
    )

    if st.button("Evaluate Trip Plan"):
        destination_region_freq = region_frequency_map.get(
            destination_region,
            region_frequency_map.mean()
        )

        input_df = pd.DataFrame([{
            "Year_of_Visit": year,
            "Month_of_Visit": month,
            "Attraction_Category": attraction_category,
            "Traveler_Group_Type": traveler_group,
            "Destination_Region_Freq": destination_region_freq
        }])

        predicted_rating = rating_pipeline.predict(input_df)[0]

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Predicted Rating (1-5)", round(predicted_rating, 2))

        with col2:
            if predicted_rating >= 4:
                st.success("✅ High satisfaction expected")
            elif predicted_rating >= 3:
                st.warning("⚠️ Moderate satisfaction – review plan")
            else:
                st.error("❌ High risk of dissatisfaction")

        st.markdown("### 📊 Historical Context")

        similar = df[
            (df["Attraction_Category"] == attraction_category) &
            (df["Traveler_Group_Type"] == traveler_group) &
            (df["Destination_Region_Name"] == destination_region)
        ]

        if not similar.empty:
            st.write(
                f"Average historical rating for similar trips: "
                f"**{similar['User_Rating'].mean():.2f}**"
            )
        else:
            st.info("Not enough historical data for exact comparison.")

################## VISIT MODE INTELLIGENCE #################
if selected_dashboard == "Visit Mode Intelligence":

    st.subheader("🧳 Visit Mode Intelligence")
    st.write(
        "Predict the most likely traveler group type to support "
        "marketing, staffing, and package design."
    )

    if st.button("Predict Visit Mode"):

        input_df = pd.DataFrame([{
            "Year_of_Visit": year,
            "Month_of_Visit": month,
            "Attraction_Category": attraction_category,
            "Destination_Region_Name": destination_region
        }])

        predicted_mode = visit_mode_model.predict(input_df)[0]

        st.metric("Predicted Visit Mode", predicted_mode)

        st.markdown("### 🧠 Business Interpretation")

        if predicted_mode.lower() == "family":
            st.info("👨‍👩‍👧 Likely family travelers – promote family-friendly packages.")
        elif predicted_mode.lower() == "couples":
            st.info("💑 Couple travel expected – highlight romantic experiences.")
        elif predicted_mode.lower() == "business":
            st.info("💼 Business travel expected – focus on convenience and hotels.")
        else:
            st.info("👥 Group travel expected – promote group discounts.")
