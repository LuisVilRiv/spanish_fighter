# scenes/base_view.py (sin cambios, pero se recomienda agregar on_resize en todas las subclases)
import arcade

class BaseView(arcade.View):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.ui_elements = []
        self.static_elements = []

    def on_show(self):
        pass

    def on_hide(self):
        pass

    def on_draw(self):
        self.clear()

    def on_update(self, delta_time):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        for elem in self.ui_elements:
            if hasattr(elem, 'on_mouse_press'):
                elem.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for elem in self.ui_elements:
            if hasattr(elem, 'on_mouse_motion'):
                elem.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def on_resize(self, width, height):
        pass