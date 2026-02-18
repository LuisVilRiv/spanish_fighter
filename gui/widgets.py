import arcade
from arcade import Text, color

class RetroLabel(Text):
    def __init__(self, text, x, y, font_size=14, color=arcade.color.WHITE,
                 anchor_x='center', anchor_y='center', **kwargs):
        super().__init__(text, x, y, color, font_size,
                         anchor_x=anchor_x, anchor_y=anchor_y, **kwargs)


class ImageButton:
    def __init__(self, x, y, width, height, text=None, image_path=None,
                 normal_color=(100,120,140), hover_color=(140,160,180),
                 hover_tint=(220,220,220), callback=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback
        self.hovered = False
        self.text = text
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.visible = True

        if image_path:
            try:
                self.texture = arcade.load_texture(image_path)
                self.has_image = True
                self.normal_tint = arcade.types.Color(255, 255, 255, 255)
                _ht = hover_tint
                self.hover_tint = arcade.types.Color(
                    _ht[0], _ht[1], _ht[2], _ht[3] if len(_ht) > 3 else 255
                )
            except:
                self.has_image = False
                self.texture = None
        else:
            self.has_image = False
            self.texture = None

        if text:
            self.text_label = RetroLabel(
                text,
                x + width//2,
                y + height//2,
                font_size=14,
                color=arcade.color.WHITE
            )
        else:
            self.text_label = None

    def update(self, x, y):
        # Si no es visible, nunca puede estar en hover
        if not self.visible:
            self.hovered = False
            return
        self.hovered = (
            self.x <= x <= self.x + self.width and
            self.y <= y <= self.y + self.height
        )

    def draw(self):
        if not self.visible:
            return

        cx = self.x + self.width // 2
        cy = self.y + self.height // 2

        if self.has_image and self.texture:
            tint_color = self.hover_tint if self.hovered else self.normal_tint
            arcade.draw_texture_rect(
                self.texture,
                arcade.LRBT(self.x, self.x + self.width, self.y, self.y + self.height),
                color=tint_color
            )
        else:
            color_rect = self.hover_color if self.hovered else self.normal_color
            arcade.draw_rect_filled(arcade.XYWH(
                cx, cy, self.width, self.height), color_rect
            )
            arcade.draw_rect_outline(arcade.XYWH(
                cx, cy, self.width, self.height), arcade.color.WHITE, 2
            )

        if self.text_label:
            self.text_label.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.visible:
            return False
        # Usar coordenadas del clic directamente, sin depender de hovered,
        # para que funcione aunque el ratón no se haya movido previamente.
        clicked = (self.x <= x <= self.x + self.width and
                   self.y <= y <= self.y + self.height)
        if clicked and button == arcade.MOUSE_BUTTON_LEFT and self.callback:
            self.callback()
            return True  # consumido: detener propagación
        return False

    def on_mouse_motion(self, x, y, dx, dy):
        self.update(x, y)


class HealthBar:
    def __init__(self, x, y, width, height, max_value, current_value,
                 color_lleno=(100,200,100), color_vacio=(60,60,60)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_value = max_value
        self._current_value = current_value
        self.color_lleno = color_lleno
        self.color_vacio = color_vacio

    @property
    def current_value(self):
        return self._current_value

    @current_value.setter
    def current_value(self, value):
        self._current_value = max(0, min(self.max_value, value))

    def draw(self):
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2

        # Fondo
        arcade.draw_rect_filled(arcade.XYWH(
            cx, cy, self.width, self.height), self.color_vacio
        )

        # Relleno proporcional
        fill_width = int(self.width * (self._current_value / self.max_value))
        if fill_width > 0:
            arcade.draw_rect_filled(arcade.XYWH(
                self.x + fill_width // 2, cy, fill_width, self.height), self.color_lleno
            )

        # Borde
        arcade.draw_rect_outline(arcade.XYWH(
            cx, cy, self.width, self.height), arcade.color.WHITE, 1
        )