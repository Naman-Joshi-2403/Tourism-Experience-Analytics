# 🌍 Tourism Experience Analytics  
### Classification, Prediction & Recommendation System  

---

## 📌 Project Overview  

Tourism Experience Analytics is an end-to-end Data Science project that analyzes tourist behavior and builds intelligent systems to:

- Predict attraction ratings  
- Classify visit modes (Business, Family, Couples, Friends)  
- Generate personalized attraction recommendations  
- Provide business-level tourism insights through dashboards  

This project combines **Data Cleaning, EDA, Machine Learning, and Streamlit deployment** into one complete solution.

---

## 🎯 Business Objectives  

1. Predict how a user will rate an attraction.  
2. Classify the likely visit mode of a traveler.  
3. Recommend attractions based on user behavior and seasonal context.  
4. Provide insights for tourism platforms and decision-makers.  

---

## 📊 Exploratory Data Analysis (EDA) Summary  

### 📌 About the Data  
- The dataset contains individual tourist visits with user and attraction information.  
- All raw datasets were merged into a single master dataset for analysis and modeling.  

### 🌍 Key Observations  
- Some regions receive much higher tourist traffic than others.  
- Different traveler groups prefer different types of attractions.  
- Tourism varies across months, but month alone does not directly determine ratings.  

### ⭐ Rating Insights  
- Most ratings fall between 3 and 5.  
- There is no strong linear relationship between ratings and numeric features.  
- Satisfaction depends on combinations of features like traveler group and attraction type.  

### 🔎 Correlation Findings  
- Correlation between numeric features is low.  
- No major multicollinearity issue was found.  
- Identifier columns were removed before modeling.  

### 🤖 Modeling Decision  
- Tree-based models like Random Forest performed better due to non-linear patterns.  
- Recommendation system uses SVD-based collaborative filtering.  

---

## 🤖 Machine Learning Components  

### 1️⃣ Rating Prediction (Regression)  
- Model: Random Forest  
- Target: User_Rating  

### 2️⃣ Visit Mode Classification  
- Model: Classification model (e.g., Random Forest)  
- Target: VisitMode  

### 3️⃣ Recommendation System  
- Technique: Matrix Factorization using Truncated SVD  
- Context-aware filtering by Month  
- Cold-start handled using popularity-based fallback  

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

# 🔧 Project Setup Instructions  

## 1️⃣ Clone the Repository  

```bash
git clone https://github.com/Naman-Joshi-2403/Tourism-Experience-Analytics.git
cd Tourism-Experience-Analytics
```

---

## 2️⃣ Create Virtual Environment  

```bash
python -m venv env
```

Activate environment:

**Windows**
```bash
env\Scripts\activate
```

---

## 3️⃣ Install Required Libraries  

```bash
pip install pandas numpy scikit-learn streamlit joblib python-dotenv
```

---

## 4️⃣ Generate Master Dataset  

If the master dataset does not exist, run:

```bash
python dataset_merge.py
```

This will generate:
```
Tourism_Final_Master_Analytical.csv
```

---

## 5️⃣ Set Environment Variable  

Update the `dev.env` file:

```
MASTER_DATA_PATH=Input/Tourism_Final_Master_Analytical.csv
```

---

## 6️⃣ Run the Dashboard  

```bash
streamlit run Dashboards/clint_dashboard.py
```

The application will open in your browser.

---

## 📌 How to Use the Dashboard  

1. Enter a **User ID**  
2. Select **Month of Visit**  
3. Click **Get Recommendations**  
4. View personalized attraction suggestions  

---

## 📈 Evaluation Metrics  

- Regression: RMSE, MAE  
- Classification: Accuracy, Precision, Recall, F1-score  
- Recommendation: Ranking-based evaluation  

---

## 🚀 Future Improvements  

- Hybrid recommendation system  
- Time-aware modeling  
- API deployment  
- Real-time user login integration  

---

## 👤 Author  

**Naman Joshi**  
---
