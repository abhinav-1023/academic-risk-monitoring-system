import os
import joblib
import numpy as np

print("NEW PREDICTION FILE LOADED")

# -----------------------------------
# BASE DIRECTORY
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------------
# MODEL PATH
# -----------------------------------

MODEL_PATH = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "models",
        "risk_model.pkl"
    )
)

print("MODEL PATH:", MODEL_PATH)
print("MODEL EXISTS:", os.path.exists(MODEL_PATH))

# -----------------------------------
# LOAD MODEL
# -----------------------------------

model = None

try:

    if os.path.exists(MODEL_PATH):

        model = joblib.load(MODEL_PATH)

        print("MODEL LOADED SUCCESSFULLY")

    else:

        print("MODEL FILE NOT FOUND")

except Exception as e:

    print("MODEL LOADING ERROR:", e)

# -----------------------------------
# PREDICTION FUNCTION
# -----------------------------------

def predict_risk(
    attendance,
    internal,
    participation,
    assignment,
    quiz,
    midsem
):

    if model is None:
        return "Model not loaded"

    try:

        # Convert input into NumPy array
        data = np.array([
            [
                attendance,
                internal,
                participation,
                assignment,
                quiz,
                midsem
            ]
        ])

        # Predict risk
        prediction = model.predict(data)

        return prediction[0]

    except Exception as e:

        return f"Prediction Error: {e}"