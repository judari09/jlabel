from annotation_and_visualization import AnnotationAndVisualization
from io_handler.save_labels import BoundingBox
from data_io_handler import DataIOHandler
from generate_dataset import YoloDatasetGenerator
from nicegui import ui, app
import os


class main:
    def __init__(self):
        self.annotate_visualize = AnnotationAndVisualization(
            image_url="",
            width=800, height=600)
        self.data_handler = DataIOHandler(save_directory="prueba", file_format='txt', encoding='utf-8', format_label='yolo')
        self.i = 0
        self.classes = []

    def run(self):
        def _assign_label():
            def on_enter(e):
                value = label.value.strip()
                if value:  # ✅ Solo agrega si no está vacío
                    self.classes.append(value)
                    label.delete()
                    print(self.classes)

                    # Aquí ya es seguro trabajar con self.classes[-1]
                    class_index = self.classes.index(value)

                    coords = gp.get_figures()  # ((xmin,ymin), (xmax,ymax))
                    if coords:
                        for coord in coords:
                            if len(coord) != 2:
                                print("❌ Coordenadas inválidas, se requiere un bounding box con dos puntos.")
                                continue
                            (xmin, ymin), (xmax, ymax) = coord
                            if xmin >= xmax or ymin >= ymax:
                                print("❌ Coordenadas inválidas, asegúrese de que xmin < xmax y ymin < ymax.")
                                continue
                            (xmin, ymin), (xmax, ymax) = coord
                            img = images[self.i]
                            img_h, img_w = img.shape[:2]

                            # Normalizar coordenadas
                            x_center = (xmin + xmax) / 2 / img_w
                            y_center = (ymin + ymax) / 2 / img_h
                            w = (xmax - xmin) / img_w
                            h = (ymax - ymin) / img_h

                            bbox = BoundingBox(
                                class_index=class_index,
                                x=x_center,
                                y=y_center,
                                w=w,
                                h=h
                            )
                            self.data_handler.bbox_labels.append(bbox)
                            label_saver.save_label_yolo(images[self.i], [bbox], 'bbox')
                            print(f"Etiqueta asignada: {bbox}")
                else:
                    print("❌ No se agregó ninguna clase, se mantiene en la misma figura.")

            label = ui.input("Etiqueta: ").classes("w-40").on('keydown.enter', on_enter)



        def next_image():
            if self.i < len(images) - 1:
                self.i += 1
            else:
                self.i = 0
            gp.clear()
            drawer.clear()
            drawer.set_image(images[self.i])

        def prev_image():
            if self.i > 0:
                self.i -= 1
            else:
                self.i = len(images) - 1
            gp.clear()
            drawer.clear()
            drawer.load_image(images[self.i])

        # cargar imagenes y etiquetas
        images = self.data_handler.image_loader.load_images_from_folder("prueba")
        print(str(images[self.i]))
        
        label_saver = self.data_handler.label_saver
        #print(images)
        gp = self.annotate_visualize.gp
        drawer = self.annotate_visualize.drawer

        #drawer.load_image(images[self.i])

        # Timer para refrescar el dibujo
        ui.timer(0.1, lambda: drawer.draw(gp.get_figures()))

        # Botones de control
        with ui.row():
            ui.button("Modo Bounding Box", on_click=lambda: drawer.set_mode("bbox"))
            ui.button("Modo Polígono", on_click=lambda: drawer.set_mode("polygon"))
            ui.button("Limpiar", on_click=lambda: [gp.clear(), drawer.clear()])
            ui.button("Nueva Figura", on_click=_assign_label)
            ui.button("Imagen siguiente", on_click=next_image)
            ui.button("Imagen anterior", on_click=prev_image)
            ui.button(
                "Generar dataset",
                on_click=lambda: YoloDatasetGenerator(
                    source_dir="prueba",
                    train_dir="prueba/train",
                    val_dir="prueba/val",
                    split_ratio=0.8,
                    class_names=self.classes,
                    yaml_output_path="prueba/dataset_config.yaml"
                ).generate()
            )
            
        ui.run()


main_class =  main()
main_class.run()