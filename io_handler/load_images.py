import os
from urllib.parse import unquote
from nicegui import app

class ImageLoader:
    def __init__(self):
        self.images = []  # lista de rutas de imágenes
        self.warnings = []

    def load_image(self, path: str):
        """Carga una sola imagen desde una ruta dada."""
        path = unquote(path)  # Decodificar la ruta
        if not os.path.isfile(path):
            self.warnings.append(f"La ruta {path} no existe o no es un archivo.")
            return
        if not path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            self.warnings.append(f"El archivo {path} no es una imagen válida.")
            return
        self.images.append(path)

    def load_images_from_folder(self, folder_path: str):
        """Carga todas las imágenes desde una carpeta dada y las expone a través de una URL estática."""
        folder_path = unquote(folder_path)  # Decodificar la ruta
        if not os.path.isdir(folder_path):
            self.warnings.append(f"La ruta {folder_path} no es una carpeta válida.")
            return []

        # Servir carpeta si no está registrada
        url_prefix = f'/{os.path.basename(folder_path)}'

        # Filtrar imágenes
        image_files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
        ]

        if not image_files:
            self.warnings.append(f"No se encontraron imágenes en la carpeta {folder_path}.")
            return []

        # Construir rutas servibles (URLs)
        self.images = [f'{url_prefix}/{filename}' for filename in image_files]
        return self.images

    
    def get_page(self, page: int, page_size: int = 50):
        """Devuelve una lista de rutas correspondiente a una página."""
        start = page * page_size
        end = start + page_size
        return self.images[start:end]

    def total_pages(self, page_size: int = 50):
        """Calcula el número total de páginas."""
        return (len(self.images) + page_size - 1) // page_size
    