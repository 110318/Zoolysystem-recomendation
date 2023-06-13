from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors



# Declare the APP server instance
app = Flask(__name__)
# Enable CORS policies
CORS(app)

#Leer el archivo CSV con los datos de las personas
df_personas = pd.read_csv("Datos.csv",delimiter=";")
nombres = list(df_personas['Nombre'])
people = []

for x in nombres:
  people.append((df_personas[df_personas["Nombre"] == x]).to_dict())
# print(people)

#Leer el archivo CSV con los datos de los animales
df_animales = pd.read_csv("animales.csv",delimiter=";")


#Remove Column name to do the promedio of characteristics
columnas = df_personas.columns.tolist()
caracteristicas = columnas[1:]

#Calculate the promedio of characteristics weight
weights = df_personas[caracteristicas].mean().to_dict()

#Create proto-person
protopersona = {}
for caracteristica in caracteristicas:
  protopersona[caracteristica] = round(weights[caracteristica])

# Add protoperson to DF
protopersona_row = pd.DataFrame(protopersona, index=[0])
df = pd.concat([df_personas, protopersona_row],ignore_index=True)


#Define features for recommendation
features = caracteristicas

# Create the feature matrix X

X = df_personas[features].values

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
    "columns" : list(df_personas.columns)
  
  })

# POST Endpoint =============================================================================
@app.route('/post_endpoint', methods=['POST'])
def create_data():
    # Get the data from the POST endpoint
    data = request.get_json()
    # print(data)
    if not data:
        return (jsonify({'error': 'No data provided'}), 400)
    return (jsonify({'response': 'ok all good', 'data': data}), 201)

# POST Endpoint 2 ==========================================================================
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    node_name = data['node']  # Obtener el nombre del nodo
    weights = data['weights']
    k_neighbors = data['k_neighbors']
    aggregation_method = data['aggregation_method']
  
    # Calcular la matriz de características ponderadas
    weighted_X = X * np.array([int(weights.get(feature, 0)) for feature in features]).reshape(1, -1)

  
    # Encontrar el índice del nodo correspondiente al nombre
    node_index = nombres.index(node_name)
  
    # Encontrar los índices de los K vecinos más cercanos
    distances, indices = knn.kneighbors(weighted_X)
  
    # Recuperar las recomendaciones
    recommendations = df.iloc[indices[node_index]]
  
    # Realizar la agregación en función del método seleccionado
    if aggregation_method == 'naive_bayes':
        aggregated_recommendation = recommendations.any(axis=0)
    elif aggregation_method == 'least_misery':
        aggregated_recommendation = recommendations.min(axis=0)
    elif aggregation_method == 'most_pleasure':
        aggregated_recommendation = recommendations.max(axis=0)
    else:
        return jsonify({'error': 'Invalid aggregation method'})
      
      
    # Multiplicar el vecindario por los pesos actualizados
    weighted_neighbors = recommendations[features] * np.array([int(weights.get(feature, 0)) for feature in features])

    # Agregar las características ponderadas al vecindario
    weighted_neighbors = pd.concat([recommendations.drop(features, axis=1), weighted_neighbors], axis=1)
  
  
  
    #Obtener las caracteristicas presentes en el DataFrame df_animales
    
    # Obtener el animal recomendado basado en la protopersona
    animal_recomendado = df_animales[(df_animales[caracteristicas] == 1).all(axis=1)]['Animales'].values
    if len(animal_recomendado) > 0:
        recommended_animal = animal_recomendado[0]
    else:
        recommended_animal = "No se encontró animal recomendado"
        
    print('Valor de aggregated_recommendation.name:', aggregated_recommendation.name)


    return jsonify({
        'recommendation': recommended_animal,
        'neighbors': recommendations.to_dict(orient='records')
    })

  


# Execute the app instance
# The app will run locally in: http://localhost:5001/ after execution
if __name__ == "__main__":
  app.run(debug=True, port=5001)