from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)
CORS(app)

df_personas = pd.read_csv("Datos.csv", delimiter=";")
nombres = list(df_personas['Nombre'])
people = []

for x in nombres:
    people.append((df_personas[df_personas["Nombre"] == x]).to_dict())

df_animales = pd.read_csv("animales.csv", delimiter=";")

columnas = df_personas.columns.tolist()
caracteristicas = columnas[1:]

weights = df_personas[caracteristicas].mean().to_dict()

protopersona = {}
for caracteristica in caracteristicas:
    protopersona[caracteristica] = round(weights[caracteristica])

protopersona_row = pd.DataFrame(protopersona, index=[0])
df = pd.concat([df_personas, protopersona_row], ignore_index=True)

features = caracteristicas

X = df_personas[features].values

knn = NearestNeighbors(n_neighbors=5, metric='euclidean')
knn.fit(X)

@app.route("/nombres", methods=["GET"])
def index():
    global nombres
    return jsonify({
        "Nombres": nombres,
        "dataFrame": people,
        "columns": list(df_personas.columns)
    })
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    node_name = data['node']
    weights = data['weights']
    k_neighbors = data['k_neighbors']
    aggregation_method = data['aggregation_method']

    weighted_X = X * np.array([float(weights.get(feature, 0)) for feature in features]).reshape(1, -1)

    node_index = nombres.index(node_name)

    distances, indices = knn.kneighbors(weighted_X)

    recommendations = df.iloc[indices[node_index]]

    if aggregation_method == 'naive_bayes':
        aggregated_recommendation = recommendations[caracteristicas].any(axis=0)
    elif aggregation_method == 'least_misery':
        aggregated_recommendation = recommendations[caracteristicas].min(axis=0)
    elif aggregation_method == 'most_pleasure':
        aggregated_recommendation = recommendations[caracteristicas].max(axis=0)
    else:
        return jsonify({'error': 'Invalid aggregation method'})
    
    print(aggregation_method)

    # Obtener las características presentes en el DataFrame df_animales
    caracteristicas_presentes = [c for c in caracteristicas if c in df_animales.columns]

    # Traducir los valores de la protopersona al rango de 1 y 0
    protopersona_valores = [int(float(data['weights'].get(caracteristica, 0)) >= 0.5) for caracteristica in caracteristicas_presentes]

    animales_recomendados = df_animales.copy()
    for caracteristica, valor in zip(caracteristicas_presentes, protopersona_valores):
        animales_recomendados = animales_recomendados[animales_recomendados[caracteristica].astype(float) >= float(valor)]

    if not animales_recomendados.empty:
        recommended_animal = animales_recomendados.iloc[0]['Animales']
    else:
        recommended_animal = ""

    return jsonify({
        'recommendation': recommended_animal,
        'neighbors': recommendations.to_dict(orient='records')
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)
