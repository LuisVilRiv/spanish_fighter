import arcade
import os
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel
from scenes.menu_scene import MenuView

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

class EulaView(BaseView):
    def __init__(self, app):
        super().__init__(app)
        self.eula_accepted = os.path.exists(EULA_FILE)
        self.ui_elements = []

        if self.eula_accepted:
            return

        try:
            self.background = arcade.load_texture('img/fondos/eula.jpg')
        except:
            self.background = None

        self.panel_x = 0
        self.panel_y = 0
        self.panel_width = 0
        self.panel_height = 0
        self.label = None
        self.accept_button = None
        self.reject_button = None
        self._setup_ui()

    def _setup_ui(self):
        if self.eula_accepted:
            return
        w = self.app.width
        h = self.app.height
        margin = 50
        panel_width = w - 2*margin
        panel_height = h - 2*margin - 100
        self.panel_x = margin
        self.panel_y = margin + 80
        self.panel_width = panel_width
        self.panel_height = panel_height

        self.label = RetroLabel(
            EULA_TEXT,
            x=margin+10, y=h - margin - 20,
            font_size=14, color=arcade.color.WHITE,
            anchor_x='left', anchor_y='top',
            width=panel_width-20, multiline=True
        )

        btn_width = 120
        btn_height = 40
        btn_y = margin
        self.accept_button = ImageButton(
            x=w//2 - btn_width - 10, y=btn_y,
            width=btn_width, height=btn_height,
            image_path='img/botones/aceptar.png',
            hover_tint=(150,255,150),
            callback=self.accept
        )
        self.reject_button = ImageButton(
            x=w//2 + 10, y=btn_y,
            width=btn_width, height=btn_height,
            image_path='img/botones/volver.png',
            hover_tint=(255,150,150),
            callback=self.reject
        )
        self.ui_elements = [self.accept_button, self.reject_button]

    def on_show(self):
        if self.eula_accepted:
            self.app.goto_view(MenuView(self.app))

    def on_draw(self):
        self.clear()
        if self.eula_accepted:
            return
        if self.background:
            arcade.draw_texture_rectangle(self.app.width//2, self.app.height//2,
                                          self.app.width, self.app.height, self.background)
        else:
            arcade.set_background_color((30,70,30))

        # Panel semitransparente usando draw_lrwh_rectangle_filled
        arcade.draw_lrwh_rectangle_filled(
            self.panel_x, self.panel_y,
            self.panel_width, self.panel_height,
            (0, 0, 0, 180)
        )
        self.label.draw()
        for btn in self.ui_elements:
            btn.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)
        for btn in self.ui_elements:
            btn.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

    def accept(self):
        with open(EULA_FILE, 'w', encoding='utf-8') as f:
            f.write("aceptado")
        self.app.goto_view(MenuView(self.app))

    def reject(self):
        arcade.close_window()

    def on_resize(self, width, height):
        self._setup_ui()