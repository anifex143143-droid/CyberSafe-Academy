import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib


# Training data
data = {
    "security_score": [
        95, 90, 88, 85, 82,
        80, 78, 75, 72, 70,
        68, 65, 62, 60, 58,
        55, 52, 50, 48, 45,
        42, 40, 38, 35, 30,
        25, 20
    ],

    "quiz_accuracy": [
        98, 92, 85, 90, 75,
        88, 70, 82, 65, 78,
        72, 68, 80, 60, 55,
        65, 50, 58, 45, 52,
        40, 48, 35, 30, 25,
        20, 15
    ],

    "mission_accuracy": [
        95, 88, 92, 78, 85,
        75, 82, 70, 60, 72,
        65, 55, 75, 58, 50,
        62, 45, 55, 40, 48,
        35, 42, 30, 25, 35,
        20, 15
    ],

    "learning_percentage": [
        100, 90, 95, 80, 85,
        75, 90, 70, 60, 80,
        65, 55, 75, 50, 60,
        70, 45, 55, 40, 50,
        35, 30, 25, 40, 20,
        15, 10
    ],

    "risk": [
        "Low", "Low", "Low", "Low", "Low",
        "Low", "Low", "Low", "Low", "Low",
        "Medium", "Medium", "Medium", "Medium", "Medium",
        "Medium", "Medium", "Medium", "Medium", "Medium",
        "High", "High", "High", "High", "High",
        "High", "High"
    ]
}



df = pd.DataFrame(data)


# Features
X = df[
    [
        "security_score",
        "quiz_accuracy",
        "mission_accuracy",
        "learning_percentage"
    ]
]


# Target
y = df["risk"]


# Create ML model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# Train model
model.fit(X, y)


# Save trained model
joblib.dump(
    model,
    "ml/risk_model.pkl"
)


print("ML risk prediction model trained successfully.")