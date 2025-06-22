
# 💘 AI Matching System – README

This repository implements an intelligent matching system combining user traits, interests, personality, and emotional intelligence. It integrates:

- ✨ Interest classification (SGD classifier with sentence embeddings)  
- 🧠 Semantic scoring (sentence-transformers)  
- 🤖 GPT2-based emotional reply generation  
- 🧍 YOLO-based image recognition  

---

## 📦 Installation

1. **Clone this repository**
   ```bash
   git clone <your-repo-url>
   cd chat_ai_project
   ```

2. **Install dependencies**
   Create a virtual environment (recommended) and install:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Required Model Files**
   You **must** manually download and place these model files:

   | File Name           | Destination Directory    | Purpose                      |
   |---------------------|--------------------------|-------------------------------|
   | `optimizer.pt`      | `EmoGpt/`                | GPT2 optimizer checkpoint     |
   | `pytorch_model.bin` | `EmoGpt/`                | BERT or GPT2 weights          |
   | `model.safetensors` | `EmoGpt/gpt2-3/`         | GPT2 model in safetensors     |

   Additionally, YOLOv8 is provided in `CV/yolov8n.pt`.

---

## 🧠 Train the Matching Classifier

Run the following script to train the interest relationship model using labeled data:

```bash
python matching_engine/train_classifier.py
```

This generates `interest_model.pkl` for relationship classification.

---

## ▶️ Run the Matching System

Launch the core interaction system:

```bash
python main.py
```

You may interact with user modeling, interest comparison, visual recognition, and AI reply.

---

## 🧱 Project Structure

```
matching_engine/
├── classifier_model.py       # Trait/interest classification logic
├── matcher.py                # Matching logic and scoring
├── sample_users.py           # Generate test users
├── train_classifier.py       # Train interest classifier
├── user_model.py             # User attribute schema
├── vectorizer.py             # Vectorizes user features
├── database/                 # Sample user profiles by race/gender
│   ├── male_Chinese.py
│   └── ...
├── interest_model/           # Interest relationship model
│   ├── interest_model.py
│   ├── evaluate_model.py
│   └── interest_pairs.json

reply_engine/
├── suggester.py              # Central reply logic
├── classifier.py             # Topic classifier
├── reply_db.py               # Stores replies
├── semantic_ranker.py        # Ranks reply candidates via embeddings

CV/
├── ImageRecognition.py       # YOLO image detection
├── CVreply.py                # Reply based on image labels
├── yolov8n.pt                # YOLOv8 model weights

EmoGpt/
├── emoReply.py               # BERT judge + GPT2 generate
├── checkpoint-3412/          # BERT classifier checkpoint
├── gpt2-3/                   # GPT2 generator model

main.py                       # Entry point
```

---

## 💡 Notes

- `sentence-transformers` will auto-download `all-MiniLM-L6-v2` on first run.
- Make sure GPU acceleration is available for optimal GPT2 and YOLO performance.
- The system is modular — you can use only the matching engine, or integrate with GPT, CV, or GUI.
