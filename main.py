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
        msg = input("\n请输入一句聊天内容（输入 /imggui 打开图片界面，exit 返回主菜单）：")
        if msg.strip().lower() == "exit":
            return
        elif msg.strip().lower() == "/imggui":
            open_image_dialog()
            continue

        suggestions = suggest_reply(msg)
        print("\n💬 AI 推荐回复：")
        for s in suggestions:
            print("-", s)

def open_image_dialog():
    global selected_image_path
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.update()

    file_path = filedialog.askopenfilename(
        title="选择一张图片",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    root.destroy()

    if file_path:
        selected_image_path = file_path
        print("🖼️ Picture received：", selected_image_path)

        types = returntype(file_path)
        if types:
            print("🔍 检测到以下物体类型：", ", ".join(types))
            cv_replies = generate_cv_replies(types)
            print("🗨️ CV 自动回复推荐：")
            for reply in cv_replies:
                print("-", reply)
        else:
            print("⚠️ 未能识别出图像中的物体。")
    else:
        print("⚠️ 没有选择任何图片。")

def input_user():
    quick = input("\n是否使用测试数据快速输入？(yes/no)：").strip().lower()
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

        clear()
        print("✅ 使用测试数据成功，当前用户信息如下：")
        print("────────────────────")
        print("【基本信息】")
        print(f"姓名：{user.name}")
        print(f"年龄：{user.age}")
        print(f"性别：{user.gender}")
        print(f"身高：{user.height} cm")
        print(f"地区：{user.location}")
        print(f"薪资：{user.salary}")
        print(f"语言：{user.language}")
        print(f"兴趣：{', '.join(user.interests)}")
        print(f"性格：{user.personality}")
        print("────────────────────")
        print("【理想伴侣偏好】")
        print(f"性别偏好：{user.ideal_profile['preferred_gender']}")
        print(f"地区偏好：{user.ideal_profile['preferred_location']}")
        print(f"年龄范围偏好：{user.ideal_profile['preferred_age_range'][0]} - {user.ideal_profile['preferred_age_range'][1]} 岁")
        print(f"薪资范围偏好：{user.ideal_profile['preferred_salary_range'][0]} - {user.ideal_profile['preferred_salary_range'][1]}")
        print(f"语言偏好：{user.ideal_profile['preferred_language']}")
        print(f"兴趣偏好：{', '.join(user.ideal_profile['preferred_interests'])}")
        print(f"性格偏好：{user.ideal_profile['preferred_personality']}")
        print(f"身高范围偏好：{user.ideal_profile['preferred_height_range'][0]} - {user.ideal_profile['preferred_height_range'][1]} cm")
        print("────────────────────")
        input("按任意键开始匹配...")
        return user


    print("\n请输入你的个人信息：")
    name = input("名字：")
    age = int(input("年龄："))
    gender = input("性别（male/female）：")
    height = int(input("身高（cm）："))
    location = input("地区（如 KL）：")
    salary = int(input("薪资（整数）："))
    language = input("母语：")
    interests = input("兴趣（如 travel,music）：").split(",")
    personality = list(map(int, input("性格维度打分（如 4 3 5 2 1）：").split()))

    print("\n请输入你对理想对象的要求：")
    preferred_gender = input("理想性别（male/female/any）：")
    preferred_location = input("理想地区（或 any）：")
    preferred_age_range = list(map(int, input("理想年龄范围（如 20 28）：").split()))
    preferred_salary_range = list(map(int, input("理想薪资范围（如 3000 6000）：").split()))
    preferred_language = input("理想语言（或 any）：")
    preferred_height_range = list(map(int, input("理想身高范围（如 155 175）：").split()))
    preferred_interests = input("理想兴趣（如 music,reading）：").split(",")
    preferred_personality = list(map(int, input("理想性格（如 4 3 5 2 1）：").split()))

    required_fields = {}
    for field in ["gender", "location", "age", "salary", "language", "height"]:
        answer = input(f"{field} 是否必须满足？(yes/no)：").strip().lower()
        required_fields[field] = (answer == "yes")

    return User(
        name, age, gender, height, location, salary, language,
        interests, personality,
        preferred_gender, preferred_location, preferred_age_range,
        preferred_salary_range, preferred_language,
        preferred_interests, preferred_personality, preferred_height_range,
        required_fields=required_fields
    )

def run_matching():
    me = input_user()
    matches = match_user(me, sample_users)

    filtered = [(user, score) for user, score in matches if score > 0]
    filtered = sorted(filtered, key=lambda x: x[1], reverse=True)[:5]

    if not filtered:
        print("\n💘 匹配结果（AI 分类器预测）：暂无符合条件的对象。")
        input("\n按任意键返回主菜单...")
        return

    selected_index = 0

    while True:
        clear()
        print("💘 匹配结果（W/S 选择对象，Enter 查看详情，Q 返回主菜单）")
        print("────────────────────────────────────")
        for i, (user, score) in enumerate(filtered):
            prefix = ">>" if i == selected_index else "  "
            print(f"{prefix} {user.name}：匹配度 {score}%")
        print("────────────────────────────────────")

        key = msvcrt.getch()
        if key in [b'w', b'W'] and selected_index > 0:
            selected_index -= 1
        elif key in [b's', b'S'] and selected_index < len(filtered) - 1:
            selected_index += 1
        elif key in [b'q', b'Q']:
            return
        elif key == b'\r':  # Enter 键
            user, score = filtered[selected_index]
            clear()
            print("👤 匹配对象详细信息")
            print("────────────────────")
            print(f"姓名：{user.name}")
            print(f"年龄：{user.age}")
            print(f"性别：{user.gender}")
            print(f"身高：{user.height} cm")
            print(f"地区：{user.location}")
            print(f"薪资：{user.salary}")
            print(f"语言：{user.language}")
            print(f"兴趣：{', '.join(user.interests)}")
            print(f"性格：{user.personality}")
            print(f"❤️ 匹配度：{score}%")
            print("────────────────────")
            input("按任意键返回匹配列表...")

def display_menu(selected_index):
    options = ["聊天回复 + 图像识别", "匹配系统（AI 分类器预测）", "退出"]
    print("╔════════════════════════════════╗")
    print("║ 欢迎使用 AI 聊天 & 匹配系统 ║")
    print("╚════════════════════════════════╝\n")
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
        elif key == b'\r':  # 回车键
            clear()
            if selected == 0:
                chat_suggestion()
            elif selected == 1:
                run_matching()
            elif selected == 2:
                print("👋 再见！")
                sys.exit()

if __name__ == "__main__":
    main()
