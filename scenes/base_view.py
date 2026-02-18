# scenes/base_view.py
import arcade

class BaseView(arcade.View):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.ui_elements = []
        self.static_elements = []
        # Bloquea el primer on_mouse_press tras mostrar la vista,
        # evitando que el clic que activó el cambio de vista se propague
        # a la nueva vista (que puede tener botones en las mismas coords).
        self._block_next_press = True

    def on_show(self):
        # Cada vez que la vista se muestra, bloquear el siguiente press.
        self._block_next_press = True

    def on_hide(self):
        pass

    def on_draw(self):
        self.clear()

    def on_update(self, delta_time):
        # Tras el primer frame renderizado, ya es seguro recibir input.
        self._block_next_press = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self._block_next_press:
            return
        for elem in self.ui_elements:
            if hasattr(elem, 'on_mouse_press'):
                # Si el elemento consume el clic (devuelve True), parar.
                # Evita que múltiples botones en la misma posición disparen.
                if elem.on_mouse_press(x, y, button, modifiers):
                    return

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