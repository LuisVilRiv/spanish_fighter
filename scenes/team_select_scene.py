# scenes/team_select_scene.py
import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel
from personajes import __all__ as personajes_list
from personajes import *

COLOR_EQUIPO1 = (60, 120, 200)
COLOR_EQUIPO2 = (200, 60, 60)
COLOR_IA      = (180, 100, 180)
COLOR_JUGADOR = (100, 200, 100)


class TeamSelectView(BaseView):
    def __init__(self, app, team_size: int):
        super().__init__(app)
        self.team_size   = team_size
        self.total_slots = team_size * 2
        self.equipo1     = []
        self.equipo2     = []
        self.slot_actual = 0
        self.fase        = 'personaje'
        self._clase_temp = None
        self.ui_elements          = []
        self.char_buttons         = []
        self.control_buttons      = []
        self.preview_sprite_list  = arcade.SpriteList()
        self._setup_ui()

    # ── Propiedades ──────────────────────────────────────────────────────────

    @property
    def _equipo_actual(self):
        return 1 if self.slot_actual < self.team_size else 2

    @property
    def _slot_en_equipo(self):
        return self.slot_actual if self._equipo_actual == 1 else self.slot_actual - self.team_size

    # ── Construcción UI ──────────────────────────────────────────────────────

    def _setup_ui(self):
        self.ui_elements.clear()
        self.char_buttons.clear()
        self.control_buttons.clear()
        self.preview_sprite_list.clear()

        w, h = self.app.width, self.app.height

        equipo    = self._equipo_actual
        slot_idx  = self._slot_en_equipo
        nombre_eq = f"EQUIPO {equipo}"

        # Título
        self.ui_elements.append(RetroLabel(
            f"SELECCIÓN DE {nombre_eq}  —  Luchador {slot_idx + 1} de {self.team_size}",
            w // 2, h - 40,
            font_size=20, color=(255, 220, 80),
            anchor_x='center', anchor_y='center'
        ))

        self._draw_slot_indicators(w, h)

        if self.fase == 'personaje':
            self._build_char_grid(w, h)
        else:
            self._build_control_selector(w, h)

        # Botón volver (siempre al fondo)
        self.ui_elements.append(ImageButton(
            x=w // 2 - 100, y=12,
            width=200, height=40,
            text="VOLVER",
            normal_color=(120, 120, 140), hover_color=(150, 150, 180),
            callback=self._back
        ))

    def _draw_slot_indicators(self, w, h):
        """Indicadores de progreso de selección."""
        total   = self.total_slots
        dot_sz  = 26
        spacing = 38
        total_w = total * spacing - (spacing - dot_sz)
        sx      = w // 2 - total_w // 2

        for i in range(total):
            eq     = 1 if i < self.team_size else 2
            col    = COLOR_EQUIPO1 if eq == 1 else COLOR_EQUIPO2
            filled = (i < len(self.equipo1)) if i < self.team_size else (i - self.team_size) < len(self.equipo2)
            label  = "✓" if filled else str(i % self.team_size + 1)
            bg     = col if filled else (60, 60, 70)
            self.ui_elements.append(ImageButton(
                x=sx + i * spacing, y=h - 80,
                width=dot_sz, height=dot_sz,
                text=label, normal_color=bg, hover_color=bg
            ))

        sep_x = sx + self.team_size * spacing - spacing // 2 - dot_sz // 2
        self.ui_elements.append(RetroLabel(
            "VS", sep_x + spacing // 2, h - 67,
            font_size=10, color=(200, 200, 100),
            anchor_x='center', anchor_y='center'
        ))

    def _build_char_grid(self, w, h):
        """Cuadrícula de selección de personaje."""
        HEADER_H     = 95     # espacio reservado para título + indicadores
        FOOTER_H     = 60     # espacio reservado para botón volver
        available_h  = h - HEADER_H - FOOTER_H

        self.ui_elements.append(RetroLabel(
            "Elige tu luchador:",
            w // 2, h - HEADER_H + 5,
            font_size=15, color=(220, 220, 220),
            anchor_x='center', anchor_y='center'
        ))

        cols    = 4
        btn_w   = 110
        btn_h   = 110
        lbl_h   = 18      # alto de la etiqueta de nombre debajo del botón
        cell_h  = btn_h + lbl_h + 6
        rows    = (len(personajes_list) + cols - 1) // cols
        gap_y   = max(6, (available_h - rows * cell_h) // (rows + 1))
        gap_x   = max(10, (w - cols * btn_w) // (cols + 1))

        # Empezamos desde arriba del área disponible
        top_y = h - HEADER_H - gap_y

        for i, clase_nombre in enumerate(personajes_list):
            clase = globals()[clase_nombre]
            inst  = clase()
            col_i = i % cols
            row_i = i // cols

            bx = gap_x + col_i * (btn_w + gap_x)
            # Centro Y del botón para esta fila
            by = top_y - row_i * (cell_h + gap_y)

            btn = ImageButton(
                x=bx, y=by - btn_h,
                width=btn_w, height=btn_h,
                image_path=f'img/personajes/{clase_nombre.lower()}.png',
                hover_tint=(220, 220, 255),
                callback=lambda c=clase: self._on_char_selected(c)
            )
            self.char_buttons.append(btn)
            self.ui_elements.append(btn)

            # Etiqueta del nombre DEBAJO del botón, con margen
            self.ui_elements.append(RetroLabel(
                inst.nombre[:12],
                bx + btn_w // 2,
                by - btn_h - lbl_h // 2 - 2,
                font_size=11,
                anchor_x='center', anchor_y='center'
            ))

    def _build_control_selector(self, w, h):
        """
        Pantalla para elegir si el personaje será JUGADOR o IA.
        Layout (de arriba a abajo):
          - Nombre del personaje  (zona alta)
          - Sprite                (zona media-alta)
          - Pregunta              (zona media)
          - Botones JUG/IA        (zona media-baja)
          - [Botón VOLVER se añade en _setup_ui al fondo]
        """
        inst = self._clase_temp()

        # ── Zonas Y ──────────────────────────────────────────────────────────
        FOOTER_H  = 65     # reservado para botón Volver
        HEADER_H  = 55     # reservado para título + indicadores
        area_top  = h - HEADER_H
        area_bot  = FOOTER_H
        area_h    = area_top - area_bot

        # Distribución proporcional dentro del área
        nombre_y  = area_top - int(area_h * 0.06)   # muy arriba
        sprite_cy = area_top - int(area_h * 0.30)   # cuarto superior
        pregunta_y= area_top - int(area_h * 0.60)   # mitad
        btns_y    = area_top - int(area_h * 0.78)   # tres cuartos

        sprite_sz = min(int(area_h * 0.32), 160)

        # ── Nombre ───────────────────────────────────────────────────────────
        self.ui_elements.append(RetroLabel(
            inst.nombre,
            w // 2, nombre_y,
            font_size=24, color=(255, 240, 150),
            anchor_x='center', anchor_y='center'
        ))

        # ── Sprite del personaje ──────────────────────────────────────────────
        try:
            tex = arcade.load_texture(
                f'img/personajes/{type(self._clase_temp()).__name__.lower()}.png'
            )
            sp = arcade.Sprite(tex)
            sp.center_x = w // 2
            sp.center_y = sprite_cy
            sp.width    = sprite_sz
            sp.height   = sprite_sz
            self.preview_sprite_list.append(sp)
            self._preview_sprite = sp
        except Exception:
            self._preview_sprite = None

        # ── Pregunta ──────────────────────────────────────────────────────────
        self.ui_elements.append(RetroLabel(
            "¿Quién controlará este personaje?",
            w // 2, pregunta_y,
            font_size=16, color=(200, 200, 200),
            anchor_x='center', anchor_y='center'
        ))

        # ── Botones JUGADOR / IA ──────────────────────────────────────────────
        btn_w_b = min(int(w * 0.22), 210)
        btn_h_b = max(55, int(area_h * 0.10))
        gap_btn = int(w * 0.04)

        btn_jugador = ImageButton(
            x=w // 2 - gap_btn // 2 - btn_w_b,
            y=btns_y - btn_h_b // 2,
            width=btn_w_b, height=btn_h_b,
            text="🎮 JUGADOR",
            normal_color=COLOR_JUGADOR, hover_color=(130, 230, 130),
            callback=lambda: self._on_control_selected(False)
        )
        btn_ia = ImageButton(
            x=w // 2 + gap_btn // 2,
            y=btns_y - btn_h_b // 2,
            width=btn_w_b, height=btn_h_b,
            text="🤖 IA",
            normal_color=COLOR_IA, hover_color=(210, 130, 210),
            callback=lambda: self._on_control_selected(True)
        )
        self.control_buttons.extend([btn_jugador, btn_ia])
        self.ui_elements.extend([btn_jugador, btn_ia])

    # ── Lógica de flujo ──────────────────────────────────────────────────────

    def _on_char_selected(self, clase):
        self._clase_temp = clase
        self.fase = 'control'
        self._block_next_press = True   # el click que eligió personaje no
        self._setup_ui()                # debe alcanzar los botones nuevos

    def _on_control_selected(self, es_ia: bool):
        entry = (self._clase_temp, es_ia)
        if self._equipo_actual == 1:
            self.equipo1.append(entry)
        else:
            self.equipo2.append(entry)

        self.slot_actual += 1
        self._clase_temp = None
        self.fase = 'personaje'
        self._block_next_press = True   # el click de JUGADOR/IA no debe
        self._setup_ui()                # llegar al grid siguiente

        if self.slot_actual >= self.total_slots:
            self._iniciar_combate()

    def _iniciar_combate(self):
        from scenes.combat_team_scene import CombatTeamView
        team1 = [clase() for clase, _ in self.equipo1]
        team2 = [clase() for clase, _ in self.equipo2]
        for p, (_, es_ia) in zip(team1, self.equipo1):
            p.es_ia = es_ia
        for p, (_, es_ia) in zip(team2, self.equipo2):
            p.es_ia = es_ia
        self.app.goto_view(CombatTeamView(self.app, team1, team2))

    def _back(self):
        self._block_next_press = True   # el click de VOLVER no debe llegar a la pantalla anterior
        if self.fase == 'control':
            self.fase = 'personaje'
            self._clase_temp = None
            self._setup_ui()
        elif self.slot_actual > 0:
            self.slot_actual -= 1
            if self._equipo_actual == 1:
                if self.equipo1:
                    self.equipo1.pop()
            else:
                if self.equipo2:
                    self.equipo2.pop()
            self._setup_ui()
        else:
            from scenes.mode_select_scene import ModeSelectView
            self.app.goto_view(ModeSelectView(self.app))

    # ── Render y eventos ─────────────────────────────────────────────────────

    def on_draw(self):
        self.clear()
        arcade.set_background_color((30, 35, 55))
        for elem in self.ui_elements:
            if hasattr(elem, 'draw'):
                elem.draw()
        self.preview_sprite_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

    def on_resize(self, width, height):
        self._setup_ui()