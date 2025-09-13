from nicegui import ui
from annotations.get_point import GetPoint
from annotations.draw_label import LabelDrawer

"""Clase que expone la funcionalidad de anotación y visualización de figuras sobre una imagen.
para ser usada en otros módulos.
"""

class AnnotationAndVisualization:
    def __init__(self, image_url: str, width: int, height: int):
        """
        Clase que une la gestión de puntos (GetPoint) con
        el dibujo de figuras (LabelDrawer) sobre una imagen.
        """
        self.gp = GetPoint()                              # encargado de capturar clics
        self.drawer = LabelDrawer(image_url, width, height, self.gp)  # encargado de dibujar

                

annotator = AnnotationAndVisualization(
    image_url="https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d",
    width=800, height=600
)

gp = annotator.gp
drawer = annotator.drawer


# Timer que actualiza el dibujo en tiempo real cada 0.3 segundos
# Dibuja siempre en base a los puntos almacenados en gp
ui.timer(0.1, lambda: drawer.draw(gp.get_figures()))

# Botones de control para cambiar el modo o limpiar el canvas
with ui.row():
    ui.button("Modo Bounding Box", on_click=lambda: drawer.set_mode("bbox"))
    ui.button("Modo Polígono", on_click=lambda: drawer.set_mode("polygon"))
    ui.button("Limpiar", on_click=lambda: [gp.clear(), drawer.clear()])
    ui.button("Nueva Figura", on_click=gp.new_figure)

# Arranca la aplicación de NiceGUI
ui.run()

