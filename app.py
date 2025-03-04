from flask import Flask, request, jsonify
import pickle
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    price = float(data.get("price", 0))
    
    with open("mobile_model.pkl", "rb") as file:
        knn, df = pickle.load(file)
       # Define get_nearest_mobile inside the function
    def get_nearest_mobile(price):
        nearest_mobiles = df.iloc[(df["Prices"] - price).abs().argsort()[:5]]
        best_mobile = nearest_mobiles.sort_values(by="Reviews", ascending=False).iloc[0]
        return best_mobile
    
    best_mobile = get_nearest_mobile(price)
    
    return jsonify({
        "best_mobile": {
            "name": best_mobile["Product Name"],
            "price": best_mobile["Prices"],
            "reviews": best_mobile["Reviews"],
            "description": best_mobile["Description"]
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)