import pickle
import numpy as np
import os

# -----------------------------------------
# Load Trained ML Model
# -----------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "..", "models", "risk_model.pkl")

model = pickle.load(open(model_path, "rb"))


# -----------------------------------------
# Prediction Function
# -----------------------------------------

def predict_risk(attendance, internal, participation, absences, gpa):

    """
    Predict student academic risk level.

    Parameters:
    attendance (float) - attendance percentage
    internal (float) - internal marks
    participation (float) - class participation score
    absences (int) - number of absences
    gpa (float) - previous semester GPA
    """

    # Convert inputs to numpy array
    data = np.array([
        [
            attendance,
            internal,
            participation,
            absences,
            gpa
        ]
    ])

    # Predict using trained model
    prediction = model.predict(data)

    # Return predicted class
    return prediction[0]