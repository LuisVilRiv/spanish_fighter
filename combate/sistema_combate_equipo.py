"""
sistema_combate_equipo.py
Sistema de combate por equipos (1v1 hasta 4v4).

Sistema de turnos:
  - Se usa orden por velocidad (mayor velocidad actúa antes).
  - En 1v1 es exactamente igual que antes.
  - En 2v2/3v3/4v4: se crea una cola de turno al inicio del round, 
    ordenada por velocidad (con pequeña varianza aleatoria).
    Cada personaje actúa una vez por round.
  - Las habilidades de curación SOLO curan a compañeros (mismo equipo).
  - Cuando un personaje cae (vida ≤ 0) sale de la cola.
  - El combate termina cuando todo un equipo ha caído.
"""

import random
from enum import Enum, auto
from typing import List, Optional, Dict, Any, Tuple

try:
    from utils import Colores as C
except ImportError:
    class C:
        VERDE = ROJO = AMARILLO = CYAN = MAGENTA = AZUL = NEGRITA = RESET = ""
        VERDE_BRILLANTE = ROJO_BRILLANTE = NARANJA = ""

try:
    from ..eventos import (EVENTOS_NORMALES, EVENTOS_RAROS,
                            EVENTOS_ULTRA_RAROS, TODOS_LOS_EVENTOS)
except ImportError:
    try:
        from eventos import (EVENTOS_NORMALES, EVENTOS_RAROS,
                              EVENTOS_ULTRA_RAROS, TODOS_LOS_EVENTOS)
    except ImportError:
        EVENTOS_NORMALES = EVENTOS_RAROS = EVENTOS_ULTRA_RAROS = TODOS_LOS_EVENTOS = []


class EstadoCombate(Enum):
    EN_CURSO         = auto()
    VICTORIA_EQUIPO1 = auto()
    VICTORIA_EQUIPO2 = auto()
    EMPATE           = auto()
    INTERRUMPIDO     = auto()


class Accion(Enum):
    ATAQUE_BASICO    = 1
    HABILIDAD_ESPECIAL = 2
    DEFENDER         = 3
    CONCENTRAR       = 4


class ResultadoAccion:
    """Resultado de la acción de UN personaje en su turno."""
    def __init__(self):
        self.actor_nombre: str = ""
        self.actor_equipo: int = 0          # 1 o 2
        self.objetivo_nombre: str = ""
        self.objetivo_equipo: int = 0
        self.descripcion: str = ""
        self.daño: int = 0
        self.curacion: int = 0
        self.es_ia: bool = False
        self.evento_aleatorio: Optional[Dict] = None
        self.mensajes_extra: List[str] = []


class ResultadoRound:
    """Agrupa todas las acciones de un round completo."""
    def __init__(self, numero: int):
        self.numero = numero
        self.acciones: List[ResultadoAccion] = []

    def add(self, accion: ResultadoAccion):
        self.acciones.append(accion)


class ResultadoCombate:
    def __init__(self):
        self.estado: EstadoCombate = EstadoCombate.INTERRUMPIDO
        self.rounds_totales: int = 0
        self.ganador_equipo: int = 0
        self.mensaje_final: str = ""
        self.historial: List[ResultadoRound] = []


# ─
# Ayuda: selección inteligente de objetivo y aliados
# ─

def _vivos(equipo: List) -> List:
    return [p for p in equipo if p.esta_vivo()]


def _objetivo_ia(atacante, equipo_rival: List):
    """La IA elige el rival con menos vida relativa."""
    vivos = _vivos(equipo_rival)
    if not vivos:
        return None
    return min(vivos, key=lambda p: p.vida_actual / p.vida_maxima)


def _aliado_ia(actor, equipo_propio: List):
    """La IA elige al aliado más herido (puede ser sí mismo)."""
    vivos = _vivos(equipo_propio)
    if not vivos:
        return actor
    return min(vivos, key=lambda p: p.vida_actual / p.vida_maxima)


# ─
# Clase principal
# ─

class CombateEquipo:
    def __init__(self, equipo1: List, equipo2: List,
                 prob_evento: float = 0.12, max_rounds: int = 80):
        self.equipo1 = equipo1   # lista de personajes
        self.equipo2 = equipo2
        self.prob_evento = prob_evento
        self.max_rounds = max_rounds

        self.round_actual = 0
        self.estado = EstadoCombate.EN_CURSO
        self.historial: List[ResultadoRound] = []

        # Cola de turno del round en curso
        self._cola_turno: List = []
        # Quién es el "activo" esperando acción del jugador
        self._turno_idx: int = 0

        # Candado anti-doble-turno: IDs de personajes que ya actuaron este round.
        self._ya_actuaron: set = set()

        # Para el sistema de GUI: track del personaje que está actuando
        self.personaje_activo = None
        self._round_en_curso: Optional[ResultadoRound] = None

        self._inicializar_personajes()
        self._iniciar_round()

    def _inicializar_personajes(self):
        for p in self.equipo1 + self.equipo2:
            p.estados = [e for e in p.estados
                         if e not in ["defendiendo", "esquivando", "concentrando"]]
            p.energia_actual = p.energia_maxima

    # ─
    # Gestión de rounds y cola de turnos
    # ─

    def _iniciar_round(self):
        self.round_actual += 1
        self._round_en_curso = ResultadoRound(self.round_actual)
        self._ya_actuaron = set()   # reset del candado para el nuevo round

        # Cola ordenada por velocidad + varianza aleatoria.
        # Alternamos la varianza según paridad del round para evitar
        # que el mismo personaje salga siempre primero.
        todos = [p for p in self.equipo1 + self.equipo2 if p.esta_vivo()]
        varianza = 0.12 if self.round_actual % 2 == 0 else 0.10
        self._cola_turno = sorted(
            todos,
            key=lambda p: p.velocidad * random.uniform(1 - varianza, 1 + varianza),
            reverse=True
        )
        self._turno_idx = 0

        # Protección: si la cola queda vacía, verificar fin de combate
        # para evitar que el bucle de IA quede sin personajes que procesar.
        if not self._cola_turno:
            self._verificar_fin_combate()
        # Saltar automáticamente los IA hasta encontrar un jugador humano
        # (o ejecutar toda la IA si todos son IA)

    def _avanzar_turno(self):
        """Mueve al siguiente personaje vivo Y que no haya actuado ya."""
        self._turno_idx += 1
        while self._turno_idx < len(self._cola_turno):
            p = self._cola_turno[self._turno_idx]
            if p.esta_vivo() and id(p) not in self._ya_actuaron:
                break
            self._turno_idx += 1

    def _fin_round(self) -> bool:
        """Retorna True si el round ha terminado (todos actuaron)."""
        return self._turno_idx >= len(self._cola_turno)

    @property
    def personaje_turno_actual(self):
        if self._turno_idx < len(self._cola_turno):
            p = self._cola_turno[self._turno_idx]
            # Doble candado: debe estar vivo Y no haber actuado ya
            if p.esta_vivo() and id(p) not in self._ya_actuaron:
                return p
        return None

    def equipo_de(self, personaje) -> int:
        """Retorna 1 o 2 según el equipo del personaje."""
        if personaje in self.equipo1:
            return 1
        return 2

    def equipo_rival_de(self, personaje) -> List:
        if personaje in self.equipo1:
            return self.equipo2
        return self.equipo1

    def equipo_propio_de(self, personaje) -> List:
        if personaje in self.equipo1:
            return self.equipo1
        return self.equipo2

    # ─
    # Ejecución de acciones
    # ─

    def ejecutar_accion_jugador(self, accion: Accion,
                                 objetivo=None,
                                 indice_habilidad: Optional[int] = None
                                 ) -> ResultadoAccion:
        """
        Ejecuta la acción del jugador humano (personaje_turno_actual).
        objetivo: personaje objetivo (puede ser aliado para curar).
        Retorna el ResultadoAccion y avanza el turno.
        """
        actor = self.personaje_turno_actual
        if actor is None:
            raise ValueError("No hay personaje activo")

        resultado = self._ejecutar_accion_interna(actor, accion, objetivo, indice_habilidad)
        self._round_en_curso.add(resultado)
        self._post_accion(actor)
        return resultado

    def ejecutar_acciones_ia_hasta_jugador(self) -> List[ResultadoAccion]:
        """
        Ejecuta las acciones de IA consecutivas dentro del round ACTUAL
        hasta encontrar un personaje controlado por jugador.

        IMPORTANTE: el bucle se detiene al finalizar el round actual aunque
        no haya encontrado un jugador. De este modo la llamada siempre es
        acotada (máximo N acciones donde N = personajes vivos), evitando
        bucles infinitos cuando no quedan jugadores humanos.

        La escena debe comprobar si el combate ha terminado o si el próximo
        en actuar sigue siendo IA (y volver a llamar en el siguiente ciclo).
        """
        resultados = []
        round_inicio = self.round_actual   # capturamos el round al entrar

        while True:
            # Parar si el combate ha terminado
            if self.estado != EstadoCombate.EN_CURSO:
                break

            # Parar si hemos cruzado a un nuevo round (ocurre dentro de
            # _post_accion cuando se llama _iniciar_round)
            if self.round_actual != round_inicio:
                break

            p = self.personaje_turno_actual
            if p is None:
                break           # fin del round actual (todos actuaron)
            if not p.es_ia:
                break           # turno del jugador humano

            resultado = self._ejecutar_accion_interna_ia(p)
            self._round_en_curso.add(resultado)
            resultados.append(resultado)
            self._post_accion(p)

        return resultados

    def _post_accion(self, actor=None):
        """Tras cada acción: marcar actor, verificar fin, avanzar turno."""
        # Registrar en el candado para que no vuelva a actuar este round
        if actor is not None:
            self._ya_actuaron.add(id(actor))
        self._verificar_fin_combate()
        if self.estado != EstadoCombate.EN_CURSO:
            self.historial.append(self._round_en_curso)
            return

        self._avanzar_turno()

        if self._fin_round():
            # Efectos de fin de round: regeneración, estados
            self._aplicar_regeneracion()
            self._aplicar_efectos_estados()
            # Evento aleatorio
            if EVENTOS_NORMALES and random.random() < self.prob_evento:
                self._activar_evento_aleatorio()

            self._verificar_fin_combate()
            self.historial.append(self._round_en_curso)

            if self.estado == EstadoCombate.EN_CURSO:
                if self.round_actual >= self.max_rounds:
                    self.estado = EstadoCombate.EMPATE
                    return
                self._iniciar_round()

    # ─
    # Lógica interna de acción
    # ─

    def _ejecutar_accion_interna(self, actor, accion: Accion,
                                  objetivo, indice_habilidad) -> ResultadoAccion:
        ra = ResultadoAccion()
        ra.actor_nombre = actor.nombre
        ra.actor_equipo = self.equipo_de(actor)
        ra.es_ia = getattr(actor, 'es_ia', False)

        equipo_rival = self.equipo_rival_de(actor)
        equipo_propio = self.equipo_propio_de(actor)

        # Estados que impiden actuar
        if "dormido" in actor.estados:
            ra.descripcion = f"{actor.nombre} está dormido y pierde el turno."
            return ra
        if "paralizado" in actor.estados and random.random() < 0.5:
            ra.descripcion = f"{actor.nombre} está paralizado y no puede moverse."
            return ra

        # Confusión: 30% ataca a sí mismo
        if "confundido" in actor.estados and random.random() < 0.3:
            objetivo = actor
            ra.mensajes_extra.append(f"¡{actor.nombre} está confundido y se ataca a sí mismo!")

        # Si no se proporcionó objetivo, asignar uno por defecto
        if objetivo is None:
            objetivo = _objetivo_ia(actor, equipo_rival) or actor

        ra.objetivo_nombre = objetivo.nombre
        ra.objetivo_equipo = self.equipo_de(objetivo)

        if accion == Accion.ATAQUE_BASICO:
            res = actor.atacar_basico(objetivo)
            ra.daño = res.get("daño", 0)
            ra.descripcion = f"{actor.nombre} ataca a {objetivo.nombre}."

        elif accion == Accion.HABILIDAD_ESPECIAL:
            if (indice_habilidad is not None and
                    0 <= indice_habilidad < len(actor.habilidades)):
                habilidad = actor.habilidades[indice_habilidad]
                # Curaciones: verificar que el objetivo sea aliado
                if getattr(habilidad, 'es_curacion', False):
                    if self.equipo_de(objetivo) != ra.actor_equipo:
                        # Redirigir al aliado más herido
                        objetivo = _aliado_ia(actor, equipo_propio)
                        ra.objetivo_nombre = objetivo.nombre
                        ra.objetivo_equipo = self.equipo_de(objetivo)
                        ra.mensajes_extra.append(
                            f"(La curación se redirigió al aliado {objetivo.nombre})"
                        )
                if actor.energia_actual >= habilidad.costo_energia:
                    res = actor.usar_habilidad(indice_habilidad, objetivo)
                    ra.daño = res.get("daño", 0)
                    ra.curacion = res.get("curacion", 0)
                    ra.descripcion = f"{actor.nombre} usa '{habilidad.nombre}' en {objetivo.nombre}."
                else:
                    res = actor.atacar_basico(objetivo)
                    ra.daño = res.get("daño", 0)
                    ra.descripcion = f"{actor.nombre} no tiene energía suficiente y ataca."
            else:
                res = actor.atacar_basico(objetivo)
                ra.daño = res.get("daño", 0)
                ra.descripcion = f"{actor.nombre} ataca (habilidad no válida)."

        elif accion == Accion.DEFENDER:
            actor.defender()
            ra.descripcion = f"{actor.nombre} se pone en guardia."

        elif accion == Accion.CONCENTRAR:
            actor.concentrar()
            ra.descripcion = f"{actor.nombre} se concentra y recupera energía."

        return ra

    def _ejecutar_accion_interna_ia(self, ia) -> ResultadoAccion:
        """IA decide qué hacer automáticamente."""
        ra = ResultadoAccion()
        ra.actor_nombre = ia.nombre
        ra.actor_equipo = self.equipo_de(ia)
        ra.es_ia = True

        equipo_rival  = self.equipo_rival_de(ia)
        equipo_propio = self.equipo_propio_de(ia)

        # Estados bloqueantes
        if "dormido" in ia.estados:
            ra.descripcion = f"{ia.nombre} está dormido y pierde el turno."
            return ra
        if "paralizado" in ia.estados and random.random() < 0.5:
            ra.descripcion = f"{ia.nombre} está paralizado."
            return ra

        objetivo_rival  = _objetivo_ia(ia, equipo_rival)
        objetivo_aliado = _aliado_ia(ia, equipo_propio)

        # Sin energía: concentrar
        if ia.energia_actual < 25:
            ia.concentrar()
            ra.descripcion = f"{ia.nombre} recupera energía."
            ra.objetivo_nombre = ia.nombre
            ra.objetivo_equipo = ra.actor_equipo
            return ra

        # Vida baja: intentar curar a aliado o a sí mismo
        if ia.vida_actual < ia.vida_maxima * 0.45:
            for idx, hab in enumerate(ia.habilidades):
                if getattr(hab, 'es_curacion', False) and ia.energia_actual >= hab.costo_energia:
                    objetivo = objetivo_aliado
                    res = ia.usar_habilidad(idx, objetivo)
                    ra.objetivo_nombre = objetivo.nombre
                    ra.objetivo_equipo = self.equipo_de(objetivo)
                    ra.curacion = res.get("curacion", 0)
                    ra.descripcion = f"{ia.nombre} usa '{hab.nombre}' en {objetivo.nombre}."
                    return ra

        # Usar habilidad ofensiva si hay energía
        if ia.energia_actual > 45 and random.random() < 0.65:
            ofensivas = [
                i for i, h in enumerate(ia.habilidades)
                if any(t in h.tipo for t in ["ofensiva", "daño", "fuerza"])
                and not getattr(h, 'es_curacion', False)
                and ia.energia_actual >= h.costo_energia
            ]
            if ofensivas and objetivo_rival:
                idx = random.choice(ofensivas)
                objetivo = objetivo_rival
                res = ia.usar_habilidad(idx, objetivo)
                ra.objetivo_nombre = objetivo.nombre
                ra.objetivo_equipo = self.equipo_de(objetivo)
                ra.daño = res.get("daño", 0)
                ra.descripcion = f"{ia.nombre} usa '{ia.habilidades[idx].nombre}' en {objetivo.nombre}."
                return ra

        # Ataque básico
        if objetivo_rival:
            res = ia.atacar_basico(objetivo_rival)
            ra.objetivo_nombre = objetivo_rival.nombre
            ra.objetivo_equipo = self.equipo_de(objetivo_rival)
            ra.daño = res.get("daño", 0)
            ra.descripcion = f"{ia.nombre} ataca a {objetivo_rival.nombre}."
        else:
            ia.concentrar()
            ra.descripcion = f"{ia.nombre} espera."

        return ra

    # ─
    # Fin de round y verificaciones
    # ─

    def _aplicar_regeneracion(self):
        for p in self.equipo1 + self.equipo2:
            if p.esta_vivo():
                p.energia_actual = min(p.energia_maxima,
                                       p.energia_actual + random.randint(8, 14))
                p.regenerar()

    def _aplicar_efectos_estados(self):
        estados_daño = {"quemado": 5, "sangrando": 3, "envenenado": 7}
        for p in self.equipo1 + self.equipo2:
            if not p.esta_vivo():
                continue
            for estado, daño in estados_daño.items():
                if estado in p.estados:
                    p.recibir_dano(daño, estado)
            if "bajon_azucar" in p.estados:
                p.energia_actual = max(0, p.energia_actual - 10)
                p.velocidad = max(5, p.velocidad - 5)
            p.actualizar_estados()

    def _activar_evento_aleatorio(self):
        if not EVENTOS_NORMALES:
            return
        rand = random.random()
        if rand < 0.70:
            clase = random.choice(EVENTOS_NORMALES)
        elif rand < 0.95:
            clase = random.choice(EVENTOS_RAROS)
        else:
            clase = random.choice(EVENTOS_ULTRA_RAROS)
        # Aplica a un personaje aleatorio vivo
        todos = [p for p in self.equipo1 + self.equipo2 if p.esta_vivo()]
        if len(todos) >= 2:
            p1, p2 = random.sample(todos, 2)
            clase().activar(p1, p2, self.round_actual)

    def _verificar_fin_combate(self):
        vivos1 = _vivos(self.equipo1)
        vivos2 = _vivos(self.equipo2)
        if not vivos1 and not vivos2:
            self.estado = EstadoCombate.EMPATE
        elif not vivos1:
            self.estado = EstadoCombate.VICTORIA_EQUIPO2
        elif not vivos2:
            self.estado = EstadoCombate.VICTORIA_EQUIPO1

    # ─
    # Resultado final
    # ─

    def obtener_resultado_final(self) -> ResultadoCombate:
        rc = ResultadoCombate()
        rc.estado = self.estado
        rc.rounds_totales = self.round_actual
        rc.historial = self.historial

        if self.estado == EstadoCombate.VICTORIA_EQUIPO1:
            rc.ganador_equipo = 1
            rc.mensaje_final = "¡VICTORIA DEL EQUIPO 1!"
        elif self.estado == EstadoCombate.VICTORIA_EQUIPO2:
            rc.ganador_equipo = 2
            rc.mensaje_final = "¡VICTORIA DEL EQUIPO 2!"
        elif self.estado == EstadoCombate.EMPATE:
            rc.mensaje_final = "¡EMPATE! Ambos equipos caen."
        else:
            rc.mensaje_final = "Combate interrumpido."

        return rc