import numpy as np
from itertools import combinations

# 五大性格维度代码
TRAIT_CODES = ['O', 'C', 'E', 'A', 'N']

def compute_weighted_vector(raw_scores: dict, weights: dict) -> np.ndarray:
    """
    将每个维度的得分乘以对应权重，返回加权后的向量（用于余弦匹配）。
    """
    return np.array([raw_scores[t] * weights[t] for t in TRAIT_CODES], dtype=float)

def cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    """
    计算两个向量之间的余弦相似度。
    """
    num = np.dot(u, v)
    den = np.linalg.norm(u) * np.linalg.norm(v)
    return num / den if den != 0 else 0.0

def bidirectional_cosine(u: np.ndarray, v: np.ndarray) -> float:
    """
    计算双向余弦相似度：A对B、B对A 的平均值。
    """
    return (cosine_similarity(u, v) + cosine_similarity(v, u)) / 2

def match_personality(user1, user2) -> float:
    """
    比较 user1 与 user2 的性格匹配程度，考虑各自的 trait_weights。
    返回 0.0 ~ 1.0 的双向相似度分数。
    """
    # 转换双方 Big Five 为字典
    p1 = dict(zip(TRAIT_CODES, user1.personality))
    p2 = dict(zip(TRAIT_CODES, user2.ideal_profile["preferred_personality"]))

    # 获取各自的权重（如果没有，默认全为 1.0）
    weights1 = user1.ideal_profile.get("trait_weights", {t: 1.0 for t in TRAIT_CODES})
    weights2 = user2.ideal_profile.get("trait_weights", {t: 1.0 for t in TRAIT_CODES})

    # 加权向量
    vec1 = compute_weighted_vector(p1, weights1)
    vec2 = compute_weighted_vector(p2, weights2)

    return bidirectional_cosine(vec1, vec2)
