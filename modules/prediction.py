import pickle
import os
import numpy as np

model_path = "models/risk_model.pkl"

if os.path.exists(model_path):
    model = pickle.load(open(model_path, "rb"))
else:
    model = None


def predict_risk(attendance, internal, participation, absences, gpa):

    if model is None:
        return "Model not loaded"

    data = np.array([[attendance, internal, participation, absences, gpa]])

    prediction = model.predict(data)

    return prediction[0]