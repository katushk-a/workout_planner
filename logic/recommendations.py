import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from logic.entities import WorkoutPlan, DayWorkout, SetOfExercises

primary_muscles = {
    'Advanced': [
        "Neck", "Shoulders", "Chest", "Biceps", "Forearms", "Abdominals",
        "Quadriceps", "Adductors", "Calves", "Traps", "Triceps", "Lats",
        "Middle Back", "Lower Back", "Abductors", "Glutes", "Hamstrings"
    ],
    'Beginner': [
        "Chest", "Biceps", "Abdominals", "Quadriceps", "Middle Back", "Glutes", 
        "Hamstrings", "Calves"
    ],
    'Intermediate': [
        "Chest", "Biceps", "Abdominals", "Quadriceps", "Middle Back", "Glutes",
        "Hamstrings", "Calves", "Traps", "Shoulders", "Triceps", "Lats"
    ],
}

muscle_priority = {
    'Neck': 1, 
    'Shoulders': 3, 
    'Chest': 4, 
    'Biceps': 3, 
    'Forearms': 2, 
    'Abdominals': 3,
    'Quadriceps': 4, 
    'Adductors': 2, 
    'Calves': 2, 
    'Traps': 2, 
    'Triceps': 3, 
    'Lats': 3,
    'Hamstrings': 3, 
    'Middle Back': 3, 
    'Lower Back': 2, 
    'Abductors': 2, 
    'Glutes': 3
}


purpose_to_type = {
        'lose_weight': ['Cardio', 'Strength', 'Plyometrics'],
        'gain_muscle': ['Strength', 'Powerlifting', 'Plyometrics'],
        'increase_stamina': ['Cardio', 'Plyometrics', 'Strength'],
        'maintain_shape': ['Strength', 'Plyometrics', 'Cardio'],
        'powerlifting': ['Powerlifting', 'Olympic Weightlifting', 'Strongman'],
        'flexibility': ['Stretching', 'Plyometrics', 'Cardio']
    }


priority_fields = ['BodyPart', 'Level', 'Equipment', 'Type']
    
priority_weights = [20, 10, 5, 3]

def get_tfidf(df):
    # Setup TF-IDF and Cosine Similarity
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['content'])
    return tfidf_vectorizer, tfidf_matrix

def generate_recommendations(df, tfidf_vectorizer, tfidf_matrix, user_input, number_of_recommendations=10):
    
    user_content = ' '.join(str(user_input.get(field, '')) * weight for field, weight in zip(priority_fields, priority_weights))
    user_tfidf_vector = tfidf_vectorizer.transform([user_content])
    cosine_sim = linear_kernel(user_tfidf_vector, tfidf_matrix)
    top_indices = cosine_sim[0].argsort()[-number_of_recommendations:][::-1]
    recommended_exercises = df.iloc[top_indices].to_dict(orient='records')
    return recommended_exercises

def generate_weekly_split(days_per_week, muscles):
    total_priority = sum(muscle_priority[muscle] for muscle in muscles)
    
    # Proportional exercises calculation
    muscle_exercises = {muscle: max(1, (6 * days_per_week * muscle_priority[muscle]) // total_priority) for muscle in muscles}

    # Shuffle muscles for random distribution
    muscle_items = list(muscle_exercises.items())
    random.shuffle(muscle_items)
    
    # Initialize the workout plan
    workout_plan = {day: [] for day in range(1, days_per_week + 1)}
    exercises_per_day = {day: [] for day in range(1, days_per_week + 1)}

    # Assign muscles to days based on priority
    for muscle, exercises in sorted(muscle_items, key=lambda x: -muscle_priority[x[0]]):
        # Find a day with space that maximizes priority balance
        day = min(exercises_per_day.keys(), key=lambda d: (sum(y[1] for y in exercises_per_day[d]), -len(exercises_per_day[d])))
        remaining_capacity = 6 - sum(ex[1] for ex in exercises_per_day[day])
        if exercises <= remaining_capacity:
            exercises_per_day[day].append((muscle, exercises))
        else:
            if remaining_capacity > 0:
                exercises_per_day[day].append((muscle, remaining_capacity))
            # Find next best day to place the remaining exercises
            remaining_exercises = exercises - remaining_capacity
            if remaining_exercises > 0:
                next_best_day = min(exercises_per_day.keys(), key=lambda d: (sum(y[1] for y in exercises_per_day[d]), -len(exercises_per_day[d])))
                exercises_per_day[next_best_day].append((muscle, remaining_exercises))

    # Convert day plans to a list and shuffle
    day_plans = list(exercises_per_day.values())
    random.shuffle(day_plans)

    # Reassign the shuffled plans to days
    for i, plan in enumerate(day_plans, 1):
        workout_plan[i] = plan

    return workout_plan

#w = generate_weekly_split(3, ["Chest", "Biceps", "Abdominals", "Quadriceps", "Middle Back", "Glutes", "Hamstrings", "Calves"])


def create_workout_plan(num_days, user_preferences, weekly_split, df):
    workout_plan = WorkoutPlan(num_days)
    tfidf_vectorizer, tfidf_matrix = get_tfidf(df)
    # Loop through each day in the weekly split
    for day in range(1, num_days + 1):
        day_workout = DayWorkout()  # Create a new DayWorkout object
        
        # Check if there is a workout for this day in the split
        if day in weekly_split:
            # Loop through each set of exercises defined for the day
            for muscle_info in weekly_split[day]:
                muscle_group, number = muscle_info
                user_preferences_new = user_preferences
                user_preferences_new['BodyPart'] = muscle_group
                exercises = generate_recommendations(df, tfidf_vectorizer, tfidf_matrix, user_preferences_new, number)  # Generate exercises for this muscle group
                set_of_exercises = SetOfExercises(muscle_group, number, exercises)  # Create a SetOfExercises object
                day_workout.add_exercises(set_of_exercises)  # Add this set to the day's workout

        workout_plan.add_day_workout(day_workout)  # Add the filled DayWorkout to the workout plan

    return workout_plan

def generate_weekly_plan(user_preferences, df):
    days_per_week = user_preferences.get("days_per_week")
    if days_per_week > 5 or days_per_week < 2:
        raise Exception("Invalid amount of workout days")
    exercise_types = purpose_to_type.get(user_preferences['purpose_of_the_workout'], ['Strength'])
    level = user_preferences.get('level')
    muscles = primary_muscles.get(level)
    weekly_split = generate_weekly_split(days_per_week, muscles)
    equipment = user_preferences.get('equipment')
    if len(equipment) == 0 :
        equipment = ['None']
    user_preferences = {
        'Level': level,
        'Equipment': equipment,
        'Type': exercise_types,
    }
    return create_workout_plan(days_per_week, user_preferences, weekly_split, df)

def run_recommendations(user_preferences):
    # Load and prepare data
    df = pd.read_csv('logic\data\megaGymDataset_cleaned.csv')
    df['content'] = df[priority_fields].apply(
    lambda row: (' '.join(str(val) * weight for val, weight in zip(row, priority_weights))),
    axis=1
    )
    a, b = get_tfidf(df)
    return generate_weekly_plan(user_preferences, df)
    #return generate_recommendations(df, a, b, user_preferences, 1)