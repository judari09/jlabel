from nicegui import ui
from annotations.get_point import GetPoint

"""Clase que expone la funcionalidad de anotación y visualización de figuras sobre una imagen.
para ser usada en otros módulos.
"""

class AnnotationAndVisualization:
    def __init__(self):
        """
        Clase que une la gestión de puntos (GetPoint) con
        el dibujo de figuras (LabelDrawer) sobre una imagen.
        """
        self.gp = GetPoint()                              # encargado de capturar clics

                

