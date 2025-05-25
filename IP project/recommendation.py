

import logging


# Logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PersonalizedDietRecommendation:
    def __init__(self, height, weight, age, gender, activity_level):
        self.height = height
        self.weight = weight
        self.age = age
        self.gender = gender.lower()
        self.activity_level = activity_level.lower()

    def calculate_bmr(self):
        if self.gender == 'male':
            bmr = 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)
        elif self.gender == 'female':
            bmr = 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.330 * self.age)
        else:
            logger.error("Invalid gender input, please enter 'male' or 'female'")
            raise ValueError("Gender input error")
        logger.info(f"Calculated BMR: {bmr:.2f}")
        return bmr

    def calculate_bmi(self):
        height_m = self.height / 100  # convert cm to meters
        bmi = self.weight / (height_m ** 2)
        logger.info(f"Calculated BMI: {bmi:.2f}")
        return round(bmi, 2)

    def calculate_tdee(self):
        activity_factors = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'veryactive': 1.9
        }
        factor = activity_factors.get(self.activity_level)
        if factor is None:
            logger.error("Invalid activity level input, please check if the input is correct.")
            raise ValueError("Activity level input error")
        tdee = self.calculate_bmr() * factor
        logger.info(f"Calculated TDEE: {tdee:.2f}")
        return tdee

    def generate_macros(self):
        tdee = self.calculate_tdee()
        macros = {
            'calories': round(tdee, 2),
            'carbs': round((tdee * 0.50) / 4, 2),
            'protein': round((tdee * 0.20) / 4, 2),
            'fats': round((tdee * 0.30) / 9, 2)
        }
        logger.info(f"Generated macronutrients: {macros}")
        return macros

    def recommend(self):
        macros = self.generate_macros()
        bmi = self.calculate_bmi()

        # Determine BMI category
        if bmi < 18.5:
            bmi_category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            bmi_category = "Normal"
        elif 24.9 <= bmi < 29.9:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obese"

        recommendation = {
            "Recommended Daily Total Calories (kcal)": macros['calories'],
            "Recommended Carbohydrates (g)": macros['carbs'],
            "Recommended Protein (g)": macros['protein'],
            "Recommended Fat (g)": macros['fats'],
            "BMI Index": f"{bmi} ({bmi_category})"
        }
        return recommendation, macros


def get_user_input():
    try:
        height = float(input("Please enter your height (cm): "))
        weight = float(input("Please enter your weight (kg): "))
        age = int(input("Please enter your age: "))

        # Ensure gender input is correct
        while True:
            gender = input("Please enter your gender (male or female): ").strip().lower()
            if gender in ['male', 'female']:
                break
            else:
                print("Gender input error, please enter 'male' or 'female'")

        print("Please select your activity level:")
        print("Options: sedentary, light, moderate, active, veryactive")

        # Ensure activity level input is correct
        valid_activity_levels = ['sedentary', 'light', 'moderate', 'active', 'veryactive']
        while True:
            activity_level = input("Enter activity level: ").strip().lower()
            if activity_level in valid_activity_levels:
                break
            else:
                print(f"Activity level input error, please select from the following options: {', '.join(valid_activity_levels)}")

        user_data = {
            'height': height,
            'weight': weight,
            'age': age,
            'gender': gender,
            'activity_level': activity_level
        }

        return user_data
    except Exception as e:
        logger.error(f"Error during data input: {e}")
        raise


def main():
    user_info = get_user_input()
    diet_recommender = PersonalizedDietRecommendation(**user_info)
    recommendation, target_macros = diet_recommender.recommend()

    print("\n======= Your Personalized Diet Recommendation =======")
    for k, v in recommendation.items():
        print(f"{k}: {v}")

    # Print BMI explanation
    bmi_info = recommendation["BMI Index"]
    # Extract numeric part from BMI index string
    bmi = float(bmi_info.split('(')[0])
    print("\nBMI Explanation:")
    if bmi < 18.5:
        print("➤ You are underweight, please focus on balanced nutrition.")
    elif 18.5 <= bmi < 24.9:
        print("➤ Normal range, keep it up!")
    elif 25 <= bmi < 29.9:
        print("➤ Overweight, recommend controlling diet and increasing exercise.")
    else:
        print("➤ Obese, please prioritize healthy eating and exercise.")


if __name__ == "__main____":
    main()
