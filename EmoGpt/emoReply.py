from transformers import BertForSequenceClassification, BertTokenizerFast
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from typing import List, Tuple
import torch
import re

# ===== 路径配置（你可以视需要外置到 config.py）=====
bert_path = r"C:\Users\zhongzhengchao\Desktop\chat_ai_project\EmoGpt\checkpoint-3412"
gpt2_path = r"C:\Users\zhongzhengchao\Desktop\chat_ai_project\EmoGpt\gpt2-3"

# ===== 加载情绪识别模型 =====
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

# ===== 加载 GPT2 模型 =====
gpt2_tokenizer = GPT2Tokenizer.from_pretrained(gpt2_path)
gpt2_tokenizer.pad_token = gpt2_tokenizer.eos_token
gpt2_model = GPT2LMHeadModel.from_pretrained(gpt2_path)

# ✅ 主函数：接受一段用户文本，返回 15 条语义相关回复
#def generate_general_replies(user_text: str = "No one messages me anymore..") -> list[str]:
def generate_general_replies(user_text: str) -> Tuple[List[str], str]:
    # ===== 情绪识别 =====
    with torch.no_grad():
        bert_inputs = bert_tokenizer(user_text, return_tensors="pt", truncation=True, padding=True)
        logits = bert_model(**bert_inputs).logits
        emotion_id = torch.argmax(logits, dim=1).item()
        emotion_label = id2label[emotion_id]

    print(f"🧠 Emotion recognition results：{emotion_label}")
    # ===== 构造 Prompt 并生成回复 =====
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

    # ===== 清洗与去重回复文本 =====
    seen = set()
    replies = []

    for output in outputs:
        decoded = gpt2_tokenizer.decode(output, skip_special_tokens=True)

        # 尝试用 “Reply:” 提取（你原来的方法）
        match = re.search(r"Reply:\s*(.*?)([\";}\\]|$)", decoded)
        if match:
            reply = match.group(1).strip()
        else:
            reply = decoded.split("AI:")[-1].strip()

        # 清除杂字符
        reply = re.sub(r"[\n\r\"{}]", "", reply)

        # 去重 + 非空
        if reply and reply not in seen and len(reply) > 3:
            seen.add(reply)
            replies.append(reply)

        if len(replies) >= 15:
            break

    return replies
