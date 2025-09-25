
from fastapi import FastAPI
from annotation_and_visualization import router as get_point_router
from data_io_handler import router as data_io_router
from generate_dataset import router as dataset_router
import os

# Crear la instancia de FastAPI
app = FastAPI()

# Incluir el router de GetPoint
app.include_router(data_io_router, prefix="/data_io", tags=["DataIO"])
app.include_router(get_point_router, prefix="/get_point", tags=["GetPoint"])
app.include_router(dataset_router, prefix="/yolo_dataset", tags=["YoloDataset"])


# Ruta raíz para verificar que el servidor está funcionando
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de anotaciones"}

