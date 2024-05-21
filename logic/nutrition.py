def calculate_nutrition(preferences):
    # Constants for BMR calculation
    if preferences['gender'] == 'male':
        bmr = 88.362 + (13.397 * preferences['weight']) + (4.799 * preferences['height']) - (5.677 * preferences['age'])
    else:
        bmr = 447.593 + (9.247 * preferences['weight']) + (3.098 * preferences['height']) - (4.330 * preferences['age'])

    # Adjust BMR based on activity level (simplified to moderate activity for example)
    if preferences['days_per_week'] >= 5:
        tdee = bmr * 1.55  # Moderate to intense activity
    elif preferences['days_per_week'] >= 3:
        tdee = bmr * 1.375  # Light to moderate activity
    else:
        tdee = bmr * 1.2  # Sedentary or light activity

    # Adjust calories based on goal
    if preferences['purpose_of_the_workout'] == 'lose_weight':
        calories = tdee - 500  # Create a deficit of 500 calories
    elif preferences['purpose_of_the_workout'] == 'gain_muscle':
        calories = tdee + 500  # Surplus of 500 calories
    else:
        calories = tdee  # Maintain for other goals

    # Macronutrient ratios based on the goal
    if preferences['purpose_of_the_workout'] == 'gain_muscle':
        protein = preferences['weight'] * 2.2  # Higher protein for muscle synthesis
        fat_percentage = 0.25
    elif preferences['purpose_of_the_workout'] == 'lose_weight':
        protein = preferences['weight'] * 1.8  # Adequate protein to preserve muscle mass
        fat_percentage = 0.30
    else:  # For stamina, maintaining shape, powerlifting, flexibility
        protein = preferences['weight'] * 1.5  # Standard protein intake
        fat_percentage = 0.25

    fats = calories * fat_percentage / 9  # Calculate fats based on percentage of total calories
    carbs = (calories - (protein * 4 + fats * 9)) / 4  # Remaining calories from carbs

    return {
        'calories': round(calories),
        'protein': round(protein),
        'fats': round(fats),
        'carbs': round(carbs)
    }