import pyglet
import os
from gui.widgets import ImageButton
from scenes.character_select_scene import CharacterSelectScene

class MenuScene:
    def __init__(self, app):
        self.app = app
        self.batch = pyglet.graphics.Batch()
        self.buttons = []

        # Fondo
        try:
            bg_image = pyglet.image.load('img/fondos/menu.jpg')
            self.background = pyglet.sprite.Sprite(bg_image, batch=self.batch)
        except:
            self.background = pyglet.shapes.Rectangle(0, 0, app.window.width, app.window.height, color=(50,50,100), batch=self.batch)

        # Título (centrado)
        try:
            title_img = pyglet.image.load('img/titulo.png')
            self.title = pyglet.sprite.Sprite(title_img, x=app.window.width//2 - title_img.width//2, y=app.window.height-150, batch=self.batch)
        except:
            self.title = pyglet.text.Label(
                "Batalla Cómica Española",
                font_name='Arial', font_size=36,
                x=app.window.width//2, y=app.window.height-100,
                anchor_x='center', anchor_y='center',
                color=(255,255,0,255), batch=self.batch
            )

        # Botones (centrados verticalmente)
        btn_width = 200
        btn_height = 50
        start_y = app.window.height * 0.6
        spacing = 70
        btn_x = app.window.width//2 - btn_width//2

        btn_new = ImageButton(
            x=btn_x, y=start_y,
            image_path='img/botones/nueva_partida.png',
            callback=self.new_game, batch=self.batch
        )
        btn_load = ImageButton(
            x=btn_x, y=start_y - spacing,
            image_path='img/botones/cargar_partida.png',
            callback=self.load_game, batch=self.batch
        )
        btn_characters = ImageButton(
            x=btn_x, y=start_y - 2*spacing,
            image_path='img/botones/personajes.png',
            callback=self.view_characters, batch=self.batch
        )
        btn_instructions = ImageButton(
            x=btn_x, y=start_y - 3*spacing,
            image_path='img/botones/instrucciones.png',
            callback=self.instructions, batch=self.batch
        )
        btn_exit = ImageButton(
            x=btn_x, y=start_y - 4*spacing,
            image_path='img/botones/volver.png',
            callback=self.exit_game, batch=self.batch
        )
        self.buttons.extend([btn_new, btn_load, btn_characters, btn_instructions, btn_exit])

    def new_game(self):
        self.app.push_scene(CharacterSelectScene(self.app))

    def load_game(self):
        print("Cargar partida - pendiente")

    def view_characters(self):
        print("Ver personajes - pendiente")

    def instructions(self):
        print("Instrucciones - pendiente")

    def exit_game(self):
        pyglet.app.exit()

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