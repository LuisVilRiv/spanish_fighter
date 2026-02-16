import pyglet
from gui.widgets import ImageButton
from personajes import __all__ as personajes_list
from personajes import *
import os

class CharacterSelectScene:
    def __init__(self, app):
        self.app = app
        self.batch = pyglet.graphics.Batch()
        self.buttons = []

        # Fondo
        try:
            bg_image = pyglet.image.load('img/fondos/menu.jpg')
            self.background = pyglet.sprite.Sprite(bg_image, batch=self.batch)
        except:
            self.background = pyglet.shapes.Rectangle(0, 0, app.window.width, app.window.height, color=(30,30,80), batch=self.batch)

        # Título
        self.title = pyglet.text.Label(
            "Selecciona tu personaje",
            font_name='Arial', font_size=28,
            x=app.window.width//2, y=app.window.height-50,
            anchor_x='center', anchor_y='center',
            color=(255,255,255,255), batch=self.batch
        )

        # Cuadrícula de personajes (4 columnas)
        cols = 4
        btn_width = 100
        btn_height = 100
        spacing_x = (app.window.width - cols * btn_width) // (cols + 1)
        start_x = spacing_x
        start_y = app.window.height - 150
        spacing_y = 120

        for i, clase_nombre in enumerate(personajes_list):
            clase = globals()[clase_nombre]
            instancia = clase()
            nombre_archivo = clase_nombre.lower() + '.png'
            ruta_icono = f'img/personajes/{nombre_archivo}'
            col = i % cols
            fila = i // cols
            x = start_x + col * (btn_width + spacing_x)
            y = start_y - fila * spacing_y
            btn = ImageButton(
                x=x, y=y,
                image_path=ruta_icono,
                hover_tint=(200,200,200),
                callback=lambda c=clase: self.select_character(c),
                batch=self.batch
            )
            self.buttons.append(btn)
            # Etiqueta con el nombre
            label = pyglet.text.Label(
                instancia.nombre[:10],
                font_size=12,
                x=x + btn_width//2,
                y=y - 20,
                anchor_x='center', anchor_y='center',
                color=(255,255,255,255), batch=self.batch
            )

        # Botón volver (centrado abajo)
        btn_back = ImageButton(
            x=app.window.width//2 - 100, y=100,
            image_path='img/botones/volver.png',
            callback=self.back, batch=self.batch
        )
        self.buttons.append(btn_back)

    def select_character(self, clase):
        personaje = clase()
        from scenes.combat_scene import CombatScene
        from personajes import Segarro
        enemigo = Segarro()
        self.app.push_scene(CombatScene(self.app, personaje, enemigo))

    def back(self):
        self.app.pop_scene()

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_resume(self):
        pass

    def draw(self):
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.buttons:
            btn.on_mouse_press(x, y, button)

    def on_mouse_motion(self, x, y, dx, dy):
        for btn in self.buttons:
            btn.update(x, y)

    def on_key_press(self, symbol, modifiers):
        pass

    def update(self, dt):
        pass