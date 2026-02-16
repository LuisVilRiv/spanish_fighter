import pyglet
from gui.widgets import ImageButton
from combate.sistema_combate import Combate, Accion, EstadoCombate

class CombatScene:
    def __init__(self, app, jugador, enemigo):
        self.app = app
        self.jugador = jugador
        self.enemigo = enemigo
        self.combate = Combate(jugador, enemigo)
        self.batch = pyglet.graphics.Batch()
        self.buttons = []
        self.resultado_turno = None

        # Fondo
        try:
            bg_image = pyglet.image.load('img/fondos/combate.jpg')
            self.background = pyglet.sprite.Sprite(bg_image, batch=self.batch)
        except:
            self.background = pyglet.shapes.Rectangle(0, 0, app.window.width, app.window.height, color=(40,40,40), batch=self.batch)

        # Sprites de personajes (posiciones fijas relativas)
        sprite_size = 100
        self.jugador_x = app.window.width * 0.2
        self.enemigo_x = app.window.width * 0.8 - sprite_size
        y_combat = app.window.height * 0.5

        try:
            sprite_jugador = pyglet.image.load(f'img/personajes/{type(jugador).__name__.lower()}.png')
            self.sprite_jugador = pyglet.sprite.Sprite(sprite_jugador, x=self.jugador_x, y=y_combat, batch=self.batch)
        except:
            self.sprite_jugador = None

        try:
            sprite_enemigo = pyglet.image.load(f'img/personajes/{type(enemigo).__name__.lower()}.png')
            self.sprite_enemigo = pyglet.sprite.Sprite(sprite_enemigo, x=self.enemigo_x, y=y_combat, batch=self.batch)
        except:
            self.sprite_enemigo = None

        # Nombres
        self.lbl_jugador = pyglet.text.Label(
            jugador.nombre, font_size=16,
            x=self.jugador_x + sprite_size//2, y=y_combat + sprite_size + 10,
            anchor_x='center', batch=self.batch
        )
        self.lbl_enemigo = pyglet.text.Label(
            enemigo.nombre, font_size=16,
            x=self.enemigo_x + sprite_size//2, y=y_combat + sprite_size + 10,
            anchor_x='center', batch=self.batch
        )

        # Barras de vida
        bar_width = 200
        bar_height = 20
        self.vida_bar_bg_j = pyglet.shapes.Rectangle(self.jugador_x, y_combat - 30, bar_width, bar_height, color=(50,50,50), batch=self.batch)
        self.vida_bar_j = pyglet.shapes.Rectangle(self.jugador_x, y_combat - 30, bar_width, bar_height, color=(0,200,0), batch=self.batch)
        self.vida_bar_bg_e = pyglet.shapes.Rectangle(self.enemigo_x, y_combat - 30, bar_width, bar_height, color=(50,50,50), batch=self.batch)
        self.vida_bar_e = pyglet.shapes.Rectangle(self.enemigo_x, y_combat - 30, bar_width, bar_height, color=(200,0,0), batch=self.batch)

        # Textos de vida/energía
        self.lbl_vida_j = pyglet.text.Label(
            f"Vida: {jugador.vida_actual}/{jugador.vida_maxima}",
            font_size=12, x=self.jugador_x, y=y_combat - 55, batch=self.batch
        )
        self.lbl_energia_j = pyglet.text.Label(
            f"Energía: {jugador.energia_actual}/{jugador.energia_maxima}",
            font_size=12, x=self.jugador_x, y=y_combat - 75, batch=self.batch
        )
        self.lbl_vida_e = pyglet.text.Label(
            f"Vida: {enemigo.vida_actual}/{enemigo.vida_maxima}",
            font_size=12, x=self.enemigo_x, y=y_combat - 55, batch=self.batch
        )
        self.lbl_energia_e = pyglet.text.Label(
            f"Energía: {enemigo.energia_actual}/{enemigo.energia_maxima}",
            font_size=12, x=self.enemigo_x, y=y_combat - 75, batch=self.batch
        )

        # Botones de acción (abajo, centrados)
        btn_y = 80
        btn_spacing = 220
        start_x = (app.window.width - 3*btn_spacing) // 2
        btn_ataque = ImageButton(
            x=start_x, y=btn_y, image_path='img/botones/ataque.png',
            callback=self.ataque_basico, batch=self.batch
        )
        btn_defender = ImageButton(
            x=start_x + btn_spacing, y=btn_y, image_path='img/botones/defender.png',
            callback=self.defender, batch=self.batch
        )
        btn_concentrar = ImageButton(
            x=start_x + 2*btn_spacing, y=btn_y, image_path='img/botones/concentrar.png',
            callback=self.concentrar, batch=self.batch
        )
        btn_habilidad = ImageButton(
            x=start_x + 3*btn_spacing, y=btn_y, image_path='img/botones/habilidad.png',
            callback=self.usar_habilidad, batch=self.batch
        )
        self.buttons.extend([btn_ataque, btn_defender, btn_concentrar, btn_habilidad])

        # Área de mensajes (panel semitransparente)
        msg_y = btn_y + 100
        msg_height = 100
        msg_bg = pyglet.shapes.Rectangle(50, msg_y, app.window.width-100, msg_height, color=(0,0,0), batch=self.batch)
        msg_bg.opacity = 150
        self.lbl_mensaje = pyglet.text.Label(
            "", x=60, y=msg_y + msg_height - 20, width=app.window.width-120,
            multiline=True, color=(255,255,255,255), batch=self.batch
        )

        self.actualizar_barras()

    def actualizar_barras(self):
        self.vida_bar_j.width = 200 * (self.jugador.vida_actual / self.jugador.vida_maxima)
        self.vida_bar_e.width = 200 * (self.enemigo.vida_actual / self.enemigo.vida_maxima)
        self.lbl_vida_j.text = f"Vida: {self.jugador.vida_actual}/{self.jugador.vida_maxima}"
        self.lbl_vida_e.text = f"Vida: {self.enemigo.vida_actual}/{self.enemigo.vida_maxima}"
        self.lbl_energia_j.text = f"Energía: {self.jugador.energia_actual}/{self.jugador.energia_maxima}"
        self.lbl_energia_e.text = f"Energía: {self.enemigo.energia_actual}/{self.enemigo.energia_maxima}"

    def ataque_basico(self):
        if self.combate.estado != EstadoCombate.EN_CURSO:
            return
        self.resultado_turno = self.combate.ejecutar_turno(Accion.ATAQUE_BASICO)
        self.actualizar_ui()

    def defender(self):
        if self.combate.estado != EstadoCombate.EN_CURSO:
            return
        self.resultado_turno = self.combate.ejecutar_turno(Accion.DEFENDER)
        self.actualizar_ui()

    def concentrar(self):
        if self.combate.estado != EstadoCombate.EN_CURSO:
            return
        self.resultado_turno = self.combate.ejecutar_turno(Accion.CONCENTRAR)
        self.actualizar_ui()

    def usar_habilidad(self):
        if self.combate.estado != EstadoCombate.EN_CURSO:
            return
        if self.jugador.habilidades:
            habilidad = self.jugador.habilidades[0]
            if self.jugador.energia_actual >= habilidad.costo_energia:
                self.resultado_turno = self.combate.ejecutar_turno(Accion.HABILIDAD_ESPECIAL, 0)
            else:
                self.lbl_mensaje.text = "Energía insuficiente"
        self.actualizar_ui()

    def actualizar_ui(self):
        self.actualizar_barras()
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
            for btn in self.buttons:
                btn.callback = None

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_resume(self):
        pass

    def draw(self):
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.buttons:
            btn.on_mouse_press(x, y, button)

    def on_mouse_motion(self, x, y, dx, dy):
        for btn in self.buttons:
            btn.update(x, y)

    def on_key_press(self, symbol, modifiers):
        pass

    def update(self, dt):
        pass