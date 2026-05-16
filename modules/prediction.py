import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier

# -----------------------------------
# BASE DIRECTORY
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dataset_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "student_performance_dataset.csv"
)

# -----------------------------------
# TRAIN MODEL DIRECTLY
# -----------------------------------

df = pd.read_csv(dataset_path)

X = df[[
    "attendance",
    "internal",
    "participation",
    "absences",
    "gpa"
]]

y = df["risk"]

model = RandomForestClassifier()

model.fit(X, y)

# -----------------------------------
# PREDICTION FUNCTION
# -----------------------------------

def predict_risk(attendance, internal, participation, absences, gpa):

    data = [[
        attendance,
        internal,
        participation,
        absences,
        gpa
    ]]

    prediction = model.predict(data)

    return prediction[0]