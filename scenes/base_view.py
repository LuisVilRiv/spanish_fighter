import arcade

class BaseView(arcade.View):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.ui_elements = []          # Lista de elementos interactivos (botones)
        self.static_elements = []      # Lista de sprites / elementos que no requieren update

    def on_show(self):
        """Se llama cuando la vista se vuelve activa."""
        pass

    def on_hide(self):
        """Se llama cuando la vista se abandona."""
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