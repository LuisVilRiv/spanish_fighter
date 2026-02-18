import arcade
import time
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

        # Estado del popup
        self.mostrar_popup = False
        self.popup_start_time = 0
        self.popup_duration = 5  # segundos

        # Textos del popup
        self.popup_title_text = None
        self.popup_message_text = None
        self.popup_timer_text = None

        self._setup_ui()

    def _setup_ui(self):
        w = self.app.width
        h = self.app.height
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
            ("NUEVA PARTIDA",   (100,160,100), (130,200,130), self.new_game),
            ("CARGAR PARTIDA",  (100,140,180), (130,170,220), self.load_game),
            ("PERSONAJES",      (160,120,160), (200,150,200), self.view_characters),
            ("INSTRUCCIONES",   (160,140,140), (200,180,180), self.instructions),
            ("SALIR",           (180,100,100), (220,130,130), self.exit_game)
        ]

        self.ui_elements = []
        for i, (text, color, hover, callback) in enumerate(btns_data):
            btn = ImageButton(
                x=btn_x, y=int(start_y - i*spacing),
                width=btn_width, height=btn_height,
                text=text, normal_color=color, hover_color=hover,
                callback=callback
            )
            self.ui_elements.append(btn)

        # Popup: Textos
        self.popup_title_text = arcade.Text(
            "⚙  PRÓXIMAMENTE",
            w // 2, h // 2 + 70,
            arcade.color.YELLOW,
            font_size=20,
            anchor_x="center", anchor_y="center",
            bold=True
        )
        self.popup_message_text = arcade.Text(
            "Esta funcionalidad estará disponible\nen futuras actualizaciones del juego.\n\n¡Gracias por tu paciencia!",
            w // 2, h // 2 - 10,
            arcade.color.LIGHT_GRAY,
            font_size=14,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=400
        )
        self.popup_timer_text = arcade.Text(
            "Cerrando en 5.0 s",
            w // 2, h // 2 - 60,
            arcade.color.WHITE,
            font_size=16,
            anchor_x="center", anchor_y="center",
            bold=True
        )

    # === POPUP ===

    def load_game(self):
        self.mostrar_popup = True
        self.popup_start_time = time.time()
        self.popup_timer_text.text = "Cerrando en 5.0 s"

    def on_draw(self):
        self.clear()

        w, h = self.app.width, self.app.height

        # Fondo general
        arcade.draw_rect_filled(arcade.XYWH(w//2, h//2, w, h), self.bg_bottom)
        arcade.draw_rect_filled(arcade.XYWH(w//2, h-40, w, 80), arcade.color.DARK_SLATE_GRAY)
        arcade.draw_rect_filled(arcade.XYWH(w//2, 40, w, 80), arcade.color.DARK_SLATE_GRAY)

        self.title.draw()

        for btn in self.ui_elements:
            btn.draw()

        # --- POPUP ---
        if self.mostrar_popup:
            elapsed = time.time() - self.popup_start_time

            # Cuando pasan los 5 segundos → cerrar
            if elapsed >= self.popup_duration:
                self.mostrar_popup = False
                return

            remaining = max(0, self.popup_duration - elapsed)
            self.popup_timer_text.text = f"Cerrando en {remaining:.1f} s"

            self._draw_popup()

    def _draw_popup(self):
        w, h = self.app.width, self.app.height
        pw, ph = 480, 220
        px = w // 2 - pw // 2
        py = h // 2 - ph // 2

        # Fondo semitransparente
        arcade.draw_rect_filled(
            arcade.XYWH(w//2, h//2, w, h),
            arcade.types.Color(0, 0, 0, 160)
        )

        # Panel central
        arcade.draw_rect_filled(
            arcade.LBWH(px, py, pw, ph),
            arcade.types.Color(40, 40, 70, 245)
        )
        arcade.draw_rect_outline(
            arcade.LBWH(px, py, pw, ph),
            arcade.types.Color(200, 180, 100, 255),
            border_width=3
        )

        # Asegurar posiciones
        self.popup_title_text.x = w // 2
        self.popup_title_text.y = h // 2 + 70

        self.popup_message_text.x = w // 2
        self.popup_message_text.y = h // 2 - 10

        self.popup_timer_text.x = w // 2
        self.popup_timer_text.y = h // 2 - 60

        # Dibujar textos
        self.popup_title_text.draw()
        self.popup_message_text.draw()
        self.popup_timer_text.draw()

    # === INPUT ===

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mostrar_popup:
            return  # Ignora hover
        super().on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.mostrar_popup:
            return  # Ignora clics mientras esté el popup
        super().on_mouse_press(x, y, button, modifiers)

    # === BOTONES ===

    def new_game(self):
        self.app.push_view(CharacterSelectView(self.app))

    def view_characters(self):
        self.app.push_view(CharactersInfoView(self.app))

    def instructions(self):
        self.app.push_view(InstructionsView(self.app))

    def exit_game(self):
        arcade.close_window()

    def on_resize(self, width, height):
        self._setup_ui()
