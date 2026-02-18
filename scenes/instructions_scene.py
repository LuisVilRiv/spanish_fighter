# scenes/instructions_scene.py
import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel

TEXTO_INSTRUCCIONES = """\
Bienvenido a Batalla Cómica Española.

Es un juego de combate por turnos entre personajes surrealistas españoles.

En tu turno puedes elegir entre cuatro acciones:

  • ATAQUE     — Golpe básico que inflige daño al rival.
  • DEFENDER   — Reduce el daño recibido en el próximo turno.
  • CONCENTRAR — Recupera energía para usar habilidades.
  • HABILIDAD  — Usa una de tus 6 habilidades especiales.
                 Cada habilidad consume energía.

Gana el primero que reduzca la vida del oponente a cero.

¡Que gane el más español!"""

class InstructionsView(BaseView):
    def __init__(self, app):
        super().__init__(app)
        self.ui_elements = []
        self._setup_ui()

    def _setup_ui(self):
        self.ui_elements.clear()
        w, h = self.app.width, self.app.height
        self.background_color = (30, 35, 50)

        # ── Zonas ─────────────────────────────────────────────────────────
        HEADER_H = int(h * 0.12)
        FOOTER_H = int(h * 0.12)
        BODY_TOP = h - HEADER_H
        BODY_BOT = FOOTER_H

        # ── Título ────────────────────────────────────────────────────────
        title_sz = max(22, int(h * 0.045))
        self.ui_elements.append(RetroLabel(
            "INSTRUCCIONES",
            w // 2, h - HEADER_H // 2,
            font_size=title_sz, color=(255, 220, 150),
            anchor_x='center', anchor_y='center'
        ))

        # ── Texto ─────────────────────────────────────────────────────────
        margin_x  = int(w * 0.10)
        text_w    = w - 2 * margin_x
        text_font = max(13, int(h * 0.022))

        # Centro vertical del área de texto
        text_center_y = (BODY_TOP + BODY_BOT) // 2

        self.ui_elements.append(RetroLabel(
            TEXTO_INSTRUCCIONES,
            x=w // 2, y=text_center_y + int((BODY_TOP - BODY_BOT) * 0.38),
            width=text_w,
            font_size=text_font, color=(210, 210, 210),
            anchor_x='center', anchor_y='top',
            multiline=True
        ))

        # ── Botón volver ──────────────────────────────────────────────────
        btn_w = int(min(w * 0.22, 220))
        btn_h = int(FOOTER_H * 0.55)
        self.ui_elements.append(ImageButton(
            x=w // 2 - btn_w // 2,
            y=(FOOTER_H - btn_h) // 2,
            width=btn_w, height=btn_h,
            text="VOLVER",
            normal_color=(110, 110, 135), hover_color=(145, 145, 175),
            callback=self.back
        ))

    def back(self):
        from scenes.menu_scene import MenuView
        self.app.goto_view(MenuView(self.app))

    def on_draw(self):
        self.clear()
        arcade.set_background_color(self.background_color)
        for elem in self.ui_elements:
            if hasattr(elem, 'draw'):
                elem.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

    def on_resize(self, width, height):
        self._setup_ui()