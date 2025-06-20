# reply_engine/cvReply.py

import random
from typing import List  # ✅ 添加这一行

# 定义人类相关关键词（根据YOLO模型返回的类别名称）
HUMAN_KEYWORDS = {"person"}

# 可配置的夸“人”的语句
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

# 可配置的夸“物体/风景/非人类”的语句
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

def generate_cv_replies(detected_types: List[str], n: int = 5) -> List[str]:  # ✅ 替换 list[str]
    """
    根据图像识别类型返回 n 条风格多样的 CV 自动回复
    - 如果有人类（"person"），返回人类回复
    - 否则返回带主语（检测类型）的物体回复变体
    """
    lower_types = [t.lower() for t in detected_types]

    if any(t in HUMAN_KEYWORDS for t in lower_types):
        pool = HUMAN_REPLIES
        return random.sample(pool, min(n, len(pool)))

    # 非人类情况处理：
    # 1. 随机基础回复
    pool = [s for s in OBJECT_REPLIES if s.strip()]
    base_replies = random.sample(pool, min(n // 2, len(pool)))

    # 2. 每个物体生成主语句式（取最多 n 条）
    subject_replies = []
    templates = [
        "The {obj} looks great!",
        "That {obj} is awesome!",
        "The {obj} seems really cool!",
        "That {obj} looks perfect!",
        "Such a nice {obj}!"
    ]
    for obj in lower_types:
        for t in random.sample(templates, k=1):  # 每个物体一句
            subject_replies.append(t.format(obj=obj))
            if len(subject_replies) >= n:
                break
        if len(subject_replies) >= n:
            break

    # 3. 合并两种风格回复并截断到 n 条
    all_replies = base_replies + subject_replies
    return all_replies[:n]
