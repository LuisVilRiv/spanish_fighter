import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel
from personajes import __all__ as personajes_list
from personajes import *
from scenes.rival_select_scene import RivalSelectView

class CharacterSelectView(BaseView):
    def __init__(self, app):
        super().__init__(app)
        self.ui_elements = []
        self._setup_ui()

    def _setup_ui(self):
        w, h = self.app.width, self.app.height
        self.background_color = (45,50,70)
        self.title = RetroLabel("SELECCIONA TU LUCHADOR", w//2, h-60,
                                font_size=32, color=(255,220,150))

        cols = 4
        btn_w, btn_h = 120, 120
        spacing_x = (w - cols*btn_w) // (cols+1)
        start_x = spacing_x
        start_y = h - 150
        spacing_y = 150

        for i, clase_nombre in enumerate(personajes_list):
            clase = globals()[clase_nombre]
            instancia = clase()
            nombre_archivo = clase_nombre.lower() + '.png'
            ruta_icono = f'img/personajes/{nombre_archivo}'
            col = i % cols
            fila = i // cols
            x = start_x + col*(btn_w + spacing_x)
            y = start_y - fila*spacing_y

            btn = ImageButton(
                x=x, y=y-btn_h,
                width=btn_w, height=btn_h,
                image_path=ruta_icono,
                hover_tint=(220,220,220),
                callback=lambda c=clase: self.select_character(c)
            )
            self.ui_elements.append(btn)

            label = RetroLabel(
                instancia.nombre[:12],
                x=x + btn_w//2, y=y-20,
                font_size=12
            )
            self.ui_elements.append(label)

        btn_back = ImageButton(
            x=w//2-100, y=50, width=200, height=50,
            text="VOLVER", normal_color=(120,120,140), hover_color=(150,150,180),
            callback=self.back
        )
        self.ui_elements.append(btn_back)

    def on_draw(self):
        self.clear()
        self.title.draw()
        for elem in self.ui_elements:
            if hasattr(elem, 'draw'):
                elem.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

    def select_character(self, clase):
        self.app.push_view(RivalSelectView(self.app, player_class=clase))

    def back(self):
        from scenes.menu_scene import MenuView
        self.app.goto_view(MenuView(self.app))

    def on_resize(self, width, height):
        self._setup_ui()