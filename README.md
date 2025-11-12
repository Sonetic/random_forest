# Apartment Location Prediction using Random Forest

This project aims to predict the **most probable street** for an apartment based on its features such as area, price, number of rooms, and floor.  
It implements a **Random Forest classifier** using **scikit-learn** to analyze data scraped from **deweloperuch.pl**.

---

## Project Structure

- `scrapping.py` & `scrapping2.py` — scripts for scraping apartment data  
- `columns_preparation.py` — data preprocessing and missing value imputation  
- `random_forest.py` — Random Forest training and prediction
- `xgb.py` — XGBoost training and prediction
- `README.md`  


---

## Dataset Overview

The dataset includes features such as:
- **Area_m2** — apartment area in square meters  
- **Price_total** — total price of the apartment  
- **Price_m2** — price per square meter  
- **Rooms** — number of rooms  
- **Floor** — floor number  
- **source** — number of transactions or source activity (categorical)
- **Address** — target variable (the street where the apartment is located)

The data is collected automatically via web scraping from **deweloperuch.pl** and converted into a structured DataFrame suitable for modeling.

---

## Implementation Details

### `scrapping.py` & `scrapping2.py` — Data Scraping
- These scripts collect apartment data automatically from **deweloperuch.pl**.  
- Extracts information such as area, price, number of rooms, floor, source transactions, and address.  
- Handles multiple pages and listings to build a comprehensive dataset.

### `columns_preparation.py` — Data Preparation
- Cleans and preprocesses the scraped data.  
- Uses **Linear Regression** to fill missing values in Rooms and Floor columns, improving data completeness.  
- Ensures proper data types for numerical features.  

### `random_forest.py` — Random Forest Prediction
- Loads the processed dataset.  
- Splits data into **training and testing sets**.  
- Trains a **Random Forest classifier** (`sklearn.ensemble.RandomForestClassifier`).  
- Outputs:
  - **Model accuracy**
  - **Feature importances**
  - **Most likely street** based on input parameters

- Each decision tree in the forest is trained on a random subset of rows and features, reducing overfitting and improving generalization.



### `xgb.py` — eXtreme Gradient Boosting Prediction
- Loads the processed dataset from `deweloperuch_all.csv`.  
- Removes **rare address classes** (appearing only once) to improve model stability.  
- Performs **one-hot encoding** of categorical features.  
- Splits data into **training and testing sets** using stratified sampling to maintain class balance.  
- Encodes target labels with **LabelEncoder**.  
- Trains an **XGBoost classifier** (`xgboost.XGBClassifier`) with optimized parameters:  
  - `n_estimators=300`, `learning_rate=0.1`, `max_depth=6`, `subsample=0.8`, `colsample_bytree=0.8`  
- Outputs:  
  - **Model accuracy**  

- Each tree is built sequentially, correcting mistakes of the previous ones.  
  This **boosting mechanism** allows XGBoost to achieve higher accuracy and better generalization than Random Forest.


---

## Results & Interpretation
### Random Forest

Example output:
Random Forest Accuracy: 0.6814

Feature importances:
Area_m2: 0.3106
Price_total: 0.2880
Price_m2: 0.3083
Rooms: 0.0282
Floor: 0.0569
source_transactions:0.0079

Most likely street: Jaśminowy Mokotów etap VI



- **Accuracy (~68%)** indicates that the model correctly predicts the street in about 2/3 of cases.  
- **Most important features**:
  - `Area_m2`, `Price_m2`, `Price_total` — collectively contributing over 90% of feature importance, showing that size and price strongly determine location.  
- **Less important features**:
  - `Rooms`, `Floor`, `source_transactions` — low influence on predictions.  
- **Predicted street**:
  - For given input parameters, the model predicts **Jaśminowy Mokotów etap VI** as the most probable street.

The results demonstrate that Random Forest can successfully capture patterns linking apartment characteristics to their location.

---


### XGBoost
Example output:
XGBoost Accuracy: 0.7026


- **Accuracy (~70%)** shows that XGBoost performs slightly better than Random Forest, capturing more complex relationships between features.  
- Thanks to its **boosting mechanism**, where each tree corrects the errors of the previous ones, XGBoost achieves higher precision and better generalization.  

---

Overall, both models demonstrate strong predictive capabilities, with **XGBoost outperforming Random Forest by about 2%**, confirming its advantage in modeling structured tabular data.


## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Sonetic/random_forest.git
   cd random_forest

2. Install dependencies:
   ```bash
   pip install pandas scikit-learn requests beautifulsoup4 xgboost
3. Run 
   ```bash
   python scrapping.py
   python scrapping2.py
   python columns_preparation.py
   python random_forest.py
   python xgb.py









