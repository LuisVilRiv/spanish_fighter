import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel
from scenes.character_select_scene import CharacterSelectView
from scenes.characters_info_scene import CharactersInfoView
from scenes.instructions_scene import InstructionsView

class MenuView(BaseView):
    def __init__(self, app):
        super().__init__(app)
        self.ui_elements = []
        self.background = None
        self.title = None
        self._setup_ui()

    def _setup_ui(self):
        w = self.app.width
        h = self.app.height
        # Fondo con gradiente simulado mediante dos rectángulos
        self.bg_top = arcade.color.DARK_SLATE_GRAY
        self.bg_bottom = arcade.color.SLATE_GRAY

        self.title = RetroLabel("Batalla Cómica Española", w//2, h-150,
                                font_size=48, color=(255,255,150))

        btn_width = 260
        btn_height = 70
        start_y = h * 0.55
        spacing = 90
        btn_x = w//2 - btn_width//2

        btns_data = [
            ("NUEVA PARTIDA", (100,160,100), (130,200,130), self.new_game),
            ("CARGAR PARTIDA", (100,140,180), (130,170,220), self.load_game),
            ("PERSONAJES", (160,120,160), (200,150,200), self.view_characters),
            ("INSTRUCCIONES", (160,140,140), (200,180,180), self.instructions),
            ("SALIR", (180,100,100), (220,130,130), self.exit_game)
        ]

        for i, (text, color, hover, callback) in enumerate(btns_data):
            btn = ImageButton(
                x=btn_x, y=int(start_y - i*spacing),
                width=btn_width, height=btn_height,
                text=text, normal_color=color, hover_color=hover,
                callback=callback
            )
            self.ui_elements.append(btn)

    def on_draw(self):
        self.clear()
        w, h = self.app.width, self.app.height
        # Gradiente simple
        arcade.draw_rect_filled(arcade.XYWH(w//2, h//2, w, h), self.bg_bottom)
        arcade.draw_rect_filled(arcade.XYWH(w//2, h-40, w, 80), arcade.color.DARK_SLATE_GRAY)
        arcade.draw_rect_filled(arcade.XYWH(w//2, 40, w, 80), arcade.color.DARK_SLATE_GRAY)
        self.title.draw()
        for btn in self.ui_elements:
            btn.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)

    def new_game(self):
        self.app.push_view(CharacterSelectView(self.app))

    def load_game(self):
        # Placeholder
        pass

    def view_characters(self):
        self.app.push_view(CharactersInfoView(self.app))

    def instructions(self):
        self.app.push_view(InstructionsView(self.app))

    def exit_game(self):
        arcade.close_window()

    def on_resize(self, width, height):
        self._setup_ui()