# reply_engine/suggester.py
'''
from .classifier import classify_topic
from .reply_db import reply_db
from .semantic_ranker import semantic_rank

def suggest_reply(user_msg):
    topic = classify_topic(user_msg)
    candidates = reply_db[topic]
    return semantic_rank(user_msg, candidates)

'''

from .reply_db import reply_db
from .classifier import classify_topic
from .semantic_ranker import semantic_rank


def suggest_reply(user_msg):
    topic = classify_topic(user_msg)

    # 取出候选回复，注意这里判断是否是函数
    entry = reply_db[topic]
    if callable(entry):  # 如果是函数
        candidates = entry(user_msg)  # 调用函数，传入用户输入
    else:
        candidates = entry  # 静态列表

    return semantic_rank(user_msg, candidates)
