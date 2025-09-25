from fastapi import APIRouter, HTTPException
from typing import List
from io_handler.load_images import ImageLoader
from io_handler.load_labels import Labelloader
from io_handler.save_labels import LabelSaver, BoundingBox, Segmentation, obbox
from collections import UserList

router = APIRouter()
image_loader = ImageLoader()
label_loader = Labelloader()

# Instancia de LabelSaver (se debe configurar el directorio de guardado)
label_saver = LabelSaver(save_directory="output")


class BoundingBoxList(UserList):
    def append(self, item):
        if not isinstance(item, BoundingBox):
            raise TypeError("Solo se permiten objetos BoundingBox")
        super().append(item)


class SegmentationList(UserList):
    def append(self, item):
        if not isinstance(item, Segmentation):
            raise TypeError("Solo se permiten objetos Segmentation")
        super().append(item)


class ObboxList(UserList):
    def append(self, item):
        if not isinstance(item, obbox):
            raise TypeError("Solo se permiten objetos obbox")
        super().append(item)


@router.post("/load_image/")
def load_image(path: str):
    """Carga una sola imagen desde una ruta dada."""
    image_loader.load_image(path)
    if image_loader.warnings:
        raise HTTPException(status_code=400, detail=image_loader.warnings[-1])
    return {"message": "Imagen cargada correctamente", "images": image_loader.images}


@router.post("/load_images_from_folder/")
def load_images_from_folder(folder_path: str):
    """Carga todas las imágenes desde una carpeta dada."""
    images = image_loader.load_images_from_folder(folder_path)
    if image_loader.warnings:
        raise HTTPException(status_code=400, detail=image_loader.warnings[-1])
    return {"message": "Imágenes cargadas correctamente", "images": images}


@router.get("/get_images/")
def get_images(page: int = 0, page_size: int = 50):
    """Devuelve una lista de imágenes correspondiente a una página."""
    return {"images": image_loader.get_page(page, page_size)}


@router.post("/load_label/")
def load_label(path: str):
    """Carga una sola etiqueta desde una ruta dada."""
    label_loader.load_label(path)
    if label_loader.warnings:
        raise HTTPException(status_code=400, detail=label_loader.warnings[-1])
    return {"message": "Etiqueta cargada correctamente", "labels": label_loader.labels}


@router.post("/load_labels_from_folder/")
def load_labels_from_folder(folder_path: str):
    """Carga todas las etiquetas desde una carpeta dada."""
    label_loader.load_labels_from_folder(folder_path)
    if label_loader.warnings:
        raise HTTPException(status_code=400, detail=label_loader.warnings[-1])
    return {
        "message": "Etiquetas cargadas correctamente",
        "labels": label_loader.labels,
    }


@router.get("/get_labels/")
def get_labels(page: int = 0, page_size: int = 50):
    """Devuelve una lista de etiquetas correspondiente a una página."""
    return {"labels": label_loader.get_page(page, page_size)}


@router.get("/total_pages/")
def total_pages(page_size: int = 50):
    """Devuelve el número total de páginas."""
    return {"total_pages": label_loader.total_pages(page_size)}


@router.post("/save_bbox_labels/")
def save_bbox_labels(image_name: str, labels: List[BoundingBox]):
    """Guarda etiquetas de tipo BoundingBox en formato YOLO."""
    try:
        label_saver.save_label_yolo(image_name, labels, type_label="bbox")
        return {"message": "Etiquetas BoundingBox guardadas correctamente"}
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/save_segmentation_labels/")
def save_segmentation_labels(image_name: str, labels: List[Segmentation]):
    """Guarda etiquetas de tipo Segmentation en formato YOLO."""
    try:
        label_saver.save_label_yolo(image_name, labels, type_label="segmentation")
        return {"message": "Etiquetas de segmentación guardadas correctamente"}
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/save_obbox_labels/")
def save_obbox_labels(image_name: str, labels: List[obbox]):
    """Guarda etiquetas de tipo OBB en formato YOLO."""
    try:
        label_saver.save_label_yolo(image_name, labels, type_label="obbox")
        return {"message": "Etiquetas OBB guardadas correctamente"}
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
