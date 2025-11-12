from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

df = pd.read_csv('deweloperuch_all.csv')

# features
X = df[["Area_m2", "Price_total", "Price_m2", "Rooms", "Floor", "source"]].copy()
y = df["Address"]

# removal of rare classes (which only occur once)
counts = y.value_counts()
mask = y.isin(counts[counts > 1].index)
X = X[mask]
y = y[mask]

# one-hot encoding
X = pd.get_dummies(X, columns=["source"], drop_first=True)

# train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42, stratify=y
)

# encoder
encoder = LabelEncoder()
y_train_encoded = encoder.fit_transform(y_train)
y_test_encoded = encoder.transform(y_test)

# model XGBoost
xgb_model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    tree_method="hist",
    eval_metric="mlogloss",
    objective="multi:softmax",
    num_class=len(np.unique(y_train_encoded))
)


xgb_model.fit(X_train, y_train_encoded)


y_pred_encoded = xgb_model.predict(X_test)
accuracy = accuracy_score(y_test_encoded, y_pred_encoded)
print("XGBoost Accuracy:", accuracy)

