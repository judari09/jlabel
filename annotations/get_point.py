class GetPoint:
    def __init__(self):
        self.figures = [[]]  # lista de figuras, cada figura es una lista de puntos

    def add_point(self, x, y):
        self.figures[-1].append((x, y))  # agrega al último polígono/box

    def new_figure(self):
        """Inicia una nueva figura vacía."""
        self.figures.append([])

    def get_figures(self):
        """Devuelve todas las figuras guardadas."""
        return self.figures

    def clear(self):
        """Limpia todas las figuras."""
        self.figures = [[]]

    def handle_click(self, e):
        x = e.args.get('offsetX')
        y = e.args.get('offsetY')
        self.add_point(x, y)
        print("Figuras actuales:", self.figures)
