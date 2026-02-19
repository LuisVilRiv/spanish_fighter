# scenes/historial_scene.py
"""
HistorialView — muestra el historial de cualquier modo de combate.

Soporta dos formatos de resultado:
  • ResultadoTurno  (modo 1v1)  — campos: jugador_accion, ia_accion,
                                   daño_jugador_a_ia, daño_ia_a_jugador,
                                   curacion_jugador, curacion_ia, evento_aleatorio
  • ResultadoAccion (modo equipo) — campos: descripcion, daño, curacion,
                                    mensajes_extra, actor (nombre), objetivo (nombre)
"""
import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel

TURNOS_POR_PAGINA = 6


class HistorialView(BaseView):
    def __init__(self, app, historial: list, on_back=None):
        super().__init__(app)
        self.historial         = historial
        self.on_back_callback  = on_back
        self.current_page      = 0
        self.ui_elements       = []
        self._setup_ui()

    # ── UI ───────────────────────────────────────────────────────────────────

    def _setup_ui(self):
        self.ui_elements.clear()
        w, h = self.app.width, self.app.height
        self.background_color = (30, 35, 50)

        HEADER_H = int(h * 0.11)
        FOOTER_H = int(h * 0.16)
        TEXT_TOP = h - HEADER_H
        TEXT_BOT = FOOTER_H

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
            return "No hay más entradas."

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
        Compatible con ResultadoTurno (1v1) y ResultadoAccion (equipo).
        """
        lines = [f"─── #{numero} ───────────────────────"]

        # ── Formato equipo: tiene atributo 'descripcion' ──────────────────────
        if hasattr(entrada, 'descripcion'):
            actor_nom = getattr(getattr(entrada, 'actor', None), 'nombre', None)
            obj_nom   = getattr(getattr(entrada, 'objetivo', None), 'nombre', None)
            if actor_nom:
                lines.append(f"  Actor   : {actor_nom}" + (f" → {obj_nom}" if obj_nom else ""))
            lines.append(f"  Acción  : {entrada.descripcion}")
            daño = getattr(entrada, 'daño', None)
            if daño:
                lines.append(f"  ⚔ Daño  : {daño}")
            cur = getattr(entrada, 'curacion', None)
            if cur:
                lines.append(f"  💚 Cur. : {cur}")
            for m in getattr(entrada, 'mensajes_extra', []):
                lines.append(f"  ⚠ {m}")
            return lines

        # ── Formato 1v1: campos clásicos ──────────────────────────────────────
        jac = getattr(entrada, 'jugador_accion', None)
        iac = getattr(entrada, 'ia_accion', None)
        dj  = getattr(entrada, 'daño_jugador_a_ia', None)
        de  = getattr(entrada, 'daño_ia_a_jugador', None)
        cj  = getattr(entrada, 'curacion_jugador', None)
        ci  = getattr(entrada, 'curacion_ia', None)
        ev  = getattr(entrada, 'evento_aleatorio', None)

        if jac:
            lines.append(f"  Jugador : {jac}")
        if iac:
            lines.append(f"  IA      : {iac}")
        if dj:
            lines.append(f"  ⚔ Daño a IA     : {dj}")
        if de:
            lines.append(f"  ⚔ Daño recibido : {de}")
        if cj:
            lines.append(f"  💚 Cur. jugador  : {cj}")
        if ci:
            lines.append(f"  💚 Cur. IA       : {ci}")
        if ev:
            lines.append(f"  ⚡ Evento: {ev.get('nombre', ev.get('mensaje', 'Evento'))}")

        return lines

    def _refresh_page_label(self):
        self.lbl_pagina.text = f"Pág. {self.current_page + 1} / {self._total_paginas()}"

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.text_label.text = self._get_page_text()
            self._refresh_page_label()

    def next_page(self):
        if self.current_page < self._total_paginas() - 1:
            self.current_page += 1
            self.text_label.text = self._get_page_text()
            self._refresh_page_label()

    def back(self):
        if self.on_back_callback:
            self.on_back_callback()
        else:
            from scenes.menu_scene import MenuView
            self.app.goto_view(MenuView(self.app))

    # ── Render y eventos ─────────────────────────────────────────────────────

    def on_draw(self):
        self.clear()
        arcade.set_background_color(self.background_color)
        for elem in self.ui_elements:
            elem.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

    def on_resize(self, width, height):
        self._setup_ui()