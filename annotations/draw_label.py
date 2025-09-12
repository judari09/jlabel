from nicegui import ui
from get_point import GetPoint

# -----------------------
# Clase para dibujar figuras sobre una imagen
# -----------------------
class ShapeDrawer:
    def __init__(self, image_url: str, width: int, height: int, getpoint: GetPoint):
        """
        Inicializa el dibujador de figuras.

        Parámetros:
        - image_url: dirección URL de la imagen que se va a mostrar como fondo.
        - width, height: dimensiones de la imagen y el área de dibujo.
        - getpoint: instancia de la clase GetPoint para registrar clics del usuario.
        """
        self.image_url = image_url
        self.width = width
        self.height = height
        self.mode = "bbox"  # modo de dibujo por defecto ("bbox" o "polygon")
        self.getpoint = getpoint

        # Renderizamos un bloque HTML que contiene la imagen de fondo y un SVG transparente encima
        # El SVG actuará como "overlay" donde se dibujarán las figuras.
        self.html = ui.html(self._template())

        # Asociamos el evento "click" a la función handle_click de GetPoint
        # De esta forma, cada clic del usuario sobre la imagen se guarda como un punto.
        self.html.on('click', self.getpoint.handle_click)

    def _template(self):
        """
        Devuelve una cadena HTML que contiene:
        - Una imagen (bg) que será el fondo clickeable.
        - Un SVG (overlay) transparente encima donde se dibujarán las figuras.
        """
        return f"""
        <div style="position: relative; display: inline-block;">
          <img id="bg" src="{self.image_url}" 
               width="{self.width}" height="{self.height}" 
               style="display: block; cursor: crosshair;">
          <svg id="overlay" width="{self.width}" height="{self.height}"
               style="position: absolute; top: 0; left: 0;"></svg>
        </div>
        """

    def clear(self):
        """
        Limpia todas las figuras dibujadas en el overlay,
        eliminando el contenido del elemento SVG.
        """
        ui.run_javascript("document.getElementById('overlay').innerHTML = '';")

    def draw_bbox(self, figure):
        """
        Dibuja un rectángulo (bounding box) con los puntos dados.
        - Requiere al menos 2 puntos: la esquina superior-izquierda y la inferior-derecha.
        """
        if len(figure) == 0:
            return  # si no hay figuras, no dibuja nada
        elif len(figure) > 1:
            confirmed = figure[:-1]  # todas menos la última figura (confirmadas)
            editing = figure[-1:]# la última figura (en edición)
            
        else:
            confirmed = []  # todas menos la última figura (confirmadas)
            editing = figure# la última figura (en edición)
            
        for points in editing:
            if len(points) < 2:
                return  # si no hay 2 puntos, no dibuja nada

            # Extraemos las coordenadas de los extremos
            x1, y1 = points[0]
            x2, y2 = points[-1]

            # Calculamos la esquina superior-izquierda y las dimensiones del rectángulo
            x_min, y_min = min(x1, x2), min(y1, y2)
            w, h = abs(x2 - x1), abs(y2 - y1)

            # Código JavaScript para crear un rectángulo en el SVG
            js = f"""
                const svg = document.getElementById("overlay");
               
                // Si ya existe un rect con id 'edited', lo borramos (reemplazo de edición)
                const old = document.getElementById("edited");
                if (old) svg.removeChild(old);

                const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
                //dibujo de la bounding box con sus atributos
                rect.setAttribute("id", "edited");
                rect.setAttribute("x", {x_min});
                rect.setAttribute("y", {y_min});
                rect.setAttribute("width", {w});
                rect.setAttribute("height", {h});
                rect.setAttribute("stroke", "lime");
                rect.setAttribute("stroke-width", "2");
                rect.setAttribute("fill", "none");
                svg.appendChild(rect);
                """

            ui.run_javascript(js)
        # Dibujamos las figuras confirmadas (no en edición)
        for idx, points in enumerate(confirmed):
            if len(points) < 2:
                continue  # no dibujamos si no hay 2 puntos

            x1, y1 = points[0]
            x2, y2 = points[-1]
            x_min, y_min = min(x1, x2), min(y1, y2)
            w, h = abs(x2 - x1), abs(y2 - y1)

            js = f"""
                const svg = document.getElementById("overlay");
                const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
                rect.setAttribute("id", "confirmed-{idx}");
                rect.setAttribute("x", {x_min});
                rect.setAttribute("y", {y_min});
                rect.setAttribute("width", {w});
                rect.setAttribute("height", {h});
                rect.setAttribute("stroke", "yellow");
                rect.setAttribute("stroke-width", "2");
                rect.setAttribute("fill", "none");
                svg.appendChild(rect);
            """
            ui.run_javascript(js)

            
    def draw_polygon(self, figure):
        """
        Dibuja uno o varios polígonos con los puntos dados.
        - confirmed: polígonos ya cerrados
        - editing: polígono actual en edición
        """

        if not figure:
            return

        if len(figure) > 1:
            confirmed = figure[:-1]   # todas menos la última
            editing = figure[-1:]     # la última en edición (lista dentro de lista)
        else:
            confirmed = []
            editing = figure          # única figura

        # 1️⃣ Dibujamos los polígonos confirmados
        for points in confirmed:
            if len(points) < 3:
                continue

            points_str = " ".join([f"{x},{y}" for x, y in points])

            js = f"""
            const svg = document.getElementById("overlay");
            const poly = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
            poly.setAttribute("points", "{points_str}");
            poly.setAttribute("stroke", "red");
            poly.setAttribute("stroke-width", "2");
            poly.setAttribute("fill", "rgba(255,0,0,0.3)");
            svg.appendChild(poly);
            """
            ui.run_javascript(js)

        # 2️⃣ Dibujamos el polígono en edición (si existe)
        for points in editing:
            if len(points) < 3:
                continue

            points_str = " ".join([f"{x},{y}" for x, y in points])

            js = f"""
            const svg = document.getElementById("overlay");

            // Eliminamos el polígono de edición previo
            const old = document.getElementById("editing-poly");
            if (old) svg.removeChild(old);

            const poly = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
            poly.setAttribute("id", "editing-poly");
            poly.setAttribute("points", "{points_str}");
            poly.setAttribute("stroke", "orange");                // color distinto para edición
            poly.setAttribute("stroke-width", "2");
            poly.setAttribute("fill", "rgba(255,165,0,0.3)");     // naranja semitransparente
            svg.appendChild(poly);
            """
            ui.run_javascript(js)


    def draw(self, points):
        """
        Decide qué tipo de figura dibujar (bounding box o polígono)
        dependiendo del modo actual.
        """
        if self.mode == "bbox":
            self.draw_bbox(points)
        elif self.mode == "polygon":
            self.draw_polygon(points)

    def set_mode(self, mode: str):
        """
        Cambia el modo de dibujo entre:
        - "bbox": bounding box (rectángulo)
        - "polygon": polígono
        """
        if mode in ["bbox", "polygon"]:
            self.mode = mode


# -----------------------
# Ejemplo de uso de la clase
# -----------------------
if __name__ in {"__main__", "__mp_main__"}:
    # Instancia para guardar los puntos del usuario
    gp = GetPoint()

    # Creamos un ShapeDrawer con una imagen de prueba
    drawer = ShapeDrawer("https://picsum.photos/600/400", 640, 480, gp)

    # Timer que actualiza el dibujo en tiempo real cada 0.3 segundos
    # Dibuja siempre en base a los puntos almacenados en gp
    ui.timer(0.1, lambda: drawer.draw(gp.get_figures()))

    # Botones de control para cambiar el modo o limpiar el canvas
    with ui.row():
        ui.button("Modo Bounding Box", on_click=lambda: drawer.set_mode("bbox"))
        ui.button("Modo Polígono", on_click=lambda: drawer.set_mode("polygon"))
        ui.button("Limpiar", on_click=lambda: [gp.clear(), drawer.clear()])
        ui.button("Nueva Figura", on_click=gp.new_figure)

    # Arranca la aplicación de NiceGUI
    ui.run()
