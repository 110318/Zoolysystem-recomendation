#Librerias proyecto final
import pandas as pd
from sklearn.metrics.pairwise import cosine_distances
import ipywidgets as widgets
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np

#Tabla de datos
datos = pd.read_csv("tabla_zooly.csv",index_col=0)

#1. El sistema de recomendacion tendra que tener un front en js y html?
#2. Que debera contener la presentacion final?
#3. El numero de metodos que podemos usar para el proyecto final?


# PASO 1 --> Definicion del nodo X (usuario de interes)

nodo_x = "Luna"

# PASO 2 --> Definir los pesos de las características
pesos = {
    "Cola esponjosa": 3,
    "Ojos redondos": 4,
    "Pelaje corto": 4,
    "Plumas": 2,
    "Osico alargado": 4,
    "Orejas puntiagudas": 5,
    "Pezuñas": 2,
    "Pico": 2,
    "Manchas": 4,
    "Garras": 3,
    "Alas": 2,
    "Aletas": 2
}



dropdown = widgets.Dropdown(
    nombre_nodox = dropdown.value
    
    
    
    
    
    
)
