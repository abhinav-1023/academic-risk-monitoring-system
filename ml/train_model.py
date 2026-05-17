import pandas as pd
import numpy as np
import os
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

# -----------------------------------
# CREATE REQUIRED FOLDERS
# -----------------------------------

os.makedirs("data", exist_ok=True)

os.makedirs("models", exist_ok=True)

# -----------------------------------
# RANDOM SEED
# -----------------------------------

np.random.seed(42)

# -----------------------------------
# NUMBER OF SAMPLES
# -----------------------------------

n_samples = 3000

# -----------------------------------
# GENERATE SYNTHETIC FEATURES
# -----------------------------------

attendance = np.random.randint(
    40,
    100,
    n_samples
)

internal = np.random.randint(
    5,
    25,
    n_samples
)

# Participation correlated with attendance

participation = np.where(

    attendance > 75,

    np.random.randint(5, 10, n_samples),

    np.random.randint(1, 6, n_samples)
)

# Assignment correlated with internal

assignment = internal + np.random.randint(
    -5,
    5,
    n_samples
)

assignment = np.clip(
    assignment,
    0,
    25
)

# Quiz correlated with internal

quiz = internal + np.random.randint(
    -8,
    5,
    n_samples
)

quiz = np.clip(
    quiz,
    0,
    20
)

# Midsem correlated with internal

midsem = internal * 1.5 + np.random.randint(
    -10,
    10,
    n_samples
)

midsem = np.clip(
    midsem,
    0,
    40
)

# -----------------------------------
# GENERATE RISK LABELS
# -----------------------------------

risk = []

for i in range(n_samples):

    score = 0

    # Attendance

    if attendance[i] < 60:
        score += 2

    # Internal Marks

    if internal[i] < 12:
        score += 2

    # Participation

    if participation[i] < 4:
        score += 1

    # Assignment

    if assignment[i] < 10:
        score += 2

    # Quiz

    if quiz[i] < 8:
        score += 1

    # Midsem

    if midsem[i] < 18:
        score += 2

    # More randomness for realistic accuracy

    score += np.random.randint(-1, 3)

    # Final Risk Category

    if score >= 7:

        risk.append("High")

    elif score >= 4:

        risk.append("Medium")

    else:

        risk.append("Low")

# -----------------------------------
# CREATE DATAFRAME
# -----------------------------------

df = pd.DataFrame({

    "attendance": attendance,

    "internal": internal,

    "participation": participation,

    "assignment": assignment,

    "quiz": quiz,

    "midsem": midsem,

    "risk": risk
})

# -----------------------------------
# SAVE DATASET
# -----------------------------------

dataset_path = "data/synthetic_student_data.csv"

df.to_csv(
    dataset_path,
    index=False
)

print("Dataset saved successfully")

print("Dataset Path:", dataset_path)

# -----------------------------------
# TRAIN MODEL
# -----------------------------------

X = df[[
    "attendance",
    "internal",
    "participation",
    "assignment",
    "quiz",
    "midsem"
]]

y = df["risk"]

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.25,

    random_state=42
)

# -----------------------------------
# RANDOM FOREST MODEL
# -----------------------------------

model = RandomForestClassifier(

    n_estimators=120,

    max_depth=6,

    min_samples_split=5,

    min_samples_leaf=3,

    random_state=42
)

# -----------------------------------
# TRAIN MODEL
# -----------------------------------

model.fit(
    X_train,
    y_train
)

# -----------------------------------
# PREDICTION
# -----------------------------------

y_pred = model.predict(X_test)

# -----------------------------------
# ACCURACY
# -----------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)

print(
    "Model Accuracy:",
    round(accuracy * 100, 2),
    "%"
)

# -----------------------------------
# CONFUSION MATRIX
# -----------------------------------

cm = confusion_matrix(
    y_test,
    y_pred
)

print("Confusion Matrix:")

print(cm)

# -----------------------------------
# SAVE MODEL
# -----------------------------------

model_path = "models/risk_model.pkl"

joblib.dump(
    model,
    model_path
)

print("Model saved successfully")

print("Model Path:", model_path)