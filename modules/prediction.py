import pickle
import os
import numpy as np


print("NEW PREDICTION FILE LOADED")
# -----------------------------------
# BASE DIRECTORY
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------------
# MODEL PATH
# -----------------------------------

model_path = os.path.join(
    BASE_DIR,
    "..",
    "models",
    "risk_model.pkl"
)

print("MODEL PATH:", model_path)
print("MODEL EXISTS:", os.path.exists(model_path))

# -----------------------------------
# LOAD MODEL
# -----------------------------------

model = None

try:

    if os.path.exists(model_path):

        with open(model_path, "rb") as file:
            model = pickle.load(file)

        print("MODEL LOADED SUCCESSFULLY")

    else:
        print("MODEL FILE NOT FOUND")

except Exception as e:

    print("MODEL LOADING ERROR:", e)

# -----------------------------------
# PREDICTION FUNCTION
# -----------------------------------

def predict_risk(attendance, internal, participation, absences, gpa):

    if model is None:
        return "Model not loaded"

    data = np.array([
        [attendance, internal, participation, absences, gpa]
    ])

    prediction = model.predict(data)

    return prediction[0]