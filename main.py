import arcade
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from scenes.eula_scene import EulaView
from scenes.menu_scene import MenuView
from scenes.character_select_scene import CharacterSelectView
from scenes.combat_scene import CombatView

SCREEN_WIDTH  = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE  = "Batalla Cómica Española"


class GameApp(arcade.Window):
    def __init__(self):
        # resizable=True permite redimensionar manualmente y también es
        # necesario para que set_fullscreen() funcione correctamente.
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
                         resizable=True)
        try:
            self.set_icon('img/icono.png')  # type: ignore[arg-type]
        except Exception:
            pass

        self.views: list = []
        first_view = MenuView(self) if os.path.exists('eula_accepted.txt') else EulaView(self)
        self.views.append(first_view)
        self.show_view(first_view)

    # ── Teclas globales ───────────────────────────────────────────────────
    def on_key_press(self, symbol, modifiers):
        # F11: alternar pantalla completa desde cualquier escena
        if symbol == arcade.key.F11:
            self.set_fullscreen(not self.fullscreen)
            return
        if self.current_view:
            self.current_view.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        if self.current_view:
            self.current_view.on_key_release(symbol, modifiers)

    # ── Ratón ─────────────────────────────────────────────────────────────
    def on_mouse_motion(self, x, y, dx, dy):
        if self.current_view:
            self.current_view.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_view:
            self.current_view.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.current_view:
            self.current_view.on_mouse_release(x, y, button, modifiers)

    # ── Redimensionado ────────────────────────────────────────────────────
    def on_resize(self, width, height):
        super().on_resize(width, height)
        if self.current_view and hasattr(self.current_view, 'on_resize'):
            self.current_view.on_resize(width, height)

    # ── Gestión de vistas ─────────────────────────────────────────────────
    def goto_view(self, view):
        """Reemplaza la vista actual (descarta la anterior)."""
        if self.views:
            self.views.pop().on_hide()
        self.views.append(view)
        self.show_view(view)
        view.on_show()

    def push_view(self, view):
        """Apila una vista nueva encima (la anterior queda en el stack)."""
        self.views.append(view)
        self.show_view(view)
        view.on_show()

    def pop_view(self):
        """Vuelve a la vista anterior."""
        if len(self.views) > 1:
            old = self.views.pop()
            old.on_hide()
            self.show_view(self.views[-1])
            self.views[-1].on_show()
        else:
            arcade.close_window()


if __name__ == "__main__":
    app = GameApp()
    arcade.run()