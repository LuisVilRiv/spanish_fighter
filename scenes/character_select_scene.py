# scenes/character_select_scene.py
import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel
from personajes import __all__ as personajes_list
from personajes import *
from scenes.rival_select_scene import RivalSelectView

class CharacterSelectView(BaseView):
    def __init__(self, app):
        super().__init__(app)
        self.ui_elements = []
        self._setup_ui()

    def _setup_ui(self):
        self.ui_elements.clear()
        w, h = self.app.width, self.app.height
        self.background_color = (45, 50, 70)

        # ── Zonas fijas ───────────────────────────────────────────────────
        TITLE_H      = int(h * 0.10)   # franja del título
        FOOTER_H     = int(h * 0.12)   # franja del botón volver
        GRID_TOP     = h - TITLE_H
        GRID_BOTTOM  = FOOTER_H
        GRID_H       = GRID_TOP - GRID_BOTTOM

        # ── Título ────────────────────────────────────────────────────────
        title_y = h - TITLE_H // 2
        font_size = max(18, int(h * 0.038))
        self.title = RetroLabel(
            "SELECCIONA TU LUCHADOR",
            w // 2, title_y,
            font_size=font_size, color=(255, 220, 150),
            anchor_x='center', anchor_y='center'
        )
        self.ui_elements.append(self.title)

        # ── Cuadrícula ────────────────────────────────────────────────────
        cols = 4
        n    = len(personajes_list)
        rows = (n + cols - 1) // cols

        # Tamaño del botón: ocupa hasta el 80 % del slot disponible
        slot_w = w / cols
        slot_h = GRID_H / (rows + 0.5)      # +0.5 deja margen extra arriba/abajo
        btn_size = int(min(slot_w, slot_h) * 0.62)
        btn_size = max(btn_size, 60)

        label_h  = int(h * 0.022)           # altura reservada para la etiqueta de nombre
        gap_lbl  = int(h * 0.010)           # hueco entre botón e etiqueta

        # Centrar la rejilla horizontalmente
        grid_w   = cols * slot_w
        offset_x = (w - grid_w) / 2 + slot_w / 2

        # Centrar la rejilla verticalmente dentro de GRID
        total_content_h = rows * slot_h
        grid_top_y = GRID_BOTTOM + (GRID_H + total_content_h) / 2 - slot_h / 2

        for i, clase_nombre in enumerate(personajes_list):
            clase    = globals()[clase_nombre]
            instancia = clase()
            ruta_icono = f'img/personajes/{clase_nombre.lower()}.png'

            col = i % cols
            fila = i // cols

            cx = offset_x + col * slot_w
            cy = grid_top_y - fila * slot_h

            btn = ImageButton(
                x=int(cx - btn_size // 2), y=int(cy - btn_size // 2),
                width=btn_size, height=btn_size,
                image_path=ruta_icono,
                hover_tint=(220, 220, 220),
                callback=lambda c=clase: self.select_character(c)
            )
            self.ui_elements.append(btn)

            label = RetroLabel(
                instancia.nombre[:12],
                x=int(cx), y=int(cy - btn_size // 2 - gap_lbl),
                font_size=max(9, label_h),
                anchor_x='center', anchor_y='top'
            )
            self.ui_elements.append(label)

        # ── Botón volver (centrado en el pie) ─────────────────────────────
        btn_back_w = int(min(w * 0.22, 220))
        btn_back_h = int(FOOTER_H * 0.55)
        btn_back = ImageButton(
            x=w // 2 - btn_back_w // 2,
            y=(FOOTER_H - btn_back_h) // 2,
            width=btn_back_w, height=btn_back_h,
            text="VOLVER",
            normal_color=(120, 120, 140), hover_color=(150, 150, 180),
            callback=self.back
        )
        self.ui_elements.append(btn_back)

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

    def select_character(self, clase):
        self.app.push_view(RivalSelectView(self.app, player_class=clase))

    def back(self):
        from scenes.menu_scene import MenuView
        self.app.goto_view(MenuView(self.app))

    def on_resize(self, width, height):
        self._setup_ui()