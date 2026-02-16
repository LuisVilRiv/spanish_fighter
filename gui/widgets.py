import arcade
from arcade import Sprite, Text, color

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
                texture = arcade.load_texture(image_path)
                self.sprite = Sprite(texture, center_x=x + width//2, center_y=y + height//2)
                self.sprite.width = width
                self.sprite.height = height
                self.has_image = True
                self.normal_tint = (255,255,255)
                self.hover_tint = hover_tint
                self.text_label = None
                if text:
                    self.text_label = RetroLabel(text, x + width//2, y + height//2,
                                                 font_size=14, color=arcade.color.WHITE)
            except:
                self.has_image = False
        else:
            self.has_image = False
            self.bg_color = normal_color
            self.border_color = arcade.color.WHITE
            self.text_label = None
            if text:
                self.text_label = RetroLabel(text, x + width//2, y + height//2,
                                             font_size=14, color=arcade.color.WHITE)

    def update(self, x, y):
        if not self.visible:
            return
        self.hovered = (self.x <= x <= self.x + self.width and
                        self.y <= y <= self.y + self.height)

    def draw(self):
        if not self.visible:
            return
        if self.has_image:
            if self.hovered:
                self.sprite.color = self.hover_tint
            else:
                self.sprite.color = self.normal_tint
            self.sprite.draw()
        else:
            color = self.hover_color if self.hovered else self.normal_color
            arcade.draw_rectangle_filled(self.x + self.width//2, self.y + self.height//2,
                                         self.width, self.height, color)
            arcade.draw_rectangle_outline(self.x + self.width//2, self.y + self.height//2,
                                          self.width, self.height, arcade.color.WHITE, 2)
        if self.text_label:
            self.text_label.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.visible and self.hovered and button == arcade.MOUSE_BUTTON_LEFT and self.callback:
            self.callback()

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
        # Fondo
        arcade.draw_rectangle_filled(self.x + self.width//2, self.y + self.height//2,
                                     self.width, self.height, self.color_vacio)
        # Relleno
        fill_width = int(self.width * (self._current_value / self.max_value))
        if fill_width > 0:
            arcade.draw_rectangle_filled(self.x + fill_width//2, self.y + self.height//2,
                                         fill_width, self.height, self.color_lleno)
        # Borde
        arcade.draw_rectangle_outline(self.x + self.width//2, self.y + self.height//2,
                                      self.width, self.height, arcade.color.WHITE, 1)