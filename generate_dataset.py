from fastapi import APIRouter, HTTPException
from dataset.separar_train_val import YoloDatasetSplitter
from dataset.generate_yaml import YoloDatasetConfig
import os
from typing import List

router = APIRouter()


@router.post("/split_dataset/")
def split_dataset(
    source_dir: str, train_dir: str, val_dir: str, split_ratio: float = 0.8
):
    """
    Divide un dataset en conjuntos de entrenamiento y validación.
    """
    try:
        splitter = YoloDatasetSplitter(source_dir, train_dir, val_dir, split_ratio)
        splitter.split()
        return {
            "message": "Dataset dividido correctamente",
            "train_dir": train_dir,
            "val_dir": val_dir,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate_yaml/")
def generate_yaml(
    root_path: str,
    train_dir: str,
    val_dir: str,
    class_names: List[str],
    yaml_output_path: str,
    test_dir: str = None,
):
    """
    Genera un archivo YAML para la configuración de un dataset YOLO.
    """
    try:
        config = YoloDatasetConfig(
            root_path=root_path,
            train_dir=train_dir,
            val_dir=val_dir,
            test_dir=test_dir,
            class_names=class_names,
        )
        config.save(yaml_output_path)
        return {"message": f"Archivo YAML generado en {yaml_output_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


