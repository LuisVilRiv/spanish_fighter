import pyglet
from pyglet.window import key, mouse
import sys
import os

# Asegurar que el directorio actual esté en el path
sys.path.insert(0, os.path.dirname(__file__))

from scenes.eula_scene import EulaScene
from scenes.menu_scene import MenuScene
from scenes.character_select_scene import CharacterSelectScene
from scenes.combat_scene import CombatScene

# Configuración de la ventana
ANCHO = 1024
ALTO = 768
TITULO = "Batalla Cómica Española"

class GameApp:
    def __init__(self):
        self.window = pyglet.window.Window(ANCHO, ALTO, TITULO)
        self.window.push_handlers(self)
        
        # Cargar icono (opcional)
        try:
            icono = pyglet.image.load('img/icono.png')
            self.window.set_icon(icono)
        except:
            pass

        # Pila de escenas (la última es la activa)
        self.scenes = []
        
        # Escena inicial: EULA
        self.goto_scene(EulaScene(self))
        
        # Reloj para FPS
        pyglet.clock.schedule_interval(self.update, 1/60.0)

    def run(self):
        pyglet.app.run()

    def on_draw(self):
        self.window.clear()
        if self.scenes:
            self.scenes[-1].draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.scenes:
            self.scenes[-1].on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.scenes:
            self.scenes[-1].on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        if self.scenes:
            self.scenes[-1].on_key_press(symbol, modifiers)

    def update(self, dt):
        if self.scenes:
            self.scenes[-1].update(dt)

    def goto_scene(self, scene):
        """Cambia a una nueva escena, eliminando la anterior."""
        if self.scenes:
            self.scenes.pop().on_exit()
        self.scenes.append(scene)
        scene.on_enter()

    def push_scene(self, scene):
        """Apila una escena encima de la actual."""
        self.scenes.append(scene)
        scene.on_enter()

    def pop_scene(self):
        """Vuelve a la escena anterior."""
        if len(self.scenes) > 1:
            old = self.scenes.pop()
            old.on_exit()
            self.scenes[-1].on_resume()
        else:
            print("No hay escena anterior, cerrando juego.")
            pyglet.app.exit()

if __name__ == "__main__":
    app = GameApp()
    app.run()