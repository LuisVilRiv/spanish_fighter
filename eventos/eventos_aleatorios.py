"""
eventos_aleatorios.py
Eventos aleatorios para Batalla Cómica Española.

Probabilidades cuando se activa un evento:
  70% NORMAL   25% RARO   5% ULTRA RARO
"""

import random

try:
    from utils import Colores as C
except ImportError:
    class C:
        VERDE = ROJO = AMARILLO = CYAN = MAGENTA = AZUL = NEGRITA = RESET = ""
        VERDE_BRILLANTE = ROJO_BRILLANTE = NARANJA = MAGENTA_BRILLANTE = AMARILLO_BRILLANTE = AZUL_BRILLANTE = ""


# ─────────────────────────────────────────────────────────────────────────────
# Clase base
# ─────────────────────────────────────────────────────────────────────────────

class EventoBase:
    def __init__(self, nombre: str, descripcion: str, tipo: str):
        self.nombre      = nombre
        self.descripcion = descripcion
        self.tipo        = tipo

    def activar(self, jugador, enemigo, turno_actual: int) -> dict:
        raise NotImplementedError

    def __str__(self):
        return f"{self.nombre} ({self.tipo}): {self.descripcion}"

    @staticmethod
    def _al_azar(jugador, enemigo):
        return random.choice([jugador, enemigo])

    @staticmethod
    def _ok(msg: str, **kwargs) -> dict:
        return {"exito": True, "mensaje": msg, **kwargs}



# ─────────────────────────────────────────────────────────────────────────────
# EVENTOS NORMALES  (70 %)
# ─────────────────────────────────────────────────────────────────────────────

class JamonVolador(EventoBase):
    def __init__(self):
        super().__init__("🍖 JAMÓN VOLADOR", "Un jamón ibérico vuela y golpea a alguien.", "normal")
    def activar(self, jugador, enemigo, turno_actual):
        objetivo = self._al_azar(jugador, enemigo)
        daño = 25
        extra = ""
        if "Segarro" in getattr(objetivo, "tipo", ""):
            daño *= 2; extra = " ¡ALERGIA AL JAMÓN! x2"
        r = objetivo.recibir_dano(daño, "jamón")
        return self._ok(f"{C.AMARILLO}¡JAMÓN VOLADOR!{C.RESET}\n"
                        f"Un jamón sale volando y golpea a {objetivo.nombre}.{extra}\n"
                        f"{objetivo.nombre} recibe {r} de daño.",
                        daño=r, objetivo=objetivo.nombre, tipo="daño")


class AbuelaAparece(EventoBase):
    def __init__(self):
        super().__init__("👵 ABUELA APARECE", "Sale una abuela: cariño o capón.", "normal")
    def activar(self, jugador, enemigo, turno_actual):
        obj = self._al_azar(jugador, enemigo)
        if random.random() < 0.5:
            v = obj.recibir_curacion(30)
            return self._ok(f"{C.VERDE}¡ABUELA APARECE!{C.RESET}\n"
                            f"La abuela: '¡Come, hijo!' {obj.nombre} recupera {v} de vida.",
                            curacion=v, objetivo=obj.nombre, tipo="curacion")
        else:
            d = obj.recibir_dano(15, "capón")
            return self._ok(f"{C.ROJO}¡ABUELA APARECE!{C.RESET}\n"
                            f"La abuela da un capón a {obj.nombre}. Recibe {d} de daño.",
                            daño=d, objetivo=obj.nombre, tipo="daño")


class OleImprovisado(EventoBase):
    def __init__(self):
        super().__init__("👏 OLÉ IMPROVISADO", "El público anima a alguien. Sube sus stats.", "normal")
    def activar(self, jugador, enemigo, turno_actual):
        obj = jugador if random.random() < 0.6 else enemigo
        obj.ataque += 10; obj.defensa += 8; obj.velocidad += 5
        e = 20
        obj.energia_actual = min(obj.energia_maxima, obj.energia_actual + e)
        return self._ok(f"{C.VERDE}¡OLÉ IMPROVISADO!{C.RESET}\n"
                        f"El público anima a {obj.nombre}.\n"
                        f"¡Ataque +10, Defensa +8, Velocidad +5, Energía +{e}!",
                        objetivo=obj.nombre, tipo="bonus")


class BotellonSorpresa(EventoBase):
    def __init__(self):
        super().__init__("🍺 BOTELLÓN SORPRESA", "¿Cerveza caducada o kalimotxo mágico?", "normal")
    def activar(self, jugador, enemigo, turno_actual):
        obj = self._al_azar(jugador, enemigo)
        if random.random() < 0.5:
            d = obj.recibir_dano(20, "cerveza_caducada")
            extra = ""
            if random.random() < 0.3:
                obj.aplicar_estado("enfermo", duracion=2); extra = " y está ENFERMO"
            return self._ok(f"{C.ROJO}¡BOTELLÓN SORPRESA!{C.RESET}\n"
                            f"Era cerveza caducada de 2019. {obj.nombre} recibe {d} daño{extra}.",
                            daño=d, objetivo=obj.nombre, tipo="daño")
        else:
            v = obj.recibir_curacion(25)
            obj.energia_actual = min(obj.energia_maxima, obj.energia_actual + 30)
            obj.ataque += 5
            return self._ok(f"{C.VERDE}¡BOTELLÓN SORPRESA!{C.RESET}\n"
                            f"¡KALIMOTXO MÁGICO! {obj.nombre} recupera {v} vida, +30 energía y +5 ataque.",
                            curacion=v, objetivo=obj.nombre, tipo="curacion")


class TuristasDespistados(EventoBase):
    def __init__(self):
        super().__init__("🧳 TURISTAS DESPISTADOS", "Piden direcciones. Propina o follón.", "normal")
    def activar(self, jugador, enemigo, turno_actual):
        if random.random() < 0.6:
            p = random.randint(10, 30)
            jugador.energia_actual = min(jugador.energia_maxima, jugador.energia_actual + p)
            return self._ok(f"{C.VERDE}¡TURISTAS DESPISTADOS!{C.RESET}\n"
                            f"Les ayudas con un mapa en servilleta. Propina: +{p} energía. ¡Grazie!",
                            energia_ganada=p, tipo="beneficio")
        else:
            d = jugador.recibir_dano(15, "follón_turistas")
            pe = min(20, jugador.energia_actual); jugador.energia_actual -= pe
            return self._ok(f"{C.ROJO}¡TURISTAS DESPISTADOS!{C.RESET}\n"
                            f"Les mandas a la mierda. Llaman al cónsul. {d} daño y -{pe} energía.",
                            daño=d, energia_perdida=pe, tipo="daño")


class AtascoMadrid(EventoBase):
    def __init__(self):
        super().__init__("🚗 ATASCO DE TRÁFICO", "Atasco monumental en la M-30. Todos pierden velocidad.", "normal")
    def activar(self, jugador, enemigo, turno_actual):
        r = random.randint(8, 15)
        jugador.velocidad = max(5, jugador.velocidad - r)
        enemigo.velocidad = max(5, enemigo.velocidad - r)
        bonus = ""
        for p in [jugador, enemigo]:
            if any(t in getattr(p, "tipo", "") for t in ["Choni", "Abuela"]):
                p.velocidad += r; bonus += f"\n{p.nombre} va en bici y no le afecta."
        return self._ok(f"{C.AMARILLO}¡ATASCO DE TRÁFICO!{C.RESET}\n"
                        f"14 km de caravana en la M-30. Todos pierden {r} velocidad.{bonus}",
                        velocidad_perdida=r, tipo="debuff")


class ChoricioEnElBolsillo(EventoBase):
    def __init__(self):
        super().__init__("🌭 CHORIZO EN EL BOLSILLO", "Siempre viene bien un chorizo.", "normal")
    def activar(self, jugador, enemigo, turno_actual):
        obj = self._al_azar(jugador, enemigo)
        v = obj.recibir_curacion(20); obj.ataque += 5
        return self._ok(f"{C.VERDE}¡CHORIZO EN EL BOLSILLO!{C.RESET}\n"
                        f"{obj.nombre} encuentra un chorizo serrano en el bolsillo trasero.\n"
                        f"¡Recupera {v} vida y +5 ataque por el chute de proteínas!",
                        curacion=v, objetivo=obj.nombre, tipo="beneficio")


class VecinaComentarista(EventoBase):
    def __init__(self):
        super().__init__("🪟 VECINA DEL 3B", "La vecina comenta el combate desde la ventana.", "normal")
    def activar(self, jugador, enemigo, turno_actual):
        opciones = [
            ("¡Qué vergüenza, en mis tiempos esto no pasaba!",
             lambda j,e: [setattr(j,'defensa',max(5,j.defensa-8)), setattr(e,'defensa',max(5,e.defensa-8))],
             "Ambos pierden 8 defensa de vergüenza."),
            ("¡Ese chico está muy delgado, que le doy un tupper!",
             lambda j,e: j.recibir_curacion(25) if j.vida_actual<=e.vida_actual else e.recibir_curacion(25),
             "Lanza un tupper de cocido. El más débil recupera 25 vida."),
            ("¡Escándalo! ¡Voy a llamar a la policía!",
             lambda j,e: [setattr(j,'energia_actual',max(0,j.energia_actual-10)),
                          setattr(e,'energia_actual',max(0,e.energia_actual-10))],
             "Todos se ponen nerviosos. -10 energía a cada uno."),
            ("¡Guapo tú, que me recuerdas a mi difunto Paco!",
             lambda j,e: setattr(random.choice([j,e]),'ataque',random.choice([j,e]).ataque+12),
             "Alguien recibe el piropo y sube +12 ataque de la emoción."),
        ]
        frase, efecto, desc = random.choice(opciones)
        efecto(jugador, enemigo)
        return self._ok(f"{C.CYAN}¡VECINA DEL 3B!{C.RESET}\n"
                        f"La señora Encarna: '{frase}'\n{desc}", tipo="mixto")


class ManifestacionInesperada(EventoBase):
    def __init__(self):
        super().__init__("📢 MANIFESTACIÓN INESPERADA", "Una manifestación irrumpe con consecuencias.", "normal")
    def activar(self, jugador, enemigo, turno_actual):
        consigna = random.choice(["¡No pasarán!", "¡Que se vayan todos!",
                                   "¡El pueblo unido jamás será vencido!", "¡Abajo los recortes!"])
        if random.random() < 0.5:
            jugador.aplicar_estado("paralizado", duracion=1)
            enemigo.aplicar_estado("paralizado", duracion=1)
            return self._ok(f"{C.MAGENTA}¡MANIFESTACIÓN INESPERADA!{C.RESET}\n"
                            f"'{consigna}' ¡Ambos PARALIZADOS 1 turno por la confusión!", tipo="estado")
        else:
            obj = self._al_azar(jugador, enemigo)
            v = obj.recibir_curacion(20); obj.ataque += 8
            return self._ok(f"{C.MAGENTA}¡MANIFESTACIÓN INESPERADA!{C.RESET}\n"
                            f"'{consigna}' {obj.nombre} se emociona: +{v} vida y +8 ataque.",
                            curacion=v, objetivo=obj.nombre, tipo="beneficio")


class HuelgaGeneral(EventoBase):
    def __init__(self):
        super().__init__("✊ HUELGA GENERAL", "Todo para 1 turno. Ambos recuperan energía.", "normal")
    def activar(self, jugador, enemigo, turno_actual):
        jugador.aplicar_estado("dormido", duracion=1)
        enemigo.aplicar_estado("dormido", duracion=1)
        e = 25
        jugador.energia_actual = min(jugador.energia_maxima, jugador.energia_actual + e)
        enemigo.energia_actual = min(enemigo.energia_maxima, enemigo.energia_actual + e)
        return self._ok(f"{C.AMARILLO}¡HUELGA GENERAL!{C.RESET}\n"
                        f"Los sindicatos convocan huelga. Ambos PARALIZADOS 1 turno "
                        f"pero recuperan {e} energía en el descanso.", energia_extra=e, tipo="estado")


class BarDeCopas(EventoBase):
    def __init__(self):
        super().__init__("🥂 BAR DE COPAS", "Una ronda gratis. Más energía, menos precisión.", "normal")
    def activar(self, jugador, enemigo, turno_actual):
        e = random.randint(20, 40)
        jugador.energia_actual = min(jugador.energia_maxima, jugador.energia_actual + e)
        enemigo.energia_actual = min(enemigo.energia_maxima, enemigo.energia_actual + e)
        jugador.velocidad = max(5, jugador.velocidad - 7)
        enemigo.velocidad = max(5, enemigo.velocidad - 7)
        return self._ok(f"{C.VERDE}¡BAR DE COPAS!{C.RESET}\n"
                        f"El camarero invita a una ronda. Ambos +{e} energía pero -7 velocidad. ¡Salud!",
                        energia_extra=e, velocidad_perdida=7, tipo="mixto")


# ─────────────────────────────────────────────────────────────────────────────
# EVENTOS RAROS  (25 %)
# ─────────────────────────────────────────────────────────────────────────────

class SiestaRepentina(EventoBase):
    def __init__(self):
        super().__init__("😴 SIESTA REPENTINA", "Un sueño de la hostia en mitad del combate.", "raro")
    def activar(self, jugador, enemigo, turno_actual):
        obj = self._al_azar(jugador, enemigo)
        dur = random.randint(1, 3)
        obj.aplicar_estado("dormido", duracion=dur)
        v = obj.recibir_curacion(40)
        return self._ok(f"{C.CYAN}¡SIESTA REPENTINA!{C.RESET}\n"
                        f"A {obj.nombre} le entra un sueño de la hostia.\n"
                        f"Duerme {dur} turno{'s' if dur>1 else ''} y recupera {v} vida.",
                        duracion_siesta=dur, curacion=v, objetivo=obj.nombre, tipo="estado")


class ConcursoDeTapas(EventoBase):
    def __init__(self):
        super().__init__("🍽️ CONCURSO DE TAPAS", "El jurado: un gato, una vecina y un borracho.", "raro")
    def activar(self, jugador, enemigo, turno_actual):
        p = self._al_azar(jugador, enemigo)
        tapa = random.choice(["patatas bravas", "croquetas", "boquerones en vinagre",
                               "oreja a la plancha", "chopitos", "tortilla de la abuela"])
        votos = sum(random.random() < 0.33 for _ in range(3))
        if votos >= 2:
            v = p.recibir_curacion(35); e = 25
            p.energia_actual = min(p.energia_maxima, p.energia_actual + e)
            return self._ok(f"{C.VERDE}¡CONCURSO DE TAPAS!{C.RESET}\n"
                            f"{p.nombre} presenta {tapa}. Jurado: {votos}/3. ¡GANA!\n"
                            f"Recupera {v} vida y {e} energía.", curacion=v, tipo="beneficio")
        else:
            d = p.recibir_dano(20, "humillacion"); p.ataque = max(5, p.ataque - 8)
            return self._ok(f"{C.ROJO}¡CONCURSO DE TAPAS!{C.RESET}\n"
                            f"{p.nombre} presenta {tapa}. Jurado: {votos}/3. ¡PIERDE!\n"
                            f"Recibe {d} daño y -8 ataque por la humillación.", daño=d, tipo="daño")


class LlamadaDeTelefono(EventoBase):
    def __init__(self):
        super().__init__("📞 LLAMADA DE TELÉFONO", "Tu madre / el banco / una teleoperadora.", "raro")
    def activar(self, jugador, enemigo, turno_actual):
        obj = jugador if random.random() < 0.7 else enemigo
        tipo_l = random.choice(["madre", "banco", "teleoperadora"])
        if tipo_l == "madre":
            if random.random() < 0.6:
                v = obj.recibir_curacion(25); obj.velocidad = max(5, obj.velocidad - 10)
                return self._ok(f"{C.CYAN}¡LLAMADA DE TELÉFONO!{C.RESET}\n"
                                f"Tu madre: '¿Has comido?' +{v} vida pero -10 velocidad.",
                                curacion=v, velocidad_perdida=10, tipo="mixto")
            else:
                d = obj.recibir_dano(30, "regaño")
                return self._ok(f"{C.ROJO}¡LLAMADA DE TELÉFONO!{C.RESET}\n"
                                f"Tu madre: '¡Limpia tu cuarto!' {obj.nombre} recibe {d} daño psicológico.",
                                daño=d, tipo="daño")
        elif tipo_l == "banco":
            if random.random() < 0.4:
                dinero = random.randint(20, 50)
                obj.energia_actual = min(obj.energia_maxima, obj.energia_actual + dinero)
                return self._ok(f"{C.VERDE}¡LLAMADA DE TELÉFONO!{C.RESET}\n"
                                f"El banco: 'Transferencia a su favor.' +{dinero} energía.",
                                energia_ganada=dinero, tipo="beneficio")
            else:
                deuda = random.randint(15, 40)
                obj.energia_actual = max(0, obj.energia_actual - deuda)
                obj.defensa = max(5, obj.defensa - 5)
                return self._ok(f"{C.ROJO}¡LLAMADA DE TELÉFONO!{C.RESET}\n"
                                f"El banco: 'Tiene una deuda pendiente.' -{deuda} energía y -5 defensa.",
                                energia_perdida=deuda, defensa_perdida=5, tipo="daño")
        else:
            d = obj.recibir_dano(15, "teleoperadora")
            pe = min(10, obj.energia_actual); obj.energia_actual -= pe
            prod = random.choice(["un seguro de vida", "fibra óptica",
                                   "un curso de bolsa", "una tarjeta sin intereses"])
            return self._ok(f"{C.MAGENTA}¡LLAMADA DE TELÉFONO!{C.RESET}\n"
                            f"Teleoperadora: '¿Le interesa {prod}?' {d} daño y -{pe} energía.",
                            daño=d, energia_perdida=pe, tipo="daño")


class QueTiempoMasRaro(EventoBase):
    def __init__(self):
        super().__init__("🌦️ QUÉ TIEMPO MÁS RARO", "Granizo, calor, sol, lluvia o viento.", "raro")
    def activar(self, jugador, enemigo, turno_actual):
        t = random.choice(["granizo", "calor_extremo", "sol_de_justicia",
                            "lluvia_torrencial", "viento_huracanado"])
        if t == "granizo":
            dj = jugador.recibir_dano(20, "hielo"); de = enemigo.recibir_dano(20, "hielo")
            return self._ok(f"{C.AZUL}¡QUÉ TIEMPO MÁS RARO! Granizo del tamaño de naranjas.{C.RESET}\n"
                            f"{jugador.nombre} -{dj} / {enemigo.nombre} -{de} de vida.",
                            daño_jugador=dj, daño_enemigo=de, tipo="daño_multi")
        elif t == "calor_extremo":
            dj = jugador.recibir_dano(25, "fuego"); de = enemigo.recibir_dano(25, "fuego")
            for p in [jugador, enemigo]:
                if random.random() < 0.4: p.aplicar_estado("quemado", duracion=2)
            return self._ok(f"{C.ROJO}¡QUÉ TIEMPO MÁS RARO! 40 grados sin sombra.{C.RESET}\n"
                            f"{jugador.nombre} -{dj} / {enemigo.nombre} -{de}. Posible quemadura.",
                            daño_jugador=dj, daño_enemigo=de, tipo="daño_multi")
        elif t == "sol_de_justicia":
            res = []
            for p in [jugador, enemigo]:
                if any(b in getattr(p,"tipo","") for b in ["Flaquito","Torero"]):
                    v = p.recibir_curacion(30); res.append(f"{p.nombre} toma el sol: +{v} vida.")
                else:
                    d = p.recibir_dano(20, "sol"); res.append(f"{p.nombre} se derrite: -{d} vida.")
            return self._ok(f"{C.AMARILLO}¡QUÉ TIEMPO MÁS RARO! Sol de justicia.{C.RESET}\n"
                            + "\n".join(res), tipo="mixto_multi")
        elif t == "lluvia_torrencial":
            for p in [jugador, enemigo]:
                p.aplicar_estado("mojado", duracion=3)
                if random.random() < 0.3: p.aplicar_estado("resfriado", duracion=3)
            return self._ok(f"{C.AZUL}¡QUÉ TIEMPO MÁS RARO! Lluvia torrencial.{C.RESET}\n"
                            f"Ambos MOJADOS. Posible resfriado.", tipo="estado_multi")
        else:
            efts = []
            if random.random() < 0.3:
                d = random.randint(10, 20)
                jugador.recibir_dano(d, "viento"); enemigo.recibir_dano(d, "viento")
                efts.append(f"Ambos reciben {d} daño.")
            if not efts: efts.append("Los papeles de la burocracia salen volando.")
            return self._ok(f"{C.CYAN}¡QUÉ TIEMPO MÁS RARO! Viento huracanado.{C.RESET}\n"
                            + " ".join(efts), tipo="aleatorio")


class CorrupcionMunicipal(EventoBase):
    def __init__(self):
        super().__init__("🏛️ CORRUPCIÓN MUNICIPAL", "Un concejal saca tajada. Roba energía.", "raro")
    def activar(self, jugador, enemigo, turno_actual):
        rj = random.randint(15, 30); re = random.randint(15, 30)
        jugador.energia_actual = max(0, jugador.energia_actual - rj)
        enemigo.energia_actual = max(0, enemigo.energia_actual - re)
        for p in [jugador, enemigo]:
            if "Político" in getattr(p, "tipo", ""):
                p.energia_actual = min(p.energia_maxima, p.energia_actual + rj + re)
                p.ataque += 10
        return self._ok(f"{C.ROJO}¡CORRUPCIÓN MUNICIPAL!{C.RESET}\n"
                        f"Aparece un concejal y saca tajada.\n"
                        f"{jugador.nombre} pierde {rj} energía / {enemigo.nombre} pierde {re} energía.\n"
                        f"El dinero desaparece en paraísos fiscales.",
                        energia_perdida_j=rj, energia_perdida_e=re, tipo="daño")


class PeleaDeVecinos(EventoBase):
    def __init__(self):
        super().__init__("🏠 PELEA DE COMUNIDAD", "Los vecinos se pelean en la escalera.", "raro")
    def activar(self, jugador, enemigo, turno_actual):
        d = random.randint(10, 25)
        jugador.recibir_dano(d, "bronca_vecinos")
        enemigo.recibir_dano(d, "bronca_vecinos")
        if random.random() < 0.4:
            self._al_azar(jugador, enemigo).aplicar_estado("confundido", duracion=2)
        motivo = random.choice(["el perro que ladra de noche", "la gotera del baño",
                                 "las obras del 4B", "quién paga el ascensor",
                                 "el portal de Navidad"])
        return self._ok(f"{C.MAGENTA}¡PELEA DE COMUNIDAD!{C.RESET}\n"
                        f"Los vecinos se pelean por {motivo}. ¡Todos a la gresca!\n"
                        f"Ambos reciben {d} de daño.",
                        daño_jugador=d, daño_enemigo=d, tipo="daño_multi")


class CorridaDeToros(EventoBase):
    def __init__(self):
        super().__init__("🐂 CORRIDA DE TOROS", "Aparece un toro. El torero se beneficia.", "raro")
    def activar(self, jugador, enemigo, turno_actual):
        res = []
        for p in [jugador, enemigo]:
            if "Torero" in getattr(p, "tipo", ""):
                v = p.recibir_curacion(50); p.ataque += 20
                res.append(f"¡{p.nombre} en su elemento! +{v} vida y +20 ataque.")
            else:
                cornada = random.randint(20, 40)
                d = p.recibir_dano(cornada, "cornada")
                res.append(f"{p.nombre} recibe cornada: -{d} vida.")
        return self._ok(f"{C.ROJO}¡CORRIDA DE TOROS!{C.RESET}\n"
                        f"Un toro de lidia irrumpe en el combate.\n" + "\n".join(res),
                        tipo="mixto_multi")


class SubidaDelAlquiler(EventoBase):
    def __init__(self):
        super().__init__("🏘️ SUBIDA DEL ALQUILER", "El casero sube el alquiler en mitad del combate.", "raro")
    def activar(self, jugador, enemigo, turno_actual):
        subida = random.randint(25, 50); pct = random.randint(15, 40)
        jugador.energia_actual = max(0, jugador.energia_actual - subida)
        enemigo.energia_actual = max(0, enemigo.energia_actual - subida)
        for p in [jugador, enemigo]:
            if "Político" in getattr(p, "tipo", ""):
                p.energia_actual = min(p.energia_maxima, p.energia_actual + subida)
        return self._ok(f"{C.ROJO}¡SUBIDA DEL ALQUILER!{C.RESET}\n"
                        f"El casero sube el alquiler un {pct}%. '¡Es que el mercado!'\n"
                        f"Ambos pierden {subida} energía. ¡Indignad@s!",
                        energia_perdida=subida, tipo="daño")


# ─────────────────────────────────────────────────────────────────────────────
# EVENTOS ULTRA RAROS  (5 %)
# ─────────────────────────────────────────────────────────────────────────────

class FurgonetaBlanca(EventoBase):
    def __init__(self):
        super().__init__("🚐 FURGONETA BLANCA", "¡LA FURGONETA! Todos corren. Daño masivo.", "ultra_raro")
    def activar(self, jugador, enemigo, turno_actual):
        dj = jugador.recibir_dano(50, "furgoneta"); de = enemigo.recibir_dano(50, "furgoneta")
        sj = random.random() < 0.1; se = random.random() < 0.1
        extra = ""
        if sj: jugador.vida_actual = 0; extra += f"\n¡SECUESTRO! {jugador.nombre} sube sin querer."
        if se: enemigo.vida_actual = 0; extra += f"\n¡SECUESTRO! {enemigo.nombre} sube sin querer."
        return self._ok(f"{C.ROJO_BRILLANTE}¡¡¡FURGONETA BLANCA!!!{C.RESET}\n"
                        f"De la nada aparece LA FURGONETA BLANCA. ¡TODOS CORREN!\n"
                        f"{jugador.nombre} -{dj} / {enemigo.nombre} -{de}.{extra}",
                        daño_jugador=dj, daño_enemigo=de, tipo="catastrofico")


class ConspiracionTortillera(EventoBase):
    def __init__(self):
        super().__init__("🥚 CONSPIRACIÓN TORTILLERA", "Con cebolla o sin: consecuencias bíblicas.", "ultra_raro")
    def activar(self, jugador, enemigo, turno_actual):
        eleccion = random.choice(["con cebolla", "sin cebolla"])
        if eleccion == "con cebolla":
            cj = jugador.recibir_curacion(60); ce = enemigo.recibir_curacion(60)
            jugador.ataque += 20; enemigo.ataque += 20
            return self._ok(f"{C.AMARILLO_BRILLANTE}¡¡¡CONSPIRACIÓN TORTILLERA!!!{C.RESET}\n"
                            f"¡LA RESPUESTA CORRECTA: {eleccion.upper()}!\n"
                            f"Ambos recuperan {cj} vida y +20 ataque por la revelación.",
                            correcto=True, tipo="eleccion")
        else:
            dj = jugador.recibir_dano(40, "herejia"); de = enemigo.recibir_dano(40, "herejia")
            jugador.defensa = max(5, jugador.defensa - 15)
            enemigo.defensa = max(5, enemigo.defensa - 15)
            return self._ok(f"{C.AMARILLO_BRILLANTE}¡¡¡CONSPIRACIÓN TORTILLERA!!!{C.RESET}\n"
                            f"¡HEREJÍA CULINARIA: {eleccion.upper()}!\n"
                            f"Ambos reciben {dj} daño y -15 defensa por la vergüenza.",
                            correcto=False, tipo="eleccion")


class RatalectricaFalsa(EventoBase):
    def __init__(self):
        super().__init__("[!] RATALECTRICA FALSA", "Explota el 70% de las veces.", "ultra_raro")
    def activar(self, jugador, enemigo, turno_actual):
        if random.random() < 0.7:
            d = random.randint(30, 80)
            obj = random.choice(["jugador", "enemigo", "ambos"])
            if obj == "jugador":
                dr = jugador.recibir_dano(d, "explosion"); msg_d = f"{jugador.nombre} recibe {dr} daño."
            elif obj == "enemigo":
                dr = enemigo.recibir_dano(d, "explosion"); msg_d = f"{enemigo.nombre} recibe {dr} daño."
            else:
                dj = jugador.recibir_dano(d, "explosion"); de = enemigo.recibir_dano(d, "explosion")
                msg_d = f"Ambos reciben {dj}/{de} daño."
            return self._ok(f"{C.AMARILLO_BRILLANTE}¡¡¡RATALECTRICA FALSA!!!{C.RESET}\n"
                            f"Aparece una ratalectrica de ImportExpress... ¡¡EXPLOTA!!\n{msg_d}",
                            explota=True, tipo="explosion")
        else:
            ef = random.choice(["cura","choque","truco","copion"])
            if ef == "cura":
                v = jugador.recibir_curacion(40); msg = f"¡Cura a {jugador.nombre} por {v}!"
            elif ef == "choque":
                obj = self._al_azar(jugador, enemigo); d = obj.recibir_dano(10,"choque")
                msg = f"Choque leve a {obj.nombre}: -{d} vida."
            elif ef == "truco":
                e=25
                jugador.energia_actual=min(jugador.energia_maxima,jugador.energia_actual+e)
                enemigo.energia_actual=min(enemigo.energia_maxima,enemigo.energia_actual+e)
                msg = f"¡Truco gracioso! Ambos +{e} energía de la risa."
            else:
                if jugador.ataque > enemigo.ataque:
                    enemigo.ataque=jugador.ataque; msg=f"{enemigo.nombre} copia ataque de {jugador.nombre}."
                else:
                    jugador.ataque=enemigo.ataque; msg=f"{jugador.nombre} copia ataque de {enemigo.nombre}."
            return self._ok(f"{C.AMARILLO_BRILLANTE}¡¡¡RATALECTRICA FALSA!!!{C.RESET}\n"
                            f"No explota (suerte de novato).\n{msg}", explota=False, tipo="aleatorio")


class EspirituDeLaFeria(EventoBase):
    def __init__(self):
        super().__init__("👻 ESPÍRITU DE LA FERIA", "Oreja de feria o Refresco de cola.", "ultra_raro")
    def activar(self, jugador, enemigo, turno_actual):
        if random.random() < 0.5:
            cj=jugador.recibir_curacion(75); ce=enemigo.recibir_curacion(75)
            jugador.ataque+=15; enemigo.ataque+=15
            return self._ok(f"{C.MAGENTA_BRILLANTE}¡¡¡ESPÍRITU DE LA FERIA!!!{C.RESET}\n"
                            f"¡OREJA DE FERIA! Ambos recuperan {cj} vida y +15 ataque.",
                            curacion_jugador=cj, curacion_enemigo=ce, tipo="beneficio")
        else:
            dj=jugador.recibir_dano(30,"mareo"); de=enemigo.recibir_dano(30,"mareo")
            jugador.aplicar_estado("mareado",duracion=2); enemigo.aplicar_estado("mareado",duracion=2)
            e=40
            jugador.energia_actual=min(jugador.energia_maxima,jugador.energia_actual+e)
            enemigo.energia_actual=min(enemigo.energia_maxima,enemigo.energia_actual+e)
            return self._ok(f"{C.MAGENTA_BRILLANTE}¡¡¡ESPÍRITU DE LA FERIA!!!{C.RESET}\n"
                            f"¡REFRESCO DE COLA! {dj}/{de} daño por mareo pero +{e} energía. ¡MAREADOS!",
                            daño_jugador=dj, daño_enemigo=de, energia_extra=e, tipo="mixto")


class MocoEnElDedo(EventoBase):
    def __init__(self):
        super().__init__("💧 MOCO EN EL DEDO", "Lo miras, lo lanzas o te lo comes.", "ultra_raro")
    def activar(self, jugador, enemigo, turno_actual):
        op = random.choice(["mirar","lanzar","comer"])
        if op == "mirar":
            v=jugador.recibir_curacion(20)
            return self._ok(f"{C.VERDE_BRILLANTE}¡¡¡MOCO EN EL DEDO!!!{C.RESET}\n"
                            f"Lo miras. Revelación científica. +{v} vida.", curacion=v, tipo="beneficio")
        elif op == "lanzar":
            d=enemigo.recibir_dano(25,"moco"); enemigo.defensa=max(5,enemigo.defensa-10)
            enemigo.aplicar_estado("asqueado",duracion=2)
            return self._ok(f"{C.VERDE_BRILLANTE}¡¡¡MOCO EN EL DEDO!!!{C.RESET}\n"
                            f"¡Impacto en {enemigo.nombre}! {d} daño, -10 defensa, ASQUEADO.", daño=d, tipo="daño")
        else:
            ef=random.choice(["curacion_masiva","enfermedad","poder","transformacion"])
            if ef=="curacion_masiva":
                v=jugador.recibir_curacion(100)
                return self._ok(f"{C.VERDE_BRILLANTE}¡¡¡MOCO EN EL DEDO!!!{C.RESET}\nTe lo comes. ¿Era caramelizado? +{v} vida.", curacion=v, tipo="beneficio")
            elif ef=="enfermedad":
                d=jugador.recibir_dano(50,"enfermedad"); jugador.aplicar_estado("enfermo_grave",duracion=3)
                return self._ok(f"{C.ROJO_BRILLANTE}¡¡¡MOCO EN EL DEDO!!!{C.RESET}\nTe lo comes. ERROR GRAVE. {d} daño + enfermedad grave.", daño=d, tipo="daño")
            elif ef=="poder":
                jugador.ataque+=30; jugador.defensa+=20; jugador.velocidad+=15
                return self._ok(f"{C.VERDE_BRILLANTE}¡¡¡MOCO EN EL DEDO!!!{C.RESET}\nTe lo comes. ¡PODER OCULTO! +30 ataque, +20 defensa, +15 velocidad.", tipo="beneficio")
            else:
                jugador.aplicar_estado("transformado",duracion=2)
                return self._ok(f"{C.MAGENTA_BRILLANTE}¡¡¡MOCO EN EL DEDO!!!{C.RESET}\nTe lo comes. ¡TRANSFORMACIÓN! {jugador.nombre} muta temporalmente.", tipo="estado")


class LoteriaDeLaNoche(EventoBase):
    def __init__(self):
        super().__init__("🎄 LOTERÍA DE NAVIDAD", "¡EL GORDO! O el décimo mojado.", "ultra_raro")
    def activar(self, jugador, enemigo, turno_actual):
        if random.random() < 0.5:
            cj=jugador.recibir_curacion(jugador.vida_maxima); ce=enemigo.recibir_curacion(enemigo.vida_maxima)
            for p in [jugador,enemigo]:
                p.ataque+=25; p.defensa+=20; p.velocidad+=15; p.energia_actual=p.energia_maxima
            return self._ok(f"{C.AMARILLO_BRILLANTE}¡¡¡LOTERÍA DE NAVIDAD!!!{C.RESET}\n"
                            f"¡¡¡EL GORDO!!! Vida llena, energía llena, +25/+20/+15 stats.\n"
                            f"¡Que sea pa bien, coño!", curacion_jugador=cj, gordo=True, tipo="beneficio")
        else:
            dj=jugador.recibir_dano(60,"decepcion"); de=enemigo.recibir_dano(60,"decepcion")
            jugador.aplicar_estado("deprimido",duracion=2); enemigo.aplicar_estado("deprimido",duracion=2)
            return self._ok(f"{C.AMARILLO_BRILLANTE}¡¡¡LOTERÍA DE NAVIDAD!!!{C.RESET}\n"
                            f"El décimo estaba mojado. No canta nada.\n"
                            f"Ambos reciben {dj}/{de} daño y están DEPRIMIDOS 2 turnos.",
                            daño_jugador=dj, daño_enemigo=de, gordo=False, tipo="daño_multi")


class ElReyEmerito(EventoBase):
    def __init__(self):
        super().__init__("👑 EL REY EMÉRITO", "Roba energía y se va a Abu Dhabi.", "ultra_raro")
    def activar(self, jugador, enemigo, turno_actual):
        rj=random.randint(30,60); re=random.randint(30,60)
        jugador.energia_actual=max(0,jugador.energia_actual-rj)
        enemigo.energia_actual=max(0,enemigo.energia_actual-re)
        extra = "\nDeja una propina antes de embarcar." if random.random()<0.3 else "\nSe va en jet privado. Sin propina."
        if "propina" in extra:
            jugador.recibir_curacion(20); enemigo.recibir_curacion(20)
        return self._ok(f"{C.AMARILLO_BRILLANTE}¡¡¡EL REY EMÉRITO!!!{C.RESET}\n"
                        f"Aparece con maletines. Roba {rj} energía a {jugador.nombre} "
                        f"y {re} a {enemigo.nombre}.{extra}\n'Tengo que hacer unas llamadas desde Ginebra.'",
                        energia_robada_j=rj, energia_robada_e=re, tipo="catastrofico")


# ─────────────────────────────────────────────────────────────────────────────
# Listas exportadas
# ─────────────────────────────────────────────────────────────────────────────

EVENTOS_NORMALES = [
    JamonVolador, AbuelaAparece, OleImprovisado, BotellonSorpresa,
    TuristasDespistados, AtascoMadrid, ChoricioEnElBolsillo,
    VecinaComentarista, ManifestacionInesperada, HuelgaGeneral, BarDeCopas,
]

EVENTOS_RAROS = [
    SiestaRepentina, ConcursoDeTapas, LlamadaDeTelefono, QueTiempoMasRaro,
    CorrupcionMunicipal, PeleaDeVecinos, CorridaDeToros, SubidaDelAlquiler,
]

EVENTOS_ULTRA_RAROS = [
    FurgonetaBlanca, ConspiracionTortillera, RatalectricaFalsa,
    EspirituDeLaFeria, MocoEnElDedo, LoteriaDeLaNoche, ElReyEmerito,
]

TODOS_LOS_EVENTOS = EVENTOS_NORMALES + EVENTOS_RAROS + EVENTOS_ULTRA_RAROS