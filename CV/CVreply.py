import random
from typing import List  # ✅ Added this line

# Define keywords related to humans (based on YOLO model labels)
HUMAN_KEYWORDS = {"person"}

# Configurable compliments for human-related images
HUMAN_REPLIES = [
    "You're stunning!",
    "Looking great!",
    "What a beautiful photo!",
    "Such a wonderful look!",
    "You look amazing :)",
    "Aww soo sweet",
    "They look absolutely amazing!",
    "Such a stylish look! Loove that"
]

# Configurable compliments for objects/scenery/non-human subjects
OBJECT_REPLIES = [
    "That's awesome!",
    "Nice scene!",
    "Looks great!",
    "Really cool!",
    "Awesome shot!",
    "OMG that's perfect!",
    "Really hope you like it",
    "That looks really nice XD",
    ""
]

def generate_cv_replies(detected_types: List[str], n: int = 5) -> List[str]:  # ✅ Replaced list[str]
    """
    Generate n diverse CV-based auto-replies based on detected object types
    - If humans are detected ("person"), return human compliments
    - Otherwise, generate replies based on object types with subject phrases
    """
    lower_types = [t.lower() for t in detected_types]

    if any(t in HUMAN_KEYWORDS for t in lower_types):
        pool = HUMAN_REPLIES
        return random.sample(pool, min(n, len(pool)))

    # Handle non-human case:
    # 1. Random base replies
    pool = [s for s in OBJECT_REPLIES if s.strip()]
    base_replies = random.sample(pool, min(n // 2, len(pool)))

    # 2. Generate subject-based replies for each object (up to n lines)
    subject_replies = []
    templates = [
        "The {obj} looks great!",
        "That {obj} is awesome!",
        "The {obj} seems really cool!",
        "That {obj} looks perfect!",
        "Such a nice {obj}!"
    ]
    for obj in lower_types:
        for t in random.sample(templates, k=1):  # One reply per object
            subject_replies.append(t.format(obj=obj))
            if len(subject_replies) >= n:
                break
        if len(subject_replies) >= n:
            break

    # 3. Combine both styles of replies and truncate to n responses
    all_replies = base_replies + subject_replies
    return all_replies[:n]
