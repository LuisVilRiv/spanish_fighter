# scenes/eula_scene.py
import arcade
import os
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel
from scenes.menu_scene import MenuView

EULA_FILE = "eula_accepted.txt"
EULA_TEXT = """\
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
todos los términos y condiciones de esta licencia."""

class EulaView(BaseView):
    def __init__(self, app):
        super().__init__(app)
        self.ui_elements = []
        self.background  = None
        try:
            self.background = arcade.load_texture('img/fondos/eula.jpg')
        except Exception:
            pass
        self._setup_ui()

    def _setup_ui(self):
        self.ui_elements.clear()
        w, h = self.app.width, self.app.height

        # ── Zonas ─────────────────────────────────────────────────────────
        MARGIN       = int(min(w, h) * 0.04)
        FOOTER_H     = int(h * 0.12)
        PANEL_PAD    = int(min(w, h) * 0.025)

        panel_x = MARGIN
        panel_y = FOOTER_H
        panel_w = w - 2 * MARGIN
        panel_h = h - FOOTER_H - MARGIN

        self.panel_rect = (panel_x, panel_y, panel_w, panel_h)

        # ── Texto EULA dentro del panel ───────────────────────────────────
        text_font = max(11, int(h * 0.018))
        self.label = RetroLabel(
            EULA_TEXT,
            x=panel_x + PANEL_PAD,
            y=panel_y + panel_h - PANEL_PAD,
            width=panel_w - 2 * PANEL_PAD,
            font_size=text_font,
            color=arcade.color.WHITE,
            anchor_x='left', anchor_y='top',
            multiline=True
        )

        # ── Botones centrados en el pie ───────────────────────────────────
        btn_w   = int(min(w * 0.16, 155))
        btn_h   = int(FOOTER_H * 0.55)
        btn_gap = int(w * 0.030)
        btn_y   = (FOOTER_H - btn_h) // 2

        self.accept_button = ImageButton(
            x=w // 2 - btn_w - btn_gap // 2,
            y=btn_y,
            width=btn_w, height=btn_h,
            text="ACEPTAR",
            normal_color=(0, 130, 0), hover_color=(0, 180, 0),
            callback=self.accept
        )
        self.reject_button = ImageButton(
            x=w // 2 + btn_gap // 2,
            y=btn_y,
            width=btn_w, height=btn_h,
            text="RECHAZAR",
            normal_color=(130, 0, 0), hover_color=(180, 0, 0),
            callback=self.reject
        )
        self.ui_elements = [self.accept_button, self.reject_button]

    def on_draw(self):
        self.clear()
        w, h = self.app.width, self.app.height

        if self.background:
            arcade.draw_texture_rectangle(
                w // 2, h // 2, w, h, self.background
            )
        else:
            arcade.draw_rect_filled(arcade.XYWH(w // 2, h // 2, w, h), (30, 70, 30))

        px, py, pw, ph = self.panel_rect
        arcade.draw_rect_filled(arcade.LBWH(px, py, pw, ph), (0, 0, 0, 190))
        arcade.draw_rect_outline(arcade.LBWH(px, py, pw, ph), (120, 180, 120, 200), border_width=2)

        self.label.draw()
        for btn in self.ui_elements:
            btn.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)

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