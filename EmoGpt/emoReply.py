from transformers import BertForSequenceClassification, BertTokenizerFast
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from typing import List, Tuple
import torch
import re

# ===== Path Configuration (can be moved to config.py if needed) =====
bert_path = r"C:\Users\zhongzhengchao\Desktop\chat_ai_project\EmoGpt\checkpoint-3412"
gpt2_path = r"C:\Users\zhongzhengchao\Desktop\chat_ai_project\EmoGpt\gpt2-3"

# ===== Load Emotion Recognition Model =====
bert_tokenizer = BertTokenizerFast.from_pretrained(bert_path)
bert_model = BertForSequenceClassification.from_pretrained(bert_path)
bert_model.eval()

id2label = {
    0: "content",
    1: "fear",
    2: "lonely",
    3: "negative",
    4: "positive",
    5: "sentimental"
}

# ===== Load GPT2 Model =====
gpt2_tokenizer = GPT2Tokenizer.from_pretrained(gpt2_path)
gpt2_tokenizer.pad_token = gpt2_tokenizer.eos_token
gpt2_model = GPT2LMHeadModel.from_pretrained(gpt2_path)

# ✅ Main Function: Accepts a user text and returns 15 semantically relevant replies
def generate_general_replies(user_text: str) -> Tuple[List[str], str]:
    # ===== Emotion Recognition =====
    with torch.no_grad():
        bert_inputs = bert_tokenizer(user_text, return_tensors="pt", truncation=True, padding=True)
        logits = bert_model(**bert_inputs).logits
        emotion_id = torch.argmax(logits, dim=1).item()
        emotion_label = id2label[emotion_id]

    print(f"🧠 Emotion recognition result: {emotion_label}")

    # ===== Construct Prompt and Generate Replies =====
    prompt = f"User ({emotion_label}): {user_text}\nAI:"
    input_ids = gpt2_tokenizer.encode(prompt, return_tensors="pt")

    outputs = gpt2_model.generate(
        input_ids,
        max_length=150,
        do_sample=True,
        top_k=150,
        top_p=0.92,
        temperature=0.9,
        num_return_sequences=20,
        pad_token_id=gpt2_tokenizer.eos_token_id
    )

    # ===== Clean and Deduplicate Generated Replies =====
    seen = set()
    replies = []

    for output in outputs:
        decoded = gpt2_tokenizer.decode(output, skip_special_tokens=True)

        # Try to extract using "Reply:" prefix (original approach)
        match = re.search(r"Reply:\s*(.*?)([\";}\\]|$)", decoded)
        if match:
            reply = match.group(1).strip()
        else:
            reply = decoded.split("AI:")[-1].strip()

        # Remove noisy characters
        reply = re.sub(r"[\n\r\"{}]", "", reply)

        # Deduplicate + ignore empty or too short replies
        if reply and reply not in seen and len(reply) > 3:
            seen.add(reply)
            replies.append(reply)

        if len(replies) >= 15:
            break

    return replies, emotion_label
