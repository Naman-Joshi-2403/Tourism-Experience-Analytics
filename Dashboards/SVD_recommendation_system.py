import pandas as pd 
import numpy as np 
import joblib
import os 
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from dotenv import load_dotenv

######### ENV Variable #####################
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
ENV_PATH = os.path.join(PROJECT_ROOT, "dev.env")
if not os.path.exists(ENV_PATH):
    raise FileNotFoundError(f"dev.env not found at: {ENV_PATH}")

load_dotenv(ENV_PATH)


MASTER_DATA_PATH = os.getenv("MASTER_DATA_PATH")


########### Read Input #####################
df = pd.read_csv(os.path.join(PROJECT_ROOT, MASTER_DATA_PATH))

df = df[["UserId",
         "AttractionId",
         "Attraction_Name",
         "User_Rating",
         "Month_of_Visit"
         ]].dropna()

########### Filter Month data #####################
def populat_attraction_month(month, top_n = 5):
    return (df[df["Month_of_Visit"] == month]
            .groupby(["AttractionId", "Attraction_Name"])['User_Rating']
            .mean()
            .sort_values(ascending=False)
            .head(top_n)
            .reset_index()
            )

########### Train SVD for given month #####################
def train_svd_month(selected_month, n_components= 30):
    filter_df = df[df['Month_of_Visit'] == selected_month].copy()

    if filter_df.empty:
        return None

    ### Encode Users and item 
    user_encoder = LabelEncoder()
    item_encoder = LabelEncoder()

    filter_df["user_idx"] = user_encoder.fit_transform(filter_df['UserId'])
    filter_df["item_idx"] = user_encoder.fit_transform(filter_df['AttractionId'])

    ### User Item Matrix
    user_item_matrix = filter_df.pivot_table(
        index = "user_idx",
        columns = "item_idx",
        values = "User_Rating"
    ).fillna(0)

    num_user, num_item = user_item_matrix.shape
    max_components = min(num_user, num_item) - 1
    n_components = min(n_components, max_components)

    if n_components < 2:
        return None

    ### Train SVD
    svd = TruncatedSVD(
        n_components = n_components,
        random_state = 42
    )

    user_factors = svd.fit_transform(user_item_matrix)
    item_factors = svd.components_

    predicted_rating = np.dot(user_factors, item_factors)

    return {
        "predicted" : predicted_rating,
        "user_encoder" : user_encoder,
        "item_encoder" : item_encoder,
        "user_item_matrix" : user_item_matrix,
        "svd" : svd
    }

def recommend_for_user_month(user_id, month, top_n = 5):
    model = train_svd_month(selected_month = month)

    if model is None:
        return "❌ No data available for this month"

    user_encoder = model['user_encoder']
    item_encoder = model['item_encoder']
    predicted = model['predicted']

    ### If user is new 
    if user_id not in user_encoder.classes_:
        return populat_attraction_month(month=month, top_n = top_n)

    ### Get user index
    u_idx = user_encoder.transform([user_id])[0]
    scores = predicted[u_idx]

    ### top n item indices
    top_items = np.argsort(scores)[ : :-1][:top_n]

    ### Map back to attractio ID
    attraction_ids = item_encoder.inverse_transform(top_items)

    recommendation = pd.DataFrame({
        "AttractionId" : attraction_ids,
        "Predication_Ratiing" : scores[top_items]
    })

    recommendation = recommendation.merge(
        df[["AttractionId", "Attraction_Name"]].drop_duplicates(),
        on = "AttractionId",
        how = "left"
    )

    return recommendation

