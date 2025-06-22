import numpy as np
from itertools import combinations

# Big Five personality trait codes
TRAIT_CODES = ['O', 'C', 'E', 'A', 'N']

def compute_weighted_vector(raw_scores: dict, weights: dict) -> np.ndarray:
    """
    Multiply each trait score by its corresponding weight,
    and return the weighted vector (for cosine similarity).
    """
    return np.array([raw_scores[t] * weights[t] for t in TRAIT_CODES], dtype=float)

def cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.
    """
    num = np.dot(u, v)
    den = np.linalg.norm(u) * np.linalg.norm(v)
    return num / den if den != 0 else 0.0

def bidirectional_cosine(u: np.ndarray, v: np.ndarray) -> float:
    """
    Compute bidirectional cosine similarity:
    average of A-to-B and B-to-A.
    """
    return (cosine_similarity(u, v) + cosine_similarity(v, u)) / 2

def match_personality(user1, user2) -> float:
    """
    Compare personality matching between user1 and user2,
    considering their respective trait_weights.
    Returns a bidirectional similarity score between 0.0 and 1.0.
    """
    # Convert each user's Big Five scores to dictionaries
    p1 = dict(zip(TRAIT_CODES, user1.personality))
    p2 = dict(zip(TRAIT_CODES, user2.ideal_profile["preferred_personality"]))

    # Retrieve each user's trait weights (default to 1.0 if not specified)
    weights1 = user1.ideal_profile.get("trait_weights", {t: 1.0 for t in TRAIT_CODES})
    weights2 = user2.ideal_profile.get("trait_weights", {t: 1.0 for t in TRAIT_CODES})

    # Compute weighted vectors
    vec1 = compute_weighted_vector(p1, weights1)
    vec2 = compute_weighted_vector(p2, weights2)

    return bidirectional_cosine(vec1, vec2)
