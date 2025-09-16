from ui.draw_label import LabelDrawer
from data_io_handler import DataIOHandler
from annotation_and_visualization import AnnotationAndVisualization
from nicegui import ui, app
import os


class UserInterface:
    def __init__(self):
        self.IMAGE_DIR = "prueba"
        self.gp = AnnotationAndVisualization().gp
        # Servir la carpeta de imágenes como estáticos
        app.add_static_files("/prueba", self.IMAGE_DIR)

        self.data_io_handler = DataIOHandler("prueba", "txt", "utf-8", "yolo")
        self.image_loader = self.data_io_handler.image_loader

        # Cargar rutas absolutas
        self.images = self.image_loader.load_images_from_folder(self.IMAGE_DIR)
        self.i = 0

        # Convertir la primera imagen a URL accesible desde el navegador
        first_image_url = f"/prueba/{os.path.basename(self.images[self.i])}"

        self.drawer = LabelDrawer(
            first_image_url, width=500, height=400, mode="bbox", gp=self.gp
        )

    def next_image(self):
        self.i = (self.i + 1) % len(self.images)
        self.drawer.clear()

        # Convertir la ruta local en URL pública
        image_url = f"/prueba/{os.path.basename(self.images[self.i])}"
        print(f"Mostrando:{image_url}", flush=True)
        self.drawer.set_image(image_url)

    def prev_image(self):
        self.i = (self.i - 1) % len(self.images)
        self.drawer.clear()

        image_url = f"/prueba/{os.path.basename(self.images[self.i])}"
        print("Mostrando:", image_url, flush=True)
        self.drawer.set_image(image_url)

    def run(self):
        ui.label("Anotador de imágenes").style(
            "font-size: 24px; font-weight: bold; margin-bottom: 10px;"
        )
        with ui.row().style("align-items: center; gap: 10px; margin-bottom: 10px;"):
            ui.button("imagen siguiente", on_click=lambda: self.next_image())
            ui.button("imagen anterior", on_click=lambda: self.prev_image())
        
        # 👇 Mostrar la imagen con el overlay
        with ui.row():
            self.drawer  # El constructor de LabelDrawer ya crea la UI

        ui.run()


ui_class = UserInterface()
ui_class.run()
