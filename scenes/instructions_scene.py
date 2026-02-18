import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel

class InstructionsView(BaseView):
    """
    Muestra las instrucciones básicas del juego.
    """
    def __init__(self, app):
        super().__init__(app)
        self.ui_elements = []
        self._setup_ui()

    def _setup_ui(self):
        w, h = self.app.width, self.app.height
        self.background_color = (30, 35, 50)

        self.title = RetroLabel("INSTRUCCIONES", w//2, h-50, font_size=32,
                                color=(255, 220, 150))
        self.ui_elements.append(self.title)

        texto = """
Bienvenido a Batalla Cómica Española.

Es un juego de combate por turnos entre personajes surrealistas españoles.

- En tu turno, puedes elegir entre ATAQUE, DEFENDER, CONCENTRAR o HABILIDAD.
- ATAQUE: Golpe básico.
- DEFENDER: Reduce el daño recibido en el próximo turno.
- CONCENTRAR: Recupera energía.
- HABILIDAD: Usa una habilidad especial (cada personaje tiene 6).

Gana el que reduzca la vida del oponente a cero.

¡Que gane el más español!
        """

        self.instructions_label = RetroLabel(
            texto, x=w//2, y=h-200, width=700, font_size=16,
            color=(200, 200, 200), anchor_x='center', multiline=True
        )
        self.ui_elements.append(self.instructions_label)

        btn_back = ImageButton(
            x=w//2 - 100, y=80, width=200, height=50,
            text="VOLVER", normal_color=(120, 120, 140), hover_color=(150, 150, 180),
            callback=self.back
        )
        self.ui_elements.append(btn_back)

    def back(self):
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
        super().on_mouse_press(x, y, button, modifiers)

    def on_resize(self, width, height):
        self._setup_ui()