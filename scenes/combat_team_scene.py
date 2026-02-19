# scenes/combat_team_scene.py
"""
Vista de combate por equipos (1v1 hasta 4v4).
"""

import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel, HealthBar, EstadoTag
from combate.sistema_combate_equipo import (
    CombateEquipo, Accion, EstadoCombate, ResultadoAccion
)
from scenes.historial_scene import HistorialView
from debug_logger import DBG


COL_EQ1 = (80, 160, 255)
COL_EQ2 = (255, 80, 80)
COL_IA  = (200, 130, 220)
COL_JUG = (130, 220, 130)

MAX_LOG = 8


class CombatTeamView(BaseView):
    def __init__(self, app, equipo1: list, equipo2: list):
        super().__init__(app)
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.combate = CombateEquipo(equipo1, equipo2)

        self.ui_elements    = []
        self.habilidad_btns = []
        self.objetivo_btns  = []
        self.post_btns      = []
        self.health_bars    = {}
        self.sprite_list    = arcade.SpriteList()

        self.mostrando_habilidades   = False
        self.esperando_objetivo      = False
        self.accion_pendiente: Accion     = None
        self.habilidad_idx_pendiente: int = None
        self._log: list = ["¡Comienza la batalla!"]
        self._combate_terminado = False
        self._historial: list = []          # acumula todos los ResultadoAccion
        self._ia_pendiente: bool = False    # hay IAs pendientes de actuar este round

        DBG.info("CombatTeamView iniciado",
                 eq1=len(equipo1), eq2=len(equipo2))
        self._setup_ui()
        self._ejecutar_ias_y_actualizar()

    # ── Construcción de la UI ────────────────────────────────────────────────

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

        combat_h = int(h * 0.58)
        log_y    = int(h * 0.32)
        log_h    = int(h * 0.18)
        btn_y    = 15

        self._combat_zone = (0, log_y + log_h, w, combat_h)
        self._log_rect    = (10, log_y, w - 20, log_h)
        self._btn_y       = btn_y    # guardado para _crear_habilidad_btns

        # ── Sprites y barras de vida ─────────────────────────────────────────
        def _place_team(team, x_start, x_end, flip=False):
            n      = len(team)
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
                    sp.width    = sp_size
                    sp.height   = sp_size
                    if flip:
                        sp.scale_xy = (-abs(sp.scale_xy[0]), sp.scale_xy[1])
                    self.sprite_list.append(sp)
                    p._sprite = sp
                except Exception:
                    p._sprite = None

                # Etiqueta nombre
                ctrl    = "🤖" if p.es_ia else "🎮"
                lbl_col = COL_IA if p.es_ia else COL_JUG
                self.ui_elements.append(RetroLabel(
                    f"{ctrl} {p.nombre[:10]}",
                    cx, y_sprite + sp_size // 2 + 18,
                    font_size=11, color=lbl_col,
                    anchor_x='center', anchor_y='center'
                ))

                # Barras de vida y energía con texto numérico
                bar_w   = min(120, slot_w - 10)
                bar_x   = cx - bar_w // 2
                bar_y_v = y_sprite - sp_size // 2 - 18
                bar_y_e = bar_y_v - 16

                vbar = HealthBar(
                    x=bar_x, y=bar_y_v, width=bar_w, height=14,
                    max_value=p.vida_maxima, current_value=p.vida_actual,
                    color_lleno=COL_EQ1 if not flip else COL_EQ2,
                    mostrar_texto=True
                )
                ebar = HealthBar(
                    x=bar_x, y=bar_y_e, width=bar_w, height=8,
                    max_value=p.energia_maxima, current_value=p.energia_actual,
                    color_lleno=(100, 180, 220),
                    mostrar_texto=False      # barra de energía demasiado pequeña
                )
                self.static_elements.extend([vbar, ebar])
                self.health_bars[p] = (vbar, ebar)

                # Guardar posición para tags de estado
                p._tag_cx = cx
                p._tag_cy = y_sprite + sp_size // 2 + 35

        _place_team(self.equipo1, 10, w // 2 - 10)
        _place_team(self.equipo2, w // 2 + 10, w - 10, flip=True)

        # ── Indicador de turno ───────────────────────────────────────────────
        self.lbl_turno = RetroLabel(
            "", w // 2, log_y + log_h + combat_h - 30,
            font_size=20, color=(255, 255, 100),
            anchor_x='center', anchor_y='center'
        )
        self.ui_elements.append(self.lbl_turno)

        # ── Log ──────────────────────────────────────────────────────────────
        self.lbl_log = RetroLabel(
            "",
            20, log_y + log_h - 10,
            font_size=12, color=(220, 220, 220),
            anchor_x='left', anchor_y='top',
            multiline=True, width=w - 40
        )
        self.ui_elements.append(self.lbl_log)

        # ── Botones de acción ────────────────────────────────────────────────
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

        # ── Botones de habilidad (ocultos) ───────────────────────────────────
        self._btn_h_sz = btn_h_sz
        self._crear_habilidad_btns(btn_y + btn_h_sz + 8)

        # ── Botones postcombate ──────────────────────────────────────────────
        pc_w   = 175
        pc_gap = int(w * 0.02)
        total3 = 3 * pc_w + 2 * pc_gap
        pc_sx  = w // 2 - total3 // 2

        self.btn_revancha = ImageButton(
            x=pc_sx, y=btn_y,
            width=pc_w, height=50,
            text="REVANCHA",
            normal_color=(0, 130, 0), hover_color=(0, 180, 0),
            callback=self._revancha
        )
        self.btn_historial = ImageButton(
            x=pc_sx + pc_w + pc_gap, y=btn_y,
            width=pc_w, height=50,
            text="HISTORIAL",
            normal_color=(130, 130, 0), hover_color=(180, 180, 0),
            callback=self._ver_historial
        )
        self.btn_menu = ImageButton(
            x=pc_sx + 2 * (pc_w + pc_gap), y=btn_y,
            width=pc_w, height=50,
            text="MENÚ",
            normal_color=(130, 0, 0), hover_color=(180, 0, 0),
            callback=self._volver_menu
        )
        self.post_btns = [self.btn_revancha, self.btn_historial, self.btn_menu]
        for b in self.post_btns:
            b.visible = False
            self.ui_elements.append(b)

        self._actualizar_ui()

    # ── Botones de habilidad y objetivo ─────────────────────────────────────

    def _crear_habilidad_btns(self, y_hab):
        self.habilidad_btns.clear()
        actor = self.combate.personaje_turno_actual
        if actor is None or actor.es_ia:
            return

        w    = self.app.width
        habs = actor.habilidades
        if not habs:
            return

        bw    = 140
        total = len(habs) * (bw + 8) - 8
        sx    = w // 2 - total // 2

        for i, hab in enumerate(habs):
            tiene_e = actor.energia_actual >= hab.costo_energia
            nc = (80, 80, 140) if tiene_e else (60, 60, 80)
            hc = (110, 110, 180) if tiene_e else (70, 70, 90)
            # Texto con costo de energía
            texto = f"{hab.nombre[:14]}\n({hab.costo_energia}E)"
            btn = ImageButton(
                x=sx + i * (bw + 8), y=y_hab,
                width=bw, height=48,
                text=texto,
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
        self.objetivo_btns.clear()
        w, h = self.app.width, self.app.height
        actor = self.combate.personaje_turno_actual
        if actor is None:
            DBG.warn("_crear_objetivo_btns: actor es None")
            return

        if accion == Accion.HABILIDAD_ESPECIAL and hab_idx is not None:
            hab    = actor.habilidades[hab_idx]
            es_cur = getattr(hab, 'es_curacion', False)
        else:
            es_cur = False

        if es_cur:
            candidatos = [p for p in self.combate.equipo_propio_de(actor) if p.esta_vivo()]
            titulo     = "Elige aliado a curar:"
        else:
            candidatos = [p for p in self.combate.equipo_rival_de(actor) if p.esta_vivo()]
            titulo     = "Elige objetivo:"

        if not candidatos:
            DBG.warn("_crear_objetivo_btns: sin candidatos válidos",
                     accion=str(accion), es_cur=es_cur)
            return

        self.lbl_turno.text  = titulo
        self.lbl_turno.color = (255, 200, 100)

        bw    = 160
        total = len(candidatos) * (bw + 10) - 10
        sx    = w // 2 - total // 2
        by    = h // 2 - 30

        for i, p in enumerate(candidatos):
            col = COL_EQ1 if p in self.combate.equipo1 else COL_EQ2
            btn = ImageButton(
                x=sx + i * (bw + 10), y=by,
                width=bw, height=55,
                text=p.nombre[:14],
                normal_color=col,
                hover_color=(min(col[0] + 40, 255), min(col[1] + 40, 255), min(col[2] + 40, 255)),
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

    # ── Comandos del jugador ─────────────────────────────────────────────────

    def _verificar_accion_permitida(self, nombre: str) -> bool:
        if self._combate_terminado:
            DBG.warn(f"{nombre}: combate ya terminado")
            return False
        actor = self.combate.personaje_turno_actual
        if actor is None:
            DBG.warn(f"{nombre}: actor_turno es None")
            return False
        if actor.es_ia:
            DBG.warn(f"{nombre}: llamado pero es turno de IA", actor=actor.nombre)
            return False
        return True

    def _cmd_ataque(self):
        if not self._verificar_accion_permitida("_cmd_ataque"):
            return
        actor  = self.combate.personaje_turno_actual
        rivales = [p for p in self.combate.equipo_rival_de(actor) if p.esta_vivo()]
        if not rivales:
            DBG.warn("_cmd_ataque: no hay rivales vivos")
            return
        if len(rivales) == 1:
            self._ejecutar_jugador(Accion.ATAQUE_BASICO, rivales[0])
        else:
            self.accion_pendiente        = Accion.ATAQUE_BASICO
            self.habilidad_idx_pendiente = None
            self.esperando_objetivo      = True
            self.mostrando_habilidades   = False
            self._crear_objetivo_btns(Accion.ATAQUE_BASICO)
            self._actualizar_visibilidad()

    def _cmd_defender(self):
        if not self._verificar_accion_permitida("_cmd_defender"):
            return
        actor = self.combate.personaje_turno_actual
        self._ejecutar_jugador(Accion.DEFENDER, actor)

    def _cmd_concentrar(self):
        if not self._verificar_accion_permitida("_cmd_concentrar"):
            return
        actor = self.combate.personaje_turno_actual
        self._ejecutar_jugador(Accion.CONCENTRAR, actor)

    def _cmd_mostrar_habilidades(self):
        if not self._verificar_accion_permitida("_cmd_mostrar_habilidades"):
            return
        self.mostrando_habilidades = True
        self.esperando_objetivo    = False
        self._crear_habilidad_btns(self._btn_y + self._btn_h_sz + 8)
        self._actualizar_visibilidad()

    def _cmd_ocultar_habilidades(self):
        self.mostrando_habilidades = False
        self._actualizar_visibilidad()

    def _cmd_usar_habilidad(self, idx: int):
        if not self._verificar_accion_permitida("_cmd_usar_habilidad"):
            return
        actor = self.combate.personaje_turno_actual
        if idx < 0 or idx >= len(actor.habilidades):
            DBG.error("_cmd_usar_habilidad: índice inválido",
                      idx=idx, total=len(actor.habilidades))
            return
        hab = actor.habilidades[idx]
        if actor.energia_actual < hab.costo_energia:
            self._log_add(f"Energía insuficiente ({int(actor.energia_actual)}/{hab.costo_energia})")
            DBG.info("Energía insuficiente", hab=hab.nombre,
                     energia=actor.energia_actual, costo=hab.costo_energia)
            return

        es_cur = getattr(hab, 'es_curacion', False)
        if es_cur:
            candidatos = [p for p in self.combate.equipo_propio_de(actor) if p.esta_vivo()]
        else:
            candidatos = [p for p in self.combate.equipo_rival_de(actor) if p.esta_vivo()]

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
        if not self.esperando_objetivo:
            DBG.warn("_cmd_confirmar_objetivo: no estábamos esperando objetivo")
            return
        self.esperando_objetivo = False
        self._ejecutar_jugador(
            self.accion_pendiente, objetivo,
            self.habilidad_idx_pendiente
        )
        self.accion_pendiente        = None
        self.habilidad_idx_pendiente = None
        self.objetivo_btns.clear()

    def _cmd_cancelar_objetivo(self):
        self.esperando_objetivo      = False
        self.accion_pendiente        = None
        self.habilidad_idx_pendiente = None
        self.objetivo_btns.clear()
        self._actualizar_visibilidad()

    # ── Ejecución y flujo de combate ─────────────────────────────────────────

    def _ejecutar_jugador(self, accion: Accion, objetivo, hab_idx: int = None):
        if self.combate.estado != EstadoCombate.EN_CURSO:
            DBG.warn("_ejecutar_jugador: combate no EN_CURSO",
                     estado=str(self.combate.estado))
            return
        DBG.info("Ejecutar jugador", accion=str(accion),
                 objetivo=getattr(objetivo, 'nombre', '?'), hab_idx=hab_idx)
        resultado = self.combate.ejecutar_accion_jugador(accion, objetivo, hab_idx)
        self._historial.append(resultado)
        self._log_accion(resultado)
        self._actualizar_barras()

        if self.combate.estado != EstadoCombate.EN_CURSO:
            self._fin_combate()
            return

        self._ejecutar_ias_y_actualizar()

    def _ejecutar_ias_y_actualizar(self):
        """
        Ejecuta las IAs del round actual y actualiza la UI.
        Si al terminar el round el siguiente turno sigue siendo de IA
        (ronda completa sin jugadores, p.ej. todos KO), activa la bandera
        _ia_pendiente para que on_update lo procese en el siguiente frame
        en lugar de bloquearse aquí.
        """
        self._ia_pendiente = False

        if self.combate.estado != EstadoCombate.EN_CURSO:
            return

        resultados = self.combate.ejecutar_acciones_ia_hasta_jugador()
        for r in resultados:
            self._historial.append(r)
            self._log_accion(r)
        self._actualizar_barras()

        if self.combate.estado != EstadoCombate.EN_CURSO:
            self._fin_combate()
            return

        # Comprobar si el siguiente en actuar es otra IA (round cruzado o
        # todos los jugadores KO). Si es así, diferir al siguiente frame.
        siguiente = self.combate.personaje_turno_actual
        if siguiente is None or siguiente.es_ia:
            self._ia_pendiente = True

        self._actualizar_ui()

    def _fin_combate(self):
        self._combate_terminado = True
        resultado = self.combate.obtener_resultado_final()
        self._log_add(f"══ {resultado.mensaje_final} ══")
        DBG.info("Combate equipo finalizado", mensaje=resultado.mensaje_final)
        self._actualizar_ui()
        for b in self._action_btns:
            b.visible = False
        for b in self.habilidad_btns:
            b.visible = False
        for b in self.post_btns:
            b.visible = True
        self.lbl_turno.text  = resultado.mensaje_final
        self.lbl_turno.color = (255, 220, 100)

    # ── Log ──────────────────────────────────────────────────────────────────

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

    # ── Actualización de UI ──────────────────────────────────────────────────

    def _actualizar_barras(self):
        for p, (vbar, ebar) in self.health_bars.items():
            vbar.current_value = p.vida_actual
            ebar.current_value = p.energia_actual

        for p in self.equipo1 + self.equipo2:
            if hasattr(p, '_sprite') and p._sprite:
                p._sprite.alpha = 60 if not p.esta_vivo() else 255

    def _actualizar_ui(self):
        self._actualizar_barras()
        actor = self.combate.personaje_turno_actual
        if actor and not self._combate_terminado:
            eq  = self.combate.equipo_de(actor)
            col = COL_EQ1 if eq == 1 else COL_EQ2
            ctrl = "🤖 IA" if actor.es_ia else "🎮 JUGADOR"
            self.lbl_turno.text  = f"Turno: {actor.nombre} ({ctrl}) — Eq.{eq}"
            self.lbl_turno.color = col
        self.lbl_log.text = "\n".join(self._log[-MAX_LOG:])
        self._actualizar_visibilidad()

    def _actualizar_visibilidad(self):
        actor             = self.combate.personaje_turno_actual
        es_turno_jugador  = (actor is not None and not actor.es_ia
                             and not self._combate_terminado)

        mostrar_principales = es_turno_jugador and not self.mostrando_habilidades and not self.esperando_objetivo
        for b in self._action_btns:
            b.visible = mostrar_principales

        mostrar_habs = es_turno_jugador and self.mostrando_habilidades and not self.esperando_objetivo
        for b in self.habilidad_btns:
            b.visible = mostrar_habs

        # Snapshot de debug
        DBG.check_turno(
            turno_jugador=es_turno_jugador,
            combate_estado=self.combate.estado,
            en_curso_valor=EstadoCombate.EN_CURSO,
            mostrando_habs=self.mostrando_habilidades,
            ubicacion="CombatTeam._actualizar_visibilidad"
        )

        # Verificar que no haya solapamiento entre listas
        DBG.check_doble_lista(self.ui_elements, self.habilidad_btns,
                              "ui_elements", "habilidad_btns")
        DBG.check_doble_lista(self.ui_elements, self.objetivo_btns,
                              "ui_elements", "objetivo_btns")

    # ── Render ───────────────────────────────────────────────────────────────

    def on_update(self, delta_time: float):
        super().on_update(delta_time)  # desbloquea _block_next_press
        if self._ia_pendiente and not self._combate_terminado:
            self._ejecutar_ias_y_actualizar()

    def on_draw(self):
        self.clear()
        arcade.set_background_color(self.background_color)

        lx, ly, lw, lh = self._log_rect
        arcade.draw_rect_filled(arcade.LBWH(lx, ly, lw, lh), (15, 15, 25, 220))
        arcade.draw_rect_outline(arcade.LBWH(lx, ly, lw, lh), (80, 80, 120), 1)

        w, h = self.app.width, self.app.height
        arcade.draw_line(w // 2, ly + lh + 10, w // 2, h - 20, (80, 80, 100), 2)

        self.sprite_list.draw()

        for elem in self.static_elements:
            elem.draw()
        for elem in self.ui_elements:
            if hasattr(elem, 'draw'):
                elem.draw()

        # Tags de estado flotantes (KO, etc.)
        for p in self.equipo1 + self.equipo2:
            if not p.esta_vivo() and hasattr(p, '_tag_cx'):
                EstadoTag(p._tag_cx, p._tag_cy, 'muerto', font_size=10).draw()

        # Botones de habilidad y objetivo (fuera de ui_elements → sin solapamiento)
        for b in self.habilidad_btns:
            b.draw()
        for b in self.objetivo_btns:
            b.draw()

        # Panel semitransparente de fondo cuando se elige objetivo
        if self.esperando_objetivo and self.objetivo_btns:
            bx = self.objetivo_btns[0].x - 10
            by = self.objetivo_btns[-1].y - 10
            bw2 = max(b.x + b.width for b in self.objetivo_btns) - bx + 10
            bh2 = max(b.y + b.height for b in self.objetivo_btns) - by + 10
            arcade.draw_rect_filled(
                arcade.LBWH(bx - 5, by - 5, bw2 + 10, bh2 + 10),
                (10, 10, 30, 200)
            )
            for b in self.objetivo_btns:
                b.draw()

    # ── Eventos de ratón con refuerzos anti-propagación ─────────────────────

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Actualiza hover de SOLO los grupos activos, sin doble procesamiento.
        """
        if self.esperando_objetivo:
            # Solo botones de objetivo reciben hover
            for b in self.objetivo_btns:
                b.on_mouse_motion(x, y, dx, dy)
            # Los demás pierden hover
            for b in self._action_btns + self.habilidad_btns:
                b.hovered = False
            return

        if self.mostrando_habilidades:
            # Solo habilidades reciben hover
            for b in self.habilidad_btns:
                b.on_mouse_motion(x, y, dx, dy)
            for b in self._action_btns:
                b.hovered = False
            # Etiquetas de texto no tienen hover
            return

        # Modo normal: ui_elements (acciones + postcombate + etiquetas)
        for elem in self.ui_elements:
            if hasattr(elem, 'on_mouse_motion'):
                if hasattr(elem, 'visible') and not elem.visible:
                    if hasattr(elem, 'hovered'):
                        elem.hovered = False
                    continue
                elem.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Enrutamiento exclusivo con refuerzo anti-propagación.
        Cada modo solo procesa su grupo de botones activo.
        """
        if self._block_next_press:
            DBG.info("Click bloqueado (block_next_press)", x=x, y=y)
            return

        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        # ── Prioridad 1: selección de objetivo ────────────────────────────
        if self.esperando_objetivo:
            for b in self.objetivo_btns:
                if not b.visible:
                    continue
                if b.on_mouse_press(x, y, button, modifiers):
                    DBG.click("objetivo_btn", x, y, True, texto=getattr(b, 'text', '?'))
                    return          # consumido
            DBG.click("objetivo_zona_vacia", x, y, False)
            return                  # no propagamos a otros grupos

        # ── Prioridad 2: habilidades abiertas ────────────────────────────
        if self.mostrando_habilidades:
            for b in self.habilidad_btns:
                if not b.visible:
                    continue
                if b.on_mouse_press(x, y, button, modifiers):
                    DBG.click("habilidad_btn_team", x, y, True, texto=getattr(b, 'text', '?'))
                    return          # consumido
            DBG.click("habilidades_zona_vacia_team", x, y, False)
            return                  # no propagamos a botones de acción

        # ── Prioridad 3: botones normales (ui_elements) ──────────────────
        for elem in self.ui_elements:
            if hasattr(elem, 'on_mouse_press'):
                if hasattr(elem, 'visible') and not elem.visible:
                    continue        # refuerzo: invisibles nunca consumen
                if elem.on_mouse_press(x, y, button, modifiers):
                    DBG.click("ui_team", x, y, True, tipo=type(elem).__name__)
                    return          # consumido
        DBG.click("zona_vacia_team", x, y, False)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.F11:
            self.app.set_fullscreen(not self.app.fullscreen)
        elif symbol == arcade.key.F12:
            print(DBG.export())
            print("\n[Solo WARN/ERROR]:")
            print(DBG.solo_warns())

    # ── Postcombate ──────────────────────────────────────────────────────────

    def _ver_historial(self):
        def _volver():
            from scenes.menu_scene import MenuView
            self.app.goto_view(MenuView(self.app))
        self.app.push_view(HistorialView(self.app, self._historial, on_back=_volver))

    def _revancha(self):
        DBG.info("Revancha equipo")
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