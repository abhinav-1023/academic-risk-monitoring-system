import pandas as pd
import numpy as np
import pickle

from sklearn.metrics import confusion_matrix

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Generate Synthetic Dataset


np.random.seed(42)

n_samples = 500

attendance = np.random.randint(40, 100, n_samples)
internal = np.random.randint(5, 25, n_samples)
participation = np.random.randint(1, 10, n_samples)
absences = np.random.randint(0, 15, n_samples)
gpa = np.round(np.random.uniform(5, 9.5, n_samples), 2)

risk = []

for i in range(n_samples):

    score = 0

    if attendance[i] < 60:
        score += 2

    if internal[i] < 12:
        score += 2

    if participation[i] < 4:
        score += 1

    if absences[i] > 8:
        score += 2

    if gpa[i] < 6.5:
        score += 2

    # small noise (not too much)
    score += np.random.randint(-1, 1)

    if score >= 5:
        risk.append("High")
    elif score >= 3:
        risk.append("Medium")
    else:
        risk.append("Low")


df = pd.DataFrame({
    "attendance": attendance,
    "internal": internal,
    "participation": participation,
    "absences": absences,
    "gpa": gpa,
    "risk": risk
})

# Save dataset
df.to_csv("data/synthetic_student_data.csv", index=False)

print("Dataset saved")


# Train Model


X = df[["attendance","internal","participation","absences","gpa"]]
y = df["risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

model = RandomForestClassifier(
    n_estimators=60,
    max_depth=6,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", round(accuracy * 100, 2), "%")


cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix of Model",cm)

# Save Model


with open("models/risk_model.pkl","wb") as f:
    pickle.dump(model,f)
print("Model saved")