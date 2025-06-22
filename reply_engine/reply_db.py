import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), r'D:\......\chat_ai_project\EmoGpt')))

# Then import the outer module
from EmoGpt.emoReply import generate_general_replies

# ===== Initialize reply_db =====
reply_db = {
    "travel": [
        "I wish I've been there. Do you like that?",
        "Beach towns are my favorite.",
        "I wish I could travel more.",
        "Please tell me more about traveling!",
        "I bet you have a good time there?",
        "I've been there too! Do you like that?",
        "Great! Please tell me more about that :)",
    ],
    "movies": [
        "I enjoy thrillers.",
        "Comedy movies make me laugh.",
        "Do you like horror films?",
        "I love a good movie night. What genre do you prefer?",
        "That sounds like a film worth watching!",
        "I’ve been meaning to catch up on some classics.",
        "Comedies always lift my mood. Got a favorite?",
        "Thrillers keep me on the edge of my seat!",
        "Are you more of a movie or TV series person?",
        "I wish I could go to the cinema more often."
    ],
    "food": [
        "That sounds delicious! Did you make it yourself?",
        "I could talk about food all day. What’s your favorite dish?",
        "Now I’m hungry just thinking about that.",
        "Homemade meals always hit different.",
        "Do you prefer sweet or savory snacks?",
        "Cooking can be so relaxing, don’t you think?",
        "Any good restaurants you’d recommend?",
        "Oh cool! Why do you prefer that?",
        "I love that special taste and good looking style!"
    ],
    "study": [
        "Studying can be exhausting—hang in there!",
        "What subject are you working on?",
        "I admire your dedication!",
        "Exams are tough, but you’ve got this.",
        "Sometimes the best study hack is a good rest.",
        "Is it a group project or solo work?",
        "I still have nightmares about late-night cramming!",
        "I'm cheering for you! Keep going!",
        "Oh dear darling you must have gone through a lot. I'm with you here.",
        "Wow that sounds like something. Anything you'd like to share with me?",
        "What a great job!! You really made it! Congratulations! :P",
        "You’ve got this babe. Just one more push."
    ],
    "work": [
        "Work can be such a grind, right?",
        "Hope your project’s going smoothly!",
        "Deadlines can be brutal, but you’ll get through it.",
        "Are you working from home or in the office?",
        "Sounds like a busy day—don’t forget to take breaks.",
        "I totally get that work stress feeling.",
        "What's your favorite part of your job?",
        "You’ve got this babe. Just one more push.",
        "How's the boss?",
        "Do you like your job now then?",
        "Work hard & earn more! Keep going :)",
        "Congratulations on your promotion!! I'm so proud of you omg :')"
    ],
    "music": [
        "Music really changes the vibe of the day.",
        "Got any good playlist recommendations?",
        "I love when a song perfectly matches my mood.",
        "Do you play any instruments?",
        "Nothing beats discovering a new favorite artist!",
        "Music is like therapy sometimes.",
        "What's your current go-to track?",
        "Lana Del Ray is my favorite musician.. who's your favorite?",
        "I can't live without music..",
        "O you're so talented! Wanna play one more for me ;)"
    ],
    "sports": [
        "Which team are you rooting for?",
        "Wow! Who do you like best?",
        "That match was intense!",
        "Playing sports is such a great stress reliever.",
        "Are you into watching or playing more?",
        "Sports bring people together, don’t they?",
        "I used to play basketball—miss those days!",
        "That goal was legendary!",
        "Luka Modric is my favorite player in football!! All of the players running deserve the same respect though.",
        "Wow that's so exciting! I'm sweating already..",
        "Tennis is really a great sport!",
        "Basketball is really a great sport!",
        "Football is really a great sport!",
        "What a goal! How wonderful!"
    ],
    "weather": [
        "Rainy days make me want to stay in bed.",
        "Sunny weather just lifts the mood!",
        "Is it cold where you are?",
        "I hope the storm passes soon.",
        "Perfect weather for a walk, don’t you think?",
        "Don’t forget your umbrella!",
        "The weather’s been so unpredictable lately.",
        "However the weather is, keep yourself optimistic though ;)"
    ],

    "general": generate_general_replies  # 👈 Dynamically generated, auto-fills 15 replies
}
