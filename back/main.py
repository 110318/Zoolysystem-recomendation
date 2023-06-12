from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors



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


#Remove Column name to do the promedio of characteristics
columnas = df.columns.tolist()
caracteristicas = columnas[1:]

#Calculate the promedio of characteristics weight
weights = df[caracteristicas].mean().to_dict()

#Create proto-person
protopersona = {}
for caracteristica in caracteristicas:
  protopersona[caracteristica] = round(weights[caracteristica])

# Add protoperson to DF
protopersona_row = pd.DataFrame(protopersona, index=[0])
df = pd.concat([df, protopersona_row],ignore_index=True)


#Define features for recommendation
features = [
    "Cola esponjosa", "Ojos redondos", "Pelaje corto", "Plumas", "Osico alargado",
    "Orejas puntiagudas", "Pezunas", "Pico", "Manchas", "Garras", "Alas", "Aletas"
]

# Create the feature matrix X

X = df[features].values

#KNN model 
knn = NearestNeighbors(n_neighbors=5, metric='euclidean')
knn.fit(X)




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

# POST Endpoint 2 ==========================================================================
@app.route('/recommend', methods=['POST'])
def recommend():
  data = request.get_json()
  node = data['node']
  weights = data['weights']
  k_neighbors = data['k_neighbors']
  aggregation_method = data['aggregation_method']
  
  #Calculate the weighted feature matrix
  weighted_X = X * np.array(list(weights.values()))
  
  #Find the indices of the K nearest neighbors
  distances,indices = knn.kneighbors(weighted_X)
  
  #Retrieve the recommendations 
  recommendations = df.loc[indices[node]]
  
  #Perform aggregation based on the selected method 
  if aggregation_method == 'naive_bayes':
    aggregated_recommendation = recommendations.any(axis=0)
  elif aggregation_method == 'least_misery':
    aggregated_recommendation = recommendations.min(axis=0)
  elif aggregation_method == 'most_pleasure':
    aggregated_recommendation = recommendations.max(axis=0)
  else:
    return jsonify({'error': 'Invalid aggregation method'})
  
  recommended_animal = df.loc[aggregated_recommendation].iloc[0]['Nombre']

  return jsonify({
        'recommendation': recommended_animal,
        'neighbors': recommendations.to_dict(orient='records')
    })
  
  







# Execute the app instance
# The app will run locally in: http://localhost:5001/ after execution
if __name__ == "__main__":
  app.run(debug=True, port=5001)