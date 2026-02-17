import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel, HealthBar
from combate.sistema_combate import Combate, Accion, EstadoCombate
from scenes.historial_scene import HistorialView

class CombatView(BaseView):
    def __init__(self, app, jugador, enemigo):
        super().__init__(app)
        self.jugador = jugador
        self.enemigo = enemigo
        self.jugador_clase = type(jugador)
        self.enemigo_clase = type(enemigo)
        self.combate = Combate(jugador, enemigo)
        self.ui_elements = []
        self.habilidad_buttons = []
        self.postcombate_buttons = []
        self.mostrando_habilidades = False
        self.turno_jugador = True
        self.ia_timer = 0
        self.resultado_turno = None
        self._setup_ui()

    def _setup_ui(self):
        # Limpiar listas anteriores
        self.ui_elements = []
        self.habilidad_buttons = []
        self.postcombate_buttons = []
        self.static_elements = []
        self.sprite_list = arcade.SpriteList()

        w, h = self.app.width, self.app.height
        self.background_color = (30, 35, 50)

        # Sprites de personajes
        sprite_size = 120
        self.jugador_x = int(w * 0.2)
        self.enemigo_x = int(w * 0.8) - sprite_size
        y_combat = h // 2

        try:
            tex = arcade.load_texture(f'img/personajes/{type(self.jugador).__name__.lower()}.png')
            self.sprite_jugador = arcade.Sprite(tex)
            self.sprite_jugador.center_x = self.jugador_x + sprite_size // 2
            self.sprite_jugador.center_y = y_combat + sprite_size // 2
            self.sprite_jugador.width = sprite_size
            self.sprite_jugador.height = sprite_size
            self.sprite_list.append(self.sprite_jugador)
        except:
            self.sprite_jugador = None

        try:
            tex = arcade.load_texture(f'img/personajes/{type(self.enemigo).__name__.lower()}.png')
            self.sprite_enemigo = arcade.Sprite(tex)
            self.sprite_enemigo.center_x = self.enemigo_x + sprite_size // 2
            self.sprite_enemigo.center_y = y_combat + sprite_size // 2
            self.sprite_enemigo.width = sprite_size
            self.sprite_enemigo.height = sprite_size
            self.sprite_list.append(self.sprite_enemigo)
        except:
            self.sprite_enemigo = None

        # Nombres
        self.lbl_jugador = RetroLabel(self.jugador.nombre,
                                      x=self.jugador_x + sprite_size//2,
                                      y=y_combat + sprite_size + 10,
                                      font_size=16, anchor_x='center')
        self.lbl_enemigo = RetroLabel(self.enemigo.nombre,
                                      x=self.enemigo_x + sprite_size//2,
                                      y=y_combat + sprite_size + 10,
                                      font_size=16, anchor_x='center')
        self.ui_elements.extend([self.lbl_jugador, self.lbl_enemigo])

        # Barras de vida y energía
        bar_w, bar_h = 220, 20
        self.vida_bar_j = HealthBar(
            x=self.jugador_x - 10, y=y_combat - 40, width=bar_w, height=bar_h,
            max_value=self.jugador.vida_maxima, current_value=self.jugador.vida_actual,
            color_lleno=(100, 200, 100)
        )
        self.vida_bar_e = HealthBar(
            x=self.enemigo_x - 10, y=y_combat - 40, width=bar_w, height=bar_h,
            max_value=self.enemigo.vida_maxima, current_value=self.enemigo.vida_actual,
            color_lleno=(200, 100, 100)
        )
        self.energia_bar_j = HealthBar(
            x=self.jugador_x - 10, y=y_combat - 65, width=bar_w, height=10,
            max_value=self.jugador.energia_maxima, current_value=self.jugador.energia_actual,
            color_lleno=(100, 150, 200)
        )
        self.energia_bar_e = HealthBar(
            x=self.enemigo_x - 10, y=y_combat - 65, width=bar_w, height=10,
            max_value=self.enemigo.energia_maxima, current_value=self.enemigo.energia_actual,
            color_lleno=(200, 150, 100)
        )
        self.static_elements = [self.vida_bar_j, self.vida_bar_e,
                                self.energia_bar_j, self.energia_bar_e]

        # Indicador de turno
        self.turn_indicator = RetroLabel(
            "TU TURNO" if self.turno_jugador else "TURNO DEL RIVAL",
            x=w//2, y=h-100, font_size=24,
            color=(255, 255, 100) if self.turno_jugador else (200, 200, 200)
        )
        self.ui_elements.append(self.turn_indicator)

        # Botones principales
        btn_y = 80
        btn_spacing = 230
        start_x = (w - 3*btn_spacing)//2

        self.btn_ataque = ImageButton(
            x=start_x, y=btn_y, width=200, height=60,
            text="ATAQUE", normal_color=(140, 90, 90), hover_color=(180, 120, 120),
            callback=self.ataque_basico
        )
        self.btn_defender = ImageButton(
            x=start_x + btn_spacing, y=btn_y, width=200, height=60,
            text="DEFENDER", normal_color=(90, 90, 140), hover_color=(120, 120, 180),
            callback=self.defender
        )
        self.btn_concentrar = ImageButton(
            x=start_x + 2*btn_spacing, y=btn_y, width=200, height=60,
            text="CONCENTRAR", normal_color=(90, 140, 90), hover_color=(120, 180, 120),
            callback=self.concentrar
        )
        self.btn_habilidad = ImageButton(
            x=start_x + 3*btn_spacing, y=btn_y, width=200, height=60,
            text="HABILIDAD", normal_color=(140, 140, 90), hover_color=(180, 180, 120),
            callback=self.mostrar_habilidades
        )
        self.ui_elements.extend([self.btn_ataque, self.btn_defender,
                                 self.btn_concentrar, self.btn_habilidad])

        # Botones de habilidades
        self._crear_botones_habilidad()

        # Botones postcombate (inicialmente invisibles)
        self.btn_revancha = ImageButton(
            x=w//2 - 300, y=btn_y, width=200, height=50,
            text="REVANCHA", normal_color=(0, 150, 0), hover_color=(0, 200, 0),
            callback=self.revancha
        )
        self.btn_historial = ImageButton(
            x=w//2 - 50, y=btn_y, width=200, height=50,
            text="HISTORIAL", normal_color=(150, 150, 0), hover_color=(200, 200, 0),
            callback=self.ver_historial
        )
        self.btn_menu = ImageButton(
            x=w//2 + 200, y=btn_y, width=200, height=50,
            text="MENÚ", normal_color=(150, 0, 0), hover_color=(200, 0, 0),
            callback=self.volver_menu
        )
        self.postcombate_buttons = [self.btn_revancha, self.btn_historial, self.btn_menu]
        for btn in self.postcombate_buttons:
            btn.visible = False
            self.ui_elements.append(btn)

        # Área de mensajes
        msg_y = btn_y + 90
        msg_height = 100
        self.msg_rect = (50, msg_y, w-100, msg_height)
        self.lbl_mensaje = RetroLabel(
            "Bienvenido al combate!",
            x=60, y=msg_y + msg_height - 20, width=w-120,
            font_size=14, anchor_x='left', anchor_y='top',
            multiline=True
        )
        self.ui_elements.append(self.lbl_mensaje)

        self._actualizar_visibilidad()

    def _crear_botones_habilidad(self):
        w = self.app.width
        if not self.jugador.habilidades:
            return
        num_hab = len(self.jugador.habilidades)
        hab_btn_w = 150
        hab_btn_h = 50
        total_w = num_hab * (hab_btn_w + 10) - 10
        start_x_hab = (w - total_w)//2
        hab_y = 80 + 70

        for i, habilidad in enumerate(self.jugador.habilidades):
            btn = ImageButton(
                x=start_x_hab + i*(hab_btn_w+10), y=hab_y,
                width=hab_btn_w, height=hab_btn_h,
                text=habilidad.nombre, normal_color=(100, 100, 150),
                hover_color=(130, 130, 180),
                callback=lambda idx=i: self.usar_habilidad_idx(idx)
            )
            self.habilidad_buttons.append(btn)

        btn_cancel = ImageButton(
            x=w//2-75, y=hab_y-60, width=150, height=40,
            text="CANCELAR", normal_color=(150, 80, 80), hover_color=(180, 100, 100),
            callback=self.ocultar_habilidades
        )
        self.habilidad_buttons.append(btn_cancel)

    def _actualizar_visibilidad(self):
        visible_principales = self.turno_jugador and not self.mostrando_habilidades
        for btn in [self.btn_ataque, self.btn_defender, self.btn_concentrar, self.btn_habilidad]:
            btn.visible = visible_principales
        for btn in self.habilidad_buttons:
            btn.visible = self.turno_jugador and self.mostrando_habilidades

    def mostrar_habilidades(self):
        self.mostrando_habilidades = True
        self._actualizar_visibilidad()

    def ocultar_habilidades(self):
        self.mostrando_habilidades = False
        self._actualizar_visibilidad()

    def usar_habilidad_idx(self, idx):
        if self.combate.estado != EstadoCombate.EN_CURSO or not self.turno_jugador:
            return
        habilidad = self.jugador.habilidades[idx]
        if self.jugador.energia_actual >= habilidad.costo_energia:
            self.resultado_turno = self.combate.ejecutar_turno(Accion.HABILIDAD_ESPECIAL, idx)
            self.turno_jugador = False
            self.mostrando_habilidades = False
            self._actualizar_ui()
            self.ia_timer = 1.0
        else:
            self.lbl_mensaje.text = "Energía insuficiente"

    def ataque_basico(self):
        if self.combate.estado != EstadoCombate.EN_CURSO or not self.turno_jugador:
            return
        self.resultado_turno = self.combate.ejecutar_turno(Accion.ATAQUE_BASICO)
        self.turno_jugador = False
        self._actualizar_ui()
        self.ia_timer = 1.0

    def defender(self):
        if self.combate.estado != EstadoCombate.EN_CURSO or not self.turno_jugador:
            return
        self.resultado_turno = self.combate.ejecutar_turno(Accion.DEFENDER)
        self.turno_jugador = False
        self._actualizar_ui()
        self.ia_timer = 1.0

    def concentrar(self):
        if self.combate.estado != EstadoCombate.EN_CURSO or not self.turno_jugador:
            return
        self.resultado_turno = self.combate.ejecutar_turno(Accion.CONCENTRAR)
        self.turno_jugador = False
        self._actualizar_ui()
        self.ia_timer = 1.0

    def on_update(self, delta_time):
        if self.ia_timer > 0:
            self.ia_timer -= delta_time
            if self.ia_timer <= 0 and not self.turno_jugador and self.combate.estado == EstadoCombate.EN_CURSO:
                self.resultado_turno = self.combate.ejecutar_turno_ia()
                self.turno_jugador = True
                self._actualizar_ui()
                self.ia_timer = 0

    def _actualizar_ui(self):
        self.vida_bar_j.current_value = self.jugador.vida_actual
        self.vida_bar_e.current_value = self.enemigo.vida_actual
        self.energia_bar_j.current_value = self.jugador.energia_actual
        self.energia_bar_e.current_value = self.enemigo.energia_actual
        self.turn_indicator.text = "TU TURNO" if self.turno_jugador else "TURNO DEL RIVAL"
        self.turn_indicator.color = (255, 255, 100) if self.turno_jugador else (200, 200, 200)

        if self.resultado_turno:
            mensajes = []
            if self.resultado_turno.jugador_accion:
                mensajes.append(self.resultado_turno.jugador_accion)
            if self.resultado_turno.ia_accion:
                mensajes.append(self.resultado_turno.ia_accion)
            if self.resultado_turno.daño_jugador_a_ia:
                mensajes.append(f"Daño a enemigo: {self.resultado_turno.daño_jugador_a_ia}")
            if self.resultado_turno.daño_ia_a_jugador:
                mensajes.append(f"Daño recibido: {self.resultado_turno.daño_ia_a_jugador}")
            if self.resultado_turno.evento_aleatorio:
                mensajes.append(self.resultado_turno.evento_aleatorio.get('mensaje', ''))
            self.lbl_mensaje.text = "\n".join(mensajes[-5:])

        if self.combate.estado != EstadoCombate.EN_CURSO:
            resultado_final = self.combate.obtener_resultado_final()
            self.lbl_mensaje.text = resultado_final.mensaje_final
            self.turno_jugador = False
            # Ocultar botones de combate y habilidades
            for btn in [self.btn_ataque, self.btn_defender, self.btn_concentrar, self.btn_habilidad]:
                btn.visible = False
            for btn in self.habilidad_buttons:
                btn.visible = False
            # Mostrar botones postcombate
            for btn in self.postcombate_buttons:
                btn.visible = True
            self.turn_indicator.text = "COMBATE FINALIZADO"
            self.turn_indicator.color = (255, 200, 200)
        else:
            self._actualizar_visibilidad()

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()
        for elem in self.static_elements:
            elem.draw()
        x, y, w, h = self.msg_rect
        arcade.draw_rect_filled(arcade.XYWH(x + w//2, y + h//2, w, h), arcade.types.Color(20, 20, 30, 200))
        for elem in self.ui_elements:
            if hasattr(elem, 'draw'):
                elem.draw()
        for btn in self.habilidad_buttons:
            btn.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)
        for btn in self.ui_elements + self.habilidad_buttons:
            if hasattr(btn, 'on_mouse_motion'):
                btn.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        # Procesar todos los botones; ellos gestionan su visibilidad
        for btn in self.habilidad_buttons:
            btn.on_mouse_press(x, y, button, modifiers)
        for elem in self.ui_elements:
            if hasattr(elem, 'on_mouse_press'):
                elem.on_mouse_press(x, y, button, modifiers)

    def revancha(self):
        nuevo_jugador = self.jugador_clase()
        nuevo_enemigo = self.enemigo_clase()
        self.app.goto_view(CombatView(self.app, nuevo_jugador, nuevo_enemigo))

    def ver_historial(self):
        self.app.push_view(HistorialView(self.app, self.combate.historial))

    def volver_menu(self):
        from scenes.menu_scene import MenuView
        self.app.goto_view(MenuView(self.app))