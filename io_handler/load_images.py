import os

class ImageLoader:
    def __init__(self):
        self.images = []  # lista de rutas de imágenes
        self.warnings = []

    def load_image(self, path: str):
        """Carga una sola imagen desde una ruta dada."""
        if not os.path.isfile(path):
            self.warnings.append(f"La ruta {path} no existe o no es un archivo.")
            return
        if not path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            self.warnings.append(f"El archivo {path} no es una imagen válida.")
            return
        self.images.append(path)

    def load_images_from_folder(self, folder_path: str):
        """Carga todas las imágenes desde una carpeta dada."""
        if not os.path.isdir(folder_path):
            self.warnings.append(f"La ruta {folder_path} no es una carpeta válida.")
            return

        # Filtrar solo imágenes válidas
        image_files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
        ]

        if not image_files:
            self.warnings.append(f"No se encontraron imágenes en la carpeta {folder_path}.")
            return

        for filename in image_files:
            path = os.path.join(folder_path, filename)
            self.images.append(path)

    def get_page(self, page: int, page_size: int = 50):
        """Devuelve una lista de rutas correspondiente a una página."""
        start = page * page_size
        end = start + page_size
        return self.images[start:end]

    def total_pages(self, page_size: int = 50):
        """Calcula el número total de páginas."""
        return (len(self.images) + page_size - 1) // page_size
    