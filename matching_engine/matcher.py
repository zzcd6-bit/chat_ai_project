from matching_engine.classifier_model import predict_match_bidirectional

def hard_filter(user, candidate):
    """
    Perform hard filtering based on user's required_fields settings
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
    Return a list of candidates sorted by AI-predicted match score (includes User objects)
    """
    results = []
    for candidate in candidates:
        if candidate.name == user.name:
            continue
        if not hard_filter(user, candidate):
            continue
        try:
            score = predict_match_bidirectional(user, candidate)
            results.append((candidate, score))  # ✅ Return User object
        except Exception as e:
            print(f"Error matching {candidate.name}: {e}")

    results.sort(key=lambda x: x[1], reverse=True)
    return results
