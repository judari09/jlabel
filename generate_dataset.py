from dataset.separar_train_val import YoloDatasetSplitter
from dataset.generate_yaml import YoloDatasetConfig
import os

class YoloDatasetGenerator:
    def __init__(self, source_dir: str, train_dir: str, val_dir: str, split_ratio: float, class_names: list, yaml_output_path: str):
        self.splitter = YoloDatasetSplitter(source_dir, train_dir, val_dir, split_ratio)
        self.config = YoloDatasetConfig(
            root_path=os.path.abspath(source_dir),
            train_dir=os.path.relpath(os.path.join(train_dir, "images"), start=source_dir),
            val_dir=os.path.relpath(os.path.join(val_dir, "images"), start=source_dir),
            class_names=class_names
        )
        self.yaml_output_path = yaml_output_path

    def generate(self):
        self.splitter.split()
        self.config.save(self.yaml_output_path)