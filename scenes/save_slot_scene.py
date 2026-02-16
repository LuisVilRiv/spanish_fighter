import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel
from sistema_guardado import GestorGuardado, crear_datos_jugador, restaurar_personaje, slot_disponible
from personajes import *
import os

class SaveSlotView(BaseView):
    """
    Gestión de slots de guardado. Modo 'new' (crear nueva partida) o 'load' (cargar).
    Si es 'new', se espera que se pase la clase del personaje seleccionado.
    """
    def __init__(self, app, mode='new', character_class=None):
        super().__init__(app)
        self.mode = mode
        self.character_class = character_class
        self.gestor = GestorGuardado()
        self.ui_elements = []
        self.slot_buttons = []
        self._setup_ui()

    def _setup_ui(self):
        w, h = self.app.width, self.app.height
        self.background_color = (30, 30, 70)

        # Fondo con textura si existe
        try:
            self.background = arcade.load_texture('img/fondos/menu.jpg')
        except:
            self.background = None

        # Título
        titulo = "SELECCIONAR SLOT" if self.mode == 'new' else "CARGAR PARTIDA"
        self.title = RetroLabel(titulo, w//2, h-70, font_size=32,
                                color=(255, 255, 0))
        self.ui_elements.append(self.title)

        # Cargar info de slots existentes
        slots = self.gestor.listar_partidas()
        slot_data = {}
        for s in slots:
            data = self.gestor.cargar_partida(s)
            if data:
                slot_data[s] = data

        # Crear botones para slots 1,2,3
        btn_width = 300
        btn_height = 150
        spacing_y = 180
        start_y = h//2 + 50

        for slot in range(1, 4):
            y = start_y - (slot-1) * spacing_y
            if slot in slot_data:
                data = slot_data[slot]
                nombre = data.get('nombre', 'Desconocido')
                nivel = data.get('nivel', 1)
                timestamp = data.get('_metadata', {}).get('timestamp', '')
                texto = f"SLOT {slot}\n{nombre}\nNivel {nivel}\n{timestamp[:10]}"
                color = (100, 100, 150)
                hover_color = (150, 150, 200)
            else:
                texto = f"SLOT {slot}\nVACÍO"
                color = (80, 80, 80)
                hover_color = (120, 120, 120)

            btn = ImageButton(
                x=w//2 - btn_width//2, y=y - btn_height//2,
                width=btn_width, height=btn_height,
                text=texto, normal_color=color, hover_color=hover_color,
                callback=lambda s=slot: self.select_slot(s)
            )
            self.ui_elements.append(btn)
            self.slot_buttons.append(btn)

        # Botón volver
        btn_back = ImageButton(
            x=w//2 - 100, y=80, width=200, height=50,
            text="VOLVER", normal_color=(100, 100, 100), hover_color=(150, 150, 150),
            callback=self.back
        )
        self.ui_elements.append(btn_back)

    def select_slot(self, slot):
        if self.mode == 'new':
            if self.character_class:
                personaje = self.character_class()
                datos = crear_datos_jugador(personaje)
                if self.gestor.guardar_partida(datos, slot):
                    # Ir a combate con ese personaje (enemigo de prueba)
                    from scenes.combat_scene import CombatView
                    from personajes import Segarro
                    enemigo = Segarro()
                    self.app.push_view(CombatView(self.app, personaje, enemigo))
                else:
                    print("Error al guardar")
        else:  # load
            datos = self.gestor.cargar_partida(slot)
            if datos:
                # Reconstruir personaje
                clase_nombre = datos.get('tipo', '').split()[-1]  # truco simple
                from personajes import __all__ as personajes_list
                personaje = None
                for nombre_clase in personajes_list:
                    if nombre_clase.lower() in clase_nombre.lower():
                        clase = globals()[nombre_clase]
                        personaje = clase()
                        restaurar_personaje(personaje, datos)
                        break
                if personaje is None:
                    print("Clase no encontrada")
                    return
                from scenes.combat_scene import CombatView
                from personajes import Segarro
                enemigo = Segarro()
                self.app.push_view(CombatView(self.app, personaje, enemigo))
            else:
                print("No se pudo cargar la partida")

    def back(self):
        self.app.pop_view()

    def on_draw(self):
        self.clear()
        if self.background:
            arcade.draw_texture_rectangle(self.app.width//2, self.app.height//2,
                                          self.app.width, self.app.height, self.background)
        else:
            arcade.set_background_color(self.background_color)

        for elem in self.ui_elements:
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