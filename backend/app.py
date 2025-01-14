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
    if not data or 'name' not in data or 'cost' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    trip = {
        'name': data['name'],
        'cost': float(data['cost'])
    }
    trips.append(trip)
    return jsonify(trip), 201

if __name__ == '__main__':
    app.run(debug=True)
