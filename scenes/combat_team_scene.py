# scenes/combat_team_scene.py
"""
Vista de combate por equipos (1v1 hasta 4v4).

Mejoras visuales del sistema de turnos:
  - Cola de turnos: franja horizontal sobre el arena mostrando el orden
    de actuación del round. El activo aparece resaltado y más grande.
  - Indicador activo: anillo pulsante + flecha ▼ sobre el sprite en turno.
  - Badges de estados: píldoras de color bajo las barras de cada personaje.
  - Contador de ronda: badge "RONDA X" en la esquina superior derecha.
  - Flash "¡TU TURNO!": banner semitransparente al empezar turno de jugador.
"""

import math
import re as _re
import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel, HealthBar
from combate.sistema_combate_equipo import (
    CombateEquipo, Accion, EstadoCombate, ResultadoAccion
)
from scenes.historial_scene import HistorialView

# ── Paleta de equipos ─────────────────────────────────────────────────────
COL_EQ1 = (80, 160, 255)
COL_EQ2 = (255, 80,  80)
COL_IA  = (200, 130, 220)
COL_JUG = (130, 220, 130)

# ── Estados: emoji corto para los badges ─────────────────────────────────
ESTADO_BADGE = {
    "dormido":     ("😴", (100, 100, 180)),
    "paralizado":  ("⚡", (200, 200,  50)),
    "confundido":  ("💫", (200, 100, 200)),
    "quemado":     ("🔥", (220,  90,  30)),
    "sangrando":   ("🩸", (200,  40,  40)),
    "envenenado":  ("☠",  ( 80, 180,  80)),
    "bajon_azucar":("🍬", (180, 140,  40)),
    "defendiendo": ("🛡", ( 70, 130, 200)),
    "concentrando":("✨", (180, 180,  60)),
}

MAX_LOG = 8


class CombatTeamView(BaseView):
    def __init__(self, app, equipo1: list, equipo2: list):
        super().__init__(app)
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.combate = CombateEquipo(equipo1, equipo2)

        self.ui_elements     = []
        self.habilidad_btns  = []
        self.objetivo_btns   = []
        self.post_btns       = []
        self.health_bars     = {}   # personaje -> (vida_bar, energia_bar)
        self.sprite_list     = arcade.SpriteList()

        self.mostrando_habilidades   = False
        self.esperando_objetivo      = False
        self.accion_pendiente: Accion      = None
        self.habilidad_idx_pendiente: int  = None
        self._log: list         = ["¡Comienza la batalla!"]
        self._combate_terminado = False
        self._ia_pendiente      = False

        # Historial plano (ResultadoAccion + entradas de evento)
        self._historial_plano: list = []

        # ── Animación ─────────────────────────────────────────────────────
        self._anim_time: float  = 0.0          # reloj continuo (segundos)
        self._flash_timer: float = 0.0         # segundos restantes del banner "¡TU TURNO!"
        self._flash_es_jugador: bool = False
        self._round_prev: int   = 0            # para detectar cambio de ronda
        self._round_flash: float = 0.0         # segundos del flash de nueva ronda

        self._setup_ui()
        self._ejecutar_ias_y_actualizar()

    # ═══════════════════════════════════════════════════════════════════════
    # Construcción de la UI
    # ═══════════════════════════════════════════════════════════════════════

    def _setup_ui(self):
        self.ui_elements.clear()
        self.habilidad_btns.clear()
        self.objetivo_btns.clear()
        self.post_btns.clear()
        self.health_bars.clear()
        self.static_elements.clear()
        self.sprite_list.clear()

        w, h = self.app.width, self.app.height
        self.background_color = (25, 30, 50)

        # ── Zonas verticales ──────────────────────────────────────────────
        # [buttons]  [log]  [turn_queue]  [arena]
        #
        btn_y       = 15
        btn_h_sz    = 55
        log_y       = int(h * 0.28)
        log_h       = int(h * 0.18)
        queue_h     = max(40, int(h * 0.07))    # franja de cola de turnos
        queue_y     = log_y + log_h
        arena_bot   = queue_y + queue_h
        arena_top   = h - 10
        arena_h     = arena_top - arena_bot
        arena_mid_y = arena_bot + arena_h // 2

        self._log_rect   = (10, log_y, w - 20, log_h)
        self._queue_rect = (0, queue_y, w, queue_h)
        self._arena_bot  = arena_bot
        self._arena_top  = arena_top
        self._queue_y    = queue_y
        self._queue_h    = queue_h

        # ── Sprites y barras de vida ──────────────────────────────────────
        def _place_team(team, x_start, x_end, flip=False):
            n      = len(team)
            slot_w = (x_end - x_start) // max(n, 1)
            sp_size = min(90, slot_w - 24)
            y_sprite = arena_mid_y

            for i, p in enumerate(team):
                cx = x_start + i * slot_w + slot_w // 2

                # Guardar posición para los indicadores visuales
                p._cx      = cx
                p._cy      = y_sprite
                p._sp_size = sp_size

                # Sprite
                try:
                    tex = arcade.load_texture(
                        f'img/personajes/{type(p).__name__.lower()}.png'
                    )
                    sp = arcade.Sprite(tex)
                    sp.center_x = cx
                    sp.center_y = y_sprite
                    sp.width    = sp_size
                    sp.height   = sp_size
                    if flip:
                        sp.scale_xy = (-abs(sp.scale_xy[0]), sp.scale_xy[1])
                    self.sprite_list.append(sp)
                    p._sprite = sp
                except Exception:
                    p._sprite = None

                # Etiqueta de nombre
                ctrl    = "🤖" if p.es_ia else "🎮"
                lbl_col = COL_IA if p.es_ia else COL_JUG
                self.ui_elements.append(RetroLabel(
                    f"{ctrl} {p.nombre[:10]}",
                    cx, y_sprite + sp_size // 2 + 16,
                    font_size=10, color=lbl_col,
                    anchor_x='center', anchor_y='center'
                ))

                # Barras de vida / energía
                bar_w   = min(110, slot_w - 12)
                bar_x   = cx - bar_w // 2
                bar_y_v = y_sprite - sp_size // 2 - 18
                bar_y_e = bar_y_v - 14

                # Guardar posición para badges de estado
                p._bar_y_bottom = bar_y_e - 2

                vbar = HealthBar(
                    x=bar_x, y=bar_y_v, width=bar_w, height=13,
                    max_value=p.vida_maxima, current_value=p.vida_actual,
                    color_lleno=COL_EQ1 if not flip else COL_EQ2
                )
                ebar = HealthBar(
                    x=bar_x, y=bar_y_e, width=bar_w, height=7,
                    max_value=p.energia_maxima, current_value=p.energia_actual,
                    color_lleno=(100, 180, 220)
                )
                self.static_elements.extend([vbar, ebar])
                self.health_bars[p] = (vbar, ebar)

        _place_team(self.equipo1, 10, w // 2 - 10)
        _place_team(self.equipo2, w // 2 + 10, w - 10, flip=True)

        # ── Log ───────────────────────────────────────────────────────────
        self.lbl_log = RetroLabel(
            "",
            20, log_y + log_h - 8,
            font_size=11, color=(220, 220, 220),
            anchor_x='left', anchor_y='top',
            multiline=True, width=w - 40
        )
        self.ui_elements.append(self.lbl_log)

        # ── Botones de acción ─────────────────────────────────────────────
        spacing  = 185
        btn_w_sz = 170
        total_w  = 4 * spacing - (spacing - btn_w_sz)
        bx_start = w // 2 - total_w // 2

        self.btn_ataque = ImageButton(
            x=bx_start, y=btn_y, width=btn_w_sz, height=btn_h_sz,
            text="ATAQUE",
            normal_color=(140, 80, 80), hover_color=(180, 110, 110),
            callback=self._cmd_ataque
        )
        self.btn_defender = ImageButton(
            x=bx_start + spacing, y=btn_y, width=btn_w_sz, height=btn_h_sz,
            text="DEFENDER",
            normal_color=(80, 80, 140), hover_color=(110, 110, 180),
            callback=self._cmd_defender
        )
        self.btn_concentrar = ImageButton(
            x=bx_start + 2 * spacing, y=btn_y, width=btn_w_sz, height=btn_h_sz,
            text="CONCENTRAR",
            normal_color=(80, 130, 80), hover_color=(110, 170, 110),
            callback=self._cmd_concentrar
        )
        self.btn_habilidad = ImageButton(
            x=bx_start + 3 * spacing, y=btn_y, width=btn_w_sz, height=btn_h_sz,
            text="HABILIDAD",
            normal_color=(130, 130, 80), hover_color=(170, 170, 110),
            callback=self._cmd_mostrar_habilidades
        )
        self._action_btns = [self.btn_ataque, self.btn_defender,
                             self.btn_concentrar, self.btn_habilidad]
        self.ui_elements.extend(self._action_btns)

        self._crear_habilidad_btns(btn_y + btn_h_sz + 8)

        # ── Botones postcombate ───────────────────────────────────────────
        pc_btn_w = 190
        pc_btn_h = 50
        pc_gap   = 20
        total_pc = 3 * pc_btn_w + 2 * pc_gap
        pc_start = w // 2 - total_pc // 2

        self.btn_revancha = ImageButton(
            x=pc_start, y=btn_y, width=pc_btn_w, height=pc_btn_h,
            text="REVANCHA",
            normal_color=(0, 130, 0), hover_color=(0, 180, 0),
            callback=self._revancha
        )
        self.btn_historial = ImageButton(
            x=pc_start + pc_btn_w + pc_gap, y=btn_y,
            width=pc_btn_w, height=pc_btn_h,
            text="HISTORIAL",
            normal_color=(130, 130, 0), hover_color=(180, 180, 0),
            callback=self._ver_historial
        )
        self.btn_menu = ImageButton(
            x=pc_start + 2 * (pc_btn_w + pc_gap), y=btn_y,
            width=pc_btn_w, height=pc_btn_h,
            text="MENÚ",
            normal_color=(130, 0, 0), hover_color=(180, 0, 0),
            callback=self._volver_menu
        )
        self.post_btns = [self.btn_revancha, self.btn_historial, self.btn_menu]
        for b in self.post_btns:
            b.visible = False
            self.ui_elements.append(b)

        self._actualizar_ui()

    # ── Habilidades y objetivos ───────────────────────────────────────────

    def _crear_habilidad_btns(self, y_hab):
        self.habilidad_btns.clear()
        actor = self.combate.personaje_turno_actual
        if actor is None or actor.es_ia:
            return
        habs = actor.habilidades
        if not habs:
            return
        w  = self.app.width
        bw = 140
        sx = w // 2 - (len(habs) * (bw + 8) - 8) // 2
        for i, hab in enumerate(habs):
            ok = actor.energia_actual >= hab.costo_energia
            btn = ImageButton(
                x=sx + i * (bw + 8), y=y_hab, width=bw, height=48,
                text=f"{hab.nombre[:14]}\n({hab.costo_energia}E)",
                normal_color=(80, 80, 140) if ok else (60, 60, 80),
                hover_color=(110, 110, 180) if ok else (70, 70, 90),
                callback=lambda idx=i: self._cmd_usar_habilidad(idx)
            )
            btn.visible = False
            self.habilidad_btns.append(btn)
        btn_cancel = ImageButton(
            x=w // 2 - 70, y=y_hab - 56, width=140, height=40,
            text="CANCELAR",
            normal_color=(140, 70, 70), hover_color=(180, 90, 90),
            callback=self._cmd_ocultar_habilidades
        )
        btn_cancel.visible = False
        self.habilidad_btns.append(btn_cancel)

    def _crear_objetivo_btns(self, accion: Accion, hab_idx: int = None):
        self.objetivo_btns.clear()
        actor = self.combate.personaje_turno_actual
        if actor is None:
            return
        w, _h = self.app.width, self.app.height
        hab    = actor.habilidades[hab_idx] if hab_idx is not None else None
        es_cur = getattr(hab, 'es_curacion', False) if hab else False
        if es_cur:
            candidatos = [p for p in self.combate.equipo_propio_de(actor) if p.esta_vivo()]
        else:
            candidatos = [p for p in self.combate.equipo_rival_de(actor) if p.esta_vivo()]
        bw, gap = 150, 10
        sx = w // 2 - (len(candidatos) * (bw + gap) - gap) // 2
        for i, cand in enumerate(candidatos):
            btn = ImageButton(
                x=sx + i * (bw + gap), y=15, width=bw, height=50,
                text=cand.nombre[:14],
                normal_color=(100, 80, 140), hover_color=(140, 110, 190),
                callback=lambda obj=cand: self._cmd_confirmar_objetivo(obj)
            )
            self.objetivo_btns.append(btn)
        self.objetivo_btns.append(ImageButton(
            x=w - 160, y=15, width=140, height=40,
            text="CANCELAR",
            normal_color=(140, 70, 70), hover_color=(180, 90, 90),
            callback=self._cmd_cancelar_objetivo
        ))

    # ═══════════════════════════════════════════════════════════════════════
    # Comandos de acción
    # ═══════════════════════════════════════════════════════════════════════

    def _cmd_ataque(self):
        if self._combate_terminado:
            return
        actor = self.combate.personaje_turno_actual
        if actor is None or actor.es_ia:
            return
        rivales = [p for p in self.combate.equipo_rival_de(actor) if p.esta_vivo()]
        if len(rivales) == 1:
            self._ejecutar_jugador(Accion.ATAQUE_BASICO, rivales[0])
        else:
            self.accion_pendiente  = Accion.ATAQUE_BASICO
            self.esperando_objetivo = True
            self._crear_objetivo_btns(Accion.ATAQUE_BASICO)
            self._actualizar_visibilidad()

    def _cmd_defender(self):
        if self._combate_terminado:
            return
        actor = self.combate.personaje_turno_actual
        if actor is None or actor.es_ia:
            return
        self._ejecutar_jugador(Accion.DEFENDER, actor)

    def _cmd_concentrar(self):
        if self._combate_terminado:
            return
        actor = self.combate.personaje_turno_actual
        if actor is None or actor.es_ia:
            return
        self._ejecutar_jugador(Accion.CONCENTRAR, actor)

    def _cmd_mostrar_habilidades(self):
        if self._combate_terminado:
            return
        actor = self.combate.personaje_turno_actual
        if actor is None or actor.es_ia:
            return
        self.mostrando_habilidades = True
        self.esperando_objetivo    = False
        self._crear_habilidad_btns(15 + 55 + 8)
        self._actualizar_visibilidad()

    def _cmd_ocultar_habilidades(self):
        self.mostrando_habilidades = False
        self._actualizar_visibilidad()

    def _cmd_usar_habilidad(self, idx: int):
        if self._combate_terminado:
            return
        actor = self.combate.personaje_turno_actual
        if actor is None or actor.es_ia:
            return
        hab = actor.habilidades[idx]
        if actor.energia_actual < hab.costo_energia:
            self._log_add("Energía insuficiente.")
            return
        es_cur     = getattr(hab, 'es_curacion', False)
        candidatos = ([p for p in self.combate.equipo_propio_de(actor) if p.esta_vivo()]
                      if es_cur else
                      [p for p in self.combate.equipo_rival_de(actor) if p.esta_vivo()])
        if len(candidatos) == 1:
            self.mostrando_habilidades = False
            self._ejecutar_jugador(Accion.HABILIDAD_ESPECIAL, candidatos[0], idx)
        else:
            self.accion_pendiente        = Accion.HABILIDAD_ESPECIAL
            self.habilidad_idx_pendiente = idx
            self.esperando_objetivo      = True
            self.mostrando_habilidades   = False
            self._crear_objetivo_btns(Accion.HABILIDAD_ESPECIAL, idx)
            self._actualizar_visibilidad()

    def _cmd_confirmar_objetivo(self, objetivo):
        self.esperando_objetivo = False
        self._ejecutar_jugador(self.accion_pendiente, objetivo,
                               self.habilidad_idx_pendiente)
        self.accion_pendiente        = None
        self.habilidad_idx_pendiente = None
        self.objetivo_btns.clear()

    def _cmd_cancelar_objetivo(self):
        self.esperando_objetivo      = False
        self.accion_pendiente        = None
        self.habilidad_idx_pendiente = None
        self.objetivo_btns.clear()
        self._actualizar_visibilidad()

    # ═══════════════════════════════════════════════════════════════════════
    # Flujo de combate
    # ═══════════════════════════════════════════════════════════════════════

    def _ejecutar_jugador(self, accion: Accion, objetivo, hab_idx: int = None):
        if self.combate.estado != EstadoCombate.EN_CURSO:
            return
        resultado = self.combate.ejecutar_accion_jugador(accion, objetivo, hab_idx)
        self._historial_plano.append(resultado)
        self._log_accion(resultado)
        self._actualizar_barras()
        if self.combate.estado != EstadoCombate.EN_CURSO:
            self._fin_combate()
            return
        self._ejecutar_ias_y_actualizar()

    def _ejecutar_ias_y_actualizar(self):
        self._ia_pendiente = False
        if self.combate.estado != EstadoCombate.EN_CURSO:
            return

        resultados = self.combate.ejecutar_acciones_ia_hasta_jugador()
        for r in resultados:
            self._historial_plano.append(r)
            self._log_accion(r)

        ev = getattr(self.combate, "ultimo_evento", None)
        if ev:
            self._log_evento(ev)
            self.combate.ultimo_evento = None
            ra_ev = ResultadoAccion()
            ra_ev.actor_nombre = "⚡ EVENTO"
            ra_ev.descripcion  = ev.get('nombre', 'Evento aleatorio')
            msg_limpio = _re.sub(r'\x1b\[[0-9;]*m', '', ev.get('mensaje', ''))
            ra_ev.mensajes_extra = [l.strip() for l in msg_limpio.splitlines()
                                    if l.strip()][:6]
            self._historial_plano.append(ra_ev)

        # Detectar cambio de ronda
        ronda_actual = self.combate.round_actual
        if ronda_actual != self._round_prev:
            self._round_prev  = ronda_actual
            self._round_flash = 1.2

        self._actualizar_barras()

        # Comprobar fin de combate ANTES de decidir qué hacer
        if self.combate.estado != EstadoCombate.EN_CURSO:
            self._fin_combate()
            return

        siguiente = self.combate.personaje_turno_actual

        if siguiente is None:
            # Motor en transición (no debería pasar con el fix del motor)
            # No ponemos _ia_pendiente para no crear bucle infinito
            pass
        elif siguiente.es_ia:
            # Quedan IAs por actuar: reintentar en el siguiente frame
            self._ia_pendiente = True
        else:
            # Turno de jugador: flash de aviso y esperar input
            self._flash_timer      = 1.0
            self._flash_es_jugador = True

        self._actualizar_ui()

    def _fin_combate(self):
        self._combate_terminado = True
        resultado = self.combate.obtener_resultado_final()
        self._log_add(f"══ {resultado.mensaje_final} ══")
        self._actualizar_ui()
        for b in self._action_btns:
            b.visible = False
        for b in self.habilidad_btns:
            b.visible = False
        for b in self.post_btns:
            b.visible = True

    # ═══════════════════════════════════════════════════════════════════════
    # Log
    # ═══════════════════════════════════════════════════════════════════════

    def _log_add(self, msg: str):
        self._log.append(msg)
        if len(self._log) > MAX_LOG:
            self._log = self._log[-MAX_LOG:]
        self.lbl_log.text = "\n".join(self._log)

    def _log_accion(self, ra):
        self._log_add(ra.descripcion)
        if ra.daño:
            self._log_add(f"  ⚔ Daño: {ra.daño}")
        if ra.curacion:
            self._log_add(f"  💚 Curación: {ra.curacion}")
        for m in ra.mensajes_extra:
            self._log_add(f"  ⚠ {m}")

    def _log_evento(self, ev: dict):
        msg_limpio = _re.sub(r'\x1b\[[0-9;]*m', '', ev.get("mensaje", ""))
        lineas = [l for l in msg_limpio.splitlines() if l.strip()]
        self._log_add("━━ 🎲 EVENTO ALEATORIO ━━")
        for l in lineas[:4]:
            self._log_add(f"  {l}")

    # ═══════════════════════════════════════════════════════════════════════
    # Actualización de la UI
    # ═══════════════════════════════════════════════════════════════════════

    def _actualizar_barras(self):
        for p, (vbar, ebar) in self.health_bars.items():
            vbar.current_value = p.vida_actual
            ebar.current_value = p.energia_actual
        for p in self.equipo1 + self.equipo2:
            if hasattr(p, '_sprite') and p._sprite:
                p._sprite.alpha = 60 if not p.esta_vivo() else 255

    def _actualizar_ui(self):
        self._actualizar_barras()
        self.lbl_log.text = "\n".join(self._log[-MAX_LOG:])
        self._actualizar_visibilidad()

    def _actualizar_visibilidad(self):
        actor = self.combate.personaje_turno_actual
        es_jug = (actor is not None and not actor.es_ia
                  and not self._combate_terminado)
        mostrar = es_jug and not self.mostrando_habilidades and not self.esperando_objetivo
        for b in self._action_btns:
            b.visible = mostrar
        mostrar_habs = es_jug and self.mostrando_habilidades and not self.esperando_objetivo
        for b in self.habilidad_btns:
            b.visible = mostrar_habs

    # ═══════════════════════════════════════════════════════════════════════
    # Dibujo de indicadores de turno
    # ═══════════════════════════════════════════════════════════════════════

    def _draw_turn_queue(self):
        """
        Franja horizontal entre el log y el arena que muestra el orden
        de actuación del round actual.

        Leyenda visual:
          • Tarjeta con color de equipo    → pendiente de actuar
          • Tarjeta gris/tachada           → ya actuó este round
          • Tarjeta más grande + borde blanco → está actuando ahora
        """
        w         = self.app.width
        qy        = self._queue_y
        qh        = self._queue_h
        cola      = getattr(self.combate, '_cola_turno', [])
        actuados  = getattr(self.combate, '_ya_actuaron', set())
        activo    = self.combate.personaje_turno_actual

        if not cola:
            return

        # Fondo de la franja
        arcade.draw_rect_filled(
            arcade.LBWH(0, qy, w, qh),
            (12, 14, 24, 235)
        )
        arcade.draw_line(0, qy + qh - 1, w, qy + qh - 1, (60, 65, 100), 1)
        arcade.draw_line(0, qy, w, qy, (60, 65, 100), 1)

        # Etiqueta de ronda a la izquierda
        ronda = self.combate.round_actual
        arcade.draw_text(
            f"RONDA {ronda}",
            10, qy + qh // 2,
            (180, 185, 210), font_size=max(9, int(qh * 0.25)),
            anchor_x='left', anchor_y='center',
            bold=True
        )

        # Calcular tamaño y posición de las fichas
        n         = len(cola)
        ficha_h   = int(qh * 0.72)
        ficha_w   = max(60, min(110, (w - 120) // max(n, 1) - 6))
        gap       = max(4, (w - 120 - n * ficha_w) // max(n + 1, 1))
        start_x   = 100

        cy_ficha  = qy + qh // 2

        for i, p in enumerate(cola):
            fx  = start_x + i * (ficha_w + gap)
            fy  = cy_ficha - ficha_h // 2

            ya_actuo = id(p) in actuados
            es_actual = (p is activo and not ya_actuo)
            eq        = self.combate.equipo_de(p)
            col_eq    = COL_EQ1 if eq == 1 else COL_EQ2

            # ── Color de fondo de la ficha ──
            if not p.esta_vivo():
                fill = (30, 30, 35, 160)
                border = (60, 60, 65, 180)
            elif ya_actuo:
                fill = (35, 35, 45, 180)
                border = (70, 70, 85, 180)
            elif es_actual:
                # Pulso de brillo en el activo
                pulse = 0.5 + 0.5 * math.sin(self._anim_time * 4.0)
                r = int(col_eq[0] * 0.3 + pulse * col_eq[0] * 0.4)
                g = int(col_eq[1] * 0.3 + pulse * col_eq[1] * 0.4)
                b = int(col_eq[2] * 0.3 + pulse * col_eq[2] * 0.4)
                fill   = (r, g, b, 230)
                border = (255, 255, 255, 220)
            else:
                fill   = (int(col_eq[0] * 0.18), int(col_eq[1] * 0.18),
                          int(col_eq[2] * 0.18), 210)
                border = (int(col_eq[0] * 0.7), int(col_eq[1] * 0.7),
                          int(col_eq[2] * 0.7), 200)

            arcade.draw_rect_filled(arcade.LBWH(fx, fy, ficha_w, ficha_h), fill)
            arcade.draw_rect_outline(arcade.LBWH(fx, fy, ficha_w, ficha_h),
                                     border[:3], 2 if es_actual else 1)

            # Número de posición (pequeño, esquina superior izquierda)
            arcade.draw_text(
                str(i + 1),
                fx + 4, fy + ficha_h - 2,
                (150, 150, 170), font_size=max(7, int(ficha_h * 0.22)),
                anchor_x='left', anchor_y='top'
            )

            # Nombre del personaje
            nombre_corto = p.nombre[:8]
            col_nombre   = (80, 80, 90) if (ya_actuo or not p.esta_vivo()) else (230, 230, 240)
            if es_actual:
                col_nombre = (255, 255, 255)
            arcade.draw_text(
                nombre_corto,
                fx + ficha_w // 2, fy + ficha_h // 2 + 3,
                col_nombre,
                font_size=max(7, int(ficha_h * 0.26)),
                anchor_x='center', anchor_y='center',
                bold=es_actual
            )

            # Equipo (pequeño, abajo centrado)
            eq_label = "🎮" if not p.es_ia else "🤖"
            arcade.draw_text(
                eq_label,
                fx + ficha_w // 2, fy + 3,
                (180, 180, 200), font_size=max(7, int(ficha_h * 0.22)),
                anchor_x='center', anchor_y='bottom'
            )

            # Tachado sobre las fichas ya actuadas
            if ya_actuo and p.esta_vivo():
                mid_y = fy + ficha_h // 2
                arcade.draw_line(fx + 4, mid_y, fx + ficha_w - 4, mid_y,
                                 (120, 120, 135, 160), 2)

    def _draw_active_indicator(self):
        """
        Anillo pulsante + flecha ▼ sobre el sprite del personaje activo.
        """
        activo = self.combate.personaje_turno_actual
        if activo is None or not hasattr(activo, '_cx'):
            return
        if self._combate_terminado:
            return

        cx = activo._cx
        cy = activo._cy
        sz = getattr(activo, '_sp_size', 80)
        eq = self.combate.equipo_de(activo)
        col = COL_EQ1 if eq == 1 else COL_EQ2

        # ── Anillo exterior pulsante ──────────────────────────────────────
        pulse  = 0.5 + 0.5 * math.sin(self._anim_time * 3.5)
        radius = sz // 2 + 6 + int(pulse * 5)
        alpha  = int(120 + pulse * 120)

        # Varios anillos concéntricos para efecto glow
        for offset, a_mult in [(0, 1.0), (4, 0.5), (8, 0.25)]:
            r_off = radius + offset
            arcade.draw_circle_outline(
                cx, cy, r_off,
                (*col, int(alpha * a_mult)),
                border_width=2
            )

        # ── Flecha ▼ sobre el sprite ──────────────────────────────────────
        arrow_y    = cy + sz // 2 + 28 + int(pulse * 4)
        arrow_size = max(10, sz // 5)
        es_jug     = not activo.es_ia

        # Color de la flecha: verde si jugador, morado si IA
        arrow_col = (100, 230, 100, 230) if es_jug else (200, 130, 230, 230)

        # Triángulo apuntando hacia abajo
        arcade.draw_triangle_filled(
            cx - arrow_size, arrow_y + arrow_size,
            cx + arrow_size, arrow_y + arrow_size,
            cx,              arrow_y,
            arrow_col
        )

        # Texto bajo la flecha
        label = "🎮 TU TURNO" if es_jug else f"🤖 {activo.nombre[:8]}"
        label_col = (130, 255, 130) if es_jug else (210, 160, 255)
        arcade.draw_text(
            label,
            cx, arrow_y + arrow_size + 14,
            label_col,
            font_size=max(9, int(sz * 0.14)),
            anchor_x='center', anchor_y='center',
            bold=True
        )

    def _draw_state_badges(self):
        """
        Pequeñas píldoras de color bajo las barras de vida de cada personaje,
        mostrando los estados activos con emoji + duración restante.
        """
        todos = self.equipo1 + self.equipo2
        for p in todos:
            if not hasattr(p, '_cx') or not p.esta_vivo():
                continue
            estados = getattr(p, 'estados', [])
            if not estados:
                continue

            duraciones = getattr(p, 'estados_duracion', {})
            badge_w = 28
            badge_h = 14
            gap     = 3
            total   = len(estados) * (badge_w + gap) - gap
            bx      = p._cx - total // 2
            by      = getattr(p, '_bar_y_bottom', p._cy - p._sp_size // 2 - 40) - badge_h - 2

            for estado in estados:
                emoji, col = ESTADO_BADGE.get(estado, ("?", (150, 150, 150)))
                dur = duraciones.get(estado, 0)

                # Fondo de la píldora
                arcade.draw_rect_filled(
                    arcade.LBWH(bx, by, badge_w, badge_h),
                    (*col, 200)
                )
                arcade.draw_rect_outline(
                    arcade.LBWH(bx, by, badge_w, badge_h),
                    (200, 200, 220, 180), 1
                )
                # Emoji
                arcade.draw_text(
                    emoji,
                    bx + badge_w // 2, by + badge_h // 2 + 1,
                    (255, 255, 255), font_size=8,
                    anchor_x='center', anchor_y='center'
                )
                # Duración (esquina inferior derecha)
                if dur > 0:
                    arcade.draw_text(
                        str(dur),
                        bx + badge_w - 2, by + 1,
                        (240, 240, 240), font_size=6,
                        anchor_x='right', anchor_y='bottom'
                    )
                bx += badge_w + gap

    def _draw_flash_banner(self):
        """
        Banner semitransparente "¡TU TURNO!" / "TURNO DE IA" al empezar cada turno.
        Se desvanece en ~1 segundo.
        """
        if self._flash_timer <= 0:
            return
        w, h  = self.app.width, self.app.height
        alpha = int(min(200, self._flash_timer * 280))

        bh = max(44, int(h * 0.08))
        by = self._queue_y + self._queue_h + int(
            (self._arena_top - self._queue_y - self._queue_h) * 0.5
        ) - bh // 2

        col_bg  = (20, 80, 20, alpha) if self._flash_es_jugador else (60, 20, 80, alpha)
        col_brd = (80, 220, 80, alpha) if self._flash_es_jugador else (180, 80, 230, alpha)
        col_txt = (130, 255, 130) if self._flash_es_jugador else (210, 150, 255)
        texto   = "¡TU TURNO!" if self._flash_es_jugador else "TURNO DE IA"

        arcade.draw_rect_filled(arcade.LBWH(0, by, w, bh), col_bg)
        arcade.draw_rect_outline(arcade.LBWH(0, by, w, bh), col_brd[:3], 2)
        arcade.draw_text(
            texto,
            w // 2, by + bh // 2,
            col_txt, font_size=max(16, int(bh * 0.45)),
            anchor_x='center', anchor_y='center', bold=True
        )

    def _draw_round_flash(self):
        """Flash de nueva ronda en la esquina superior derecha del arena."""
        if self._round_flash <= 0:
            return
        w    = self.app.width
        alpha = int(min(220, self._round_flash * 300))
        pulse = 0.5 + 0.5 * math.sin(self._anim_time * 6)
        col  = (int(60 + pulse * 80), int(90 + pulse * 90), int(160 + pulse * 60), alpha)

        bw, bh = 130, 32
        bx = w - bw - 10
        by = self._arena_top - bh - 6

        arcade.draw_rect_filled(arcade.LBWH(bx, by, bw, bh), col)
        arcade.draw_rect_outline(arcade.LBWH(bx, by, bw, bh),
                                 (160, 200, 255), 2)
        arcade.draw_text(
            f"✦ RONDA {self.combate.round_actual} ✦",
            bx + bw // 2, by + bh // 2,
            (220, 235, 255), font_size=11,
            anchor_x='center', anchor_y='center', bold=True
        )

    # ═══════════════════════════════════════════════════════════════════════
    # Update & Draw
    # ═══════════════════════════════════════════════════════════════════════

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        self._anim_time   += delta_time
        self._flash_timer  = max(0.0, self._flash_timer  - delta_time)
        self._round_flash  = max(0.0, self._round_flash  - delta_time)
        if self._ia_pendiente and not self._combate_terminado:
            # Guardia: si el turno actual ya es del jugador, ceder control sin ejecutar IAs
            siguiente = self.combate.personaje_turno_actual
            if siguiente is not None and not siguiente.es_ia:
                self._ia_pendiente = False
                self._flash_timer      = 1.0
                self._flash_es_jugador = True
                self._actualizar_ui()
            else:
                self._ejecutar_ias_y_actualizar()

    def on_draw(self):
        self.clear()
        w, h = self.app.width, self.app.height

        # Fondo base
        arcade.draw_rect_filled(arcade.XYWH(w // 2, h // 2, w, h),
                                self.background_color)

        # Separador VS central (arena)
        lx, ly, lw, lh = self._log_rect
        arcade.draw_line(w // 2, ly + lh + self._queue_h + 10,
                         w // 2, h - 10, (80, 80, 100), 2)

        # 1. Cola de turnos (franja intermedia)
        self._draw_turn_queue()

        # 2. Anillo pulsante del activo (BAJO los sprites)
        self._draw_active_indicator()

        # 3. Sprites
        self.sprite_list.draw()

        # 4. Barras de vida/energía (static_elements)
        for elem in self.static_elements:
            elem.draw()

        # 5. Badges de estados (sobre barras, bajo sprites)
        self._draw_state_badges()

        # 6. Fondo del log
        arcade.draw_rect_filled(arcade.LBWH(lx, ly, lw, lh), (15, 15, 25, 220))
        arcade.draw_rect_outline(arcade.LBWH(lx, ly, lw, lh), (80, 80, 120), 1)

        # 7. Flash de nueva ronda
        self._draw_round_flash()

        # 8. Banner de turno (se desvanece)
        self._draw_flash_banner()

        # 9. Etiquetas y botones
        for elem in self.ui_elements:
            if hasattr(elem, 'draw'):
                elem.draw()
        for b in self.habilidad_btns:
            b.draw()
        for b in self.objetivo_btns:
            b.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)
        for elem in self.ui_elements + self.habilidad_btns + self.objetivo_btns:
            if hasattr(elem, 'on_mouse_motion'):
                elem.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        if super().on_mouse_press(x, y, button, modifiers):
            return
        for b in self.objetivo_btns:
            if b.on_mouse_press(x, y, button, modifiers):
                return
        for b in self.habilidad_btns:
            if b.on_mouse_press(x, y, button, modifiers):
                return

    # ═══════════════════════════════════════════════════════════════════════
    # Postcombate
    # ═══════════════════════════════════════════════════════════════════════

    def _revancha(self):
        eq1 = [(type(p), p.es_ia) for p in self.equipo1]
        eq2 = [(type(p), p.es_ia) for p in self.equipo2]
        new_eq1 = [cls() for cls, _ in eq1]
        new_eq2 = [cls() for cls, _ in eq2]
        for p, (_, ei) in zip(new_eq1, eq1):
            p.es_ia = ei
        for p, (_, ei) in zip(new_eq2, eq2):
            p.es_ia = ei
        self.app.goto_view(CombatTeamView(self.app, new_eq1, new_eq2))

    def _ver_historial(self):
        def _volver():
            from scenes.menu_scene import MenuView
            self.app.goto_view(MenuView(self.app))
        self.app.push_view(HistorialView(self.app, self._historial_plano,
                                         on_back=_volver))

    def _volver_menu(self):
        from scenes.menu_scene import MenuView
        self.app.goto_view(MenuView(self.app))

    def on_resize(self, width, height):
        self._setup_ui()
        self._ejecutar_ias_y_actualizar()