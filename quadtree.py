import numpy as np


# clase que representa cada nodo del quadtree
class NodoQuadtree:

    # inicializa los datos de cada nodo
    def __init__(self, x, y, ancho, alto, color=None):

        # coordenadas donde comienza la region
        self.x = x
        self.y = y

        # tamaño de la region
        self.ancho = ancho
        self.alto = alto

        # color que representa la region cuando es una hoja
        self.color = color

        # cada nodo puede tener hasta 4 hijos
        # 0 = arriba izquierda
        # 1 = arriba derecha
        # 2 = abajo izquierda
        # 3 = abajo derecha
        self.hijos = [None, None, None, None]

    # verifica si el nodo no tiene hijos
    def es_hoja(self):
        return all(hijo is None for hijo in self.hijos)


# clase principal que se encarga de construir y recorrer el quadtree
class Quadtree:

    # recibe la imagen y la tolerancia que se utilizara
    def __init__(self, imagen, tolerancia=0):
        self.imagen = imagen
        self.tolerancia = tolerancia

    # verifica si los pixeles de una region tienen colores suficientemente parecidos
    def es_uniforme(self, region):

        # convierte los pixeles de la region en una lista de colores
        pixeles = region.reshape(-1, region.shape[-1])

        # calcula el color promedio de todos los pixeles de la region
        promedio = np.mean(pixeles, axis=0)

        # calcula la diferencia entre cada pixel y el color promedio
        diferencias = np.abs(pixeles - promedio)

        # obtiene la diferencia mas grande encontrada
        diferencia_maxima = np.max(diferencias)

        # si la diferencia esta dentro de la tolerancia
        # la region se considera uniforme
        return diferencia_maxima <= self.tolerancia


    # construye el quadtree utilizando recursividad
    def construir(self, x, y, ancho, alto):

        # obtiene los pixeles que pertenecen a la region actual
        region = self.imagen[y:y + alto, x:x + ancho]

        # caso base: si la region tiene un solo pixel
        if ancho == 1 and alto == 1:

            # obtiene el color del pixel
            color = region[0, 0].copy()

            # crea un nodo hoja con ese color
            return NodoQuadtree(x, y, ancho, alto, color)


        # verifica si la region es suficientemente uniforme
        if self.es_uniforme(region):

            # calcula el color promedio de la region
            color = np.mean(
                region.reshape(-1, region.shape[-1]),
                axis=0
            ).astype(np.uint8)

            # crea un nodo hoja con el color promedio
            return NodoQuadtree(x, y, ancho, alto, color)


        # si la region no es uniforme se divide en cuatro partes
        mitad_ancho = ancho // 2
        mitad_alto = alto // 2

        # crea un nodo padre para almacenar las cuatro regiones
        nodo = NodoQuadtree(x, y, ancho, alto)


        # crea la region de arriba a la izquierda
        if mitad_ancho > 0 and mitad_alto > 0:

            nodo.hijos[0] = self.construir(
                x, y,
                mitad_ancho,
                mitad_alto
            )


        # crea la region de arriba a la derecha
        if ancho - mitad_ancho > 0 and mitad_alto > 0:

            nodo.hijos[1] = self.construir(
                x + mitad_ancho,
                y,
                ancho - mitad_ancho,
                mitad_alto
            )


        # crea la region de abajo a la izquierda
        if mitad_ancho > 0 and alto - mitad_alto > 0:

            nodo.hijos[2] = self.construir(
                x,
                y + mitad_alto,
                mitad_ancho,
                alto - mitad_alto
            )


        # crea la region de abajo a la derecha
        if ancho - mitad_ancho > 0 and alto - mitad_alto > 0:

            nodo.hijos[3] = self.construir(
                x + mitad_ancho,
                y + mitad_alto,
                ancho - mitad_ancho,
                alto - mitad_alto
            )


        # regresa el nodo que contiene las cuatro regiones
        return nodo


    # reconstruye la imagen utilizando el quadtree
    def reconstruir(self, nodo, salida):

        # si el nodo es una hoja significa que toda su region
        # puede representarse con un solo color
        if nodo.es_hoja():

            # asigna el color del nodo a todos los pixeles de su region
            salida[
                nodo.y:nodo.y + nodo.alto,
                nodo.x:nodo.x + nodo.ancho
            ] = nodo.color

            return


        # si no es una hoja recorre cada uno de sus hijos
        for hijo in nodo.hijos:

            # verifica que el hijo exista
            if hijo is not None:

                # reconstruye la region de forma recursiva
                self.reconstruir(hijo, salida)