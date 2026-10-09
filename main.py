from PIL import Image
import numpy as np

from quadtree import Quadtree


# carga la imagen que se va a utilizar
imagen = Image.open("imagenes/prueba.png").convert("RGB")

# convierte la imagen en una matriz de pixeles
matriz = np.array(imagen)


# crea el quadtree y establece la tolerancia
quadtree = Quadtree(matriz, tolerancia=10)


# construye el arbol comenzando desde toda la imagen
arbol = quadtree.construir(
    0,
    0,
    matriz.shape[1],
    matriz.shape[0]
)


# muestra informacion sobre el quadtree construido
print("Quadtree construido correctamente")

# muestra el tamaño de la imagen
print("Tamaño de la imagen:", matriz.shape)

# muestra las coordenadas donde comienza la raiz
print("Raíz:", arbol.x, arbol.y)

# muestra el ancho de la region de la raiz
print("Ancho:", arbol.ancho)

# muestra el alto de la region de la raiz
print("Alto:", arbol.alto)

# indica si la raiz es una hoja
print("¿La raíz es hoja?:", arbol.es_hoja())


# crea una matriz vacia del mismo tamaño que la imagen original
reconstruida = np.zeros_like(matriz)


# reconstruye la imagen utilizando el quadtree
quadtree.reconstruir(arbol, reconstruida)


# convierte la matriz reconstruida nuevamente en una imagen
imagen_reconstruida = Image.fromarray(reconstruida)


# guarda la imagen reconstruida en la carpeta correspondiente
imagen_reconstruida.save("reconstruidas/prueba_reconstruida.png")


# muestra un mensaje indicando que la reconstruccion termino
print("Imagen reconstruida correctamente")

# muestra la ubicacion donde se guardo la imagen
print("Guardada en: reconstruidas/prueba_reconstruida.png")