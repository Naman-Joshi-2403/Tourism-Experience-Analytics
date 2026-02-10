# 🌍 Tourism Experience Analytics  
### Classification, Prediction & Recommendation System

## 📌 Project Overview
Tourism Experience Analytics is an end-to-end data science and machine learning project designed to analyze tourist behavior, predict satisfaction, classify visit modes, and generate personalized attraction recommendations.

The project combines **data analytics**, **machine learning**, and **interactive dashboards** to deliver actionable insights for tourism platforms and stakeholders.

---

## 🎯 Business Objectives
1. **Predict Attraction Ratings** – Estimate how a user might rate an attraction.
2. **Classify Visit Mode** – Predict whether a user is traveling for Business, Family, Couples, or Friends.
3. **Personalized Recommendations** – Suggest attractions based on user behavior and seasonal context.
4. **Tourism Insights Dashboard** – Visualize trends, popularity, and user behavior.

---

## 🧠 Key Features
- 📊 Exploratory Data Analysis (EDA)
- ⭐ Rating Prediction (Regression Models)
- 🧳 Visit Mode Classification (Classification Models)
- 🎯 Personalized Recommendation System (SVD-based Collaborative Filtering)
- 🖥️ Interactive Streamlit Dashboards
- ❄️ Cold-start handling for new users

---

## 🗂️ Project Structure

```
Tourism-Experience-Analytics/
│
├── Dashboards/
│   ├── clint_dashboard.py
│   ├── EDA_dashboard.py
│   ├── organization_dashboard.py
│   └── SVD_recommendation_system.py
│
├── Model Training/
│   ├── rating_prediction.ipynb
│   ├── rating_pred_all_features.ipynb
│   └── visit_mode_model_training.ipynb
│
├── Models/
│   ├── rating_model.pkl
│   ├── tourism_rating_model_random_forest.pkl
│   └── visit_mode_classifier.pkl
│
├── Input/
├── Final Raw Data/
├── Doc/
├── env/
│
├── dev.env
├── README.md
└── .gitignore
```

---

## 🔍 Dataset Description
The project uses a tourism dataset containing:
- User demographics and location hierarchy
- Visit details such as month, mode, and ratings
- Attraction attributes like type and location

All datasets are merged into a **master analytical dataset** for modeling and analysis.

---

## 🤖 Machine Learning Models Used

### 1️⃣ Rating Prediction (Regression)
- Algorithms: Random Forest
- Target: User_Rating

### 2️⃣ Visit Mode Classification
- Algorithms: Classification models
- Target: VisitMode

### 3️⃣ Recommendation System
- Technique: Matrix Factorization using Truncated SVD
- Context-aware: Month of Visit
- Cold-start handling via popularity-based fallback

---

## 🖥️ Dashboards
- Client Dashboard (UserId-based recommendations)
- EDA Dashboard
- Organization Insights Dashboard

---

## ⚙️ How to Run

```bash
pip install -r requirements.txt
streamlit run Dashboards/clint_dashboard.py
```

---

## 📈 Evaluation Metrics
- Regression: RMSE, MAE
- Classification: Accuracy, Precision, Recall, F1-score
- Recommendation: Ranking-based evaluation

---

## 🚀 Future Enhancements
- Hybrid recommendation system
- Time-aware modeling
- API deployment

---

## 👤 Author
**Naman Joshi**
