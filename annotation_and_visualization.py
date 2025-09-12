from nicegui import ui
from annotations.get_point import GetPoint
from annotations.draw_label import ShapeDrawer

image_url = "https://picsum.photos/600/400"

collector = GetPoint()
drawer = ShapeDrawer(image_url, 600, 400)

def handle_click(e):
    x, y = e.args.get('offsetX'), e.args.get('offsetY')
    collector.add_point(x, y)
    drawer.draw(collector.get_points())

ui.button("Modo Bounding Box", on_click=lambda: drawer.set_mode("bbox"))
ui.button("Modo Polígono", on_click=lambda: drawer.set_mode("polygon"))
ui.on('click', handle_click)


ui.run()

