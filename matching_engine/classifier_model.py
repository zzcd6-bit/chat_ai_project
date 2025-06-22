import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor  
from matching_engine.vectorizer import build_feature_vector

# Path to save the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "match_model.pkl")

def train_model(X, y):
    """Train the regression model and save it"""
    reg = RandomForestRegressor(n_estimators=100, random_state=42)
    reg.fit(X, y)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(reg, f)
    print("[✔] Model saved to", MODEL_PATH)

def predict_match_bidirectional(user, candidate):
    """Bidirectional prediction of match score (as percentage)"""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not found. Please run train_classifier.py first.")

    with open(MODEL_PATH, "rb") as f:
        reg = pickle.load(f)

    # user → candidate
    X1 = build_feature_vector(user, candidate)
    score1 = reg.predict([X1])[0]

    # candidate → user
    X2 = build_feature_vector(candidate, user)
    score2 = reg.predict([X2])[0]

    # Average score (clipped between 0 and 1)
    avg_score = max(0.0, min((score1 + score2) / 2, 1.0))
    return round(avg_score * 100, 2)  # Convert to percentage

def load_trained_model():
    """Load the trained regression model"""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model file not found. Please train the model first.")
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)
