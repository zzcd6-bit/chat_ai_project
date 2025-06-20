import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor  
from matching_engine.vectorizer import build_feature_vector

# 模型保存路径
MODEL_PATH = os.path.join(os.path.dirname(__file__), "match_model.pkl")

def train_model(X, y):
    """训练回归模型并保存"""
    reg = RandomForestRegressor(n_estimators=100, random_state=42)
    reg.fit(X, y)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(reg, f)
    print("[✔] 模型已保存至", MODEL_PATH)

def predict_match_bidirectional(user, candidate):
    """双向预测匹配度（百分比形式）"""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("未找到模型，请先运行 train_classifier.py")

    with open(MODEL_PATH, "rb") as f:
        reg = pickle.load(f)

    # user → candidate
    X1 = build_feature_vector(user, candidate)
    score1 = reg.predict([X1])[0]

    # candidate → user
    X2 = build_feature_vector(candidate, user)
    score2 = reg.predict([X2])[0]

    # 平均匹配度（限制在 0~1）
    avg_score = max(0.0, min((score1 + score2) / 2, 1.0))
    return round(avg_score * 100, 2)  # 转换为百分比

def load_trained_model():
    """加载训练好的回归模型"""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("未找到模型文件，请先训练模型。")
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)
