import arcade
from arcade import Text, color


class RetroLabel(Text):
    def __init__(self, text, x, y, font_size=14, color=arcade.color.WHITE,
                 anchor_x='center', anchor_y='center', **kwargs):
        super().__init__(text, x, y, color, font_size,
                         anchor_x=anchor_x, anchor_y=anchor_y, **kwargs)


class ImageButton:
    """
    Botón con texto y/o imagen.

    Anti-propagación garantizada:
    - on_mouse_press devuelve True SOLO si visible Y hit Y botón izquierdo.
    - Si no es visible devuelve False sin ejecutar callback.
    - El callback NO se llama si el botón no debería responder.
    """

    def __init__(self, x, y, width, height, text=None, image_path=None,
                 normal_color=(100, 120, 140), hover_color=(140, 160, 180),
                 hover_tint=(220, 220, 220), callback=None):
        self.x = x
        self.y = y
        self.width  = width
        self.height = height
        self.callback = callback
        self.hovered  = False
        self.text     = text
        self.normal_color = normal_color
        self.hover_color  = hover_color
        self.visible  = True

        # ── Imagen opcional ─────────────────────────────────────────────────
        if image_path:
            try:
                self.texture = arcade.load_texture(image_path)
                self.has_image = True
                self.normal_tint = arcade.types.Color(255, 255, 255, 255)
                _ht = hover_tint
                self.hover_tint = arcade.types.Color(
                    _ht[0], _ht[1], _ht[2], _ht[3] if len(_ht) > 3 else 255
                )
            except Exception:
                self.has_image = False
                self.texture   = None
        else:
            self.has_image = False
            self.texture   = None

        # ── Etiqueta de texto con tamaño dinámico ───────────────────────────
        if text:
            fs = self._calc_font_size(text, width, height)
            self.text_label = RetroLabel(
                text,
                x + width  // 2,
                y + height // 2,
                font_size=fs,
                color=arcade.color.WHITE,
                multiline=True,
                width=width - 6,
                anchor_x='center',
                anchor_y='center',
            )
        else:
            self.text_label = None

    # ── Helpers ─────────────────────────────────────────────────────────────

    @staticmethod
    def _calc_font_size(text: str, width: int, height: int) -> int:
        """
        Tamaño de fuente adaptativo según el área disponible del botón.
        Líneas largas o botones pequeños → fuente más chica.
        """
        lineas = text.split('\n')
        max_chars = max(len(l) for l in lineas)
        n_lineas  = len(lineas)

        # Base proporcional al alto del botón (aprox 1 línea ≈ 1.4 * font_size px)
        fs_por_alto = max(7, int(height / (n_lineas * 1.65)))
        # Base proporcional al ancho (ancho disponible / chars)
        fs_por_ancho = max(7, int((width - 8) / max(max_chars * 0.65, 1)))

        return min(fs_por_alto, fs_por_ancho, 18)

    def _hit(self, x: int, y: int) -> bool:
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)

    # ── Interfaz pública ────────────────────────────────────────────────────

    def update(self, x: int, y: int):
        if not self.visible:
            self.hovered = False
            return
        self.hovered = self._hit(x, y)

    def draw(self):
        if not self.visible:
            return

        cx = self.x + self.width  // 2
        cy = self.y + self.height // 2

        if self.has_image and self.texture:
            tint = self.hover_tint if self.hovered else self.normal_tint
            arcade.draw_texture_rect(
                self.texture,
                arcade.LRBT(self.x, self.x + self.width, self.y, self.y + self.height),
                color=tint
            )
        else:
            color_rect = self.hover_color if self.hovered else self.normal_color
            arcade.draw_rect_filled(arcade.XYWH(cx, cy, self.width, self.height), color_rect)

            # Borde más grueso en hover para feedback visual claro
            border_w = 3 if self.hovered else 2
            border_c = (255, 255, 255) if self.hovered else (180, 180, 200)
            arcade.draw_rect_outline(arcade.XYWH(cx, cy, self.width, self.height),
                                     border_c, border_w)

        if self.text_label:
            self.text_label.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool:
        """
        Devuelve True si el click ha sido consumido por este botón.
        NUNCA devuelve True si el botón no es visible.
        NUNCA devuelve True si el botón izquierdo no fue el pulsado.
        """
        if not self.visible:
            return False          # refuerzo 1: invisible = no consume
        if button != arcade.MOUSE_BUTTON_LEFT:
            return False          # refuerzo 2: solo botón izquierdo
        if not self._hit(x, y):
            return False          # refuerzo 3: fuera del área
        if self.callback:
            self.callback()
        return True               # consumido: detiene propagación

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.update(x, y)


# ───────────────────────────────────────────────────────────────────────────
class HealthBar:
    """
    Barra de vida/energía con etiqueta numérica opcional y color dinámico.

    Parámetros nuevos:
        mostrar_texto : bool  — muestra "actual / max" encima de la barra
        texto_color   : tuple — color del texto
        label_offset  : int   — desplazamiento Y del texto respecto al centro
    """

    def __init__(self, x, y, width, height, max_value, current_value,
                 color_lleno=(100, 200, 100), color_vacio=(60, 60, 60),
                 mostrar_texto: bool = True,
                 texto_color: tuple = (220, 220, 220),
                 label_offset: int = 0):
        self.x = x
        self.y = y
        self.width  = width
        self.height = height
        self.max_value      = max(1, max_value)      # evitar división por cero
        self._current_value = current_value
        self.color_lleno = color_lleno
        self.color_vacio = color_vacio
        self.mostrar_texto = mostrar_texto
        self.texto_color   = texto_color
        self.label_offset  = label_offset

        self._fs = max(7, min(int(height * 0.85), 13))

    @property
    def current_value(self):
        return self._current_value

    @current_value.setter
    def current_value(self, value):
        self._current_value = max(0, min(self.max_value, value))

    def draw(self):
        cx = self.x + self.width  // 2
        cy = self.y + self.height // 2

        # Fondo
        arcade.draw_rect_filled(arcade.XYWH(cx, cy, self.width, self.height),
                                self.color_vacio)

        # Relleno proporcional con color dinámico
        ratio  = self._current_value / self.max_value
        fill_w = int(self.width * ratio)
        if fill_w > 0:
            fill_color = _elegir_color_lleno(self.color_lleno, ratio)
            arcade.draw_rect_filled(
                arcade.XYWH(self.x + fill_w // 2, cy, fill_w, self.height),
                fill_color
            )

        # Borde
        arcade.draw_rect_outline(arcade.XYWH(cx, cy, self.width, self.height),
                                 arcade.color.WHITE, 1)

        # Texto numérico (solo si la barra es suficientemente alta)
        if self.mostrar_texto and self.height >= 12:
            label = f"{int(self._current_value)}/{int(self.max_value)}"
            arcade.draw_text(
                label,
                cx, cy + self.label_offset,
                self.texto_color,
                font_size=self._fs,
                anchor_x='center', anchor_y='center',
            )


def _elegir_color_lleno(color_base: tuple, ratio: float) -> tuple:
    """
    Para barras de vida (tonos verdes/rojos) aplica degradado según porcentaje.
    Para barras de energía (azules/naranjas) mantiene el color base.
    """
    r, g, b = color_base[0], color_base[1], color_base[2]

    # Detectar si es una barra de vida (componente verde o rojo dominante, azul bajo)
    es_vida_jugador = (g > 150 and b < 130)   # verde alto
    es_vida_enemigo = (r > 150 and g < 130)   # rojo alto

    if es_vida_jugador:
        if ratio > 0.6:
            return (50, 200, 70)
        elif ratio > 0.3:
            return (220, 180, 30)
        else:
            return (220, 55, 55)

    if es_vida_enemigo:
        if ratio > 0.6:
            return (200, 70, 70)
        elif ratio > 0.3:
            return (220, 100, 35)
        else:
            return (240, 35, 35)

    # Energía u otras barras → color base sin modificar
    return color_base


# ───────────────────────────────────────────────────────────────────────────
class EstadoTag:
    """
    Etiqueta flotante que muestra estados especiales sobre un personaje
    (MUERTO, DEFENDIENDO, CONCENTRADO, etc.).
    Se instancia y .draw() se llama desde on_draw de la escena.
    """

    ESTADOS = {
        'muerto':      ((200,  50,  50), "✗ KO"),
        'defendiendo': (( 80, 120, 200), "🛡 DEF"),
        'concentrado': (( 80, 200,  80), "⬆ CONC"),
        'stunned':     ((200, 200,  50), "⚡ STUN"),
    }

    def __init__(self, cx: int, cy: int, estado: str, font_size: int = 11):
        col, txt = self.ESTADOS.get(estado, ((180, 180, 180), estado))
        self._cx  = cx
        self._cy  = cy
        self._col = col
        self._txt = txt
        self._fs  = font_size
        self._pad = 4
        self._w   = max(40, len(txt) * int(font_size * 0.7) + self._pad * 2)
        self._h   = int(font_size * 1.7)

    def draw(self):
        x0 = self._cx - self._w // 2
        y0 = self._cy - self._h // 2
        arcade.draw_rect_filled(arcade.LBWH(x0, y0, self._w, self._h),
                                (*self._col, 200))
        arcade.draw_rect_outline(arcade.LBWH(x0, y0, self._w, self._h),
                                 (255, 255, 255, 120), 1)
        arcade.draw_text(self._txt, self._cx, self._cy, (255, 255, 255),
                         font_size=self._fs, anchor_x='center', anchor_y='center')