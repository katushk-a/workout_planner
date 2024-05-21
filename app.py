from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from logic.recommendations import run_recommendations
from logic.nutrition import calculate_nutrition
from logic.data import get_info
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workoutplans.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)


class PlanHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    preferences = db.Column(db.JSON, nullable=False)
    workout_plan = db.Column(db.JSON, nullable=False)
    nutrition_plan = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()

@app.route('/api/workout', methods=['POST'])
def get_workout_plan():
    user_preferences = request.get_json()
    print('REQUEST')
    print(user_preferences)
    try:
        workout_plan = run_recommendations(user_preferences)
        print("WORKOUT PLAN")
        print(workout_plan)
        return jsonify(workout_plan.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/api/nutrition', methods=['POST'])
def get_nutrition_plan():
    user_preferences = request.get_json()
    print('REQUEST')
    print(user_preferences)
    try:
        nutrition_plan = calculate_nutrition(user_preferences)
        print("NUTRITION PLAN")
        print(nutrition_plan)
        return jsonify(nutrition_plan)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@app.route('/api/workout/info', methods=['GET'])
def get_info_for_form():
    try:
        info = get_info()
        print('INFO')
        print(info)
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@app.route('/api/plans', methods=['POST'])
def save_history():
    try:
        data = request.json
        print("Received data:", data)  
        new_plan = PlanHistory(
            user_name=data['user_name'],
            preferences=data['preferences'],
            workout_plan=data['workout_plan'],
            nutrition_plan=data['nutrition_plan']
        )
        db.session.add(new_plan)
        db.session.commit()
        return jsonify({'id': new_plan.id}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing key in data: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/plans', methods=['GET'])
def get_plans():
    try:
        plans = PlanHistory.query.all()
        return jsonify([
            {
                'username': plan.user_name,
                'preferences': plan.preferences,
                'workout_plan': plan.workout_plan,
                'nutrition_plan': plan.nutrition_plan,
                'created_at': plan.created_at.isoformat()  # or str(plan.created_at) for simplicity
            } for plan in plans
        ])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
