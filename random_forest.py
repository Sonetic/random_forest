from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

df = pd.read_csv('deweloperuch_all.csv')

# zakładamy df z kolumnami: Area_m2, Price_total, Price_m2, Rooms, Floor, source, Address
X = df[["Area_m2", "Price_total", "Price_m2", "Rooms", "Floor", "source"]].copy()
y = df["Address"]

# zakoduj source
X = pd.get_dummies(X, columns=["source"], drop_first=True)

# podział danych
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# model Random Forest
rf_model = RandomForestClassifier(n_estimators=125, random_state=42)
rf_model.fit(X_train, y_train)

# predykcja i accuracy
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Random Forest Accuracy:", accuracy)
