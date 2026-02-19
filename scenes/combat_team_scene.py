# scenes/combat_team_scene.py
"""
Vista de combate por equipos (1v1 hasta 4v4).

Layout:
  ┌──────────────────────────────────────────────────────────┐
  │  EQUIPO 1 (izquierda)         EQUIPO 2 (derecha)         │
  │  [sprite] vida/energía        [sprite] vida/energía       │
  │            ...                         ...               │
  │                                                          │
  │  ┌────────────────────────────────────────────────────┐  │
  │  │  LOG DE COMBATE                                    │  │
  │  └────────────────────────────────────────────────────┘  │
  │  [ATAQUE] [DEFENDER] [CONCENTRAR] [HABILIDAD]            │
  │  (o selector de objetivo si es necesario)                │
  └──────────────────────────────────────────────────────────┘
"""

import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel, HealthBar
from combate.sistema_combate_equipo import (
    CombateEquipo, Accion, EstadoCombate, ResultadoAccion
)
from scenes.historial_scene import HistorialView


# Colores de equipos
COL_EQ1 = (80, 160, 255)
COL_EQ2 = (255, 80, 80)
COL_IA  = (200, 130, 220)
COL_JUG = (130, 220, 130)

MAX_LOG = 8   # Líneas visibles en el log


class CombatTeamView(BaseView):
    def __init__(self, app, equipo1: list, equipo2: list):
        super().__init__(app)
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.combate = CombateEquipo(equipo1, equipo2)

        self.ui_elements   = []
        self.habilidad_btns = []
        self.objetivo_btns  = []
        self.post_btns      = []
        self.health_bars    = {}   # personaje -> (vida_bar, energia_bar)
        self.sprite_list    = arcade.SpriteList()   # <-- AÑADIDO

        self.mostrando_habilidades  = False
        self.esperando_objetivo     = False
        self.accion_pendiente: Accion = None
        self.habilidad_idx_pendiente: int = None
        self._log: list = ["¡Comienza la batalla!"]
        self._combate_terminado = False

        self._setup_ui()
        # Ejecutar IAs iniciales si el primer turno es de IA
        self._ejecutar_ias_y_actualizar()

    # ──────────────────────────────────────────────
    # Construcción de la UI
    # ──────────────────────────────────────────────

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

        # Zona de combate: parte superior (60% de altura)
        combat_h = int(h * 0.58)
        # Zona de log: franja media
        log_y   = int(h * 0.32)
        log_h   = int(h * 0.18)
        # Zona de botones: parte inferior
        btn_y   = 15

        self._combat_zone = (0, log_y + log_h, w, combat_h)
        self._log_rect    = (10, log_y, w - 20, log_h)

        # ── Sprites y barras de vida ──
        n1 = len(self.equipo1)
        n2 = len(self.equipo2)

        def _place_team(team, x_start, x_end, flip=False):
            n = len(team)
            slot_w = (x_end - x_start) // max(n, 1)
            sp_size = min(100, slot_w - 20)
            y_sprite = log_y + log_h + combat_h // 2 - 10

            for i, p in enumerate(team):
                cx = x_start + i * slot_w + slot_w // 2
                # Sprite
                try:
                    tex = arcade.load_texture(
                        f'img/personajes/{type(p).__name__.lower()}.png'
                    )
                    sp = arcade.Sprite(tex)
                    sp.center_x = cx
                    sp.center_y = y_sprite
                    sp.width = sp_size
                    sp.height = sp_size
                    if flip:
                        sp.scale_xy = (-abs(sp.scale_xy[0]), sp.scale_xy[1])
                    self.sprite_list.append(sp)
                    p._sprite = sp
                except Exception:
                    p._sprite = None

                # Nombre + etiqueta IA/JUG
                ctrl = "🤖" if p.es_ia else "🎮"
                lbl_col = COL_IA if p.es_ia else COL_JUG
                self.ui_elements.append(RetroLabel(
                    f"{ctrl} {p.nombre[:10]}",
                    cx, y_sprite + sp_size // 2 + 18,
                    font_size=11, color=lbl_col,
                    anchor_x='center', anchor_y='center'
                ))

                # Barras
                bar_w = min(120, slot_w - 10)
                bar_x = cx - bar_w // 2
                bar_y_v = y_sprite - sp_size // 2 - 18
                bar_y_e = bar_y_v - 16

                vbar = HealthBar(
                    x=bar_x, y=bar_y_v, width=bar_w, height=14,
                    max_value=p.vida_maxima, current_value=p.vida_actual,
                    color_lleno=COL_EQ1 if not flip else COL_EQ2
                )
                ebar = HealthBar(
                    x=bar_x, y=bar_y_e, width=bar_w, height=8,
                    max_value=p.energia_maxima, current_value=p.energia_actual,
                    color_lleno=(100, 180, 220)
                )
                self.static_elements.extend([vbar, ebar])
                self.health_bars[p] = (vbar, ebar)

        _place_team(self.equipo1, 10, w // 2 - 10)
        _place_team(self.equipo2, w // 2 + 10, w - 10, flip=True)

        # ── Indicador de turno ──
        self.lbl_turno = RetroLabel(
            "", w // 2, log_y + log_h + combat_h - 30,
            font_size=20, color=(255, 255, 100),
            anchor_x='center', anchor_y='center'
        )
        self.ui_elements.append(self.lbl_turno)

        # ── Log ──
        self.lbl_log = RetroLabel(
            "",
            20, log_y + log_h - 10,
            font_size=12, color=(220, 220, 220),
            anchor_x='left', anchor_y='top',
            multiline=True, width=w - 40
        )
        self.ui_elements.append(self.lbl_log)

        # ── Botones de acción ──
        btn_h_sz = 55
        btn_w_sz = 170
        spacing  = 185
        total_w  = 4 * spacing - (spacing - btn_w_sz)
        bx_start = w // 2 - total_w // 2

        self.btn_ataque = ImageButton(
            x=bx_start, y=btn_y,
            width=btn_w_sz, height=btn_h_sz,
            text="ATAQUE",
            normal_color=(140, 80, 80), hover_color=(180, 110, 110),
            callback=self._cmd_ataque
        )
        self.btn_defender = ImageButton(
            x=bx_start + spacing, y=btn_y,
            width=btn_w_sz, height=btn_h_sz,
            text="DEFENDER",
            normal_color=(80, 80, 140), hover_color=(110, 110, 180),
            callback=self._cmd_defender
        )
        self.btn_concentrar = ImageButton(
            x=bx_start + 2 * spacing, y=btn_y,
            width=btn_w_sz, height=btn_h_sz,
            text="CONCENTRAR",
            normal_color=(80, 130, 80), hover_color=(110, 170, 110),
            callback=self._cmd_concentrar
        )
        self.btn_habilidad = ImageButton(
            x=bx_start + 3 * spacing, y=btn_y,
            width=btn_w_sz, height=btn_h_sz,
            text="HABILIDAD",
            normal_color=(130, 130, 80), hover_color=(170, 170, 110),
            callback=self._cmd_mostrar_habilidades
        )
        self._action_btns = [self.btn_ataque, self.btn_defender,
                             self.btn_concentrar, self.btn_habilidad]
        self.ui_elements.extend(self._action_btns)

        # ── Botones de habilidad (ocultos por defecto) ──
        self._crear_habilidad_btns(btn_y + btn_h_sz + 8)

        # ── Botones postcombate ──
        self.btn_revancha = ImageButton(
            x=w // 2 - 310, y=btn_y,
            width=190, height=50,
            text="REVANCHA",
            normal_color=(0, 130, 0), hover_color=(0, 180, 0),
            callback=self._revancha
        )
        self.btn_menu = ImageButton(
            x=w // 2 + 120, y=btn_y,
            width=190, height=50,
            text="MENÚ",
            normal_color=(130, 0, 0), hover_color=(180, 0, 0),
            callback=self._volver_menu
        )
        self.post_btns = [self.btn_revancha, self.btn_menu]
        for b in self.post_btns:
            b.visible = False
            self.ui_elements.append(b)

        self._actualizar_ui()

    def _crear_habilidad_btns(self, y_hab):
        self.habilidad_btns.clear()
        actor = self.combate.personaje_turno_actual
        if actor is None or actor.es_ia:
            return

        w = self.app.width
        habs = actor.habilidades
        if not habs:
            return

        bw = 140
        total = len(habs) * (bw + 8) - 8
        sx = w // 2 - total // 2

        for i, hab in enumerate(habs):
            tiene_energia = actor.energia_actual >= hab.costo_energia
            nc = (80, 80, 140) if tiene_energia else (60, 60, 80)
            hc = (110, 110, 180) if tiene_energia else (70, 70, 90)
            btn = ImageButton(
                x=sx + i * (bw + 8), y=y_hab,
                width=bw, height=48,
                text=f"{hab.nombre[:14]}\n({hab.costo_energia}E)",
                normal_color=nc, hover_color=hc,
                callback=lambda idx=i: self._cmd_usar_habilidad(idx)
            )
            btn.visible = False
            self.habilidad_btns.append(btn)

        btn_cancel = ImageButton(
            x=w // 2 - 70, y=y_hab - 56,
            width=140, height=40,
            text="CANCELAR",
            normal_color=(140, 70, 70), hover_color=(180, 90, 90),
            callback=self._cmd_ocultar_habilidades
        )
        btn_cancel.visible = False
        self.habilidad_btns.append(btn_cancel)

    def _crear_objetivo_btns(self, accion: Accion, hab_idx: int = None):
        """Crea botones para seleccionar objetivo (rival o aliado)."""
        self.objetivo_btns.clear()
        w, h = self.app.width, self.app.height
        actor = self.combate.personaje_turno_actual
        if actor is None:
            return

        # Determinar candidatos: para curaciones solo aliados; demás solo rivales
        if accion == Accion.HABILIDAD_ESPECIAL and hab_idx is not None:
            hab = actor.habilidades[hab_idx]
            es_cur = getattr(hab, 'es_curacion', False)
        else:
            es_cur = False

        if es_cur:
            candidatos = [p for p in self.combate.equipo_propio_de(actor) if p.esta_vivo()]
            titulo = "Elige aliado a curar:"
        else:
            candidatos = [p for p in self.combate.equipo_rival_de(actor) if p.esta_vivo()]
            titulo = "Elige objetivo:"

        self.lbl_turno.text = titulo
        self.lbl_turno.color = (255, 200, 100)

        bw = 160
        total = len(candidatos) * (bw + 10) - 10
        sx = w // 2 - total // 2
        by = h // 2 - 30

        for i, p in enumerate(candidatos):
            col = COL_EQ1 if p in self.combate.equipo1 else COL_EQ2
            btn = ImageButton(
                x=sx + i * (bw + 10), y=by,
                width=bw, height=55,
                text=p.nombre[:14],
                normal_color=col, hover_color=(min(col[0]+40,255), min(col[1]+40,255), min(col[2]+40,255)),
                callback=lambda tgt=p: self._cmd_confirmar_objetivo(tgt)
            )
            self.objetivo_btns.append(btn)

        btn_cancel = ImageButton(
            x=w // 2 - 80, y=by - 65,
            width=160, height=40,
            text="CANCELAR",
            normal_color=(140, 70, 70), hover_color=(180, 90, 90),
            callback=self._cmd_cancelar_objetivo
        )
        self.objetivo_btns.append(btn_cancel)

    # ──────────────────────────────────────────────
    # Comandos del jugador
    # ──────────────────────────────────────────────

    def _cmd_ataque(self):
        if self._combate_terminado:
            return
        actor = self.combate.personaje_turno_actual
        if actor is None or actor.es_ia:
            return
        rivales = [p for p in self.combate.equipo_rival_de(actor) if p.esta_vivo()]
        if not rivales:
            return
        if len(rivales) == 1:
            self._ejecutar_jugador(Accion.ATAQUE_BASICO, rivales[0])
        else:
            self.accion_pendiente = Accion.ATAQUE_BASICO
            self.habilidad_idx_pendiente = None
            self.esperando_objetivo = True
            self.mostrando_habilidades = False
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
        self.esperando_objetivo = False
        # Rebuild habilidad buttons for current actor
        btn_h_sz = 55
        self._crear_habilidad_btns(15 + btn_h_sz + 8)
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

        es_cur = getattr(hab, 'es_curacion', False)
        # Para curaciones, si hay un solo aliado vivo: automático
        # Para ofensivas, si hay un solo rival: automático
        if es_cur:
            candidatos = [p for p in self.combate.equipo_propio_de(actor) if p.esta_vivo()]
        else:
            candidatos = [p for p in self.combate.equipo_rival_de(actor) if p.esta_vivo()]

        if len(candidatos) == 1:
            self.mostrando_habilidades = False
            self._ejecutar_jugador(Accion.HABILIDAD_ESPECIAL, candidatos[0], idx)
        else:
            self.accion_pendiente = Accion.HABILIDAD_ESPECIAL
            self.habilidad_idx_pendiente = idx
            self.esperando_objetivo = True
            self.mostrando_habilidades = False
            self._crear_objetivo_btns(Accion.HABILIDAD_ESPECIAL, idx)
            self._actualizar_visibilidad()

    def _cmd_confirmar_objetivo(self, objetivo):
        self.esperando_objetivo = False
        self._ejecutar_jugador(
            self.accion_pendiente, objetivo,
            self.habilidad_idx_pendiente
        )
        self.accion_pendiente = None
        self.habilidad_idx_pendiente = None
        self.objetivo_btns.clear()

    def _cmd_cancelar_objetivo(self):
        self.esperando_objetivo = False
        self.accion_pendiente = None
        self.habilidad_idx_pendiente = None
        self.objetivo_btns.clear()
        self._actualizar_visibilidad()

    # ──────────────────────────────────────────────
    # Ejecución y flujo de combate
    # ──────────────────────────────────────────────

    def _ejecutar_jugador(self, accion: Accion, objetivo, hab_idx: int = None):
        """Ejecuta la acción del jugador y luego procesa IAs."""
        if self.combate.estado != EstadoCombate.EN_CURSO:
            return
        resultado = self.combate.ejecutar_accion_jugador(accion, objetivo, hab_idx)
        self._log_accion(resultado)
        self._actualizar_barras()

        if self.combate.estado != EstadoCombate.EN_CURSO:
            self._fin_combate()
            return

        self._ejecutar_ias_y_actualizar()

    def _ejecutar_ias_y_actualizar(self):
        """Ejecuta IAs del round actual, muestra evento si ocurrió y actualiza UI."""
        self._ia_pendiente = False

        if self.combate.estado != EstadoCombate.EN_CURSO:
            return

        resultados = self.combate.ejecutar_acciones_ia_hasta_jugador()
        for r in resultados:
            self._historial.append(r) if hasattr(self, "_historial") else None
            self._log_accion(r)

        # Mostrar evento aleatorio si ocurrió en este round
        ev = getattr(self.combate, "ultimo_evento", None)
        if ev:
            self._log_evento(ev)
            self.combate.ultimo_evento = None

        self._actualizar_barras()

        if self.combate.estado != EstadoCombate.EN_CURSO:
            self._fin_combate()
            return

        # Si el siguiente en actuar es IA, diferir al siguiente frame
        siguiente = self.combate.personaje_turno_actual
        if siguiente is None or getattr(siguiente, "es_ia", True):
            self._ia_pendiente = True

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
        self.lbl_turno.text = resultado.mensaje_final
        self.lbl_turno.color = (255, 220, 100)

    # ──────────────────────────────────────────────
    # Log
    # ──────────────────────────────────────────────

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

    # ──────────────────────────────────────────────
    # Actualización de la UI
    # ──────────────────────────────────────────────

    def _actualizar_barras(self):
        for p, (vbar, ebar) in self.health_bars.items():
            vbar.current_value = p.vida_actual
            ebar.current_value = p.energia_actual

        # Atenuar sprites de muertos
        for p in self.equipo1 + self.equipo2:
            if hasattr(p, '_sprite') and p._sprite:
                if not p.esta_vivo():
                    p._sprite.alpha = 60
                else:
                    p._sprite.alpha = 255

    def _actualizar_ui(self):
        self._actualizar_barras()
        actor = self.combate.personaje_turno_actual
        if actor and not self._combate_terminado:
            eq = self.combate.equipo_de(actor)
            col = COL_EQ1 if eq == 1 else COL_EQ2
            ctrl = "🤖 IA" if actor.es_ia else "🎮 JUGADOR"
            self.lbl_turno.text = f"Turno: {actor.nombre} ({ctrl}) — Eq.{eq}"
            self.lbl_turno.color = col
        self.lbl_log.text = "\n".join(self._log[-MAX_LOG:])
        self._actualizar_visibilidad()

    def _actualizar_visibilidad(self):
        actor = self.combate.personaje_turno_actual
        es_turno_jugador = (actor is not None and not actor.es_ia
                            and not self._combate_terminado)

        mostrar_principales = es_turno_jugador and not self.mostrando_habilidades and not self.esperando_objetivo
        for b in self._action_btns:
            b.visible = mostrar_principales

        mostrar_habs = es_turno_jugador and self.mostrando_habilidades and not self.esperando_objetivo
        for b in self.habilidad_btns:
            b.visible = mostrar_habs

    # ──────────────────────────────────────────────
    # Render
    # ──────────────────────────────────────────────

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        if self._ia_pendiente and not self._combate_terminado:
            self._ejecutar_ias_y_actualizar()

    def _log_evento(self, ev: dict):
        """Muestra un evento aleatorio en el log, limpiando códigos ANSI."""
        import re as _re
        msg = ev.get("mensaje", "")
        msg_limpio = _re.sub(r'\x1b\[[0-9;]*m', '', msg)
        lineas = [l for l in msg_limpio.splitlines() if l.strip()]
        self._log_add("━━ 🎲 EVENTO ALEATORIO ━━")
        for l in lineas[:4]:
            self._log_add(f"  {l}")

    def on_draw(self):
        self.clear()
        arcade.set_background_color(self.background_color)

        # Zona de combate (fondo)
        lx, ly, lw, lh = self._log_rect
        arcade.draw_rect_filled(
            arcade.LBWH(lx, ly, lw, lh), (15, 15, 25, 220)
        )
        arcade.draw_rect_outline(
            arcade.LBWH(lx, ly, lw, lh), (80, 80, 120), 1
        )

        # Separador VS central
        w, h = self.app.width, self.app.height
        arcade.draw_line(w // 2, ly + lh + 10, w // 2, h - 20,
                         (80, 80, 100), 2)

        self.sprite_list.draw()

        for elem in self.static_elements:
            elem.draw()
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
        # Primero dejar que la clase base maneje los ui_elements
        if super().on_mouse_press(x, y, button, modifiers):
            return

        # Si no, procesar listas especiales
        for b in self.objetivo_btns:
            if b.on_mouse_press(x, y, button, modifiers):
                return
        for b in self.habilidad_btns:
            if b.on_mouse_press(x, y, button, modifiers):
                return

    # ──────────────────────────────────────────────
    # Postcombate
    # ──────────────────────────────────────────────

    def _revancha(self):
        # Reinstanciar los mismos tipos de personajes con los mismos flags
        eq1 = [(type(p), p.es_ia) for p in self.equipo1]
        eq2 = [(type(p), p.es_ia) for p in self.equipo2]
        new_eq1 = [cls() for cls, _ in eq1]
        new_eq2 = [cls() for cls, _ in eq2]
        for p, (_, ei) in zip(new_eq1, eq1):
            p.es_ia = ei
        for p, (_, ei) in zip(new_eq2, eq2):
            p.es_ia = ei
        self.app.goto_view(CombatTeamView(self.app, new_eq1, new_eq2))

    def _volver_menu(self):
        from scenes.menu_scene import MenuView
        self.app.goto_view(MenuView(self.app))

    def on_resize(self, width, height):
        self._setup_ui()
        self._ejecutar_ias_y_actualizar()