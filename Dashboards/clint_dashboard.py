import streamlit as st
import pandas as pd
from SVD_recommendation_system import recommend_for_user_month


st.set_page_config(
    page_title="Tourism Recommendation Dashboard",
    layout="wide"
)

st.title("🌍 Tourism Experience Recommendation System")
st.markdown(
    """
    This dashboard provides **personalized attraction recommendations**
    using a **machine learning-based SVD recommendation engine**.
    """
)

st.divider()
st.sidebar.header("🔎 Recommendation Filters")

user_id = st.sidebar.number_input(
    "Enter User ID",
    min_value=1,
    step=1,
    help="Simulated user identifier (no login system)"
)

month = st.sidebar.selectbox(
    "Month of Visit",
    options=list(range(1, 13)),
    format_func=lambda x: pd.to_datetime(str(x), format="%m").strftime("%B")
)

top_n = st.sidebar.slider(
    "Number of Recommendations",
    min_value=1,
    max_value=10,
    value=5
)

st.subheader("🎯 Recommended Attractions")

if st.sidebar.button("Get Recommendations"):
    with st.spinner("Generating personalized recommendations..."):
        result = recommend_for_user_month(
            user_id=user_id,
            month=month,
            top_n=top_n
        )


    if isinstance(result, str):
        st.warning(result)
    else:
        st.success("Here are the top attractions for you 👇")
        st.dataframe(
            result,
            use_container_width=True,
            hide_index = True
        )

else:
    st.info(
        "👈 Please select filters from the sidebar and click **Get Recommendations**"
    )

