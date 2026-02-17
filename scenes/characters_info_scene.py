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
        self.sprite_list = arcade.SpriteList()
        self.sprite = None
        self._setup_ui()

    def _setup_ui(self):
        self.ui_elements.clear()
        self.static_elements.clear()
        self.sprite_list.clear()

        w, h = self.app.width, self.app.height
        self.background_color = (30, 35, 50)

        # Botones de navegación fijos en la parte inferior
        BOTTOM_MARGIN = 20
        BTN_H = 45
        BTN_W_NAV = 150
        BTN_W_BACK = 200

        btn_prev = ImageButton(
            x=w // 2 - 200, y=BOTTOM_MARGIN + BTN_H + 10,
            width=BTN_W_NAV, height=BTN_H,
            text="ANTERIOR", normal_color=(100, 100, 120), hover_color=(130, 130, 150),
            callback=self.prev_character
        )
        btn_next = ImageButton(
            x=w // 2 + 50, y=BOTTOM_MARGIN + BTN_H + 10,
            width=BTN_W_NAV, height=BTN_H,
            text="SIGUIENTE", normal_color=(100, 100, 120), hover_color=(130, 130, 150),
            callback=self.next_character
        )
        btn_back = ImageButton(
            x=w // 2 - BTN_W_BACK // 2, y=BOTTOM_MARGIN,
            width=BTN_W_BACK, height=BTN_H - 5,
            text="VOLVER", normal_color=(120, 120, 140), hover_color=(150, 150, 180),
            callback=self.back
        )

        self.btn_prev = btn_prev
        self.btn_next = btn_next
        self.btn_back = btn_back
        self.ui_elements.extend([btn_prev, btn_next, btn_back])

        # La zona de contenido disponible va desde arriba hasta encima de los botones
        self.content_top = h - 30        # margen superior
        self.content_bottom = BOTTOM_MARGIN + BTN_H * 2 + 20  # justo encima de botones

        self._mostrar_personaje()

    def _mostrar_personaje(self):
        botones_fijos = [self.btn_prev, self.btn_next, self.btn_back]
        self.ui_elements = [e for e in self.ui_elements if e in botones_fijos]
        self.static_elements.clear()
        self.sprite_list.clear()

        w, h = self.app.width, self.app.height
        clase_nombre = personajes_list[self.current_index]
        clase = globals()[clase_nombre]
        personaje = clase()
        desc = clase.descripcion()

        # --- Configuración de espaciado ---
        PADDING_TOP = 20        # margen bajo el borde superior
        SPRITE_H = 120          # altura reservada para el sprite (más espacio)
        LINE_NOMBRE = 32
        LINE_TIPO = 22
        LINE_DESC = 38          # altura estimada para la descripción multiline
        LINE_STAT = 22
        LINE_HAB_TITLE = 28
        LINE_HAB = 42           # altura por habilidad

        num_habilidades = len(personaje.habilidades)

        # Calcular altura total necesaria para el contenido
        total_needed = (PADDING_TOP + SPRITE_H + LINE_NOMBRE + LINE_TIPO +
                        LINE_DESC + 10 +
                        5 * LINE_STAT + 15 +
                        LINE_HAB_TITLE +
                        num_habilidades * LINE_HAB + 10)

        content_height = h - self.content_bottom
        # Si el contenido no cabe, reducimos espaciados proporcionalmente
        scale = min(1.0, content_height / max(total_needed, 1))

        def sp(val):
            return int(val * scale)

        # Centrar verticalmente el bloque de contenido en la zona disponible
        slack = max(0, content_height - total_needed)
        y = h - sp(PADDING_TOP) - slack // 2

        # Sprite
        try:
            tex = arcade.load_texture(f'img/personajes/{clase_nombre.lower()}.png')
            sprite_scale = max(0.5, sp(SPRITE_H) / max(tex.height, 1))
            self.sprite = arcade.Sprite(tex, center_x=w // 2,
                                        center_y=y - sp(SPRITE_H) // 2)
            self.sprite.scale = sprite_scale
            self.sprite_list.append(self.sprite)
        except Exception:
            self.sprite = None

        y -= sp(SPRITE_H)

        # Nombre
        self.ui_elements.append(RetroLabel(
            personaje.nombre, w // 2, y,
            font_size=max(14, sp(24)), color=(255, 255, 200)
        ))
        y -= sp(LINE_NOMBRE)

        # Tipo / gamertag
        self.ui_elements.append(RetroLabel(
            personaje.tipo, w // 2, y,
            font_size=max(10, sp(14)), color=(200, 200, 200)
        ))
        y -= sp(LINE_TIPO)

        # Descripción
        self.ui_elements.append(RetroLabel(
            desc, x=w // 2, y=y, width=600, font_size=max(10, sp(13)),
            color=(180, 180, 180), anchor_x='center', multiline=True
        ))
        y -= sp(LINE_DESC) + 10

        # Estadísticas
        stats = [
            f"Vida: {personaje.vida_maxima}",
            f"Ataque: {personaje.ataque_base}",
            f"Defensa: {personaje.defensa_base}",
            f"Velocidad: {personaje.velocidad_base}",
            f"Energía: {personaje.energia_maxima}"
        ]
        for stat in stats:
            self.ui_elements.append(RetroLabel(
                stat, w // 2, y, font_size=max(10, sp(13)),
                color=(200, 200, 150)
            ))
            y -= sp(LINE_STAT)

        y -= 10

        # Habilidades
        self.ui_elements.append(RetroLabel(
            "HABILIDADES:", w // 2, y,
            font_size=max(11, sp(15)), color=(255, 200, 100)
        ))
        y -= sp(LINE_HAB_TITLE)

        for i, hab in enumerate(personaje.habilidades):
            texto = f"{i+1}. {hab.nombre} ({hab.costo_energia}E): {hab.descripcion}"
            self.ui_elements.append(RetroLabel(
                texto, x=w // 2, y=y, width=700, font_size=max(9, sp(11)),
                color=(180, 180, 180), anchor_x='center', multiline=True
            ))
            y -= sp(LINE_HAB)

    def prev_character(self):
        self.current_index = (self.current_index - 1) % len(personajes_list)
        self._mostrar_personaje()

    def next_character(self):
        self.current_index = (self.current_index + 1) % len(personajes_list)
        self._mostrar_personaje()

    def back(self):
        from scenes.menu_scene import MenuView
        self.app.goto_view(MenuView(self.app))

    def on_draw(self):
        self.clear()
        arcade.set_background_color(self.background_color)
        self.sprite_list.draw()
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