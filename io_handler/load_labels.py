import os 

class Labelloader:
    def __init__(self):
        self.labels = []  # lista de rutas de etiquetas
        self.warnings = []

    def load_label(self, path: str):
        """Carga una sola etiqueta desde una ruta dada."""
        if not os.path.isfile(path):
            self.warnings.append(f"La ruta {path} no existe o no es un archivo.")
            return
        if not path.lower().endswith(('.txt', '.xml', '.json', '.csv')):
            self.warnings.append(f"El archivo {path} no es una etiqueta válida.")
            return
        self.labels.append(path)

    def load_labels_from_folder(self, folder_path: str):
        """Carga todas las etiquetas desde una carpeta dada."""
        if not os.path.isdir(folder_path):
            self.warnings.append(f"La ruta {folder_path} no es una carpeta válida.")
            return

        # Filtrar solo etiquetas válidas
        label_files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(('.txt', '.xml', '.json', '.csv'))
        ]

        if not label_files:
            self.warnings.append(f"No se encontraron etiquetas en la carpeta {folder_path}.")
            return

        for filename in label_files:
            path = os.path.join(folder_path, filename)
            self.labels.append(path)

    def get_page(self, page: int, page_size: int = 50):
        """Devuelve una lista de rutas correspondiente a una página."""
        start = page * page_size
        end = start + page_size
        return self.labels[start:end]

    def total_pages(self, page_size: int = 50):
        """Calcula el número total de páginas."""
        return (len(self.labels) + page_size - 1) // page_size