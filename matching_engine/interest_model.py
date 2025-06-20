# interest_model_incremental.py

import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import SGDClassifier
import joblib
import os

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
    print("🔄 已加载旧模型，准备增量训练")
else:
    clf = SGDClassifier(loss="log_loss", max_iter=1000)
    clf.partial_fit(X[:1], y[:1], classes=CLASSES)  # 初始化类别

# 增量训练（支持任意小批数据）
clf.partial_fit(X, y)

# 保存
joblib.dump(clf, MODEL_PATH)
print("✅ 增量训练完成，模型已保存至 interest_model.pkl")




