# scenes/historial_scene.py
import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel

class HistorialView(BaseView):
    def __init__(self, app, historial, on_back=None):
        super().__init__(app)
        self.historial         = historial
        self.on_back_callback  = on_back
        self.current_page      = 0
        self.ui_elements       = []
        self._setup_ui()

    def _setup_ui(self):
        self.ui_elements.clear()
        w, h = self.app.width, self.app.height
        self.background_color = (30, 35, 50)

        # ── Zonas ─────────────────────────────────────────────────────────
        HEADER_H   = int(h * 0.11)
        FOOTER_H   = int(h * 0.16)
        TEXT_TOP   = h - HEADER_H
        TEXT_BOT   = FOOTER_H
        TEXT_H     = TEXT_TOP - TEXT_BOT

        # ── Título ────────────────────────────────────────────────────────
        title_sz = max(20, int(h * 0.042))
        self.title = RetroLabel(
            "HISTORIAL DEL COMBATE",
            w // 2, h - HEADER_H // 2,
            font_size=title_sz, color=(255, 220, 150),
            anchor_x='center', anchor_y='center'
        )
        self.ui_elements.append(self.title)

        # Paginación junto al título
        total_paginas = max(1, (len(self.historial) + 4) // 5)
        self.lbl_pagina = RetroLabel(
            f"Pág. {self.current_page + 1} / {total_paginas}",
            w - int(w * 0.04), h - HEADER_H // 2,
            font_size=max(11, int(h * 0.020)),
            color=(160, 160, 180),
            anchor_x='right', anchor_y='center'
        )
        self.ui_elements.append(self.lbl_pagina)

        # ── Texto del historial ───────────────────────────────────────────
        margin_x  = int(w * 0.05)
        text_font = max(11, int(h * 0.019))
        self.text_label = RetroLabel(
            self._get_page_text(),
            x=margin_x, y=TEXT_TOP,
            width=w - 2 * margin_x,
            font_size=text_font, color=(200, 200, 200),
            anchor_x='left', anchor_y='top', multiline=True
        )
        self.ui_elements.append(self.text_label)

        # ── Botones de pie ────────────────────────────────────────────────
        BTN_H    = int(FOOTER_H * 0.38)
        BTN_GAP  = int(w * 0.025)
        nav_w    = int(min(w * 0.18, 175))
        back_w   = int(min(w * 0.22, 210))

        # Fila superior: ANTERIOR | SIGUIENTE
        nav_row_y  = TEXT_BOT + int(FOOTER_H * 0.55) - BTN_H // 2
        btn_prev = ImageButton(
            x=w // 2 - nav_w - BTN_GAP,
            y=nav_row_y,
            width=nav_w, height=BTN_H,
            text="◀ ANTERIOR",
            normal_color=(90, 90, 120), hover_color=(120, 120, 160),
            callback=self.prev_page
        )
        btn_next = ImageButton(
            x=w // 2 + BTN_GAP,
            y=nav_row_y,
            width=nav_w, height=BTN_H,
            text="SIGUIENTE ▶",
            normal_color=(90, 90, 120), hover_color=(120, 120, 160),
            callback=self.next_page
        )

        # Fila inferior: VOLVER
        back_row_y = TEXT_BOT + int(FOOTER_H * 0.12)
        btn_back = ImageButton(
            x=w // 2 - back_w // 2,
            y=back_row_y,
            width=back_w, height=BTN_H,
            text="VOLVER",
            normal_color=(110, 110, 135), hover_color=(145, 145, 175),
            callback=self.back
        )

        self.ui_elements.extend([btn_prev, btn_next, btn_back])

    def _get_page_text(self):
        turnos_por_pagina = 5
        start      = self.current_page * turnos_por_pagina
        page_items = self.historial[start:start + turnos_por_pagina]
        if not page_items:
            return "No hay más turnos."
        lines = []
        for i, turno in enumerate(page_items, start=start + 1):
            lines.append(f"─── Turno {i} ───────────────────────")
            if turno.jugador_accion:
                lines.append(f"  Jugador : {turno.jugador_accion}")
            if turno.ia_accion:
                lines.append(f"  IA      : {turno.ia_accion}")
            if turno.daño_jugador_a_ia:
                lines.append(f"  Daño a IA      : {turno.daño_jugador_a_ia}")
            if turno.daño_ia_a_jugador:
                lines.append(f"  Daño recibido  : {turno.daño_ia_a_jugador}")
            if turno.curacion_jugador:
                lines.append(f"  Curación jugador: {turno.curacion_jugador}")
            if turno.curacion_ia:
                lines.append(f"  Curación IA     : {turno.curacion_ia}")
            if turno.evento_aleatorio:
                lines.append(f"  Evento : {turno.evento_aleatorio.get('nombre', 'Evento')}")
            lines.append("")
        return "\n".join(lines)

    def _refresh_page_label(self):
        total = max(1, (len(self.historial) + 4) // 5)
        self.lbl_pagina.text = f"Pág. {self.current_page + 1} / {total}"

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.text_label.text = self._get_page_text()
            self._refresh_page_label()

    def next_page(self):
        total = (len(self.historial) + 4) // 5
        if self.current_page < total - 1:
            self.current_page += 1
            self.text_label.text = self._get_page_text()
            self._refresh_page_label()

    def back(self):
        if self.on_back_callback:
            self.on_back_callback()
        else:
            from scenes.menu_scene import MenuView
            self.app.goto_view(MenuView(self.app))

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