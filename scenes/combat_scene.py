# scenes/combat_scene.py
import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel, HealthBar
from combate.sistema_combate import Combate, Accion, EstadoCombate
from scenes.historial_scene import HistorialView

class CombatView(BaseView):
    def __init__(self, app, jugador, enemigo):
        super().__init__(app)
        self.jugador       = jugador
        self.enemigo       = enemigo
        self.jugador_clase = type(jugador)
        self.enemigo_clase = type(enemigo)
        self.combate       = Combate(jugador, enemigo)
        self.ui_elements        = []
        self.habilidad_buttons  = []
        self.postcombate_buttons= []
        self.mostrando_habilidades = False
        self.turno_jugador = True
        self.ia_timer      = 0
        self.resultado_turno = None
        self._setup_ui()

    # ─────────────────────────────────────────────────────────────────────
    def _setup_ui(self):
        self.ui_elements.clear()
        self.habilidad_buttons.clear()
        self.postcombate_buttons.clear()
        self.static_elements.clear()
        self.sprite_list.clear()

        w, h = self.app.width, self.app.height
        self.background_color = (28, 32, 48)

        # ── Proporciones verticales ───────────────────────────────────────
        # [header turno 8%] [arena sprites+barras 44%] [log mensajes 16%] [botones acción 16%] [pie postcombate/habilidades 16%]
        HEADER_H   = int(h * 0.08)
        ACTION_H   = int(h * 0.14)        # altura de la zona de botones principales
        MSG_H      = int(h * 0.14)        # altura del log de mensajes
        FOOTER_PAD = int(h * 0.025)       # padding inferior

        action_zone_y  = FOOTER_PAD
        action_zone_top = action_zone_y + ACTION_H

        msg_zone_y   = action_zone_top + int(h * 0.015)
        msg_zone_top = msg_zone_y + MSG_H

        arena_bottom = msg_zone_top + int(h * 0.02)
        arena_top    = h - HEADER_H - int(h * 0.02)
        arena_h      = arena_top - arena_bottom
        arena_mid_y  = (arena_bottom + arena_top) // 2

        # ── Sprites ───────────────────────────────────────────────────────
        sprite_size = int(min(arena_h * 0.55, w * 0.15, 150))
        sprite_size = max(sprite_size, 70)

        margin_x = int(w * 0.05)
        self.jugador_cx = margin_x + int(w * 0.15)
        self.enemigo_cx = w - margin_x - int(w * 0.15)

        def _load_sprite(nombre_clase, cx, cy):
            try:
                tex = arcade.load_texture(f'img/personajes/{nombre_clase.lower()}.png')
                s   = arcade.Sprite(tex, center_x=cx, center_y=cy)
                s.width  = sprite_size
                s.height = sprite_size
                self.sprite_list.append(s)
                return s
            except Exception:
                return None

        sprite_cy = int(arena_mid_y + arena_h * 0.05)
        self.sprite_jugador = _load_sprite(type(self.jugador).__name__, self.jugador_cx, sprite_cy)
        self.sprite_enemigo = _load_sprite(type(self.enemigo).__name__, self.enemigo_cx, sprite_cy)

        # ── Nombres ───────────────────────────────────────────────────────
        name_y  = sprite_cy + sprite_size // 2 + int(h * 0.022)
        name_sz = max(12, int(h * 0.024))
        self.lbl_jugador = RetroLabel(
            self.jugador.nombre, self.jugador_cx, name_y,
            font_size=name_sz, color=(180, 230, 180),
            anchor_x='center', anchor_y='center'
        )
        self.lbl_enemigo = RetroLabel(
            self.enemigo.nombre, self.enemigo_cx, name_y,
            font_size=name_sz, color=(230, 180, 180),
            anchor_x='center', anchor_y='center'
        )
        self.ui_elements.extend([self.lbl_jugador, self.lbl_enemigo])

        # ── Barras de vida y energía ──────────────────────────────────────
        bar_w  = int(min(w * 0.28, 260))
        bar_h  = int(h * 0.028)
        ebar_h = int(h * 0.016)
        bar_gap = int(h * 0.010)

        bar_y      = sprite_cy - sprite_size // 2 - int(h * 0.035)
        ebar_y     = bar_y - bar_h - bar_gap

        self.vida_bar_j = HealthBar(
            x=self.jugador_cx - bar_w // 2, y=bar_y,
            width=bar_w, height=bar_h,
            max_value=self.jugador.vida_maxima,
            current_value=self.jugador.vida_actual,
            color_lleno=(80, 200, 100)
        )
        self.vida_bar_e = HealthBar(
            x=self.enemigo_cx - bar_w // 2, y=bar_y,
            width=bar_w, height=bar_h,
            max_value=self.enemigo.vida_maxima,
            current_value=self.enemigo.vida_actual,
            color_lleno=(200, 80, 80)
        )
        self.energia_bar_j = HealthBar(
            x=self.jugador_cx - bar_w // 2, y=ebar_y,
            width=bar_w, height=ebar_h,
            max_value=self.jugador.energia_maxima,
            current_value=self.jugador.energia_actual,
            color_lleno=(80, 140, 210)
        )
        self.energia_bar_e = HealthBar(
            x=self.enemigo_cx - bar_w // 2, y=ebar_y,
            width=bar_w, height=ebar_h,
            max_value=self.enemigo.energia_maxima,
            current_value=self.enemigo.energia_actual,
            color_lleno=(210, 140, 80)
        )
        self.static_elements.extend([
            self.vida_bar_j, self.vida_bar_e,
            self.energia_bar_j, self.energia_bar_e
        ])

        # ── Indicador de turno (header) ───────────────────────────────────
        turn_y  = h - HEADER_H // 2
        turn_sz = max(16, int(h * 0.035))
        self.turn_indicator = RetroLabel(
            "TU TURNO" if self.turno_jugador else "TURNO DEL RIVAL",
            w // 2, turn_y,
            font_size=turn_sz,
            color=(255, 255, 100) if self.turno_jugador else (200, 200, 200),
            anchor_x='center', anchor_y='center'
        )
        self.ui_elements.append(self.turn_indicator)

        # ── Área de mensajes ──────────────────────────────────────────────
        self.msg_rect = (
            int(w * 0.04), msg_zone_y,
            int(w * 0.92), MSG_H
        )
        msg_font = max(11, int(h * 0.019))
        self.lbl_mensaje = RetroLabel(
            "¡Bienvenido al combate!",
            x=int(w * 0.05),
            y=msg_zone_top - int(h * 0.005),
            width=int(w * 0.90),
            font_size=msg_font,
            anchor_x='left', anchor_y='top',
            multiline=True, color=(230, 230, 230)
        )
        self.ui_elements.append(self.lbl_mensaje)

        # ── Botones de acción principales ─────────────────────────────────
        n_btns  = 4
        btn_pad = int(w * 0.025)
        btn_w   = int((w - (n_btns + 1) * btn_pad) / n_btns)
        btn_h   = int(ACTION_H * 0.72)
        btn_y   = action_zone_y + (ACTION_H - btn_h) // 2

        btns_info = [
            ("ATAQUE",      (140, 80,  80),  (180, 110, 110), self.ataque_basico),
            ("DEFENDER",    (80,  80,  140), (110, 110, 180), self.defender),
            ("CONCENTRAR",  (80,  130, 80),  (110, 170, 110), self.concentrar),
            ("HABILIDAD",   (130, 130, 70),  (170, 170, 100), self.mostrar_habilidades),
        ]
        action_btns = []
        for i, (text, nc, hc, cb) in enumerate(btns_info):
            bx = btn_pad + i * (btn_w + btn_pad)
            btn = ImageButton(
                x=bx, y=btn_y, width=btn_w, height=btn_h,
                text=text, normal_color=nc, hover_color=hc,
                callback=cb
            )
            action_btns.append(btn)

        self.btn_ataque, self.btn_defender, self.btn_concentrar, self.btn_habilidad = action_btns
        self.ui_elements.extend(action_btns)

        # ── Botones de habilidades (superpuestos sobre los principales) ───
        self._crear_botones_habilidad(action_zone_y, ACTION_H)

        # ── Botones postcombate ───────────────────────────────────────────
        pc_btn_w = int(min(w * 0.20, 200))
        pc_btn_h = int(ACTION_H * 0.65)
        pc_btn_y = action_zone_y + (ACTION_H - pc_btn_h) // 2
        pc_gap   = int(w * 0.03)
        total_pc = 3 * pc_btn_w + 2 * pc_gap
        pc_start = (w - total_pc) // 2

        self.btn_revancha = ImageButton(
            x=pc_start, y=pc_btn_y,
            width=pc_btn_w, height=pc_btn_h,
            text="REVANCHA",
            normal_color=(0, 130, 0), hover_color=(0, 180, 0),
            callback=self.revancha
        )
        self.btn_historial = ImageButton(
            x=pc_start + pc_btn_w + pc_gap, y=pc_btn_y,
            width=pc_btn_w, height=pc_btn_h,
            text="HISTORIAL",
            normal_color=(130, 130, 0), hover_color=(180, 180, 0),
            callback=self.ver_historial
        )
        self.btn_menu = ImageButton(
            x=pc_start + 2 * (pc_btn_w + pc_gap), y=pc_btn_y,
            width=pc_btn_w, height=pc_btn_h,
            text="MENÚ",
            normal_color=(130, 0, 0), hover_color=(180, 0, 0),
            callback=self.volver_menu
        )
        self.postcombate_buttons = [self.btn_revancha, self.btn_historial, self.btn_menu]
        for btn in self.postcombate_buttons:
            btn.visible = False
            self.ui_elements.append(btn)

        self._actualizar_visibilidad()

    # ─────────────────────────────────────────────────────────────────────
    def _crear_botones_habilidad(self, action_zone_y, ACTION_H):
        w = self.app.width
        if not self.jugador.habilidades:
            return

        num_hab    = len(self.jugador.habilidades)
        hab_btn_h  = int(ACTION_H * 0.52)
        cancel_h   = int(ACTION_H * 0.35)
        hab_btn_w  = int(min((w * 0.88) / (num_hab + 0.5), 160))
        hab_btn_w  = max(hab_btn_w, 80)

        total_w    = num_hab * hab_btn_w + (num_hab - 1) * 8
        start_x    = (w - total_w) // 2
        hab_y      = action_zone_y + (ACTION_H - hab_btn_h) // 2

        for i, habilidad in enumerate(self.jugador.habilidades):
            btn = ImageButton(
                x=start_x + i * (hab_btn_w + 8), y=hab_y,
                width=hab_btn_w, height=hab_btn_h,
                text=habilidad.nombre,
                normal_color=(90, 90, 145), hover_color=(120, 120, 185),
                callback=lambda idx=i: self.usar_habilidad_idx(idx)
            )
            self.habilidad_buttons.append(btn)

        cancel_y = action_zone_y + (ACTION_H - cancel_h) // 2
        btn_cancel = ImageButton(
            x=w - int(w * 0.10) - hab_btn_w // 2, y=cancel_y,
            width=int(w * 0.10), height=cancel_h,
            text="✕",
            normal_color=(140, 60, 60), hover_color=(180, 90, 90),
            callback=self.ocultar_habilidades
        )
        self.habilidad_buttons.append(btn_cancel)

    # ─────────────────────────────────────────────────────────────────────
    def _actualizar_visibilidad(self):
        visible_principales = self.turno_jugador and not self.mostrando_habilidades
        for btn in [self.btn_ataque, self.btn_defender, self.btn_concentrar, self.btn_habilidad]:
            btn.visible = visible_principales
        for btn in self.habilidad_buttons:
            btn.visible = self.turno_jugador and self.mostrando_habilidades

    def mostrar_habilidades(self):
        self.mostrando_habilidades = True
        self._actualizar_visibilidad()

    def ocultar_habilidades(self):
        self.mostrando_habilidades = False
        self._actualizar_visibilidad()

    def usar_habilidad_idx(self, idx):
        if self.combate.estado != EstadoCombate.EN_CURSO or not self.turno_jugador:
            return
        habilidad = self.jugador.habilidades[idx]
        if self.jugador.energia_actual >= habilidad.costo_energia:
            self.resultado_turno = self.combate.ejecutar_turno(Accion.HABILIDAD_ESPECIAL, idx)
            self.turno_jugador   = False
            self.mostrando_habilidades = False
            self._actualizar_ui()
            self.ia_timer = 1.0
        else:
            self.lbl_mensaje.text = "Energía insuficiente"

    def ataque_basico(self):
        if self.combate.estado != EstadoCombate.EN_CURSO or not self.turno_jugador:
            return
        self.resultado_turno = self.combate.ejecutar_turno(Accion.ATAQUE_BASICO)
        self.turno_jugador   = False
        self._actualizar_ui()
        self.ia_timer = 1.0

    def defender(self):
        if self.combate.estado != EstadoCombate.EN_CURSO or not self.turno_jugador:
            return
        self.resultado_turno = self.combate.ejecutar_turno(Accion.DEFENDER)
        self.turno_jugador   = False
        self._actualizar_ui()
        self.ia_timer = 1.0

    def concentrar(self):
        if self.combate.estado != EstadoCombate.EN_CURSO or not self.turno_jugador:
            return
        self.resultado_turno = self.combate.ejecutar_turno(Accion.CONCENTRAR)
        self.turno_jugador   = False
        self._actualizar_ui()
        self.ia_timer = 1.0

    def on_update(self, delta_time):
        if self.ia_timer > 0:
            self.ia_timer -= delta_time
            if self.ia_timer <= 0 and not self.turno_jugador and self.combate.estado == EstadoCombate.EN_CURSO:
                self.resultado_turno = self.combate.ejecutar_turno_ia()
                self.turno_jugador   = True
                self._actualizar_ui()
                self.ia_timer = 0

    def _actualizar_ui(self):
        self.vida_bar_j.current_value    = self.jugador.vida_actual
        self.vida_bar_e.current_value    = self.enemigo.vida_actual
        self.energia_bar_j.current_value = self.jugador.energia_actual
        self.energia_bar_e.current_value = self.enemigo.energia_actual

        self.turn_indicator.text  = "TU TURNO" if self.turno_jugador else "TURNO DEL RIVAL"
        self.turn_indicator.color = (255, 255, 100) if self.turno_jugador else (200, 200, 200)

        if self.resultado_turno:
            mensajes = []
            if self.resultado_turno.jugador_accion:
                mensajes.append(self.resultado_turno.jugador_accion)
            if self.resultado_turno.ia_accion:
                mensajes.append(self.resultado_turno.ia_accion)
            if self.resultado_turno.daño_jugador_a_ia:
                mensajes.append(f"Daño a enemigo: {self.resultado_turno.daño_jugador_a_ia}")
            if self.resultado_turno.daño_ia_a_jugador:
                mensajes.append(f"Daño recibido: {self.resultado_turno.daño_ia_a_jugador}")
            if self.resultado_turno.evento_aleatorio:
                mensajes.append(self.resultado_turno.evento_aleatorio.get('mensaje', ''))
            self.lbl_mensaje.text = "\n".join(mensajes[-4:])

        if self.combate.estado != EstadoCombate.EN_CURSO:
            resultado_final = self.combate.obtener_resultado_final()
            self.lbl_mensaje.text = resultado_final.mensaje_final
            self.turno_jugador    = False
            for btn in [self.btn_ataque, self.btn_defender, self.btn_concentrar, self.btn_habilidad]:
                btn.visible = False
            for btn in self.habilidad_buttons:
                btn.visible = False
            for btn in self.postcombate_buttons:
                btn.visible = True
            self.turn_indicator.text  = "COMBATE FINALIZADO"
            self.turn_indicator.color = (255, 200, 200)
        else:
            self._actualizar_visibilidad()

    def on_draw(self):
        self.clear()
        w, h = self.app.width, self.app.height

        # Fondo degradado sutil
        arcade.draw_rect_filled(arcade.XYWH(w // 2, h // 2, w, h), (28, 32, 48))

        self.sprite_list.draw()

        for elem in self.static_elements:
            elem.draw()

        # Rectángulo de mensajes con fondo oscuro semitransparente
        mx, my, mw, mh = self.msg_rect
        arcade.draw_rect_filled(
            arcade.LBWH(mx, my, mw, mh),
            (15, 17, 28, 210)
        )
        arcade.draw_rect_outline(
            arcade.LBWH(mx, my, mw, mh),
            (60, 65, 90, 180), border_width=1
        )

        for elem in self.ui_elements:
            if hasattr(elem, 'draw'):
                elem.draw()
        for btn in self.habilidad_buttons:
            btn.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)
        for btn in self.ui_elements + self.habilidad_buttons:
            if hasattr(btn, 'on_mouse_motion'):
                btn.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.habilidad_buttons:
            btn.on_mouse_press(x, y, button, modifiers)
        for elem in self.ui_elements:
            if hasattr(elem, 'on_mouse_press'):
                elem.on_mouse_press(x, y, button, modifiers)

    def revancha(self):
        nuevo_jugador = self.jugador_clase()
        nuevo_enemigo = self.enemigo_clase()
        self.app.goto_view(CombatView(self.app, nuevo_jugador, nuevo_enemigo))

    def ver_historial(self):
        def volver_de_historial():
            from scenes.menu_scene import MenuView
            self.app.goto_view(MenuView(self.app))
        self.app.push_view(HistorialView(self.app, self.combate.historial, on_back=volver_de_historial))

    def volver_menu(self):
        from scenes.menu_scene import MenuView
        self.app.goto_view(MenuView(self.app))

    def on_resize(self, width, height):
        self._setup_ui()