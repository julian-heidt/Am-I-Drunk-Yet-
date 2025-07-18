from flask import Flask, request, jsonify, render_template
from calculator import calculate_drinks_to_target_bac, calculate_time_to_sober

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    try:
        weight = float(data['weight'])
        gender = data['gender']
        current_drinks = int(data['current_drinks'])

        if weight <= 0:
            return jsonify({'error': 'Weight must be a positive number.'}), 400

        drinks_to_target = calculate_drinks_to_target_bac(weight, gender, current_drinks)
        time_to_sober = calculate_time_to_sober(current_drinks, weight, gender)

        return jsonify({
            'drinks_to_reach_target': drinks_to_target,
            'time_to_sober': time_to_sober
        })

    except (ValueError, KeyError):
        return jsonify({'error': 'Invalid input. Please provide weight (kg), gender, and current number of drinks.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
