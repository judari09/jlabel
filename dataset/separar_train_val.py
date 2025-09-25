import os
import shutil
import random
from urllib.parse import unquote

class YoloDatasetSplitter:
    def __init__(self, source_dir: str, train_dir: str, val_dir: str, split_ratio: float = 0.8):
        """
        Clase para dividir un dataset en conjuntos de entrenamiento y validación.

        Parámetros:
        - source_dir (str): carpeta con las imágenes y etiquetas.
        - train_dir (str): carpeta donde se guardarán las imágenes/labels de entrenamiento.
        - val_dir (str): carpeta donde se guardarán las imágenes/labels de validación.
        - split_ratio (float): proporción de datos para entrenamiento (por defecto 0.8).
        """
        
        self.source_dir = unquote(source_dir)
        self.train_dir = unquote(train_dir)
        self.val_dir = unquote(val_dir)
        self.split_ratio = split_ratio

        # Crear carpetas de destino si no existen
        for folder in [train_dir, val_dir]:
            os.makedirs(os.path.join(folder, "images"), exist_ok=True)
            os.makedirs(os.path.join(folder, "labels"), exist_ok=True)

    def split(self):
        """Separa los datos en entrenamiento y validación."""
        # Obtener lista de imágenes
        files = [f for f in os.listdir(self.source_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        random.shuffle(files)

        # División según split_ratio
        num_train = int(len(files) * self.split_ratio)
        train_files = files[:num_train]
        val_files = files[num_train:]

        # Mover archivos
        for file in train_files:
            self._move_file(file, self.train_dir)
        for file in val_files:
            self._move_file(file, self.val_dir)

        print(f"✅ Datos separados: {len(train_files)} en entrenamiento, {len(val_files)} en validación")

    def _move_file(self, file: str, destination_dir: str):
        """Copia imagen y su etiqueta asociada a la carpeta destino."""
        name, _ = os.path.splitext(file)
        image_src = os.path.join(self.source_dir, file)
        label_src = os.path.join(self.source_dir, name + ".txt")

        shutil.copy2(image_src, os.path.join(destination_dir, "images", file))
        if os.path.exists(label_src):
            shutil.copy2(label_src, os.path.join(destination_dir, "labels", name + ".txt"))


if __name__ == "__main__":
    splitter = YoloDatasetSplitter(
    source_dir="dataset",
    train_dir="dataset_split/train",
    val_dir="dataset_split/val",
    split_ratio=0.8
)

    splitter.split()
    """dataset_split/
    ├── train/
    │   ├── images/
    │   └── labels/
    ├── val/
    │   ├── images/
    │   └── labels/
    """

