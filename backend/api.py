from flask import Flask, request, jsonify
from flask_cors import CORS  # konieczne, żeby frontend mógł wysyłać fetch z innego portu
import joblib
import pandas as pd

model = joblib.load("model.pkl")



app = Flask(__name__)
CORS(app)  # włączenie CORS dla wszystkich domen

@app.route("/predict", methods=["GET"])
def predict_get():
    return "Wejdź tutaj z POST, żeby wysłać dane JSON."


X_train_columns = ["Area_m2", "Price_total", "Price_m2", "Rooms", "Floor", "source_transactions"]

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    print("Odebrane dane:", data)  # debug w konsoli

    # Tworzymy DataFrame z przesłanych danych
    sample = pd.DataFrame([data])

    # Dodaj brakujące kolumny
    for col in X_train_columns:
        if col not in sample.columns:
            sample[col] = 0

    # Ustawiamy kolejność kolumn jak w modelu
    sample = sample[X_train_columns]

    # Predykcja
    predicted_address = model.predict(sample)[0]

    # Zwracamy tylko przewidywaną ulicę
    return jsonify({"predicted_address": predicted_address})

if __name__ == "__main__":
    app.run(debug=True)