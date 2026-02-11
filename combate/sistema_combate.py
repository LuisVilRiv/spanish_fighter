"""
sistema_combate.py - Sistema de combate por turnos.
(Se mantiene igual que en la versión anterior, con los balanceos aplicados,
 pero se asegura que mostrar_resumen_turno siempre se llame)
"""

import random
import time
from enum import Enum, auto
from typing import Optional, Dict, Any, List, Tuple

from utils import Colores as C

try:
    from ..eventos import (
        EVENTOS_NORMALES, EVENTOS_RAROS, EVENTOS_ULTRA_RAROS,
        TODOS_LOS_EVENTOS
    )
except ImportError:
    from eventos import (
        EVENTOS_NORMALES, EVENTOS_RAROS, EVENTOS_ULTRA_RAROS,
        TODOS_LOS_EVENTOS
    )

class EstadoCombate(Enum):
    EN_CURSO = auto()
    VICTORIA_JUGADOR = auto()
    VICTORIA_IA = auto()
    EMPATE = auto()
    INTERRUMPIDO = auto()

class Accion(Enum):
    ATAQUE_BASICO = 1
    HABILIDAD_ESPECIAL = 2
    DEFENDER = 3
    CONCENTRAR = 4

class ResultadoTurno:
    def __init__(self):
        self.jugador_accion: Optional[str] = None
        self.ia_accion: Optional[str] = None
        self.daño_jugador_a_ia: int = 0
        self.daño_ia_a_jugador: int = 0
        self.curacion_jugador: int = 0
        self.curacion_ia: int = 0
        self.evento_aleatorio: Optional[Dict[str, Any]] = None
        self.mensajes: List[str] = []
        self.jugador_vida_actual: int = 0
        self.ia_vida_actual: int = 0
        self.jugador_energia_actual: int = 0
        self.ia_energia_actual: int = 0

class ResultadoCombate:
    def __init__(self):
        self.estado: EstadoCombate = EstadoCombate.INTERRUMPIDO
        self.turnos_totales: int = 0
        self.daño_total_jugador: int = 0
        self.daño_total_ia: int = 0
        self.eventos_ocurridos: int = 0
        self.ganador: Optional[str] = None
        self.perdedor: Optional[str] = None
        self.experiencia_ganada: int = 0
        self.mensaje_final: str = ""

class Combate:
    def __init__(self, jugador, ia, probabilidad_evento: float = 0.15, max_turnos: int = 100):
        self.jugador = jugador
        self.ia = ia
        self.ia.es_ia = True
        self.probabilidad_evento = probabilidad_evento
        self.max_turnos = max_turnos
        self.turno_actual = 0
        self.historial: List[ResultadoTurno] = []
        self.daño_total_jugador = 0
        self.daño_total_ia = 0
        self.eventos_ocurridos = 0
        self.estado = EstadoCombate.EN_CURSO
        self._inicializar_personajes()

    def _inicializar_personajes(self):
        self.jugador.estados = [e for e in self.jugador.estados if e not in ["defendiendo", "esquivando", "concentrando"]]
        self.ia.estados = [e for e in self.ia.estados if e not in ["defendiendo", "esquivando", "concentrando"]]
        self.jugador.energia_actual = self.jugador.energia_maxima
        self.ia.energia_actual = self.ia.energia_maxima

    def mostrar_intro_combate(self):
        print(f"\n{C.NEGRITA}{C.ROJO_BRILLANTE}+---------------------------------------------------+{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}|     ¡COMIENZA LA BATALLA CÓMICA ESPAÑOLA!         |{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}+---------------------------------------------------+{C.RESET}")
        print(f"\n{C.NEGRITA}{C.CYAN}JUGADOR:{C.RESET} {self.jugador.nombre} {self.jugador.tipo}")
        print(f"{C.NEGRITA}{C.CYAN}VS{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO}IA:{C.RESET} {self.ia.nombre} {self.ia.tipo}")
        print(f"\n{C.AMARILLO}¡Que gane el más español!{C.RESET}")
        print(f"{C.CYAN}─────────────────────────────────────────────────{C.RESET}")

    def ejecutar_turno(self, accion_jugador: Accion, indice_habilidad: Optional[int] = None) -> ResultadoTurno:
        if self.estado != EstadoCombate.EN_CURSO:
            raise ValueError("El combate ya ha terminado")

        self.turno_actual += 1
        resultado = ResultadoTurno()

        print(f"\n{C.NEGRITA}{C.AMARILLO}========== TURNO {self.turno_actual} =========={C.RESET}")

        velocidad_jugador = self.jugador.velocidad * random.uniform(0.9, 1.1)
        velocidad_ia = self.ia.velocidad * random.uniform(0.9, 1.1)

        if velocidad_jugador >= velocidad_ia:
            resultado_jugador = self._ejecutar_accion(self.jugador, self.ia, accion_jugador, indice_habilidad)
            resultado.jugador_accion = resultado_jugador.get("mensaje", "")
            self._actualizar_resultado_jugador(resultado, resultado_jugador)

            if not self.ia.esta_vivo():
                resultado.ia_vida_actual = 0
                resultado.jugador_vida_actual = self.jugador.vida_actual
                resultado.jugador_energia_actual = self.jugador.energia_actual
                resultado.ia_energia_actual = self.ia.energia_actual
                resultado.mensajes.append(f"{C.ROJO_BRILLANTE}¡{self.ia.nombre} ha sido derrotado!{C.RESET}")
                self._verificar_fin_combate()
                return resultado

            resultado_ia = self._ejecutar_accion_ia()
            resultado.ia_accion = resultado_ia.get("mensaje", "")
            self._actualizar_resultado_ia(resultado, resultado_ia)

            if not self.jugador.esta_vivo():
                resultado.jugador_vida_actual = 0
                resultado.ia_vida_actual = self.ia.vida_actual
                resultado.jugador_energia_actual = self.jugador.energia_actual
                resultado.ia_energia_actual = self.ia.energia_actual
                resultado.mensajes.append(f"{C.ROJO_BRILLANTE}¡{self.jugador.nombre} ha sido derrotado!{C.RESET}")
                self._verificar_fin_combate()
                return resultado
        else:
            resultado_ia = self._ejecutar_accion_ia()
            resultado.ia_accion = resultado_ia.get("mensaje", "")
            self._actualizar_resultado_ia(resultado, resultado_ia)

            if not self.jugador.esta_vivo():
                resultado.jugador_vida_actual = 0
                resultado.ia_vida_actual = self.ia.vida_actual
                resultado.jugador_energia_actual = self.jugador.energia_actual
                resultado.ia_energia_actual = self.ia.energia_actual
                resultado.mensajes.append(f"{C.ROJO_BRILLANTE}¡{self.jugador.nombre} ha sido derrotado!{C.RESET}")
                self._verificar_fin_combate()
                return resultado

            resultado_jugador = self._ejecutar_accion(self.jugador, self.ia, accion_jugador, indice_habilidad)
            resultado.jugador_accion = resultado_jugador.get("mensaje", "")
            self._actualizar_resultado_jugador(resultado, resultado_jugador)

            if not self.ia.esta_vivo():
                resultado.ia_vida_actual = 0
                resultado.jugador_vida_actual = self.jugador.vida_actual
                resultado.jugador_energia_actual = self.jugador.energia_actual
                resultado.ia_energia_actual = self.ia.energia_actual
                resultado.mensajes.append(f"{C.ROJO_BRILLANTE}¡{self.ia.nombre} ha sido derrotado!{C.RESET}")
                self._verificar_fin_combate()
                return resultado

        self._aplicar_regeneracion(resultado)

        if random.random() < self.probabilidad_evento:
            evento_resultado = self._activar_evento_aleatorio()
            resultado.evento_aleatorio = evento_resultado
            resultado.mensajes.append(evento_resultado.get("mensaje", ""))
            self.eventos_ocurridos += 1

        self._aplicar_efectos_estados(resultado)

        resultado.jugador_vida_actual = self.jugador.vida_actual
        resultado.ia_vida_actual = self.ia.vida_actual
        resultado.jugador_energia_actual = self.jugador.energia_actual
        resultado.ia_energia_actual = self.ia.energia_actual

        self._verificar_fin_combate()
        self.historial.append(resultado)
        return resultado

    def _ejecutar_accion(self, atacante, objetivo, accion: Accion, indice_habilidad: Optional[int] = None) -> Dict[str, Any]:
        if "dormido" in atacante.estados:
            return {
                "exito": False,
                "mensaje": f"{atacante.nombre} está dormido y pierde el turno.",
                "tipo": "estado",
                "dormido": True
            }
        if "paralizado" in atacante.estados:
            if random.random() < 0.5:
                return {
                    "exito": False,
                    "mensaje": f"{atacante.nombre} está paralizado y no puede moverse.",
                    "tipo": "estado",
                    "paralizado": True
                }
        if "confundido" in atacante.estados:
            if random.random() < 0.3:
                objetivo = atacante
                mensaje_confusion = f" ¡Está confundido y se ataca a sí mismo!"
            else:
                mensaje_confusion = f" (a pesar de estar confundido)"
        else:
            mensaje_confusion = ""

        if accion == Accion.ATAQUE_BASICO:
            resultado = atacante.atacar_basico(objetivo)
            resultado["mensaje"] = f"{atacante.nombre} ataca a {objetivo.nombre}.{mensaje_confusion}"
        elif accion == Accion.HABILIDAD_ESPECIAL:
            if indice_habilidad is None or indice_habilidad < 0 or indice_habilidad >= len(atacante.habilidades):
                resultado = atacante.atacar_basico(objetivo)
                resultado["mensaje"] = f"{atacante.nombre} intenta usar una habilidad pero falla. En su lugar ataca.{mensaje_confusion}"
            else:
                resultado = atacante.usar_habilidad(indice_habilidad, objetivo)
                if resultado["exito"]:
                    habilidad = atacante.habilidades[indice_habilidad]
                    resultado["mensaje"] = f"{atacante.nombre} usa '{habilidad.nombre}' en {objetivo.nombre}.{mensaje_confusion}"
                else:
                    resultado = atacante.atacar_basico(objetivo)
                    resultado["mensaje"] = f"{atacante.nombre} intenta usar una habilidad pero falla. En su lugar ataca.{mensaje_confusion}"
        elif accion == Accion.DEFENDER:
            resultado = atacante.defender()
            resultado["mensaje"] = f"{atacante.nombre} se prepara para defender."
        elif accion == Accion.CONCENTRAR:
            resultado = atacante.concentrar()
            resultado["mensaje"] = f"{atacante.nombre} se concentra para recuperar energía."
        else:
            resultado = atacante.atacar_basico(objetivo)
            resultado["mensaje"] = f"{atacante.nombre} no sabe qué hacer y ataca por instinto.{mensaje_confusion}"

        if "daño" in resultado:
            if atacante == self.jugador:
                self.daño_total_jugador += resultado["daño"]
            else:
                self.daño_total_ia += resultado["daño"]
        return resultado

    def _ejecutar_accion_ia(self) -> Dict[str, Any]:
        ia = self.ia
        jugador = self.jugador

        if ia.energia_actual < 30:
            resultado = ia.concentrar()
            resultado["mensaje"] = f"{ia.nombre} se concentra para recuperar energía."
            return resultado

        if ia.vida_actual < ia.vida_maxima * 0.4:
            habilidades_curativas = []
            for i, habilidad in enumerate(ia.habilidades):
                if hasattr(habilidad, 'es_curacion') and habilidad.es_curacion:
                    habilidades_curativas.append(i)
            if habilidades_curativas and ia.energia_actual >= 20:
                indice = random.choice(habilidades_curativas)
                resultado = ia.usar_habilidad(indice, ia)
                if resultado.get("exito", False):
                    habilidad = ia.habilidades[indice]
                    resultado["mensaje"] = f"{ia.nombre} usa '{habilidad.nombre}' en sí mismo."
                else:
                    resultado = ia.atacar_basico(jugador)
                    resultado["mensaje"] = f"{ia.nombre} intenta curarse pero falla. Ataca en su lugar."
                return resultado

        if "defendiendo" in jugador.estados:
            habilidades_especiales = []
            for i, habilidad in enumerate(ia.habilidades):
                if any(palabra in habilidad.tipo for palabra in ["estado", "especial", "verdad"]):
                    habilidades_especiales.append(i)
            if habilidades_especiales:
                indice = random.choice(habilidades_especiales)
                if ia.energia_actual >= ia.habilidades[indice].costo_energia:
                    resultado = ia.usar_habilidad(indice, jugador)
                    if resultado.get("exito", False):
                        habilidad = ia.habilidades[indice]
                        resultado["mensaje"] = f"{ia.nombre} usa '{habilidad.nombre}' en {jugador.nombre}."
                    else:
                        resultado = ia.atacar_basico(jugador)
                        resultado["mensaje"] = f"{ia.nombre} intenta usar una habilidad pero falla. Ataca en su lugar."
                    return resultado

        if ia.energia_actual > 50 and random.random() < 0.7:
            habilidades_ofensivas = []
            for i, habilidad in enumerate(ia.habilidades):
                if any(palabra in habilidad.tipo for palabra in ["ofensiva", "daño", "fuerza"]):
                    habilidades_ofensivas.append(i)
            if habilidades_ofensivas:
                indice = random.choice(habilidades_ofensivas)
                if ia.energia_actual >= ia.habilidades[indice].costo_energia:
                    resultado = ia.usar_habilidad(indice, jugador)
                    if resultado.get("exito", False):
                        habilidad = ia.habilidades[indice]
                        resultado["mensaje"] = f"{ia.nombre} usa '{habilidad.nombre}' en {jugador.nombre}."
                    else:
                        resultado = ia.atacar_basico(jugador)
                        resultado["mensaje"] = f"{ia.nombre} intenta usar una habilidad pero falla. Ataca en su lugar."
                    return resultado

        resultado = ia.atacar_basico(jugador)
        resultado["mensaje"] = f"{ia.nombre} ataca a {jugador.nombre}."
        return resultado

    def _actualizar_resultado_jugador(self, resultado: ResultadoTurno, accion_resultado: Dict[str, Any]):
        if "daño" in accion_resultado:
            resultado.daño_jugador_a_ia = accion_resultado["daño"]
        if "curacion" in accion_resultado:
            resultado.curacion_jugador = accion_resultado["curacion"]

    def _actualizar_resultado_ia(self, resultado: ResultadoTurno, accion_resultado: Dict[str, Any]):
        if "daño" in accion_resultado:
            resultado.daño_ia_a_jugador = accion_resultado["daño"]
        if "curacion" in accion_resultado:
            resultado.curacion_ia = accion_resultado["curacion"]

    def _aplicar_regeneracion(self, resultado: ResultadoTurno):
        self.jugador.energia_actual = min(self.jugador.energia_maxima, self.jugador.energia_actual + random.randint(10, 15))
        self.ia.energia_actual = min(self.ia.energia_maxima, self.ia.energia_actual + random.randint(10, 15))
        self.jugador.regenerar()
        self.ia.regenerar()

    def _activar_evento_aleatorio(self) -> Dict[str, Any]:
        rand = random.random()
        if rand < 0.70:
            clase_evento = random.choice(EVENTOS_NORMALES)
        elif rand < 0.95:
            clase_evento = random.choice(EVENTOS_RAROS)
        else:
            clase_evento = random.choice(EVENTOS_ULTRA_RAROS)
        evento = clase_evento()
        return evento.activar(self.jugador, self.ia, self.turno_actual)

    def _aplicar_efectos_estados(self, resultado: ResultadoTurno):
        mensajes_estados = []

        if "quemado" in self.jugador.estados:
            daño = 5
            self.jugador.recibir_dano(daño, "quemadura")
            mensajes_estados.append(f"{self.jugador.nombre} sufre {daño} de daño por quemadura.")
        if "sangrando" in self.jugador.estados:
            daño = 3
            self.jugador.recibir_dano(daño, "sangrado")
            mensajes_estados.append(f"{self.jugador.nombre} pierde {daño} de vida por sangrado.")
        if "envenenado" in self.jugador.estados:
            daño = 7
            self.jugador.recibir_dano(daño, "veneno")
            mensajes_estados.append(f"{self.jugador.nombre} sufre {daño} de daño por veneno.")
        if "bajon_azucar" in self.jugador.estados:
            perdida_energia = 10
            reduccion_velocidad = 5
            self.jugador.energia_actual = max(0, self.jugador.energia_actual - perdida_energia)
            self.jugador.velocidad = max(5, self.jugador.velocidad - reduccion_velocidad)
            mensajes_estados.append(f"{self.jugador.nombre} sufre bajón de azúcar: energía -{perdida_energia}, velocidad -{reduccion_velocidad}.")

        if "quemado" in self.ia.estados:
            daño = 5
            self.ia.recibir_dano(daño, "quemadura")
            mensajes_estados.append(f"{self.ia.nombre} sufre {daño} de daño por quemadura.")
        if "sangrando" in self.ia.estados:
            daño = 3
            self.ia.recibir_dano(daño, "sangrado")
            mensajes_estados.append(f"{self.ia.nombre} pierde {daño} de vida por sangrado.")
        if "envenenado" in self.ia.estados:
            daño = 7
            self.ia.recibir_dano(daño, "veneno")
            mensajes_estados.append(f"{self.ia.nombre} sufre {daño} de daño por veneno.")
        if "bajon_azucar" in self.ia.estados:
            perdida_energia = 10
            reduccion_velocidad = 5
            self.ia.energia_actual = max(0, self.ia.energia_actual - perdida_energia)
            self.ia.velocidad = max(5, self.ia.velocidad - reduccion_velocidad)
            mensajes_estados.append(f"{self.ia.nombre} sufre bajón de azúcar: energía -{perdida_energia}, velocidad -{reduccion_velocidad}.")

        self.jugador.actualizar_estados()
        self.ia.actualizar_estados()

        if mensajes_estados:
            resultado.mensajes.extend(mensajes_estados)

    def _verificar_fin_combate(self):
        jugador_vivo = self.jugador.esta_vivo()
        ia_vivo = self.ia.esta_vivo()

        if not jugador_vivo and not ia_vivo:
            self.estado = EstadoCombate.EMPATE
        elif not jugador_vivo:
            self.estado = EstadoCombate.VICTORIA_IA
        elif not ia_vivo:
            self.estado = EstadoCombate.VICTORIA_JUGADOR
        elif self.turno_actual >= self.max_turnos:
            self.estado = EstadoCombate.EMPATE

    def obtener_resultado_final(self) -> ResultadoCombate:
        resultado = ResultadoCombate()
        resultado.estado = self.estado
        resultado.turnos_totales = self.turno_actual
        resultado.daño_total_jugador = self.daño_total_jugador
        resultado.daño_total_ia = self.daño_total_ia
        resultado.eventos_ocurridos = self.eventos_ocurridos

        if self.estado == EstadoCombate.VICTORIA_JUGADOR:
            resultado.ganador = self.jugador.nombre
            resultado.perdedor = self.ia.nombre
            resultado.experiencia_ganada = self._calcular_experiencia()
            resultado.mensaje_final = (
                f"{C.VERDE_BRILLANTE}+---------------------------------------------------+\n"
                f"|         ¡VICTORIA DEL JUGADOR!                  |\n"
                f"|     {self.jugador.nombre} ha derrotado a {self.ia.nombre}    |\n"
                f"+---------------------------------------------------+{C.RESET}"
            )
        elif self.estado == EstadoCombate.VICTORIA_IA:
            resultado.ganador = self.ia.nombre
            resultado.perdedor = self.jugador.nombre
            resultado.mensaje_final = (
                f"{C.ROJO_BRILLANTE}+---------------------------------------------------+\n"
                f"|          ¡VICTORIA DE LA IA!                    |\n"
                f"|     {self.ia.nombre} ha derrotado a {self.jugador.nombre}    |\n"
                f"+---------------------------------------------------+{C.RESET}"
            )
        elif self.estado == EstadoCombate.EMPATE:
            resultado.mensaje_final = (
                f"{C.AMARILLO}+---------------------------------------------------+\n"
                f"|               ¡EMPATE!                        |\n"
                f"|      Ambos combatientes caen exhaustos        |\n"
                f"+---------------------------------------------------+{C.RESET}"
            )
        else:
            resultado.mensaje_final = f"{C.CYAN}Combate interrumpido.{C.RESET}"
        return resultado

    def _calcular_experiencia(self) -> int:
        base = 100
        if self.turno_actual < 10:
            bonus_rapidez = 50
        elif self.turno_actual < 20:
            bonus_rapidez = 30
        elif self.turno_actual < 30:
            bonus_rapidez = 15
        else:
            bonus_rapidez = 0
        bonus_eventos = self.eventos_ocurridos * 5
        bonus_daño = self.daño_total_jugador // 10
        vida_perdida = self.jugador.vida_maxima - self.jugador.vida_actual
        bonus_defensa = 20 if vida_perdida < self.jugador.vida_maxima * 0.3 else 0
        return base + bonus_rapidez + bonus_eventos + bonus_daño + bonus_defensa

    def mostrar_resumen_turno(self, resultado: ResultadoTurno):
        print(f"\n{C.CYAN}────────── RESUMEN DEL TURNO ──────────{C.RESET}")
        if resultado.jugador_accion:
            print(f"{C.VERDE}- {resultado.jugador_accion}{C.RESET}")
        if resultado.ia_accion:
            print(f"{C.ROJO}- {resultado.ia_accion}{C.RESET}")
        if resultado.daño_jugador_a_ia > 0:
            print(f"{C.VERDE}  → Daño a IA: {resultado.daño_jugador_a_ia}{C.RESET}")
        if resultado.daño_ia_a_jugador > 0:
            print(f"{C.ROJO}  → Daño a jugador: {resultado.daño_ia_a_jugador}{C.RESET}")
        if resultado.curacion_jugador > 0:
            print(f"{C.VERDE}  → Curación jugador: {resultado.curacion_jugador}{C.RESET}")
        if resultado.curacion_ia > 0:
            print(f"{C.ROJO}  → Curación IA: {resultado.curacion_ia}{C.RESET}")
        if resultado.evento_aleatorio:
            print(f"\n{C.MAGENTA}¡EVENTO ALEATORIO!{C.RESET}")
            print(f"{resultado.evento_aleatorio.get('mensaje', '')}")
        for mensaje in resultado.mensajes:
            print(f"{C.CYAN}  {mensaje}{C.RESET}")

        print(f"\n{C.AMARILLO}+---------------------------------------+{C.RESET}")
        print(f"{C.AMARILLO}|        ESTADO ACTUAL                  |{C.RESET}")
        print(f"{C.AMARILLO}╠---------------------------------------╣{C.RESET}")
        vida_porcentaje_j = (resultado.jugador_vida_actual / self.jugador.vida_maxima) * 100
        barra_j = self._crear_barra_vida(vida_porcentaje_j)
        print(f"{C.VERDE}{self.jugador.nombre:20} {barra_j} {resultado.jugador_vida_actual:3}/{self.jugador.vida_maxima:3}{C.RESET}")
        vida_porcentaje_i = (resultado.ia_vida_actual / self.ia.vida_maxima) * 100
        barra_i = self._crear_barra_vida(vida_porcentaje_i)
        print(f"{C.ROJO}{self.ia.nombre:20} {barra_i} {resultado.ia_vida_actual:3}/{self.ia.vida_maxima:3}{C.RESET}")
        print(f"{C.AZUL}Energía jugador: {resultado.jugador_energia_actual}/{self.jugador.energia_maxima}{C.RESET}")
        print(f"{C.AZUL}Energía IA: {resultado.ia_energia_actual}/{self.ia.energia_maxima}{C.RESET}")
        if self.jugador.estados:
            print(f"{C.MAGENTA}Estados jugador: {', '.join(self.jugador.estados)}{C.RESET}")
        if self.ia.estados:
            print(f"{C.MAGENTA}Estados IA: {', '.join(self.ia.estados)}{C.RESET}")
        print(f"{C.AMARILLO}+---------------------------------------+{C.RESET}")

    def _crear_barra_vida(self, porcentaje: float) -> str:
        if porcentaje > 75:
            color = C.VERDE
        elif porcentaje > 40:
            color = C.AMARILLO
        elif porcentaje > 20:
            color = C.NARANJA
        else:
            color = C.ROJO
        barras_completas = int(porcentaje / 5)
        barras_vacias = 20 - barras_completas
        return f"{color}[{'█' * barras_completas}{'░' * barras_vacias}]{C.RESET}"

    def mostrar_estadisticas_finales(self, resultado: ResultadoCombate):
        print(f"\n{C.CYAN}+---------------------------------------------------+{C.RESET}")
        print(f"{C.CYAN}|        ESTADÍSTICAS FINALES DEL COMBATE        |{C.RESET}")
        print(f"{C.CYAN}╠---------------------------------------------------╣{C.RESET}")
        print(f"{C.CYAN}| Turnos totales: {resultado.turnos_totales:30} |{C.RESET}")
        print(f"{C.CYAN}| Daño total jugador: {resultado.daño_total_jugador:24} |{C.RESET}")
        print(f"{C.CYAN}| Daño total IA: {resultado.daño_total_ia:29} |{C.RESET}")
        print(f"{C.CYAN}| Eventos ocurridos: {resultado.eventos_ocurridos:26} |{C.RESET}")
        if resultado.estado == EstadoCombate.VICTORIA_JUGADOR:
            print(f"{C.CYAN}| Experiencia ganada: {resultado.experiencia_ganada:26} |{C.RESET}")
        print(f"{C.CYAN}+---------------------------------------------------+{C.RESET}")
        if self.eventos_ocurridos > 3:
            print(f"\n{C.MAGENTA}Eventos más destacados:{C.RESET}")
            eventos_destacados = []
            for turno in self.historial:
                if turno.evento_aleatorio:
                    nombre_evento = turno.evento_aleatorio.get("tipo", "Evento")
                    eventos_destacados.append(f"Turno {self.historial.index(turno)+1}: {nombre_evento}")
            for evento in eventos_destacados[:5]:
                print(f"  {C.CYAN}- {evento}{C.RESET}")
            if len(eventos_destacados) > 5:
                print(f"  {C.CYAN}- ... y {len(eventos_destacados)-5} eventos más{C.RESET}")