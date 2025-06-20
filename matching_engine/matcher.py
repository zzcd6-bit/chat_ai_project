# matcher.py
from matching_engine.classifier_model import predict_match_bidirectional

def hard_filter(user, candidate):
    """
    根据用户设定的 required_fields 进行软硬筛选
    """
    ideal = user.ideal_profile
    required = user.required_fields

    if required.get("gender", True):
        if ideal["preferred_gender"] != "any" and candidate.gender != ideal["preferred_gender"]:
            return False

    if required.get("location", True):
        if ideal["preferred_location"] != "any" and candidate.location != ideal["preferred_location"]:
            return False

    if required.get("age", True):
        if not (ideal["preferred_age_range"][0] <= candidate.age <= ideal["preferred_age_range"][1]):
            return False

    if required.get("salary", True):
        if not (ideal["preferred_salary_range"][0] <= candidate.salary <= ideal["preferred_salary_range"][1]):
            return False

    if required.get("language", True):
        if ideal["preferred_language"] != "any" and candidate.language != ideal["preferred_language"]:
            return False

    if required.get("height", True):
        if not (ideal["preferred_height_range"][0] <= candidate.height <= ideal["preferred_height_range"][1]):
            return False

    return True

def match_user(user, candidates):
    """
    返回按 AI 预测匹配度排序的候选人列表（包含 User 对象）
    """
    results = []
    for candidate in candidates:
        if candidate.name == user.name:
            continue
        if not hard_filter(user, candidate):
            continue
        try:
            score = predict_match_bidirectional(user, candidate)
            results.append((candidate, score))  # ✅ 返回 User 对象
        except Exception as e:
            print(f"匹配 {candidate.name} 时出错：{e}")

    results.sort(key=lambda x: x[1], reverse=True)
    return results

