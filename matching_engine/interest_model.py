# interest_model_incremental.py

import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import SGDClassifier
import joblib
import os

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# 加载/初始化兴趣模型
MODEL_PATH = "interest_model.pkl"
CLASSES = [0, 1]  # 0: 不相关，1: 相关

# 语义模型 & 缓存
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
embedding_cache = {}

def get_embedding(text):
    if text not in embedding_cache:
        embedding_cache[text] = embedding_model.encode(text)
    return embedding_cache[text]

# 加载兴趣对样本
with open("interest_pairs.json", "r", encoding="utf-8") as f:
    pairs = json.load(f)

X, y = [], []
for w1, w2, label in pairs:
    v1 = get_embedding(w1)
    v2 = get_embedding(w2)
    combined = np.concatenate([v1, v2])
    X.append(combined)
    y.append(label)

X, y = np.array(X), np.array(y)

# 如果已有模型，就加载继续训练；否则新建
if os.path.exists(MODEL_PATH):
    clf = joblib.load(MODEL_PATH)
    print("The old model has been loaded, ready for incremental training.")
else:
    clf = SGDClassifier(loss="log_loss", max_iter=1000)
    clf.partial_fit(X[:1], y[:1], classes=CLASSES)  # 初始化类别

# 增量训练（支持任意小批数据）
clf.partial_fit(X, y)

# 保存
joblib.dump(clf, MODEL_PATH)
print("Incremental training is complete, the model has been saved to interest_model.pkl.")

# 模型评估（只对训练集）
y_pred = clf.predict(X)

acc = accuracy_score(y, y_pred)
prec = precision_score(y, y_pred)
rec = recall_score(y, y_pred)
f1 = f1_score(y, y_pred)

print("\nThe result of the model evaluation is：")
print(f"Accuracy: {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall: {rec:.4f}")
print(f"F1 Score: {f1:.4f}")

# 可视化混淆矩阵
cm = confusion_matrix(y, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()





