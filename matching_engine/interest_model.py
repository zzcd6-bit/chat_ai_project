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

# 🟩 获取当前脚本所在目录
BASE_DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(BASE_DIR, "interest_model", "interest_pairs.json")
MODEL_PATH = os.path.join(BASE_DIR, "interest_model.pkl")
CLASSES = [0, 1]  # 0: 不相关，1: 相关

# 加载语义模型
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
embedding_cache = {}

def get_embedding(text):
    if text not in embedding_cache:
        embedding_cache[text] = embedding_model.encode(text)
    return embedding_cache[text]

# 🟩 加载兴趣对数据
if not os.path.exists(JSON_PATH):
    raise FileNotFoundError(f"❌ 找不到数据文件：{JSON_PATH}")
with open(JSON_PATH, "r", encoding="utf-8") as f:
    pairs = json.load(f)

# 构造样本
X, y = [], []
for w1, w2, label in pairs:
    v1 = get_embedding(w1)
    v2 = get_embedding(w2)
    combined = np.concatenate([v1, v2])
    X.append(combined)
    y.append(label)
X, y = np.array(X), np.array(y)

# 🟩 初始化/加载模型
if os.path.exists(MODEL_PATH):
    clf = joblib.load(MODEL_PATH)
    print("✅ 已加载旧模型，开始增量训练...")
else:
    clf = SGDClassifier(loss="log_loss", max_iter=1000)
    clf.partial_fit(X[:1], y[:1], classes=CLASSES)
    print("🆕 已初始化新模型...")

clf.partial_fit(X, y)

# 保存模型
joblib.dump(clf, MODEL_PATH)
print(f"✅ 模型已保存至 {MODEL_PATH}")

# 模型评估（仅训练集）
y_pred = clf.predict(X)
acc = accuracy_score(y, y_pred)
prec = precision_score(y, y_pred)
rec = recall_score(y, y_pred)
f1 = f1_score(y, y_pred)

print("\n📊 模型训练结果：")
print(f"Accuracy:  {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall:    {rec:.4f}")
print(f"F1 Score:  {f1:.4f}")

# 混淆矩阵可视化
cm = confusion_matrix(y, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()
