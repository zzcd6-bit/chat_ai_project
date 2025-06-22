from .reply_db import reply_db
from .classifier import classify_topic
from .semantic_ranker import semantic_rank

def suggest_reply(user_msg):
    topic = classify_topic(user_msg)

    # Retrieve candidate replies, check whether it's a function
    entry = reply_db[topic]
    if callable(entry):  # If it's a function
        candidates = entry(user_msg)  # Call the function with user input
    else:
        candidates = entry  # Static reply list

    return semantic_rank(user_msg, candidates)
