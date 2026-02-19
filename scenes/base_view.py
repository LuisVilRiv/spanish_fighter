# scenes/base_view.py
import arcade
from debug_logger import DBG


class BaseView(arcade.View):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.ui_elements     = []
        self.static_elements = []
        self._block_next_press = True
        DBG.info(f"Vista creada: {type(self).__name__}")

    def on_show(self):
        self._block_next_press = True
        DBG.info(f"on_show: {type(self).__name__}")

    def on_hide(self):
        DBG.info(f"on_hide: {type(self).__name__}")

    def on_draw(self):
        self.clear()

    def on_update(self, delta_time):
        self._block_next_press = False

    def on_mouse_press(self, x, y, button, modifiers):
        """Itera ui_elements con propagación controlada."""
        if self._block_next_press:
            DBG.info(f"Click bloqueado (block_next_press) en {type(self).__name__}", x=x, y=y)
            return False

        if button != arcade.MOUSE_BUTTON_LEFT:
            return False

        for elem in self.ui_elements:
            if hasattr(elem, 'on_mouse_press'):
                if hasattr(elem, 'visible') and not elem.visible:
                    continue
                resultado = elem.on_mouse_press(x, y, button, modifiers)
                if resultado:
                    # origen como primer arg posicional, luego x, y, consumido
                    DBG.click(type(elem).__name__, x, y, True)
                    return True

        DBG.click("ninguno", x, y, False)
        return False

    def on_mouse_motion(self, x, y, dx, dy):
        for elem in self.ui_elements:
            if hasattr(elem, 'on_mouse_motion'):
                if hasattr(elem, 'visible') and not elem.visible:
                    if hasattr(elem, 'hovered'):
                        elem.hovered = False
                    continue
                elem.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def on_resize(self, width, height):
        pass