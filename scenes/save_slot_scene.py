# scenes/save_slot_scene.py
import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel
from sistema_guardado import GestorGuardado, crear_datos_jugador, restaurar_personaje
from personajes import *

class SaveSlotView(BaseView):
    def __init__(self, app, mode='new', character_class=None):
        super().__init__(app)
        self.mode            = mode
        self.character_class = character_class
        self.gestor          = GestorGuardado()
        self.ui_elements     = []
        self.slot_buttons    = []
        self._setup_ui()

    def _setup_ui(self):
        self.ui_elements.clear()
        self.slot_buttons.clear()

        w, h = self.app.width, self.app.height
        self.background_color = (30, 30, 70)

        try:
            self.background = arcade.load_texture('img/fondos/menu.jpg')
        except Exception:
            self.background = None

        # ── Zonas ─────────────────────────────────────────────────────────
        HEADER_H = int(h * 0.12)
        FOOTER_H = int(h * 0.11)
        SLOTS_TOP = h - HEADER_H
        SLOTS_BOT = FOOTER_H
        SLOTS_H   = SLOTS_TOP - SLOTS_BOT

        # ── Título ────────────────────────────────────────────────────────
        titulo   = "SELECCIONAR SLOT" if self.mode == 'new' else "CARGAR PARTIDA"
        title_sz = max(22, int(h * 0.042))
        self.title = RetroLabel(
            titulo, w // 2, h - HEADER_H // 2,
            font_size=title_sz, color=(255, 255, 0),
            anchor_x='center', anchor_y='center'
        )
        self.ui_elements.append(self.title)

        # ── Slots ─────────────────────────────────────────────────────────
        slots     = self.gestor.listar_partidas()
        slot_data = {}
        for s in slots:
            data = self.gestor.cargar_partida(s)
            if data:
                slot_data[s] = data

        N_SLOTS  = 3
        btn_w    = int(min(w * 0.40, 360))
        btn_h    = int(min(SLOTS_H / (N_SLOTS + 1), 130))
        btn_h    = max(btn_h, 70)
        gap_y    = (SLOTS_H - N_SLOTS * btn_h) / (N_SLOTS + 1)

        for slot in range(1, N_SLOTS + 1):
            # Posición vertical distribuida uniformemente
            center_y = int(SLOTS_BOT + gap_y * (N_SLOTS - slot + 1) + btn_h * (N_SLOTS - slot) + btn_h / 2)

            if slot in slot_data:
                data      = slot_data[slot]
                nombre    = data.get('nombre', 'Desconocido')
                nivel     = data.get('nivel', 1)
                timestamp = data.get('_metadata', {}).get('timestamp', '')
                texto     = f"SLOT {slot}  —  {nombre}  (Nivel {nivel})\n{timestamp[:10]}"
                color     = (90, 90, 145)
                hover_c   = (130, 130, 190)
            else:
                texto   = f"SLOT {slot}  —  VACÍO"
                color   = (65, 65, 65)
                hover_c = (100, 100, 100)

            font_sz = max(13, int(h * 0.022))
            btn = ImageButton(
                x=w // 2 - btn_w // 2,
                y=center_y - btn_h // 2,
                width=btn_w, height=btn_h,
                text=texto,
                normal_color=color, hover_color=hover_c,
                callback=lambda s=slot: self.select_slot(s)
            )
            self.ui_elements.append(btn)
            self.slot_buttons.append(btn)

        # ── Botón volver ──────────────────────────────────────────────────
        back_w = int(min(w * 0.22, 210))
        back_h = int(FOOTER_H * 0.55)
        btn_back = ImageButton(
            x=w // 2 - back_w // 2,
            y=(FOOTER_H - back_h) // 2,
            width=back_w, height=back_h,
            text="VOLVER",
            normal_color=(90, 90, 90), hover_color=(130, 130, 130),
            callback=self.back
        )
        self.ui_elements.append(btn_back)

    def select_slot(self, slot):
        if self.mode == 'new':
            if self.character_class:
                personaje = self.character_class()
                datos     = crear_datos_jugador(personaje)
                if self.gestor.guardar_partida(datos, slot):
                    from scenes.combat_scene import CombatView
                    from personajes import Segarro
                    enemigo = Segarro()
                    self.app.push_view(CombatView(self.app, personaje, enemigo))
                else:
                    print("Error al guardar")
        else:
            datos = self.gestor.cargar_partida(slot)
            if datos:
                clase_nombre = datos.get('tipo', '').split()[-1]
                from personajes import __all__ as personajes_list
                personaje = None
                for nombre_clase in personajes_list:
                    if nombre_clase.lower() in clase_nombre.lower():
                        clase     = globals()[nombre_clase]
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
        from scenes.menu_scene import MenuView
        self.app.goto_view(MenuView(self.app))

    def on_draw(self):
        self.clear()
        if self.background:
            arcade.draw_texture_rectangle(
                self.app.width // 2, self.app.height // 2,
                self.app.width, self.app.height, self.background
            )
        else:
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