from nicegui import ui


# -----------------------
# Clase encargada de generar el HTML, SVG y JS (Renderer)
# -----------------------
class LabelDrawerRenderer:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def template(self) -> str:
        """Solo devuelve el overlay SVG, no la imagen."""
        return f"""
        <svg id="overlay" 
             style="position: absolute; top: 0; left: 0; 
                    width: {self.width}px; height: {self.height}px; 
                    pointer-events: all; object-fit:contain; cursor:crosshair;</svg>
        """

    def render_bbox(
        self, bboxes: list[tuple], editing: list[tuple] | None = None
    ) -> str:
        """Genera SVG para bounding boxes."""
        svg_elements = []
        for i, (x1, y1, x2, y2) in enumerate(bboxes):
            svg_elements.append(
                f'<rect id="confirmed-bbox-{i}" x="{x1}" y="{y1}" '
                f'width="{x2-x1}" height="{y2-y1}" '
                f'stroke="lime" stroke-width="2" fill="none"/>'
            )
        if editing:
            x1, y1, x2, y2 = editing
            svg_elements.append(
                f'<rect id="edited-bbox" x="{x1}" y="{y1}" '
                f'width="{x2-x1}" height="{y2-y1}" '
                f'stroke="orange" stroke-width="2" fill="rgba(255,165,0,0.1)"/>'
            )
        return "".join(svg_elements)

    def render_polygons(
        self, polygons: list[list[tuple]], editing: list[tuple] | None = None
    ) -> str:
        """Genera SVG para polígonos."""
        svg_elements = []
        for i, poly in enumerate(polygons):
            points_str = " ".join(f"{x},{y}" for x, y in poly)
            svg_elements.append(
                f'<polygon id="confirmed-poly-{i}" points="{points_str}" '
                f'stroke="yellow" stroke-width="2" fill="none"/>'
            )
        if editing:
            points_str = " ".join(f"{x},{y}" for x, y in editing)
            svg_elements.append(
                f'<polygon id="edited-poly" points="{points_str}" '
                f'stroke="orange" stroke-width="2" fill="rgba(255,165,0,0.1)"/>'
            )
        return "".join(svg_elements)

    def update_overlay(self, svg_content: str):
        """Ejecuta el JS para actualizar el SVG en la UI."""
        ui.run_javascript(
            f'document.getElementById("overlay").innerHTML = `{svg_content}`;'
        )


# -----------------------
# Controlador principal que usa el Renderer
# -----------------------
class LabelDrawer:
    def __init__(
        self,
        image_path: str,
        width: int = 640,
        height: int = 480,
        mode: str = "bbox",
        gp=None,
    ):
        if not image_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            raise ValueError("El archivo no es una imagen válida.")

        self.mode = mode
        self.renderer = LabelDrawerRenderer(width, height)
        self.gp = gp
        with ui.column().style("position: relative; width: fit-content;"):
            self.image = ui.image(image_path).style(
                f"width:{width}px; height:{height}px; object-fit:contain;"
            )
            self.overlay = (
                ui.html(self.renderer.template())
                .style(
                    f"position:absolute; top:0; left:0; width:{width}px; height:{height}px;pointer-events: all;cursor:crosshair;"
                )
                .on("click", lambda e: self._handle_click(e))
            )


    def _handle_click(self, e):
        data = e.args or {}  # args viene con el detail
        x = data.get("x")
        y = data.get("y")
        ui.notify(f"Clic en imagen: {x}, {y}")
        print(f"Clic en imagen: {x}, {y}")
        if self.gp:
            self.gp.handle_click(x, y)

    def set_image(self, image_url: str):
        """Cambia la imagen de fondo fácilmente."""
        self.image.set_source(image_url)
        self.clear()

    def set_mode(self, mode: str):
        if mode not in ("bbox", "polygon"):
            raise ValueError("Modo inválido, use 'bbox' o 'polygon'.")
        self.mode = mode

    def draw(self, figures: list, editing: list | None = None):
        if self.mode == "bbox":
            svg_content = self.renderer.render_bbox(figures, editing)
        elif self.mode == "polygon":
            svg_content = self.renderer.render_polygons(figures, editing)
        else:
            raise ValueError(f"Modo no soportado: {self.mode}")

        self.renderer.update_overlay(svg_content)

    def clear(self):
        self.renderer.update_overlay("")
