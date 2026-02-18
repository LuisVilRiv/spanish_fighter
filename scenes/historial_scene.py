import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel

class HistorialView(BaseView):
    def __init__(self, app, historial, on_back=None):
        super().__init__(app)
        self.historial = historial
        self.on_back_callback = on_back  # callback opcional para volver a la vista anterior
        self.current_page = 0
        self.ui_elements = []
        self._setup_ui()

    def _setup_ui(self):
        w, h = self.app.width, self.app.height
        self.background_color = (30, 35, 50)

        self.title = RetroLabel("HISTORIAL DEL COMBATE", w//2, h-50, font_size=32, color=(255, 220, 150))
        self.ui_elements.append(self.title)

        self.text_label = RetroLabel(
            self._get_page_text(),
            x=50, y=h-150, width=w-100, font_size=12,
            color=(200, 200, 200), anchor_x='left', anchor_y='top', multiline=True
        )
        self.ui_elements.append(self.text_label)

        btn_prev = ImageButton(
            x=w//2 - 200, y=80, width=150, height=50,
            text="ANTERIOR", normal_color=(100, 100, 120), hover_color=(130, 130, 150),
            callback=self.prev_page
        )
        btn_next = ImageButton(
            x=w//2 + 50, y=80, width=150, height=50,
            text="SIGUIENTE", normal_color=(100, 100, 120), hover_color=(130, 130, 150),
            callback=self.next_page
        )
        btn_back = ImageButton(
            x=w//2 - 100, y=20, width=200, height=40,
            text="VOLVER", normal_color=(120, 120, 140), hover_color=(150, 150, 180),
            callback=self.back
        )
        self.ui_elements.extend([btn_prev, btn_next, btn_back])

    def _get_page_text(self):
        turnos_por_pagina = 5
        start = self.current_page * turnos_por_pagina
        end = start + turnos_por_pagina
        page_items = self.historial[start:end]
        if not page_items:
            return "No hay más turnos."
        lines = []
        for i, turno in enumerate(page_items, start=start+1):
            lines.append(f"--- Turno {i} ---")
            if turno.jugador_accion:
                lines.append(f"Jugador: {turno.jugador_accion}")
            if turno.ia_accion:
                lines.append(f"IA: {turno.ia_accion}")
            if turno.daño_jugador_a_ia:
                lines.append(f"Daño a IA: {turno.daño_jugador_a_ia}")
            if turno.daño_ia_a_jugador:
                lines.append(f"Daño recibido: {turno.daño_ia_a_jugador}")
            if turno.curacion_jugador:
                lines.append(f"Curación jugador: {turno.curacion_jugador}")
            if turno.curacion_ia:
                lines.append(f"Curación IA: {turno.curacion_ia}")
            if turno.evento_aleatorio:
                lines.append(f"Evento: {turno.evento_aleatorio.get('nombre', 'Evento')}")
            lines.append("")
        return "\n".join(lines)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.text_label.text = self._get_page_text()

    def next_page(self):
        total_paginas = (len(self.historial) + 4) // 5
        if self.current_page < total_paginas - 1:
            self.current_page += 1
            self.text_label.text = self._get_page_text()

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