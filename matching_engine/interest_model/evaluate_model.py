import json
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sentence_transformers import SentenceTransformer
import joblib
import os

# Load trained model
clf = joblib.load("interest_model.pkl")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load evaluation data
with open("interest_pairs.json", "r", encoding="utf-8") as f:
    pairs = json.load(f)

X, y = [], []
for w1, w2, label in pairs:
    v1 = embedding_model.encode(w1)
    v2 = embedding_model.encode(w2)
    X.append(np.concatenate([v1, v2]))
    y.append(label)

X = np.array(X)
y_pred = clf.predict(X)

acc = accuracy_score(y, y_pred)
prec = precision_score(y, y_pred)
rec = recall_score(y, y_pred)
f1 = f1_score(y, y_pred)

print("Model Evaluation:")
print(f"Accuracy: {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall: {rec:.4f}")
print(f"F1 Score: {f1:.4f}")

# Confusion Matrix
cm = confusion_matrix(y, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()
