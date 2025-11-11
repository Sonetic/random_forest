from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

df = pd.read_csv('deweloperuch_all.csv')


X = df[["Area_m2", "Price_total", "Price_m2", "Rooms", "Floor", "source"]].copy()
y = df["Address"]


X = pd.get_dummies(X, columns=["source"], drop_first=True)

# split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# create and train the random forest model
rf_model = RandomForestClassifier(n_estimators=135, random_state=42)
rf_model.fit(X_train, y_train)

# accuracy
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Random Forest Accuracy:", accuracy)

# test example
sample = pd.DataFrame([{
    "Area_m2": 80,
    "Price_total": 2400000,
    "Price_m2": 30000,
    "Rooms": 5,
    "Floor": 3,
    "source_transactions": 0
}])

for col in X_train.columns:
    if col not in sample.columns:
        sample[col] = 0
sample = sample[X_train.columns]



# weights of features in model
importances = rf_model.feature_importances_
for col, imp in zip(X_train.columns, importances):
    print(f"{col}: {imp:.4f}")


# prediction of address
predicted_address = rf_model.predict(sample)
print("Most likely street:", predicted_address[0])