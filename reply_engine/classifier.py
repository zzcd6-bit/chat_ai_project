# reply_engine/classifier.py

def classify_topic(message: str) -> str:
    msg = message.lower()

    if any(word in msg for word in ["travel", "trip", "vacation",  "flight", "beach", "abroad","destination"]):
        return "travel"
    elif any(word in msg for word in ["movie", "film", "cinema", "comedy", "theater"]):
        return "movies"
    elif any(word in msg for word in ["eat", "food",  "snack", "restaurant", "cook", "cuisine"]):
        return "food"
    elif any(word in msg for word in ["homework", "study", "exam", "school", "class", "lecture", "test"]):
        return "study"
    elif any(word in msg for word in ["work", "job", "project", "office", "meeting", "deadline", "promotion"]):
        return "work"
    elif any(word in msg for word in ["music", "song", "listen", "playlist", "guitar", "album", "singer"]):
        return "music"
    elif any(word in msg for word in ["sport", "game", "soccer", "basketball", "match", "tennis", "player", "goal"]):
        return "sports"
    elif any(word in msg for word in ["weather", "rain", "sunny", "cold", "hot", "windy", "storm"]):
        return "weather"
    else:
        return "general"

