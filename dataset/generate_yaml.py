import os
import yaml  # PyYAML
from urllib.parse import unquote

class YoloDatasetConfig:
    def __init__(
        self,
        root_path: str,
        train_dir: str,
        val_dir: str,
        test_dir: str = None,
        class_names: list = None,
    ):
        """
        Clase para generar archivos .yaml de configuración de datasets YOLO.

        Parámetros:
        - root_path (str): directorio raíz del dataset.
        - train_dir (str): ruta relativa a las imágenes de entrenamiento.
        - val_dir (str): ruta relativa a las imágenes de validación.
        - test_dir (str, opcional): ruta relativa a las imágenes de test.
        - class_names (list): lista de nombres de clases.
        """
        self.root_path = root_path
        self.train_dir = train_dir
        self.val_dir = val_dir
        self.test_dir = test_dir
        self.class_names = class_names or []

    def to_dict(self) -> dict:
        """Convierte la configuración a diccionario compatible con YOLO."""
        data = {
            "path": self.root_path,
            "train": self.train_dir,
            "val": self.val_dir,
        }
        if self.test_dir:
            data["test"] = self.test_dir

        # Formato requerido: {id: name}
        data["names"] = dict(enumerate(self.class_names))
        return data

    def save(self, output_path: str):
        """Guarda el archivo YAML en la ruta especificada."""
        # Crear el directorio si no existe
        output_path = unquote(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        data = self.to_dict()
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)

        print(f"Archivo YAML guardado en: {output_path}")


if __name__ == "__main__":
    # Ejemplo de uso
    config = YoloDatasetConfig(
        root_path="/ruta/al/dataset",
        train_dir="train/images",
        val_dir="val/images",
        test_dir="test/images",
        class_names=["persona", "bicicleta", "coche"],
    )
    config.save("dataset_config.yaml")
