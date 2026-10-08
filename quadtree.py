class NodoQuadtree;
def __init__(self, x, y, ancho, alto, color=None):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.color = color

        # hijos: arriba-izquierda, arriba-derecha,
        # abajo-izquierda, abajo-derecha
        self.hijos = [None, None, None, None]

    def es_hoja(self):
        return all(hijo is None for hijo in self.hijos)