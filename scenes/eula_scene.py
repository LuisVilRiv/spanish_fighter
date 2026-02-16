import pyglet
import os
from gui.widgets import ImageButton
from scenes.menu_scene import MenuScene

EULA_FILE = "eula_accepted.txt"
EULA_TEXT = """
ACUERDO DE LICENCIA DE USUARIO FINAL (EULA)
Batalla Cómica Española
Copyright (c) 2026 Luis Villegas Rivera

Este software se proporciona bajo una licencia limitada, no exclusiva
e intransferible para su uso personal y no comercial.

TÉRMINOS PERMITIDOS:
  • Jugar y disfrutar el juego.
  • Crear y distribuir modificaciones (mods) gratuitas siempre que:
      - No incluyan el juego base completo.
      - No se vendan ni moneticen.
      - Atribuyan crédito al autor original.

TÉRMINOS PROHIBIDOS:
  • Vender, alquilar o distribuir el juego sin autorización.
  • Realizar ingeniería inversa o descompilar el código.
  • Eliminar avisos de copyright.
  • Usar el software con fines ilegales.

SIN GARANTÍA:
El software se entrega "tal cual", sin garantías de ningún tipo.
El autor no será responsable de daños derivados de su uso.

Al hacer clic en "Aceptar", usted confirma que ha leído y acepta
todos los términos y condiciones de esta licencia.
"""

class EulaScene:
    def __init__(self, app):
        self.app = app
        self.batch = pyglet.graphics.Batch()
        self.buttons = []
        self.eula_accepted = os.path.exists(EULA_FILE)

        if self.eula_accepted:
            # No inicializamos nada gráfico, saltaremos en on_enter
            return

        # Fondo
        try:
            bg_image = pyglet.image.load('img/fondos/eula.jpg')
            self.background = pyglet.sprite.Sprite(bg_image, batch=self.batch)
        except:
            self.background = pyglet.shapes.Rectangle(0, 0, app.window.width, app.window.height, color=(30,70,30), batch=self.batch)

        # Panel semitransparente para el texto (centrado, con márgenes)
        margin = 50
        panel_width = app.window.width - 2*margin
        panel_height = app.window.height - 2*margin - 100  # dejar espacio para botones
        self.panel = pyglet.shapes.Rectangle(margin, margin+80, panel_width, panel_height, color=(0,0,0), batch=self.batch)
        self.panel.opacity = 180

        # Texto del EULA
        self.label = pyglet.text.Label(
            EULA_TEXT,
            font_name='Arial', font_size=14,
            x=margin+10, y=app.window.height - margin - 20, width=panel_width-20,
            multiline=True, anchor_y='top',
            color=(255,255,255,255), batch=self.batch
        )

        # Botones (centrados horizontalmente)
        btn_width = 120
        btn_height = 40
        btn_y = margin
        btn_accept = ImageButton(
            x=app.window.width//2 - btn_width - 10, y=btn_y,
            image_path='img/botones/aceptar.png',
            hover_tint=(150,255,150),
            callback=self.accept, batch=self.batch
        )
        btn_reject = ImageButton(
            x=app.window.width//2 + 10, y=btn_y,
            image_path='img/botones/volver.png',
            hover_tint=(255,150,150),
            callback=self.reject, batch=self.batch
        )
        self.buttons.extend([btn_accept, btn_reject])

    def accept(self):
        with open(EULA_FILE, 'w', encoding='utf-8') as f:
            f.write("aceptado")
        self.app.goto_scene(MenuScene(self.app))

    def reject(self):
        pyglet.app.exit()

    def on_enter(self):
        if self.eula_accepted:
            # Si ya estaba aceptado, vamos al menú directamente
            self.app.goto_scene(MenuScene(self.app))

    def on_exit(self):
        pass

    def on_resume(self):
        pass

    def draw(self):
        if not self.eula_accepted:
            self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.eula_accepted:
            for btn in self.buttons:
                btn.on_mouse_press(x, y, button)

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.eula_accepted:
            for btn in self.buttons:
                btn.update(x, y)

    def on_key_press(self, symbol, modifiers):
        pass

    def update(self, dt):
        pass