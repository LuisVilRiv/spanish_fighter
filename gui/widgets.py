import pyglet
from pyglet import sprite

class ImageButton:
    def __init__(self, x, y, image_path, hover_tint=(200,200,200), callback=None, batch=None):
        self.x = x
        self.y = y
        self.callback = callback
        self.batch = batch or pyglet.graphics.Batch()
        self.hovered = False
        self.hover_tint = hover_tint

        try:
            self.image = pyglet.image.load(image_path)
            self.sprite = pyglet.sprite.Sprite(self.image, x=x, y=y, batch=self.batch)
            self.width = self.image.width
            self.height = self.image.height
            self.original_color = self.sprite.color
            self.has_image = True
        except:
            # Fallback: rectángulo de color
            self.width = 200
            self.height = 60
            self.rect = pyglet.shapes.Rectangle(x, y, self.width, self.height, color=(100,100,100), batch=self.batch)
            self.label = pyglet.text.Label("?", x=x+self.width//2, y=y+self.height//2, anchor_x='center', anchor_y='center', batch=self.batch)
            self.has_image = False

    def update(self, x, y):
        self.hovered = (self.x <= x <= self.x + self.width and
                        self.y <= y <= self.y + self.height)
        if self.has_image:
            if self.hovered:
                self.sprite.color = self.hover_tint
            else:
                self.sprite.color = self.original_color
        else:
            if self.hovered:
                self.rect.color = (150,150,150)
            else:
                self.rect.color = (100,100,100)

    def on_mouse_press(self, x, y, button):
        if self.hovered and button == pyglet.window.mouse.LEFT and self.callback:
            self.callback()

    def draw(self):
        self.batch.draw()