import arcade
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from scenes.eula_scene import EulaView
from scenes.menu_scene import MenuView
from scenes.character_select_scene import CharacterSelectView
from scenes.combat_scene import CombatView

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Batalla Cómica Española"

class GameApp(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
        try:
            icon = arcade.load_image('img/icono.png')
            self.set_icon(icon)
        except:
            pass

        self.views = []
        if os.path.exists('eula_accepted.txt'):
            first_view = MenuView(self)
        else:
            first_view = EulaView(self)
        self.views.append(first_view)
        self.show_view(first_view)

    def on_key_press(self, symbol, modifiers):
        if self.current_view:
            self.current_view.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        if self.current_view:
            self.current_view.on_key_release(symbol, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.current_view:
            self.current_view.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_view:
            self.current_view.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.current_view:
            self.current_view.on_mouse_release(x, y, button, modifiers)

    def goto_view(self, view):
        if self.views:
            self.views.pop().on_hide()
        self.views.append(view)
        self.show_view(view)
        view.on_show()

    def push_view(self, view):
        self.views.append(view)
        self.show_view(view)
        view.on_show()

    def pop_view(self):
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