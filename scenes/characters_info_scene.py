import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel
from personajes import __all__ as personajes_list
from personajes import *

class CharactersInfoView(BaseView):
    """
    Muestra información detallada de cada personaje: estadísticas, descripción y habilidades.
    Permite navegar entre personajes con botones anterior/siguiente.
    """
    def __init__(self, app):
        super().__init__(app)
        self.current_index = 0
        self.ui_elements = []
        self.static_elements = []
        self.sprite = None
        self._setup_ui()

    def _setup_ui(self):
        w, h = self.app.width, self.app.height
        self.background_color = (30, 35, 50)

        # Título
        self.title = RetroLabel("PERSONAJES", w//2, h-50, font_size=32,
                                color=(255, 220, 150))
        self.ui_elements.append(self.title)

        # Botones anterior/siguiente
        btn_prev = ImageButton(
            x=w//2 - 200, y=80, width=150, height=50,
            text="ANTERIOR", normal_color=(100, 100, 120), hover_color=(130, 130, 150),
            callback=self.prev_character
        )
        btn_next = ImageButton(
            x=w//2 + 50, y=80, width=150, height=50,
            text="SIGUIENTE", normal_color=(100, 100, 120), hover_color=(130, 130, 150),
            callback=self.next_character
        )
        btn_back = ImageButton(
            x=w//2 - 100, y=20, width=200, height=40,
            text="VOLVER", normal_color=(120, 120, 140), hover_color=(150, 150, 180),
            callback=self.back
        )
        self.ui_elements.extend([btn_prev, btn_next, btn_back])

        self._mostrar_personaje()

    def _mostrar_personaje(self):
        # Eliminar elementos antiguos (excepto los botones fijos)
        # Pero como regeneramos todo, mejor reconstruir la lista manteniendo botones.
        # Guardamos los botones fijos
        botones_fijos = [elem for elem in self.ui_elements if isinstance(elem, ImageButton)]
        self.ui_elements = botones_fijos
        self.static_elements = []

        w, h = self.app.width, self.app.height
        clase_nombre = personajes_list[self.current_index]
        clase = globals()[clase_nombre]
        personaje = clase()
        desc = clase.descripcion()

        # Sprite
        try:
            tex = arcade.load_texture(f'img/personajes/{clase_nombre.lower()}.png')
            self.sprite = arcade.Sprite(tex, center_x=w//2, center_y=h-250)
            self.sprite.scale = 2.0
        except:
            self.sprite = None

        # Nombre
        self.nombre_label = RetroLabel(personaje.nombre, w//2, h-180,
                                       font_size=24, color=(255, 255, 200))
        self.ui_elements.append(self.nombre_label)

        # Tipo
        self.tipo_label = RetroLabel(personaje.tipo, w//2, h-220,
                                     font_size=16, color=(200, 200, 200))
        self.ui_elements.append(self.tipo_label)

        # Descripción (multilínea)
        self.desc_label = RetroLabel(
            desc, x=w//2, y=h-280, width=600, font_size=14,
            color=(180, 180, 180), anchor_x='center', multiline=True
        )
        self.ui_elements.append(self.desc_label)

        # Estadísticas
        stats = [
            f"Vida: {personaje.vida_maxima}",
            f"Ataque: {personaje.ataque_base}",
            f"Defensa: {personaje.defensa_base}",
            f"Velocidad: {personaje.velocidad_base}",
            f"Energía: {personaje.energia_maxima}"
        ]
        y_stat = h - 320
        for stat in stats:
            lbl = RetroLabel(stat, w//2, y_stat, font_size=14,
                            color=(200, 200, 150))
            self.ui_elements.append(lbl)
            y_stat -= 25

        # Habilidades
        y_habilidad = h - 480
        self.habilidades_titulo = RetroLabel("HABILIDADES:", w//2, y_habilidad,
                                             font_size=16, color=(255, 200, 100))
        self.ui_elements.append(self.habilidades_titulo)
        y_habilidad -= 25

        for i, habilidad in enumerate(personaje.habilidades):
            texto = f"{i+1}. {habilidad.nombre} ({habilidad.costo_energia}E): {habilidad.descripcion}"
            # Dividir en líneas si es muy largo
            # Arcade no soporta word wrap directamente, así que usamos RetroLabel con width y multiline
            lbl = RetroLabel(
                texto, x=w//2, y=y_habilidad, width=700, font_size=12,
                color=(180, 180, 180), anchor_x='center', multiline=True
            )
            self.ui_elements.append(lbl)
            y_habilidad -= 40  # espacio para líneas adicionales

    def prev_character(self):
        self.current_index = (self.current_index - 1) % len(personajes_list)
        self._mostrar_personaje()

    def next_character(self):
        self.current_index = (self.current_index + 1) % len(personajes_list)
        self._mostrar_personaje()

    def back(self):
        self.app.pop_view()

    def on_draw(self):
        self.clear()
        arcade.set_background_color(self.background_color)

        # Dibujar sprite
        if self.sprite:
            self.sprite.draw()

        # Dibujar todos los elementos UI
        for elem in self.ui_elements:
            if hasattr(elem, 'draw'):
                elem.draw()
        for elem in self.static_elements:
            if hasattr(elem, 'draw'):
                elem.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)
        for btn in self.ui_elements:
            if hasattr(btn, 'on_mouse_motion'):
                btn.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)

    def on_resize(self, width, height):
        self._setup_ui()