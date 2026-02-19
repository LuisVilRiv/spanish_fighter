# scenes/mode_select_scene.py
import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel


class ModeSelectView(BaseView):
    def __init__(self, app):
        super().__init__(app)
        self.ui_elements = []
        self._modo_seleccionado = False
        self._setup_ui()

    def on_show(self):
        super().on_show()
        self._modo_seleccionado = False

    def _setup_ui(self):
        self.ui_elements.clear()
        w, h = self.app.width, self.app.height
        self.background_color = (25, 30, 50)

        TITLE_H = int(h * 0.10)
        FOOTER_H = int(h * 0.12)
        GRID_TOP = h - TITLE_H
        GRID_BOTTOM = FOOTER_H
        GRID_H = GRID_TOP - GRID_BOTTOM

        font_size = max(18, int(h * 0.038))
        self.ui_elements.append(RetroLabel(
            "SELECCIONA EL MODO DE COMBATE",
            w // 2, h - TITLE_H // 2,
            font_size=font_size, color=(255, 220, 80),
            anchor_x='center', anchor_y='center'
        ))

        modos = [
            ("1 VS 1",  1, (140, 90,  90), (180, 120, 120)),
            ("2 VS 2",  2, (90,  110, 140), (120, 140, 180)),
            ("3 VS 3",  3, (90,  130, 90), (120, 170, 120)),
            ("4 VS 4",  4, (130, 90,  130), (170, 120, 170)),
        ]

        cols = 2
        rows = 2
        slot_w = w / cols
        slot_h = GRID_H / (rows + 0.5)
        btn_size = int(min(slot_w, slot_h) * 0.62)
        btn_size = max(btn_size, 80)

        grid_w = cols * slot_w
        offset_x = (w - grid_w) / 2 + slot_w / 2
        total_content_h = rows * slot_h
        grid_top_y = GRID_BOTTOM + (GRID_H + total_content_h) / 2 - slot_h / 2

        for i, (label, size, col, hcol) in enumerate(modos):
            col_idx = i % cols
            row_idx = i // cols
            cx = offset_x + col_idx * slot_w
            cy = grid_top_y - row_idx * slot_h

            btn = ImageButton(
                x=int(cx - btn_size // 2),
                y=int(cy - btn_size // 2),
                width=btn_size, height=btn_size,
                text=label,
                normal_color=col, hover_color=hcol,
                callback=lambda s=size: self._select_mode(s)
            )
            self.ui_elements.append(btn)

            self.ui_elements.append(RetroLabel(
                f"{size} vs {size}",
                x=int(cx), y=int(cy - btn_size // 2 - 10),
                font_size=12, color=(200, 200, 200),
                anchor_x='center', anchor_y='top'
            ))

        btn_back_w = int(min(w * 0.22, 220))
        btn_back_h = int(FOOTER_H * 0.55)
        self.ui_elements.append(ImageButton(
            x=w // 2 - btn_back_w // 2,
            y=(FOOTER_H - btn_back_h) // 2,
            width=btn_back_w, height=btn_back_h,
            text="VOLVER",
            normal_color=(120, 120, 140), hover_color=(150, 150, 180),
            callback=self._back
        ))

    def _select_mode(self, team_size: int):
        if self._modo_seleccionado:
            return
        self._modo_seleccionado = True
        print(f"Modo seleccionado: {team_size} vs {team_size}")
        from scenes.team_select_scene import TeamSelectView
        self.app.goto_view(TeamSelectView(self.app, team_size=team_size))

    def _back(self):
        from scenes.menu_scene import MenuView
        self.app.goto_view(MenuView(self.app))

    def on_draw(self):
        self.clear()
        arcade.set_background_color(self.background_color)
        for elem in self.ui_elements:
            if hasattr(elem, 'draw'):
                elem.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        if super().on_mouse_press(x, y, button, modifiers):
            return

    def on_resize(self, width, height):
        self._setup_ui()