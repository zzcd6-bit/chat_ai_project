from matching_engine.classifier_model import train_model, load_trained_model
from matching_engine.vectorizer import build_feature_vector
from matching_engine.sample_users import sample_users

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# ---------- Construct training data (soft labels as regression targets) ----------
X = []
y = []

def compute_soft_score(user1, user2):
    interests1 = set(user1.interests)
    interests2 = set(user2.interests)
    pref1 = set(user1.ideal_profile["preferred_interests"])
    pref2 = set(user2.ideal_profile["preferred_interests"])
    score1 = len(interests1 & pref2) / max(1, len(interests1 | pref2))
    score2 = len(interests2 & pref1) / max(1, len(interests2 | pref1))
    interest_score = (score1 + score2) / 2
    diff1 = sum(abs(a - b) for a, b in zip(user1.personality, user2.ideal_profile["preferred_personality"]))
    diff2 = sum(abs(a - b) for a, b in zip(user2.personality, user1.ideal_profile["preferred_personality"]))
    personality_score = 1 - (diff1 + diff2) / 40 
    def range_match(u, c, key):
        low, high = c.ideal_profile[f"preferred_{key}_range"]
        return int(low <= getattr(u, key) <= high)
    age_match = (range_match(user1, user2, "age") + range_match(user2, user1, "age")) / 2
    height_match = (range_match(user1, user2, "height") + range_match(user2, user1, "height")) / 2
    salary_match = (range_match(user1, user2, "salary") + range_match(user2, user1, "salary")) / 2
    lang_match = int(user1.language == user2.language)
    gender_match = int(user1.ideal_profile["preferred_gender"] in ["any", user2.gender]) and int(user2.ideal_profile["preferred_gender"] in ["any", user1.gender])
    location_match = int(user1.ideal_profile["preferred_location"] in ["any", user2.location]) and int(user2.ideal_profile["preferred_location"] in ["any", user1.location])

    # ---------- Weighted combination (final score between 0~1) ----------
    soft_score = round(
        0.2 * interest_score +
        0.2 * personality_score +
        0.15 * age_match +
        0.15 * height_match +
        0.15 * salary_match +
        0.075 * lang_match +
        0.05 * gender_match +
        0.025 * location_match,
        3
    )

    return max(0.0, min(soft_score, 1.0))

# ---------- Generate pair samples ----------
for i in range(len(sample_users)):
    for j in range(len(sample_users)):
        if i == j:
            continue
        u1 = sample_users[i]
        u2 = sample_users[j]

        fv1 = build_feature_vector(u1, u2)
        fv2 = build_feature_vector(u2, u1)
        label1 = compute_soft_score(u1, u2)
        label2 = compute_soft_score(u2, u1)

        X.append(fv1)
        y.append(label1)
        X.append(fv2)
        y.append(label2)

# ---------- Split training and validation sets ----------
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"[✔] Number of training samples: {len(X_train)}")
print(f"[🧪] Number of validation samples: {len(X_val)}")

# ---------- Train the model ----------
train_model(X_train, y_train)

# ---------- Validate the model ----------
model = load_trained_model()
y_pred = model.predict(X_val)

mse = mean_squared_error(y_val, y_pred)
mae = mean_absolute_error(y_val, y_pred)
r2 = r2_score(y_val, y_pred)

print("\n[📊 Evaluation on Validation Set]")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"R² Score: {r2:.4f}")

# ---------- Visualization: Predicted vs Actual ----------
plt.figure(figsize=(6, 5))
plt.scatter(y_val, y_pred, alpha=0.6, color='teal')
plt.plot([0, 1], [0, 1], 'r--')
plt.xlabel("True Matching Score")
plt.ylabel("Predicted Matching Score")
plt.title("Predicted vs True Matching Scores")
plt.grid(True)
plt.tight_layout()
plt.show()

# ---------- Visualization: Error Distribution ----------
errors = [pred - true for pred, true in zip(y_pred, y_val)]
plt.figure(figsize=(6, 4))
plt.hist(errors, bins=30, color='orange', edgecolor='black', alpha=0.75)
plt.xlabel("Prediction Error")
plt.ylabel("Frequency")
plt.title("Prediction Error Distribution")
plt.grid(True)
plt.tight_layout()
plt.show()
