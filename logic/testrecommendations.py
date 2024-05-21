from logic.recommendations import generate_recommendations, run_recommendations
from logic.nutrition import calculate_nutrition
# Example usage with user preferences
if __name__ == "__main__":
    user_preferences = {
    'days_per_week': 3,
    'purpose_of_the_workout': 'lose_weight',
    'level': 'Beginner',
    'equipment': [],
    'age': 17,
    'gender': 'male',
    'height': 175,  # Height in cm
    'weight': 75,   # Weight in kg
    }
    
    # Generate a weekly plan from the recommendations
    weekly_plan = run_recommendations(user_preferences)
    print(weekly_plan)

    nutrition_info = calculate_nutrition(user_preferences)
    print(nutrition_info)