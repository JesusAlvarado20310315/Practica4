import sys
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import messagebox

def prim(graph):
    # Inicializar las estructuras de datos
    vertices = set(graph.keys())
    selected_vertices = set()
    selected_edges = []
    min_distances = {v: sys.maxsize for v in vertices}
    min_distances[next(iter(vertices))] = 0

    while vertices:
        # Encontrar el vértice con la distancia mínima no seleccionado
        min_distance = sys.maxsize
        min_vertex = None
        for vertex in vertices:
            if min_distances[vertex] < min_distance:
                min_distance = min_distances[vertex]
                min_vertex = vertex
        
        # Marcar el vértice actual como seleccionado
        vertices.remove(min_vertex)
        selected_vertices.add(min_vertex)

        # Actualizar las distancias mínimas de los vértices adyacentes
        for neighbor, weight in graph[min_vertex].items():
            if neighbor in vertices and weight < min_distances[neighbor]:
                min_distances[neighbor] = weight

                # Agregar la arista al árbol parcial mínimo
                selected_edges.append((min_vertex, neighbor, weight))

    return selected_edges

def procesar_grafo():
    # Obtener los datos ingresados por el usuario
    datos = entrada.get()

    # Dividir los datos en conexiones individuales
    conexiones = datos.split(',')

    # Crear un grafo vacío
    graph = {}

    # Procesar cada conexión
    for conexion in conexiones:
        # Dividir la conexión en nodo1-nodo2 y peso
        nodos, peso = conexion.split(':')

        # Extraer los nodos individuales
        nodo1, nodo2 = nodos.split('-')

        # Agregar la conexión al grafo
        if nodo1 not in graph:
            graph[nodo1] = {}
        if nodo2 not in graph:
            graph[nodo2] = {}

        graph[nodo1][nodo2] = int(peso)
        graph[nodo2][nodo1] = int(peso)

    # Ejecutar el algoritmo del Árbol Parcial Mínimo de Prim
    selected_edges = prim(graph)

    # Crear un objeto de grafo no dirigido utilizando NetworkX
    G = nx.Graph()

    # Agregar las aristas al grafo con los pesos como atributos
    for edge in selected_edges:
        u, v, weight = edge
        G.add_edge(u, v, weight=weight)

    # Crear una lista con las etiquetas de peso de las aristas
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}

    # Crear un diseño para el grafo
    pos = nx.spring_layout(G)

    # Dibujar los nodos del grafo
    nx.draw_networkx_nodes(G, pos)

    # Dibujar las aristas del grafo con las etiquetas de peso
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Mostrar el grafo
    plt.axis('off')
    plt.show()
    
# Crear la ventana
ventana = tk.Tk()

# Configurar la ventana
ventana.title("Algoritmo de Dijkstra")
ventana.geometry("350x275")

# Texto de explicación para el usuario
graph_label = tk.Label(ventana, text="Para ingresar el grafo, utiliza la siguiente sintaxis:\nA-B:#,A-C:#,B-C:#,B-D:#,C-D:#\nPor ejemplo, si hay una conexión entre A y B con peso 5,\nse escribiría 'A-B:5'.")
graph_label.pack(pady=5)

# Etiqueta para el campo de entrada del grafo
graph_label = tk.Label(ventana, text="Ingrese el grafo:")
graph_label.pack(pady=1)

# Campo de entrada del grafo
entrada = tk.Entry(ventana, width=30)
entrada.pack(pady=2)

# Etiqueta para el campo de entrada del nodo de inicio
start_label = tk.Label(ventana, text="Nodo de inicio:")
start_label.pack(pady=1)

# Campo de entrada del nodo de inicio
start_entry = tk.Entry(ventana, width=10)
start_entry.pack(pady=2)

# Etiqueta para el campo de entrada del nodo de destino
end_label = tk.Label(ventana, text="Nodo de destino:")
end_label.pack(pady=1)

# Campo de entrada del nodo de destino
end_entry = tk.Entry(ventana, width=10)
end_entry.pack(pady=2)

# Botón para procesar el grafo
procesar_boton = tk.Button(ventana, text="Procesar", command=procesar_grafo)
procesar_boton.pack(pady=5)

# Ejecutar el bucle de eventos de la ventana
ventana.mainloop()