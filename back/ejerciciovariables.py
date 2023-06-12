print("Ejecutando el programa")

# Librerías
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import ipywidgets as widgets
from IPython.display import display

datos = pd.read_csv("Datos.csv", delimiter=";")

# Obtener las características
caracteristicas = datos.columns[1:]

# Creación de los sliders de las características de las columnas del csv jeje
sliders = []
for caracteristica in caracteristicas:
    slider = widgets.IntSlider(min=1, max=5, description=caracteristica)
    sliders.append(slider)

# El botón de recomendación como función
def recomendar(button):
    # Obtener los valores seleccionados en los sliders
    valores = [slider.value for slider in sliders]
    
    registro_usuario = pd.DataFrame([valores], columns=caracteristicas)
    
    # Parte de los vecinos (KNN)
    knn = NearestNeighbors(n_neighbors=3, metric='euclidean')
    knn.fit(datos[caracteristicas])
    _, indices_vecinos = knn.kneighbors(registro_usuario)
    vecindario = datos.iloc[indices_vecinos[0]].reset_index(drop=True)
    
    # Mostrar vecindario de recomendados con display
    display(vecindario)

boton_recomendar = widgets.Button(description="Recomendar")
boton_recomendar.on_click(recomendar)

# Mostrar interfaz
display(*sliders)
display(boton_recomendar)