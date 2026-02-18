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

        # ── Puntero de colocación vertical (empieza en la parte superior del contenido)
        # Repartir el espacio de contenido en secciones proporcionales:
        #   sprite 22% | nombre+tipo 14% | descripción 20% | stats 22% | habilidades 22%
        ct  = self.content_top
        ch  = self.content_height

        # Sprite
        sprite_h = int(ch * 0.22)
        sprite_y = ct - sprite_h // 2
        try:
            tex = arcade.load_texture(f'img/personajes/{clase_nombre.lower()}.png')
            sz  = min(sprite_h, int(w * 0.15))
            self.sprite = arcade.Sprite(tex,
                center_x=w // 2,
                center_y=sprite_y
            )
            self.sprite.width  = sz
            self.sprite.height = sz
            self.sprite_list.append(self.sprite)
        except Exception:
            self.sprite = None

        # Contador de personaje (esquina, pequeño)
        self.ui_elements.append(RetroLabel(
            f"{self.current_index + 1} / {len(personajes_list)}",
            x=w - 20, y=ct,
            font_size=max(10, int(h * 0.018)),
            color=(150, 150, 170),
            anchor_x='right', anchor_y='top'
        ))

        # Nombre
        nombre_y = ct - int(ch * 0.22) - int(ch * 0.03)
        name_size = max(16, int(h * 0.032))
        self.ui_elements.append(RetroLabel(
            personaje.nombre,
            w // 2, nombre_y,
            font_size=name_size, color=(255, 255, 200),
            anchor_x='center', anchor_y='top'
        ))

        # Tipo
        tipo_y = nombre_y - int(h * 0.045)
        tipo_size = max(12, int(h * 0.022))
        self.ui_elements.append(RetroLabel(
            personaje.tipo,
            w // 2, tipo_y,
            font_size=tipo_size, color=(180, 220, 255),
            anchor_x='center', anchor_y='top'
        ))

        # Separador visual (descripción)
        desc_y    = tipo_y - int(h * 0.032)
        desc_size = max(11, int(h * 0.019))
        desc_w    = int(w * 0.65)
        self.ui_elements.append(RetroLabel(
            desc,
            x=w // 2, y=desc_y,
            width=desc_w,
            font_size=desc_size, color=(170, 170, 170),
            anchor_x='center', anchor_y='top',
            multiline=True
        ))

        # ── Estadísticas: dos columnas ────────────────────────────────────
        stats_y    = desc_y - int(ch * 0.22)
        stat_size  = max(11, int(h * 0.020))
        stat_gap_y = int(h * 0.030)
        col_offset = int(w * 0.12)

        stats_left = [
            f"❤  Vida:      {personaje.vida_maxima}",
            f"⚔  Ataque:    {personaje.ataque_base}",
            f"🛡  Defensa:   {personaje.defensa_base}",
        ]
        stats_right = [
            f"💨  Velocidad: {personaje.velocidad_base}",
            f"⚡  Energía:   {personaje.energia_maxima}",
        ]

        for j, stat in enumerate(stats_left):
            self.ui_elements.append(RetroLabel(
                stat,
                x=w // 2 - col_offset, y=stats_y - j * stat_gap_y,
                font_size=stat_size, color=(210, 210, 150),
                anchor_x='right', anchor_y='top'
            ))
        for j, stat in enumerate(stats_right):
            self.ui_elements.append(RetroLabel(
                stat,
                x=w // 2 + col_offset, y=stats_y - j * stat_gap_y,
                font_size=stat_size, color=(210, 210, 150),
                anchor_x='left', anchor_y='top'
            ))

        # ── Habilidades ───────────────────────────────────────────────────
        hab_title_y = stats_y - max(len(stats_left), len(stats_right)) * stat_gap_y - int(h * 0.025)
        hab_title_size = max(12, int(h * 0.024))
        self.ui_elements.append(RetroLabel(
            "HABILIDADES",
            w // 2, hab_title_y,
            font_size=hab_title_size, color=(255, 200, 100),
            anchor_x='center', anchor_y='top'
        ))

        hab_y      = hab_title_y - int(h * 0.038)
        hab_size   = max(10, int(h * 0.017))
        hab_gap_y  = int(h * 0.028)
        hab_w      = int(w * 0.72)

        for i, hab in enumerate(personaje.habilidades):
            texto = f"{i+1}. {hab.nombre}  ({hab.costo_energia}E)  —  {hab.descripcion}"
            self.ui_elements.append(RetroLabel(
                texto,
                x=w // 2, y=hab_y - i * hab_gap_y,
                width=hab_w,
                font_size=hab_size, color=(175, 175, 175),
                anchor_x='center', anchor_y='top',
                multiline=True
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