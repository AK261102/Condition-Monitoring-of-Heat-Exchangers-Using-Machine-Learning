import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

# Load the trained model
model_path = "best_rf_model.pkl"  # Replace with the path to your saved model
model = joblib.load(model_path)

# Initialize Flask app
app = Flask(__name__)

# Define an endpoint for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Parse the incoming JSON data from the request
    data = request.get_json()
    
    # Convert the JSON data to a DataFrame
    input_data = pd.DataFrame([data])
    
    # Make a prediction using the loaded model
    prediction = model.predict(input_data)

    # Return the prediction as a JSON response
    return jsonify({'fouling_factor': prediction[0]})

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
