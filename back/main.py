from flask import Flask, request, jsonify
from flask_cors import CORS

# Declare the APP server instance
app = Flask(__name__)
# Enable CORS policies
CORS(app)

# GET Endpoint =============================================================================
@app.route("/", methods=["GET"])
def index():
  return jsonify({"msg": "Hello Python REST API"})

# POST Endpoint =============================================================================
@app.route('/post_endpoint', methods=['POST'])
def create_data():
    # Get the data from the POST endpoint
    data = request.get_json()
    if not data:
        return (jsonify({'error': 'No data provided'}), 400)
    return (jsonify({'response': 'ok all good'}), 201)

# Execute the app instance
# The app will run locally in: http://localhost:5001/ after execution
if __name__ == "__main__":
  app.run(debug=True, port=5001)