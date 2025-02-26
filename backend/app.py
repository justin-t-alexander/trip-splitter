from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# In-memory storage for trips
trips = []

# Home route
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Trip Splitter API'}), 200

# Get all trips
@app.route('/api/trips', methods=['GET'])
def get_trips():
    return jsonify(trips), 200

# Add a new trip
@app.route('/api/trips', methods=['POST'])
def add_trip():
    data = request.get_json()
    
    if not data or 'name' not in data or 'cost' not in data or 'participants' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    split_type = data.get('splitType', 'equal')  # Match frontend key name
    participants = data['participants']
    total_cost = float(data['cost'])
    contributions = {}
    paid_status = {} # track who has paid

    if split_type == 'equal':
        split_amount = total_cost / len(participants)
        for participant in participants:
            contributions[participant] = round(split_amount, 2)
            paid_status[participant] = False # Default to unpaid
    
    elif split_type == 'percentage':
        percentages = data.get('percentages', {})  #  Get as a dictionary
        total_percent = sum(percentages.values())

        if total_percent != 100:
            return jsonify({'error': 'Total percentage must equal 100%'}), 400
        
        for participant in participants:
            if participant in percentages:
                contributions[participant] = round(total_cost * (percentages[participant] / 100), 2)
                paid_status[participant] = False # Default to unpaid
            else:
                return jsonify({'error': f'Missing percentage for {participant}'}), 400

    else:
        return jsonify({'error': 'Invalid split type'}), 400

    # Create the trip object
    trip = {
        'name': data['name'],
        'cost': total_cost,
        'participants': participants,
        'splitType': split_type,  #  Consistent key naming
        'percentages': data.get('percentages', {}),
        'contributions': contributions,
        'paid_status': paid_status # Track payments
    }
    trips.append(trip)
    
    return jsonify(trip), 201



# Mark a participant as paid
@app.route('/api/trips/<int:trip_id>/pay', methods=['POST'])
def mark_paid(trip_id):
    data = request.get_json()
    participant = data.get('participant')

    trip = next((t for t in trips if t['id'] == trip_id), None)
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404

    if participant not in trip['paidStatus']:
        return jsonify({'error': 'Participant not found'}), 400

    trip['paidStatus'][participant] = True
    return jsonify({'message': f'{participant} marked as paid'}), 200

# Get unpaid participants for reminders
@app.route('/api/trips/<int:trip_id>/unpaid', methods=['GET'])
def get_unpaid(trip_id):
    trip = next((t for t in trips if t['id'] == trip_id), None)
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404

    unpaid = [p for p, status in trip['paidStatus'].items() if not status]
    return jsonify({'unpaid': unpaid}), 200








if __name__ == '__main__':
    app.run(debug=True)
