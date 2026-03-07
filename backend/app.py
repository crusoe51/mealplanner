from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import database

app = Flask(__name__)
CORS(app)

database.init_db()

# TEST ROUTE (lösche später)
@app.route('/')
def home():
    return "<h1>Meal Planner Live! 🚀</h1><p>Gunicorn OK, Flask OK</p>"

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})



# ==================== MEALS ====================

@app.route('/api/meals', methods=['GET'])
def get_meals():
    return jsonify(database.get_all_meals())


@app.route('/api/meals', methods=['POST'])
def create_meal():
    data = request.get_json()
    name = data.get('name', '').strip()
    
    if not name:
        return jsonify({"error": "Name ist erforderlich"}), 400
    
    try:
        meal = database.create_meal(name, data.get('color', '#3B82F6'))
        return jsonify(meal), 201
    except Exception as e:
        return jsonify({"error": "Gericht existiert bereits"}), 400


@app.route('/api/meals/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id):
    data = request.get_json()
    name = data.get('name', '').strip()
    
    if not name:
        return jsonify({"error": "Name ist erforderlich"}), 400
    
    meal = database.update_meal(meal_id, name, data.get('color', '#3B82F6'))
    return jsonify(meal)


@app.route('/api/meals/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id):
    database.delete_meal(meal_id)
    return jsonify({"success": True})


# ==================== PLAN ====================

@app.route('/api/plan/<int:year>/<int:week>', methods=['GET'])
def get_plan(year, week):
    return jsonify(database.get_week_plan(year, week))


@app.route('/api/plan/<int:year>/<int:week>/<int:day>', methods=['PUT'])
def set_meal(year, week, day):
    data = request.get_json()
    meal_id = data.get('meal_id')
    
    if not meal_id:
        return jsonify({"error": "meal_id erforderlich"}), 400
    
    database.set_day_meal(year, week, day, meal_id)
    return jsonify({"success": True})


@app.route('/api/plan/<int:year>/<int:week>/<int:day>', methods=['DELETE'])
def clear_meal(year, week, day):
    database.clear_day_meal(year, week, day)
    return jsonify({"success": True})


@app.route('/api/plan/<int:year>/<int:week>', methods=['DELETE'])
def clear_week(year, week):
    database.clear_week(year, week)
    return jsonify({"success": True})


# Mehrere Wochen laden
@app.route('/api/plan/weeks', methods=['GET'])
def get_weeks():
    year = request.args.get('year', type=int)
    start = request.args.get('start', type=int)
    count = request.args.get('count', type=int, default=3)
    
    plans = {}
    y, w = year, start
    
    for _ in range(count):
        plans[f"{y}-{w}"] = database.get_week_plan(y, w)
        w += 1
        if w > 52:
            w = 1
            y += 1
    
    return jsonify(plans)


# Mehrere Wochen leeren
@app.route('/api/plan/weeks', methods=['DELETE'])
def clear_weeks():
    year = request.args.get('year', type=int)
    start = request.args.get('start', type=int)
    count = request.args.get('count', type=int, default=3)
    
    y, w = year, start
    
    for _ in range(count):
        database.clear_week(y, w)
        w += 1
        if w > 52:
            w = 1
            y += 1
    
    return jsonify({"success": True})


@app.route('/api/current-week')
def current_week():
    now = datetime.now()
    year, week, _ = now.isocalendar()
    return jsonify({"year": year, "week": week})


if __name__ == '__main__':
    import os
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=5000, debug=debug)
