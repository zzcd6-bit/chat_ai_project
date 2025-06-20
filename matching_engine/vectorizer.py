# vectorizer.py
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
# === 向量模型 + 小模型：只加载一次 ===
from sentence_transformers import SentenceTransformer
import joblib

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
import os
MODEL_PATH = os.path.join(os.path.dirname(__file__), "interest_model.pkl")
interest_clf = joblib.load(MODEL_PATH)


embedding_cache = {}

def get_embedding(text):
    if text not in embedding_cache:
        embedding_cache[text] = embedding_model.encode(text)
    return embedding_cache[text]

#性格匹配
def match_interest_set(set1, set2):
    matched = 0
    total = max(1, len(set(set1) | set(set2)))
    for i in set1:
        v1 = get_embedding(i)
        for j in set2:
            v2 = get_embedding(j)
            combined = np.concatenate([v1, v2]).reshape(1, -1)
            prob = interest_clf.predict_proba(combined)[0][1]
            if prob >= 0.7:
                matched += 1
                break
    return matched / total

def jaccard(set1, set2):
    return len(set1 & set2) / max(1, len(set1 | set2))

def build_feature_vector(user, candidate):
    # 数值型匹配：互相是否落在对方的理想范围内
    age_match_u2c = int(candidate.ideal_profile["preferred_age_range"][0] <= user.age <= candidate.ideal_profile["preferred_age_range"][1])
    age_match_c2u = int(user.ideal_profile["preferred_age_range"][0] <= candidate.age <= user.ideal_profile["preferred_age_range"][1])
    age_match = (age_match_u2c + age_match_c2u) / 2

    height_match_u2c = int(candidate.ideal_profile["preferred_height_range"][0] <= user.height <= candidate.ideal_profile["preferred_height_range"][1])
    height_match_c2u = int(user.ideal_profile["preferred_height_range"][0] <= candidate.height <= user.ideal_profile["preferred_height_range"][1])
    height_match = (height_match_u2c + height_match_c2u) / 2

    salary_match_u2c = int(candidate.ideal_profile["preferred_salary_range"][0] <= user.salary <= candidate.ideal_profile["preferred_salary_range"][1])
    salary_match_c2u = int(user.ideal_profile["preferred_salary_range"][0] <= candidate.salary <= user.ideal_profile["preferred_salary_range"][1])
    salary_match = (salary_match_u2c + salary_match_c2u) / 2

    # 类别型匹配（双向）
    lang_match = int(user.language == candidate.language)
    gender_match = int(user.ideal_profile["preferred_gender"] in ["any", candidate.gender]) and int(candidate.ideal_profile["preferred_gender"] in ["any", user.gender])
    location_match = int(user.ideal_profile["preferred_location"] in ["any", candidate.location]) and int(candidate.ideal_profile["preferred_location"] in ["any", user.location])

    # 性格匹配（双向余弦相似度）
    p1 = np.array(user.personality).reshape(1, -1)
    p2 = np.array(candidate.ideal_profile["preferred_personality"]).reshape(1, -1)
    sim1 = cosine_similarity(p1, p2)[0][0]

    p3 = np.array(candidate.personality).reshape(1, -1)
    p4 = np.array(user.ideal_profile["preferred_personality"]).reshape(1, -1)
    sim2 = cosine_similarity(p3, p4)[0][0]

    personality_score = (sim1 + sim2) / 2

    interest_score = match_interest_set(user.interests, candidate.interests)

    return [
        age_match,
        height_match,
        salary_match,
        lang_match,
        gender_match,
        location_match,
        interest_score,
        personality_score
    ]
