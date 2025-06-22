import numpy as np
from itertools import combinations

TRAIT_CODES = ['O', 'C', 'E', 'A', 'N']

def compute_weighted_vector(raw_scores: dict, weights: dict) -> np.ndarray:
    return np.array([raw_scores[t] * weights[t] for t in TRAIT_CODES], dtype=float)

def cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    num = np.dot(u, v)
    den = np.linalg.norm(u) * np.linalg.norm(v)
    return num / den if den != 0 else 0.0

def bidirectional_cosine(u: np.ndarray, v: np.ndarray) -> float:
    return (cosine_similarity(u, v) + cosine_similarity(v, u)) / 2

def match_personality(user1, user2) -> float:
    p1 = dict(zip(TRAIT_CODES, user1.personality))
    p2 = dict(zip(TRAIT_CODES, user2.ideal_profile["preferred_personality"]))

    weights1 = {t: 1.0 for t in TRAIT_CODES}
    weights2 = {t: 1.0 for t in TRAIT_CODES}

    vec1 = compute_weighted_vector(p1, weights1)
    vec2 = compute_weighted_vector(p2, weights2)

    return bidirectional_cosine(vec1, vec2)
