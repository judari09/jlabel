from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Tuple
from annotations.get_point import GetPoint

# Crear una instancia de GetPoint
get_point = GetPoint()

# Crear un router para los endpoints relacionados con GetPoint
router = APIRouter()


# Modelo para recibir puntos
class Point(BaseModel):
    x: float
    y: float

# Modelo para crear una nueva figura
class NewFigure(BaseModel):
    figure_type: str

# Endpoint para agregar un punto
@router.post("/add_point/")
def add_point(point: Point):
    """Agrega un punto a la figura actual."""
    try:
        get_point.add_point(point.x, point.y)
        return {
            "message": "Punto agregado correctamente",
            "figures": get_point.get_figures(),
        }
    except TypeError as e:
        return {"error": str(e)}


# Endpoint para iniciar una nueva figura
@router.post("/new_figure/")
def new_figure(new_figure: NewFigure):
    """Inicia una nueva figura del tipo especificado."""
    get_point.new_figure(new_figure.figure_type)
    return {
        "message": f"Nueva figura de tipo '{new_figure.figure_type}' creada",
        "figures": get_point.get_figures(),
    }


# Endpoint para obtener todas las figuras
@router.get("/get_figures/")
def get_figures():
    """Devuelve todas las figuras."""
    return {"figures": get_point.get_figures()}


# Endpoint para limpiar todas las figuras
@router.post("/clear/")
def clear():
    """Limpia todas las figuras."""
    get_point.clear()
    return {
        "message": "Todas las figuras han sido eliminadas",
        "figures": get_point.get_figures(),
    }
