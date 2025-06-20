# user_model.py
class User:
    def __init__(self, name, age, gender, height, location, salary, language,
                 interests, personality,
                 preferred_gender, preferred_location, preferred_age_range,
                 preferred_salary_range, preferred_language,
                 preferred_interests, preferred_personality, preferred_height_range,
                 required_fields=None):

        self.name = name
        self.age = age
        self.gender = gender
        self.height = height
        self.location = location
        self.salary = salary
        self.language = language
        self.interests = interests  
        self.personality = personality  

        self.ideal_profile = {
            "preferred_gender": preferred_gender,
            "preferred_location": preferred_location,
            "preferred_age_range": preferred_age_range,
            "preferred_salary_range": preferred_salary_range,
            "preferred_language": preferred_language,
            "preferred_interests": preferred_interests,
            "preferred_personality": preferred_personality,
            "preferred_height_range": preferred_height_range
        }

        self.required_fields = required_fields or {
            "gender": False,
            "location": False,
            "age": False,
            "salary": False,
            "language": False,
            "height": False
        }

