import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import SGDClassifier
import joblib
import os

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# 🟩 Get the current script directory
BASE_DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(BASE_DIR, "interest_model", "interest_pairs.json")
MODEL_PATH = os.path.join(BASE_DIR, "interest_model.pkl")
CLASSES = [0, 1]  # 0: Not Related, 1: Related

# Load sentence embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
embedding_cache = {}

def get_embedding(text):
    if text not in embedding_cache:
        embedding_cache[text] = embedding_model.encode(text)
    return embedding_cache[text]

# 🟩 Load interest pairs data
if not os.path.exists(JSON_PATH):
    raise FileNotFoundError(f"❌ Data file not found: {JSON_PATH}")
with open(JSON_PATH, "r", encoding="utf-8") as f:
    pairs = json.load(f)

# Build training samples
X, y = [], []
for w1, w2, label in pairs:
    v1 = get_embedding(w1)
    v2 = get_embedding(w2)
    combined = np.concatenate([v1, v2])
    X.append(combined)
    y.append(label)
X, y = np.array(X), np.array(y)

# 🟩 Initialize or load model
if os.path.exists(MODEL_PATH):
    clf = joblib.load(MODEL_PATH)
    print("✅ Loaded existing model. Starting incremental training...")
else:
    clf = SGDClassifier(loss="log_loss", max_iter=1000)
    clf.partial_fit(X[:1], y[:1], classes=CLASSES)
    print("🆕 Initialized new model...")

clf.partial_fit(X, y)

# Save model
joblib.dump(clf, MODEL_PATH)
print(f"✅ Model saved to {MODEL_PATH}")

# Evaluate model (on training set only)
y_pred = clf.predict(X)
acc = accuracy_score(y, y_pred)
prec = precision_score(y, y_pred)
rec = recall_score(y, y_pred)
f1 = f1_score(y, y_pred)

print("\n📊 Training Evaluation Results:")
print(f"Accuracy:  {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall:    {rec:.4f}")
print(f"F1 Score:  {f1:.4f}")

# Confusion Matrix Visualization
cm = confusion_matrix(y, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()
