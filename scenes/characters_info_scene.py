# scenes/characters_info_scene.py
import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel
from personajes import __all__ as personajes_list
from personajes import *

class CharactersInfoView(BaseView):
    def __init__(self, app):
        super().__init__(app)
        self.current_index = 0
        self.ui_elements = []
        self.static_elements = []
        self.sprite_list = arcade.SpriteList()
        self.sprite = None
        self._setup_ui()

    def _setup_ui(self):
        self.ui_elements.clear()
        self.static_elements.clear()
        self.sprite_list.clear()

        w, h = self.app.width, self.app.height
        self.background_color = (30, 35, 50)

        # ── Zonas verticales ──────────────────────────────────────────────
        # Pie: dos filas de botones + margen
        BTN_H      = max(38, int(h * 0.055))
        BTN_GAP    = max(8,  int(h * 0.012))
        MARGIN_BOT = max(14, int(h * 0.020))
        FOOTER_H   = MARGIN_BOT + BTN_H + BTN_GAP + BTN_H + MARGIN_BOT

        HEADER_H   = max(50, int(h * 0.09))

        self.content_bottom = FOOTER_H
        self.content_top    = h - HEADER_H
        self.content_height = self.content_top - self.content_bottom

        # ── Botones de navegación ─────────────────────────────────────────
        nav_btn_w  = int(min(w * 0.18, 170))
        back_btn_w = int(min(w * 0.22, 210))

        # Fila superior del pie: ANTERIOR  |  SIGUIENTE
        nav_y = MARGIN_BOT + BTN_H + BTN_GAP

        btn_prev = ImageButton(
            x=w // 2 - nav_btn_w - BTN_GAP * 2,
            y=nav_y,
            width=nav_btn_w, height=BTN_H,
            text="◀ ANTERIOR",
            normal_color=(90, 90, 120), hover_color=(120, 120, 160),
            callback=self.prev_character
        )
        btn_next = ImageButton(
            x=w // 2 + BTN_GAP * 2,
            y=nav_y,
            width=nav_btn_w, height=BTN_H,
            text="SIGUIENTE ▶",
            normal_color=(90, 90, 120), hover_color=(120, 120, 160),
            callback=self.next_character
        )

        # Fila inferior del pie: VOLVER (centrado)
        btn_back = ImageButton(
            x=w // 2 - back_btn_w // 2,
            y=MARGIN_BOT,
            width=back_btn_w, height=BTN_H,
            text="VOLVER",
            normal_color=(110, 110, 135), hover_color=(145, 145, 175),
            callback=self.back
        )

        self.btn_prev = btn_prev
        self.btn_next = btn_next
        self.btn_back = btn_back
        self.ui_elements.extend([btn_prev, btn_next, btn_back])

        # ── Contenido del personaje ───────────────────────────────────────
        self._mostrar_personaje()

    def _mostrar_personaje(self):
        botones_fijos = [self.btn_prev, self.btn_next, self.btn_back]
        self.ui_elements = [e for e in self.ui_elements if e in botones_fijos]
        self.static_elements.clear()
        self.sprite_list.clear()

        w, h = self.app.width, self.app.height

        clase_nombre = personajes_list[self.current_index]
        clase        = globals()[clase_nombre]
        personaje    = clase()
        desc         = clase.descripcion()

        ct = self.content_top     # y más alta disponible
        cb = self.content_bottom  # y más baja disponible
        ch = ct - cb              # altura total del área de contenido

        # ── Dividir el área en 6 bandas proporcionales ────────────────────
        # sprite | nombre | tipo | descripción | stats | habilidades
        FRACS = [0.20, 0.10, 0.08, 0.16, 0.18, 0.28]
        # Calcular los bordes superiores de cada banda
        tops = []
        y = ct
        for f in FRACS:
            tops.append(y)
            y -= int(ch * f)

        # ── Contador esquina ──────────────────────────────────────────────
        self.ui_elements.append(RetroLabel(
            f"{self.current_index + 1} / {len(personajes_list)}",
            x=w - 20, y=ct,
            font_size=max(10, int(h * 0.018)),
            color=(150, 150, 170),
            anchor_x='right', anchor_y='top'
        ))

        # ── Banda 0: Sprite ───────────────────────────────────────────────
        band_h_0 = int(ch * FRACS[0])
        sprite_sz = int(min(band_h_0 * 0.85, w * 0.14))
        sprite_cy = tops[0] - band_h_0 // 2
        try:
            tex = arcade.load_texture(f'img/personajes/{clase_nombre.lower()}.png')
            self.sprite = arcade.Sprite(tex, center_x=w // 2, center_y=sprite_cy)
            self.sprite.width  = sprite_sz
            self.sprite.height = sprite_sz
            self.sprite_list.append(self.sprite)
        except Exception:
            self.sprite = None

        # ── Banda 1: Nombre ───────────────────────────────────────────────
        name_sz = max(15, int(ch * FRACS[1] * 0.55))
        self.ui_elements.append(RetroLabel(
            personaje.nombre,
            w // 2, tops[1] - int(ch * FRACS[1] * 0.25),
            font_size=name_sz, color=(255, 255, 200),
            anchor_x='center', anchor_y='center'
        ))

        # ── Banda 2: Tipo ─────────────────────────────────────────────────
        tipo_sz = max(11, int(ch * FRACS[2] * 0.55))
        self.ui_elements.append(RetroLabel(
            personaje.tipo,
            w // 2, tops[2] - int(ch * FRACS[2] * 0.35),
            font_size=tipo_sz, color=(180, 220, 255),
            anchor_x='center', anchor_y='center'
        ))

        # ── Banda 3: Descripción ──────────────────────────────────────────
        desc_sz = max(10, int(ch * FRACS[3] * 0.22))
        desc_w  = int(w * 0.68)
        self.ui_elements.append(RetroLabel(
            desc,
            x=w // 2, y=tops[3],
            width=desc_w,
            font_size=desc_sz, color=(170, 170, 170),
            anchor_x='center', anchor_y='top',
            multiline=True
        ))

        # ── Banda 4: Estadísticas en dos columnas ─────────────────────────
        band_h_4  = int(ch * FRACS[4])
        stat_sz   = max(10, int(band_h_4 * 0.18))
        stats_all = [
            f"Vida: {personaje.vida_maxima}",
            f"Ataque: {personaje.ataque_base}",
            f"Defensa: {personaje.defensa_base}",
            f"Velocidad: {personaje.velocidad_base}",
            f"Energía: {personaje.energia_maxima}",
        ]
        n_stats  = len(stats_all)
        n_left   = (n_stats + 1) // 2
        left_stats  = stats_all[:n_left]
        right_stats = stats_all[n_left:]
        stat_gap = band_h_4 / (max(n_left, len(right_stats)) + 1)
        col_x    = int(w * 0.14)

        for j, stat in enumerate(left_stats):
            sy = tops[4] - stat_gap * (j + 0.7)
            self.ui_elements.append(RetroLabel(
                stat, x=w // 2 - col_x, y=int(sy),
                font_size=stat_sz, color=(210, 210, 150),
                anchor_x='right', anchor_y='center'
            ))
        for j, stat in enumerate(right_stats):
            sy = tops[4] - stat_gap * (j + 0.7)
            self.ui_elements.append(RetroLabel(
                stat, x=w // 2 + col_x, y=int(sy),
                font_size=stat_sz, color=(210, 210, 150),
                anchor_x='left', anchor_y='center'
            ))

        # ── Banda 5: Habilidades ──────────────────────────────────────────
        band_h_5  = int(ch * FRACS[5])
        n_habs    = len(personaje.habilidades)
        # Reservar espacio para título + N habilidades
        slots     = n_habs + 1          # título ocupa 1 slot
        slot_h    = band_h_5 / (slots + 0.5)
        hab_sz    = max(9, int(slot_h * 0.40))
        title_sz  = max(11, int(slot_h * 0.55))
        hab_w     = int(w * 0.76)

        hab_title_y = tops[5] - slot_h * 0.4
        self.ui_elements.append(RetroLabel(
            "HABILIDADES",
            w // 2, int(hab_title_y),
            font_size=title_sz, color=(255, 200, 100),
            anchor_x='center', anchor_y='center'
        ))

        for i, hab in enumerate(personaje.habilidades):
            hy    = tops[5] - slot_h * (i + 1.4)
            texto = f"{i+1}. {hab.nombre} ({hab.costo_energia}E): {hab.descripcion}"
            self.ui_elements.append(RetroLabel(
                texto,
                x=w // 2, y=int(hy),
                width=hab_w,
                font_size=hab_sz, color=(175, 175, 175),
                anchor_x='center', anchor_y='center',
                multiline=False
            ))

    def prev_character(self):
        self.current_index = (self.current_index - 1) % len(personajes_list)
        self._mostrar_personaje()

    def next_character(self):
        self.current_index = (self.current_index + 1) % len(personajes_list)
        self._mostrar_personaje()

    def back(self):
        from scenes.menu_scene import MenuView
        self.app.goto_view(MenuView(self.app))

    def on_draw(self):
        self.clear()
        arcade.set_background_color(self.background_color)
        self.sprite_list.draw()
        for elem in self.ui_elements:
            if hasattr(elem, 'draw'):
                elem.draw()
        for elem in self.static_elements:
            if hasattr(elem, 'draw'):
                elem.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

    def on_resize(self, width, height):
        self._setup_ui()