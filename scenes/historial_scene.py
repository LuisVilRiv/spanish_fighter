# scenes/historial_scene.py
"""
HistorialView — muestra el historial de cualquier modo de combate.

Soporta dos formatos de resultado:
  • ResultadoTurno  (modo 1v1)  — campos: jugador_accion, ia_accion,
                                   daño_jugador_a_ia, daño_ia_a_jugador,
                                   curacion_jugador, curacion_ia, evento_aleatorio
  • ResultadoAccion (modo equipo) — campos: descripcion, daño, curacion,
                                    mensajes_extra, actor_nombre, objetivo_nombre,
                                    actor_equipo, es_ia
"""
import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel

TURNOS_POR_PAGINA = 7


class HistorialView(BaseView):
    def __init__(self, app, historial: list, on_back=None):
        super().__init__(app)
        self.historial        = historial
        self.on_back_callback = on_back
        self.current_page     = 0
        self.ui_elements      = []
        self._setup_ui()

    # ── UI ───────────────────────────────────────────────────────────────────

    def _setup_ui(self):
        self.ui_elements.clear()
        w, h = self.app.width, self.app.height
        self.background_color = (30, 35, 50)

        HEADER_H = int(h * 0.11)
        FOOTER_H = int(h * 0.16)
        TEXT_TOP  = h - HEADER_H
        TEXT_BOT  = FOOTER_H

        # Título
        self.ui_elements.append(RetroLabel(
            "HISTORIAL DEL COMBATE",
            w // 2, h - HEADER_H // 2,
            font_size=max(20, int(h * 0.042)),
            color=(255, 220, 150),
            anchor_x='center', anchor_y='center'
        ))

        # Indicador de página
        total_pags = self._total_paginas()
        self.lbl_pagina = RetroLabel(
            f"Pág. {self.current_page + 1} / {total_pags}",
            w - int(w * 0.04), h - HEADER_H // 2,
            font_size=max(11, int(h * 0.020)),
            color=(160, 160, 180),
            anchor_x='right', anchor_y='center'
        )
        self.ui_elements.append(self.lbl_pagina)

        # Cuerpo de texto
        self.text_label = RetroLabel(
            self._get_page_text(),
            x=int(w * 0.05), y=TEXT_TOP,
            width=int(w * 0.90),
            font_size=max(11, int(h * 0.019)),
            color=(200, 200, 200),
            anchor_x='left', anchor_y='top', multiline=True
        )
        self.ui_elements.append(self.text_label)

        # Botones de pie
        BTN_H   = int(FOOTER_H * 0.38)
        BTN_GAP = int(w * 0.025)
        nav_w   = int(min(w * 0.18, 175))
        back_w  = int(min(w * 0.22, 210))

        nav_row_y  = TEXT_BOT + int(FOOTER_H * 0.55) - BTN_H // 2
        back_row_y = TEXT_BOT + int(FOOTER_H * 0.12)

        self.ui_elements.extend([
            ImageButton(
                x=w // 2 - nav_w - BTN_GAP, y=nav_row_y,
                width=nav_w, height=BTN_H,
                text="◀ ANTERIOR",
                normal_color=(90, 90, 120), hover_color=(120, 120, 160),
                callback=self.prev_page
            ),
            ImageButton(
                x=w // 2 + BTN_GAP, y=nav_row_y,
                width=nav_w, height=BTN_H,
                text="SIGUIENTE ▶",
                normal_color=(90, 90, 120), hover_color=(120, 120, 160),
                callback=self.next_page
            ),
            ImageButton(
                x=w // 2 - back_w // 2, y=back_row_y,
                width=back_w, height=BTN_H,
                text="VOLVER",
                normal_color=(110, 110, 135), hover_color=(145, 145, 175),
                callback=self.back
            ),
        ])

    # ── Paginación ───────────────────────────────────────────────────────────

    def _total_paginas(self) -> int:
        return max(1, (len(self.historial) + TURNOS_POR_PAGINA - 1) // TURNOS_POR_PAGINA)

    def _get_page_text(self) -> str:
        start = self.current_page * TURNOS_POR_PAGINA
        page  = self.historial[start:start + TURNOS_POR_PAGINA]
        if not page:
            return "No hay entradas en el historial."

        lines = []
        for i, entrada in enumerate(page, start=start + 1):
            lines.extend(self._formatear_entrada(i, entrada))
            lines.append("")
        return "\n".join(lines)

    # ── Formateo adaptativo ───────────────────────────────────────────────────

    @staticmethod
    def _formatear_entrada(numero: int, entrada) -> list:
        """
        Devuelve una lista de strings representando la entrada.
        Compatible con:
          - ResultadoTurno  (modo 1v1)
          - ResultadoAccion (modo equipo), incluyendo entradas de evento
        """

        # ── Formato equipo: tiene atributo 'descripcion' ──────────────────────
        if hasattr(entrada, 'descripcion'):
            # Detectar si es entrada de evento (actor_nombre empieza por ⚡)
            actor_nom = getattr(entrada, 'actor_nombre', None)
            es_evento = actor_nom and actor_nom.startswith("⚡")

            if es_evento:
                lines = [f"─── #{numero} ⚡ EVENTO ALEATORIO ───────────"]
                lines.append(f"  {entrada.descripcion}")
                for m in getattr(entrada, 'mensajes_extra', []):
                    lines.append(f"  {m}")
                return lines

            # Acción normal de combate
            obj_nom   = getattr(entrada, 'objetivo_nombre', None)
            eq_actor  = getattr(entrada, 'actor_equipo', None)
            es_ia     = getattr(entrada, 'es_ia', False)
            ctrl      = "🤖" if es_ia else "🎮"
            eq_tag    = f" [Eq.{eq_actor}]" if eq_actor else ""

            lines = [f"─── #{numero} ───────────────────────"]
            if actor_nom:
                linea_actor = f"  {ctrl} {actor_nom}{eq_tag}"
                if obj_nom:
                    obj_eq = getattr(entrada, 'objetivo_equipo', None)
                    obj_eq_tag = f" [Eq.{obj_eq}]" if obj_eq else ""
                    linea_actor += f" → {obj_nom}{obj_eq_tag}"
                lines.append(linea_actor)

            lines.append(f"  Acción  : {entrada.descripcion}")

            daño = getattr(entrada, 'daño', None)
            if daño:
                lines.append(f"  ⚔ Daño  : {daño}")

            cur = getattr(entrada, 'curacion', None)
            if cur:
                lines.append(f"  💚 Cur.  : {cur}")

            for m in getattr(entrada, 'mensajes_extra', []):
                lines.append(f"  ⚠  {m}")

            return lines

        # ── Formato 1v1: campos clásicos ──────────────────────────────────────
        lines = [f"─── #{numero} ───────────────────────"]

        jac = getattr(entrada, 'jugador_accion', None)
        iac = getattr(entrada, 'ia_accion', None)
        dj  = getattr(entrada, 'daño_jugador_a_ia', None)
        de  = getattr(entrada, 'daño_ia_a_jugador', None)
        cj  = getattr(entrada, 'curacion_jugador', None)
        ci  = getattr(entrada, 'curacion_ia', None)
        ev  = getattr(entrada, 'evento_aleatorio', None)

        if jac:
            lines.append(f"  🎮 Jugador : {jac}")
        if iac:
            lines.append(f"  🤖 IA      : {iac}")
        if dj:
            lines.append(f"  ⚔ Daño a IA     : {dj}")
        if de:
            lines.append(f"  ⚔ Daño recibido : {de}")
        if cj:
            lines.append(f"  💚 Cur. jugador  : {cj}")
        if ci:
            lines.append(f"  💚 Cur. IA       : {ci}")
        if ev:
            import re as _re
            nombre_ev = ev.get('nombre', 'Evento aleatorio')
            msg_limpio = _re.sub(r'\x1b\[[0-9;]*m', '', ev.get('mensaje', ''))
            lineas_ev = [l.strip() for l in msg_limpio.splitlines() if l.strip()]
            lines.append(f"  ⚡ Evento: {nombre_ev}")
            for l in lineas_ev[:3]:
                lines.append(f"     {l}")

        return lines

    def _refresh_page_label(self):
        self.lbl_pagina.text = f"Pág. {self.current_page + 1} / {self._total_paginas()}"

    def _refresh_text(self):
        self.text_label.text = self._get_page_text()

    # ── Controles de página ──────────────────────────────────────────────────

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._refresh_page_label()
            self._refresh_text()

    def next_page(self):
        if self.current_page < self._total_paginas() - 1:
            self.current_page += 1
            self._refresh_page_label()
            self._refresh_text()

    def back(self):
        if self.on_back_callback:
            self.on_back_callback()
        else:
            self.app.pop_view()

    # ── Render / eventos ─────────────────────────────────────────────────────

    def on_draw(self):
        self.clear()
        for elem in self.ui_elements:
            if hasattr(elem, 'draw'):
                elem.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for elem in self.ui_elements:
            if hasattr(elem, 'on_mouse_press'):
                if elem.on_mouse_press(x, y, button, modifiers):
                    return True
        return False

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)
        for elem in self.ui_elements:
            if hasattr(elem, 'on_mouse_motion'):
                elem.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.prev_page()
        elif symbol == arcade.key.RIGHT:
            self.next_page()
        elif symbol == arcade.key.ESCAPE:
            self.back()

    def on_resize(self, width, height):
        self._setup_ui()