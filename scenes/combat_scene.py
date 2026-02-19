# scenes/combat_scene.py
import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel, HealthBar
from combate.sistema_combate import Combate, Accion, EstadoCombate
from scenes.historial_scene import HistorialView


class CombatView(BaseView):
    def __init__(self, app, jugador, enemigo):
        super().__init__(app)
        self.jugador        = jugador
        self.enemigo        = enemigo
        self.jugador_clase  = type(jugador)
        self.enemigo_clase  = type(enemigo)
        self.combate        = Combate(jugador, enemigo)
        self.ui_elements         = []
        self.habilidad_buttons   = []
        self.postcombate_buttons = []
        self.mostrando_habilidades = False
        self.turno_jugador      = True
        self.ia_timer            = 0
        self.evento_timer        = 0      # pausa para mostrar evento entre turnos
        self.evento_pendiente    = None   # dict del evento activo o None
        self.resultado_turno = None
        self.sprite_list    = arcade.SpriteList()
        # â”€â”€ Historial propio: acumulamos cada ResultadoTurno aquí â”€â”€â”€â”€â”€â”€â”€â”€â”€
        self.historial_turnos: list = []
        self._setup_ui()

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _setup_ui(self):
        self.ui_elements.clear()
        self.habilidad_buttons.clear()
        self.postcombate_buttons.clear()
        self.static_elements.clear()
        self.sprite_list.clear()

        w, h = self.app.width, self.app.height
        self.background_color = (28, 32, 48)

        # â”€â”€ Zonas verticales (de abajo hacia arriba) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        #
        #  [FOOTER_PAD]
        #  [ACTION_H  ]  â† botones principales / postcombate
        #  [GAP       ]
        #  [HAB_H     ]  â† botones de habilidad + cancelar  (banda propia)
        #  [GAP       ]
        #  [MSG_H     ]  â† log de mensajes
        #  [GAP       ]
        #  [arena     ]  â† sprites + barras
        #  [HEADER_H  ]  â† indicador de turno
        #
        FOOTER_PAD = int(h * 0.020)
        ACTION_H   = int(h * 0.130)
        HAB_H      = int(h * 0.095)
        MSG_H      = int(h * 0.120)
        GAP        = int(h * 0.012)
        HEADER_H   = int(h * 0.080)

        self.action_zone_y   = FOOTER_PAD
        self.action_zone_top = self.action_zone_y + ACTION_H

        # Banda de habilidades: ENCIMA de la de acción, sin contacto
        self.hab_zone_y      = self.action_zone_top + GAP
        self.hab_zone_top    = self.hab_zone_y + HAB_H

        msg_zone_y           = self.hab_zone_top + GAP
        msg_zone_top         = msg_zone_y + MSG_H

        arena_bottom = msg_zone_top + GAP
        arena_top    = h - HEADER_H - GAP
        arena_h      = arena_top - arena_bottom
        arena_mid_y  = (arena_bottom + arena_top) // 2

        # â”€â”€ Sprites â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        sprite_size = int(min(arena_h * 0.55, w * 0.15, 150))
        sprite_size = max(sprite_size, 70)

        margin_x        = int(w * 0.05)
        self.jugador_cx = margin_x + int(w * 0.15)
        self.enemigo_cx = w - margin_x - int(w * 0.15)
        sprite_cy       = int(arena_mid_y + arena_h * 0.04)

        def _load_sprite(cls_nombre, cx, cy):
            try:
                tex = arcade.load_texture(f'img/personajes/{cls_nombre.lower()}.png')
                s   = arcade.Sprite(tex, center_x=cx, center_y=cy)
                s.width = s.height = sprite_size
                self.sprite_list.append(s)
                return s
            except Exception:
                return None

        self.sprite_jugador = _load_sprite(type(self.jugador).__name__, self.jugador_cx, sprite_cy)
        self.sprite_enemigo = _load_sprite(type(self.enemigo).__name__, self.enemigo_cx, sprite_cy)

        # â”€â”€ Nombres â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        name_y  = sprite_cy + sprite_size // 2 + int(h * 0.022)
        name_sz = max(12, int(h * 0.024))
        self.lbl_jugador = RetroLabel(
            self.jugador.nombre, self.jugador_cx, name_y,
            font_size=name_sz, color=(180, 230, 180), anchor_x='center', anchor_y='center'
        )
        self.lbl_enemigo = RetroLabel(
            self.enemigo.nombre, self.enemigo_cx, name_y,
            font_size=name_sz, color=(230, 180, 180), anchor_x='center', anchor_y='center'
        )
        self.ui_elements.extend([self.lbl_jugador, self.lbl_enemigo])

        # â”€â”€ Barras de vida y energía â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        bar_w   = int(min(w * 0.28, 260))
        bar_h   = int(h * 0.028)
        ebar_h  = int(h * 0.016)
        bar_gap = int(h * 0.010)
        bar_y   = sprite_cy - sprite_size // 2 - int(h * 0.038)
        ebar_y  = bar_y - bar_h - bar_gap

        self.vida_bar_j = HealthBar(
            x=self.jugador_cx - bar_w // 2, y=bar_y,
            width=bar_w, height=bar_h,
            max_value=self.jugador.vida_maxima, current_value=self.jugador.vida_actual,
            color_lleno=(80, 200, 100)
        )
        self.vida_bar_e = HealthBar(
            x=self.enemigo_cx - bar_w // 2, y=bar_y,
            width=bar_w, height=bar_h,
            max_value=self.enemigo.vida_maxima, current_value=self.enemigo.vida_actual,
            color_lleno=(200, 80, 80)
        )
        self.energia_bar_j = HealthBar(
            x=self.jugador_cx - bar_w // 2, y=ebar_y,
            width=bar_w, height=ebar_h,
            max_value=self.jugador.energia_maxima, current_value=self.jugador.energia_actual,
            color_lleno=(80, 140, 210)
        )
        self.energia_bar_e = HealthBar(
            x=self.enemigo_cx - bar_w // 2, y=ebar_y,
            width=bar_w, height=ebar_h,
            max_value=self.enemigo.energia_maxima, current_value=self.enemigo.energia_actual,
            color_lleno=(210, 140, 80)
        )
        self.static_elements.extend([
            self.vida_bar_j, self.vida_bar_e,
            self.energia_bar_j, self.energia_bar_e
        ])

        # â”€â”€ Indicador de turno (header) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        turn_sz = max(16, int(h * 0.035))
        self.turn_indicator = RetroLabel(
            "TU TURNO" if self.turno_jugador else "TURNO DEL RIVAL",
            w // 2, h - HEADER_H // 2,
            font_size=turn_sz,
            color=(255, 255, 100) if self.turno_jugador else (200, 200, 200),
            anchor_x='center', anchor_y='center'
        )
        self.ui_elements.append(self.turn_indicator)

        # Hint F11 en el header
        self.ui_elements.append(RetroLabel(
            "F11 â€” Pantalla completa",
            w - int(w * 0.01), h - HEADER_H // 2,
            font_size=max(9, int(h * 0.016)),
            color=(120, 120, 140),
            anchor_x='right', anchor_y='center'
        ))

        # â”€â”€ Área de mensajes â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        self.msg_rect = (int(w * 0.04), msg_zone_y, int(w * 0.92), MSG_H)
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

        # â”€â”€ Botones de acción principales â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        n_btns  = 4
        btn_pad = int(w * 0.025)
        btn_w   = int((w - (n_btns + 1) * btn_pad) / n_btns)
        btn_h   = int(ACTION_H * 0.72)
        btn_y   = self.action_zone_y + (ACTION_H - btn_h) // 2

        btns_info = [
            ("ATAQUE",     (140, 80,  80),  (180, 110, 110), self.ataque_basico),
            ("DEFENDER",   (80,  80,  140), (110, 110, 180), self.defender),
            ("CONCENTRAR", (80,  130, 80),  (110, 170, 110), self.concentrar),
            ("HABILIDAD",  (130, 130, 70),  (170, 170, 100), self.mostrar_habilidades),
        ]
        action_btns = []
        for i, (text, nc, hc, cb) in enumerate(btns_info):
            bx = btn_pad + i * (btn_w + btn_pad)
            action_btns.append(ImageButton(
                x=bx, y=btn_y, width=btn_w, height=btn_h,
                text=text, normal_color=nc, hover_color=hc, callback=cb
            ))
        self.btn_ataque, self.btn_defender, self.btn_concentrar, self.btn_habilidad = action_btns
        self.ui_elements.extend(action_btns)

        # â”€â”€ Botones de habilidades (banda propia, SIN solapamiento) â”€â”€â”€â”€â”€â”€â”€
        self._crear_botones_habilidad()

        # â”€â”€ Botones postcombate â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        pc_btn_w = int(min(w * 0.20, 200))
        pc_btn_h = int(ACTION_H * 0.65)
        pc_btn_y = self.action_zone_y + (ACTION_H - pc_btn_h) // 2
        pc_gap   = int(w * 0.03)
        total_pc = 3 * pc_btn_w + 2 * pc_gap
        pc_start = (w - total_pc) // 2

        self.btn_revancha  = ImageButton(
            x=pc_start, y=pc_btn_y, width=pc_btn_w, height=pc_btn_h,
            text="REVANCHA", normal_color=(0, 130, 0), hover_color=(0, 180, 0),
            callback=self.revancha
        )
        self.btn_historial = ImageButton(
            x=pc_start + pc_btn_w + pc_gap, y=pc_btn_y, width=pc_btn_w, height=pc_btn_h,
            text="HISTORIAL", normal_color=(130, 130, 0), hover_color=(180, 180, 0),
            callback=self.ver_historial
        )
        self.btn_menu = ImageButton(
            x=pc_start + 2 * (pc_btn_w + pc_gap), y=pc_btn_y, width=pc_btn_w, height=pc_btn_h,
            text="MENÃš", normal_color=(130, 0, 0), hover_color=(180, 0, 0),
            callback=self.volver_menu
        )
        self.postcombate_buttons = [self.btn_revancha, self.btn_historial, self.btn_menu]
        for btn in self.postcombate_buttons:
            btn.visible = False
            self.ui_elements.append(btn)

        self._actualizar_visibilidad()

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _crear_botones_habilidad(self):
        """
        Los botones de habilidad viven EXCLUSIVAMENTE en [hab_zone_y, hab_zone_top].
        El botón Cancelar también está en esa misma banda, en el extremo derecho.
        No hay ningún píxel compartido con la zona de acción principal.
        """
        w = self.app.width
        if not self.jugador.habilidades:
            return

        num_hab  = len(self.jugador.habilidades)
        band_h   = self.hab_zone_top - self.hab_zone_y

        # Cancelar: 10 % del ancho, pegado a la derecha
        cancel_w   = int(w * 0.10)
        cancel_gap = int(w * 0.015)
        cancel_h   = int(band_h * 0.62)
        cancel_y   = self.hab_zone_y + (band_h - cancel_h) // 2

        # Habilidades: el resto del ancho, dividido equitativamente
        avail_w    = w - cancel_w - cancel_gap * 3
        gap_entre  = 8
        hab_btn_w  = int((avail_w - (num_hab - 1) * gap_entre) / num_hab)
        hab_btn_w  = max(hab_btn_w, 60)
        hab_btn_h  = int(band_h * 0.72)
        hab_btn_y  = self.hab_zone_y + (band_h - hab_btn_h) // 2

        total_hab  = num_hab * hab_btn_w + (num_hab - 1) * gap_entre
        start_x    = cancel_gap + (avail_w - total_hab) // 2

        for i, hab in enumerate(self.jugador.habilidades):
            btn = ImageButton(
                x=start_x + i * (hab_btn_w + gap_entre),
                y=hab_btn_y,
                width=hab_btn_w, height=hab_btn_h,
                text=hab.nombre,
                normal_color=(85, 85, 140), hover_color=(115, 115, 185),
                callback=lambda idx=i: self.usar_habilidad_idx(idx)
            )
            self.habilidad_buttons.append(btn)

        btn_cancel = ImageButton(
            x=w - cancel_w - cancel_gap,
            y=cancel_y,
            width=cancel_w, height=cancel_h,
            text="âœ• Cancelar",
            normal_color=(140, 50, 50), hover_color=(190, 80, 80),
            callback=self.ocultar_habilidades
        )
        self.habilidad_buttons.append(btn_cancel)

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _actualizar_visibilidad(self):
        en_curso = (self.combate.estado == EstadoCombate.EN_CURSO)
        visible_accion = self.turno_jugador and not self.mostrando_habilidades and en_curso
        visible_hab    = self.turno_jugador and self.mostrando_habilidades and en_curso

        for btn in [self.btn_ataque, self.btn_defender, self.btn_concentrar, self.btn_habilidad]:
            btn.visible = visible_accion
        for btn in self.habilidad_buttons:
            btn.visible = visible_hab

    def mostrar_habilidades(self):
        self.mostrando_habilidades = True
        self._actualizar_visibilidad()

    def ocultar_habilidades(self):
        self.mostrando_habilidades = False
        self._actualizar_visibilidad()

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _registrar_resultado(self, resultado):
        """Guarda el ResultadoTurno en nuestro historial propio."""
        if resultado is not None:
            self.historial_turnos.append(resultado)

    def usar_habilidad_idx(self, idx):
        if self.combate.estado != EstadoCombate.EN_CURSO or not self.turno_jugador:
            return
        hab = self.jugador.habilidades[idx]
        if self.jugador.energia_actual >= hab.costo_energia:
            res = self.combate.ejecutar_turno(Accion.HABILIDAD_ESPECIAL, idx)
            self._registrar_resultado(res)
            self.resultado_turno       = res
            self.turno_jugador         = False
            self.mostrando_habilidades = False
            self._actualizar_ui()
            self.evento_timer = 0.5
        else:
            self.lbl_mensaje.text = "Energía insuficiente"

    def ataque_basico(self):
        if self.combate.estado != EstadoCombate.EN_CURSO or not self.turno_jugador:
            return
        res = self.combate.ejecutar_turno(Accion.ATAQUE_BASICO)
        self._registrar_resultado(res)
        self.resultado_turno = res
        self.turno_jugador   = False
        self._actualizar_ui()
        self.evento_timer = 0.5

    def defender(self):
        if self.combate.estado != EstadoCombate.EN_CURSO or not self.turno_jugador:
            return
        res = self.combate.ejecutar_turno(Accion.DEFENDER)
        self._registrar_resultado(res)
        self.resultado_turno = res
        self.turno_jugador   = False
        self._actualizar_ui()
        self.evento_timer = 0.5

    def concentrar(self):
        if self.combate.estado != EstadoCombate.EN_CURSO or not self.turno_jugador:
            return
        res = self.combate.ejecutar_turno(Accion.CONCENTRAR)
        self._registrar_resultado(res)
        self.resultado_turno = res
        self.turno_jugador   = False
        self._actualizar_ui()
        self.evento_timer = 0.5

    def on_update(self, delta_time):
        super().on_update(delta_time)

        # ── FASE 1: pequeña pausa tras la acción del jugador ─────────────────
        if self.evento_timer > 0 and not self.turno_jugador:
            self.evento_timer -= delta_time
            if self.evento_timer <= 0 and self.combate.estado == EstadoCombate.EN_CURSO:
                ev = self.combate.verificar_y_activar_evento()
                self.evento_pendiente = ev
                if ev:
                    self._mostrar_evento(ev)
                    self.ia_timer = 1.8    # más tiempo para leer el evento
                else:
                    self.ia_timer = 0.7    # sin evento, pausa breve

        # ── FASE 2: pausa (con o sin evento) antes de que actúe la IA ────────
        elif self.ia_timer > 0 and not self.turno_jugador:
            self.ia_timer -= delta_time
            if self.ia_timer <= 0 and self.combate.estado == EstadoCombate.EN_CURSO:
                res = self.combate.ejecutar_turno_ia()
                self._registrar_resultado(res)
                self.resultado_turno  = res
                self.evento_pendiente = None
                self.turno_jugador    = True
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
            r = self.resultado_turno
            if getattr(r, 'jugador_accion', None):
                mensajes.append(r.jugador_accion)
            if getattr(r, 'ia_accion', None):
                mensajes.append(r.ia_accion)
            daño_j = getattr(r, 'daño_jugador_a_ia', None)
            if daño_j:
                mensajes.append(f"Daño a enemigo: {daño_j}")
            daño_e = getattr(r, 'daño_ia_a_jugador', None)
            if daño_e:
                mensajes.append(f"Daño recibido: {daño_e}")
            evento = getattr(r, 'evento_aleatorio', None)
            if evento:
                mensajes.append(evento.get('mensaje', ''))
            self.lbl_mensaje.text  = "\n".join(mensajes[-4:])
            self.lbl_mensaje.color = (220, 220, 220)

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

        arcade.draw_rect_filled(arcade.XYWH(w // 2, h // 2, w, h), (28, 32, 48))
        self.sprite_list.draw()

        for elem in self.static_elements:
            elem.draw()

        # Fondo del log de mensajes
        mx, my, mw, mh = self.msg_rect
        arcade.draw_rect_filled(arcade.LBWH(mx, my, mw, mh), (15, 17, 28, 210))
        arcade.draw_rect_outline(arcade.LBWH(mx, my, mw, mh), (60, 65, 90, 180), border_width=1)

        # Fondo sutil de la banda de habilidades cuando está activa
        if self.mostrando_habilidades:
            arcade.draw_rect_filled(
                arcade.LBWH(0, self.hab_zone_y,
                            w, self.hab_zone_top - self.hab_zone_y),
                (25, 28, 52, 220)
            )
            arcade.draw_rect_outline(
                arcade.LBWH(0, self.hab_zone_y,
                            w, self.hab_zone_top - self.hab_zone_y),
                (80, 80, 140, 180), border_width=1
            )

        for elem in self.ui_elements:
            if hasattr(elem, 'draw'):
                elem.draw()

        for btn in self.habilidad_buttons:
            if hasattr(btn, 'draw'):
                btn.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        # Actualizar hover SOLO de los botones actualmente visibles/activos
        if self.mostrando_habilidades:
            for btn in self.habilidad_buttons:
                if hasattr(btn, 'on_mouse_motion'):
                    btn.on_mouse_motion(x, y, dx, dy)
        else:
            super().on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        # Si acabamos de entrar en la vista, ignorar el primer press.
        if self._block_next_press:
            return
        # Enrutamiento exclusivo: habilidades abiertas â†’ solo esos botones.
        if self.mostrando_habilidades:
            for btn in self.habilidad_buttons:
                if hasattr(btn, 'on_mouse_press'):
                    if btn.on_mouse_press(x, y, button, modifiers):
                        return
        else:
            for elem in self.ui_elements:
                if hasattr(elem, 'on_mouse_press'):
                    if elem.on_mouse_press(x, y, button, modifiers):
                        return

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.F11:
            self.app.set_fullscreen(not self.app.fullscreen)

    # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def revancha(self):
        nuevo_jugador = self.jugador_clase()
        nuevo_enemigo = self.enemigo_clase()
        self.app.goto_view(CombatView(self.app, nuevo_jugador, nuevo_enemigo))

    def ver_historial(self):
        # Preferimos nuestro historial propio; si está vacío usamos el del combate
        historial = self.historial_turnos or getattr(self.combate, 'historial', [])
        def _volver():
            from scenes.menu_scene import MenuView
            self.app.goto_view(MenuView(self.app))
        self.app.push_view(HistorialView(self.app, historial, on_back=_volver))

    def volver_menu(self):
        from scenes.menu_scene import MenuView
        self.app.goto_view(MenuView(self.app))

    def on_resize(self, width, height):
        self._setup_ui()