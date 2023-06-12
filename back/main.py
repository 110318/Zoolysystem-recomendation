from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd



# Declare the APP server instance
app = Flask(__name__)
# Enable CORS policies
CORS(app)

df = pd.read_csv("Datos.csv",delimiter=";")
nombres = list(df['Nombre'])
people = []

for x in nombres:
  people.append((df[df["Nombre"] == x]).to_dict())
print(people)

# GET Endpoint =============================================================================
@app.route("/nombres", methods=["GET"])
def index():
  global nombres
  return jsonify({
    "Nombres": nombres ,
    "dataFrame" : people,
    "columns" : list(df.columns)
  
  })

# POST Endpoint =============================================================================
@app.route('/post_endpoint', methods=['POST'])
def create_data():
    # Get the data from the POST endpoint
    data = request.get_json()
    print(data)
    if not data:
        return (jsonify({'error': 'No data provided'}), 400)
    return (jsonify({'response': 'ok all good', 'data': data}), 201)

# Execute the app instance
# The app will run locally in: http://localhost:5001/ after execution
if __name__ == "__main__":
  app.run(debug=True, port=5001)