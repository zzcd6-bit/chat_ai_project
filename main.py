import os
import sys
import msvcrt
from tkinter import Tk, filedialog

from reply_engine.suggester import suggest_reply
from matching_engine.user_model import User
from matching_engine.sample_users import sample_users
from matching_engine.matcher import match_user
from CV.ImageRecognition import returntype
from CV.CVreply import generate_cv_replies

selected_image_path = None

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def chat_suggestion():
    while True:
        msg = input("\nPlease enter a message (type /imggui to open image interface, exit to return to main menu):")
        if msg.strip().lower() == "exit":
            return
        elif msg.strip().lower() == "/imggui":
            open_image_dialog()
            continue

        suggestions = suggest_reply(msg)
        print("\n💬 AI Recommended Replies:")
        for s in suggestions:
            print("-", s)

def open_image_dialog():
    global selected_image_path
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.update()

    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    root.destroy()

    if file_path:
        selected_image_path = file_path
        print("🖼️ Picture received:", selected_image_path)

        types = returntype(file_path)
        if types:
            print("🔍 Detected object types:", ", ".join(types))
            cv_replies = generate_cv_replies(types)
            print("🗨️ CV Auto-generated Replies:")
            for reply in cv_replies:
                print("-", reply)
        else:
            print("⚠️ Unable to recognize objects in the image.")
    else:
        print("⚠️ No image was selected.")

def input_user():
    quick = input("\nUse test data for quick input? (yes/no):").strip().lower()
    if quick == "yes":
        user = User(
            name='Liu Yin',
            age=21,
            gender='male',
            height=174,
            location='Ipoh', 
            salary=6964,
            language='Chinese',
            interests=['movies', 'sports', 'music'],
            personality=[4, 1, 4, 3, 2],
            preferred_gender='female',
            preferred_location='Johor',
            preferred_age_range=[19, 27],
            preferred_salary_range=[4893, 6453],
            preferred_language='Chinese',
            preferred_interests=['movies', 'music'],
            preferred_personality=[2, 1, 4, 2, 5],
            preferred_height_range=[160, 172],
            required_fields={
                "gender": True, "location": False, "age": True,
                "salary": False, "language": True, "height": False
            }
        )

        user.ideal_profile["trait_weights"] = {'O': 1.0, 'C': 1.0, 'E': 1.0, 'A': 1.0, 'N': 1.0}

        clear()
        print("✅ Test data loaded successfully. Current user info:")
        print("──────────────────────────")
        print("【Basic Info】")
        print(f"Name: {user.name}")
        print(f"Age: {user.age}")
        print(f"Gender: {user.gender}")
        print(f"Height: {user.height} cm")
        print(f"Location: {user.location}")
        print(f"Salary: {user.salary}")
        print(f"Language: {user.language}")
        print(f"Interests: {', '.join(user.interests)}")
        print(f"Personality: {user.personality}")
        print("──────────────────────────")
        print("【Ideal Partner Preferences】")
        print(f"Preferred Gender: {user.ideal_profile['preferred_gender']}")
        print(f"Preferred Location: {user.ideal_profile['preferred_location']}")
        print(f"Preferred Age Range: {user.ideal_profile['preferred_age_range'][0]} - {user.ideal_profile['preferred_age_range'][1]} years")
        print(f"Preferred Salary Range: {user.ideal_profile['preferred_salary_range'][0]} - {user.ideal_profile['preferred_salary_range'][1]}")
        print(f"Preferred Language: {user.ideal_profile['preferred_language']}")
        print(f"Preferred Interests: {', '.join(user.ideal_profile['preferred_interests'])}")
        print(f"Preferred Personality: {user.ideal_profile['preferred_personality']}")
        print(f"Preferred Height Range: {user.ideal_profile['preferred_height_range'][0]} - {user.ideal_profile['preferred_height_range'][1]} cm")
        print(f"Trait Weights: {user.ideal_profile['trait_weights']}")
        print("──────────────────────────")
        input("Press any key to start matching...")
        return user

    print("\nPlease enter your personal information:")
    name = input("Name: ")
    age = int(input("Age: "))
    gender = input("Gender (male/female): ")
    height = int(input("Height (cm): "))
    location = input("Location (e.g. KL): ")
    salary = int(input("Salary (integer): "))
    language = input("Mother Tongue: ")
    interests = input("Interests (e.g. travel,music):").split(",")

    print("\nRate your Big Five personality traits (1–5):")
    print("O: Openness, C: Conscientiousness, E: Extraversion, A: Agreeableness, N: Neuroticism")
    while True:
        raw = input("Enter five numbers (space-separated):").strip()
        try:
            personality = list(map(int, raw.split()))
            if len(personality) == 5 and all(1 <= x <= 5 for x in personality):
                break
        except:
            pass
        print("❌ Invalid format. Please try again.")

    print("\nPlease enter your ideal partner preferences:")
    preferred_gender = input("Preferred Gender (male/female/any): ")
    preferred_location = input("Preferred Location (or any): ")
    preferred_age_range = list(map(int, input("Preferred Age Range (e.g. 20 28): ").split()))
    preferred_salary_range = list(map(int, input("Preferred Salary Range (e.g. 3000 6000): ").split()))
    preferred_language = input("Preferred Language (or any): ")
    preferred_height_range = list(map(int, input("Preferred Height Range (e.g. 155 175): ").split()))
    preferred_interests = input("Preferred Interests (e.g. music,reading):").split(",")

    print("\nRate your ideal partner’s Big Five personality (1–5):")
    while True:
        raw = input("Enter five numbers (space-separated):").strip()
        try:
            preferred_personality = list(map(int, raw.split()))
            if len(preferred_personality) == 5 and all(1 <= x <= 5 for x in preferred_personality):
                break
        except:
            pass
        print("❌ Invalid format. Please try again.")

    trait_codes = ['O', 'C', 'E', 'A', 'N']
    trait_names = {
        'O': 'Openness',
        'C': 'Conscientiousness',
        'E': 'Extraversion',
        'A': 'Agreeableness',
        'N': 'Neuroticism'
    }
    trait_weights = {}
    print("\nSet trait weights for your ideal partner (0.0–1.0, higher = more important):")
    for t in trait_codes:
        while True:
            val = input(f"  Weight {t} - {trait_names[t]}:").strip()
            try:
                weight = float(val)
                if 0 < weight <= 1.0:
                    trait_weights[t] = weight
                    break
            except:
                pass
            print("❌ Please enter a valid number (range: 0.0–1.0, non-zero).")

    required_fields = {}
    for field in ["gender", "location", "age", "salary", "language", "height"]:
        answer = input(f"Is {field} required? (yes/no):").strip().lower()
        required_fields[field] = (answer == "yes")

    user = User(
        name, age, gender, height, location, salary, language,
        interests, personality,
        preferred_gender, preferred_location, preferred_age_range,
        preferred_salary_range, preferred_language,
        preferred_interests, preferred_personality, preferred_height_range,
        required_fields=required_fields
    )
    user.ideal_profile["trait_weights"] = trait_weights

    order = ['O', 'C', 'E', 'A', 'N']
    weighted_vector = {
        t: user.ideal_profile['preferred_personality'][i] * user.ideal_profile['trait_weights'][t]
        for i, t in enumerate(order)
    }

    print("\nWeighted Personality Preference Vector:")
    for t in order:
        print(f"  {t}: {weighted_vector[t]:.2f}")

    return user

def run_matching():
    me = input_user()
    matches = match_user(me, sample_users)

    filtered = [(user, score) for user, score in matches if score > 0]
    filtered = sorted(filtered, key=lambda x: x[1], reverse=True)[:5]

    if not filtered:
        print("\n💘 Match Results (AI Classifier Prediction): No suitable match found.")
        input("\nPress any key to return to the main menu...")
        return

    selected_index = 0

    while True:
        clear()
        print("💘 Match Results (Use W/S to navigate, Enter to view details, Q to return to menu)")
        print("────────────────────────────────────")
        for i, (user, score) in enumerate(filtered):
            prefix = ">>" if i == selected_index else "  "
            print(f"{prefix} {user.name}: Match Score {score}%")
        print("────────────────────────────────────")

        key = msvcrt.getch()
        if key in [b'w', b'W'] and selected_index > 0:
            selected_index -= 1
        elif key in [b's', b'S'] and selected_index < len(filtered) - 1:
            selected_index += 1
        elif key in [b'q', b'Q']:
            return
        elif key == b'\r':  # Enter key
            user, score = filtered[selected_index]
            clear()
            print("👤 Match Detail")
            print("────────────────────")
            print(f"Name: {user.name}")
            print(f"Age: {user.age}")
            print(f"Gender: {user.gender}")
            print(f"Height: {user.height} cm")
            print(f"Location: {user.location}")
            print(f"Salary: {user.salary}")
            print(f"Language: {user.language}")
            print(f"Interests: {', '.join(user.interests)}")
            print(f"Personality: {user.personality}")
            print(f"❤️ Match Score: {score}%")
            print("────────────────────")
            input("Press any key to return to the list...")

def display_menu(selected_index):
    options = ["Chat Reply + Image Recognition", "Matching System (AI Classifier Prediction)", "Exit"]
    print("╔═══════════════════════════════════════╗")
    print("║ Welcome to the AI Chat & Match System ║")
    print("╚═══════════════════════════════════════╝\n")
    for i, option in enumerate(options):
        if i == selected_index:
            print(f"👉 >> {option} <<")
        else:
            print(f"   {option}")

def main():
    selected = 0
    while True:
        clear()
        display_menu(selected)
        key = msvcrt.getch()
        if key in [b'w', b'W'] and selected > 0:
            selected -= 1
        elif key in [b's', b'S'] and selected < 2:
            selected += 1
        elif key == b'\r':  # Enter key
            clear()
            if selected == 0:
                chat_suggestion()
            elif selected == 1:
                run_matching()
            elif selected == 2:
                print("👋 Goodbye!")
                sys.exit()

if __name__ == "__main__":
    main()
