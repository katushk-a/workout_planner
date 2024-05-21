class SetOfExercises:
    def __init__(self, muscle_group, number, exercises):
        self.muscle_group = muscle_group
        self.number = number
        self.exercises = exercises
    
    def to_dict(self):
        return {
            'muscle_group': self.muscle_group,
            'number': self.number,
            'exercises': self.exercises
        }

class DayWorkout:
    def __init__(self):
        self.exercises = []
    
    def add_exercises(self, setOfExercises):
        self.exercises.append(setOfExercises)
    
    def to_dict(self):
        return {'exercises': [ex.to_dict() for ex in self.exercises]}

class WorkoutPlan:
    def __init__(self, num_days_per_week):
        self.num_days_per_week = num_days_per_week
        self.days = []
    
    def add_day_workout(self, day_workout):
        self.days.append(day_workout)
    
    def to_dict(self):
        return {
            'num_days_per_week': self.num_days_per_week,
            'days': [day.to_dict() for day in self.days]
        }

    def __str__(self):
        output = f'Workout Plan: {self.num_days_per_week} days per week\n'
        for day_number, day in enumerate(self.days, 1):
            output += f'Day {day_number}:\n'
            for workout in day.exercises:
                output += f'  - Muscle Group: {workout.muscle_group}, Exercises: {workout.number}\n'
                for ex in workout.exercises:
                    output += f'    - {ex}\n'
        return output
