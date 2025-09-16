from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Figure:
    figure_type: str  # "bbox", "polygon", "obb"
    points: List[Tuple[float, float]]

class GetPoint:
    def __init__(self):
        self.figures: List[Figure] = [Figure("bbox", [])]

    def add_point(self, x: float, y: float):
        """Agrega un punto a la última figura activa."""
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("Las coordenadas deben ser numéricas")
        self.figures[-1].points.append((x, y))

    def new_figure(self, figure_type="polygon"):
        """Inicia una nueva figura vacía del tipo indicado."""
        self.figures.append(Figure(figure_type, []))

    def get_figures(self) -> List[Figure]:
        """Devuelve todas las figuras."""
        return self.figures

    def clear(self):
        """Limpia todas las figuras."""
        self.figures = [Figure("polygon", [])]

    def handle_click(self, x: float, y: float):
        """Maneja un clic (abstraído de la UI)."""
        self.add_point(x, y)
        print("Figuras actuales:", self.figures, flush=True)
