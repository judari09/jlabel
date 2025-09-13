import os 
from dataclasses import dataclass
from typing import List, Tuple
@dataclass
class BoundingBox:
    class_index: int
    x: float
    y: float
    w: float
    h: float

    def __post_init__(self):
        if not isinstance(self.class_index, int):
            raise TypeError("class index debe ser un entero")
        if self.w <= 0 or self.h <= 0:
            raise ValueError("El ancho y alto del bounding box deben ser positivos")
        if not (0 <= self.x <= 1 and 0 <= self.y <= 1):
            raise ValueError("Las coordenadas deben estar normalizadas entre 0 y 1")


@dataclass
class Segmentation:
    class_index: int
    points: List[Tuple[float, float]]

    def __post_init__(self):
        if not isinstance(self.class_index, int):
            raise TypeError("class_index debe ser un entero")
        if len(self.points) < 3:
            raise ValueError("Una segmentación debe tener al menos 3 puntos")
        for (x, y) in self.points:
            if not (0 <= x <= 1 and 0 <= y <= 1):
                raise ValueError("Los puntos de segmentación deben estar normalizados entre 0 y 1")


@dataclass
class obbox:
    class_index: int
    points: List[Tuple[float, float]]  # 4 vértices (x, y)

    def __post_init__(self):
        if not isinstance(self.class_index, int):
            raise TypeError("class_index debe ser un entero")
        if len(self.points) != 4:
            raise ValueError("Un OBB debe tener exactamente 4 puntos (x1,y1 ... x4,y4)")
        for (x, y) in self.points:
            if not (0 <= x <= 1 and 0 <= y <= 1):
                raise ValueError("Los puntos OBB deben estar normalizados entre 0 y 1")

    def to_yolo_format(self) -> str:
        coords = " ".join([f"{x:.6f} {y:.6f}" for x, y in self.points])
        return f"{self.class_index} {coords}"


class LabelSaver:
    def __init__(self, save_directory: str, file_format: str = 'txt', encoding: str = 'utf-8', format_label: str = 'yolo'):
        self.file_format = file_format
        self.encoding = encoding
        self.format_label = format_label
        self.save_directory = save_directory
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
            
    def save_label_yolo(self, image_name: str, labels: list, type_label: str):
        """Guarda las etiquetas en formato YOLO. y puede ser 'bbox', 'segmentation' o 'obbox'
        ademas verifica que los objetos en labels sean del tipo correcto."""
        base_name = os.path.splitext(os.path.basename(image_name))[0]
        label_path = os.path.join(self.save_directory, f"{base_name}.{self.file_format}")
        with open(label_path, 'w', encoding=self.encoding) as f:
            
            if type_label == 'bbox':
                    for label in labels:# ahora label es BoundingBox
                        if not isinstance(label, BoundingBox):
                            raise TypeError("Se esperaba un objeto 'BoundingBox'")
                        f.write(f"{label.class_id} {label.x_center} {label.y_center} {label.width} {label.height}\n")
                        
            elif type_label == 'segmentation':
                    for label in labels:  # ahora label es Segmentation
                        if not isinstance(label, Segmentation):
                            raise TypeError("Se esperaba un objeto 'Segmentation'")
                        points_str = ' '.join(f"{x} {y}" for x, y in label.points)
                        f.write(f"{label.class_id} {points_str}\n")
                        
            elif type_label == 'obbox':
                    for label in labels:  # ahora label es obbox
                        if not isinstance(label, obbox):
                            raise TypeError("Se esperaba un objeto 'obbox'")
                        points_str = ' '.join(f"{x} {y}" for x, y in label.points)
                        f.write(f"{label.class_id} {points_str}\n")
            else:
                raise ValueError("type_label debe ser 'bbox' o 'segmentation'")
