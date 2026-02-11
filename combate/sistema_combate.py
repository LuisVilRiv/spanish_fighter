"""
Sistema de combate principal para Batalla Cómica Española.
Maneja el combate por turnos, acciones, eventos aleatorios y fin del combate.
"""

import random
import time
from enum import Enum, auto
from typing import Optional, Dict, Any, List, Tuple

from utils import Colores as C

# Importación absoluta o relativa según la estructura del proyecto
try:
    # Si se ejecuta como módulo dentro del paquete
    from ..eventos import (
        EVENTOS_NORMALES, EVENTOS_RAROS, EVENTOS_ULTRA_RAROS,
        TODOS_LOS_EVENTOS
    )
except ImportError:
    # Fallback para ejecución directa
    from eventos import (
        EVENTOS_NORMALES, EVENTOS_RAROS, EVENTOS_ULTRA_RAROS,
        TODOS_LOS_EVENTOS
    )

class EstadoCombate(Enum):
    """Estados posibles del combate."""
    EN_CURSO = auto()
    VICTORIA_JUGADOR = auto()
    VICTORIA_IA = auto()
    EMPATE = auto()
    INTERRUMPIDO = auto()

class Accion(Enum):
    """Acciones disponibles por turno."""
    ATAQUE_BASICO = 1
    HABILIDAD_ESPECIAL = 2
    DEFENDER = 3
    CONCENTRAR = 4

class ResultadoTurno:
    """Resultado de un turno de combate."""
    
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
    """Resultado final del combate."""
    
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
    """
    Clase principal que maneja el combate por turnos.
    
    Atributos:
        jugador: Personaje controlado por el jugador
        ia: Personaje controlado por la IA
        probabilidad_evento: Probabilidad de que ocurra un evento aleatorio (15% base)
        turno_actual: Número de turno actual
        max_turnos: Máximo de turnos antes de empate (100 por defecto)
        historial: Lista de resultados de turnos
    """
    
    def __init__(self, jugador, ia, probabilidad_evento: float = 0.15, max_turnos: int = 100):
        """
        Inicializa un nuevo combate.
        
        Args:
            jugador: Personaje controlado por el jugador
            ia: Personaje controlado por la IA
            probabilidad_evento: Probabilidad de evento aleatorio (0.0 a 1.0)
            max_turnos: Máximo de turnos antes de empate
        """
        self.jugador = jugador
        self.ia = ia
        self.ia.es_ia = True  # Marcar como controlado por IA
        
        self.probabilidad_evento = probabilidad_evento
        self.max_turnos = max_turnos
        self.turno_actual = 0
        self.historial: List[ResultadoTurno] = []
        
        # Estadísticas del combate
        self.daño_total_jugador = 0
        self.daño_total_ia = 0
        self.eventos_ocurridos = 0
        
        # Estado del combate
        self.estado = EstadoCombate.EN_CURSO
        
        # Inicializar personajes para combate
        self._inicializar_personajes()
    
    def _inicializar_personajes(self):
        """Prepara los personajes para el combate."""
        # Resetear estados temporales
        self.jugador.estados = [estado for estado in self.jugador.estados if estado not in [
            "defendiendo", "esquivando", "concentrando"
        ]]
        self.ia.estados = [estado for estado in self.ia.estados if estado not in [
            "defendiendo", "esquivando", "concentrando"
        ]]
        
        # Asegurar que la energía esté llena al inicio
        self.jugador.energia_actual = self.jugador.energia_maxima
        self.ia.energia_actual = self.ia.energia_maxima
    
    def mostrar_intro_combate(self):
        """Muestra la introducción del combate."""
        print(f"\n{C.NEGRITA}{C.ROJO_BRILLANTE}+---------------------------------------------------+{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}|     ¡COMIENZA LA BATALLA CÓMICA ESPAÑOLA!         |{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}+---------------------------------------------------+{C.RESET}")
        print(f"\n{C.NEGRITA}{C.CYAN}JUGADOR:{C.RESET} {self.jugador.nombre} {self.jugador.tipo}")
        print(f"{C.NEGRITA}{C.CYAN}VS{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO}IA:{C.RESET} {self.ia.nombre} {self.ia.tipo}")
        print(f"\n{C.AMARILLO}¡Que gane el más español!{C.RESET}")
        print(f"{C.CYAN}─────────────────────────────────────────────────{C.RESET}")
    
    def ejecutar_turno(self, accion_jugador: Accion, indice_habilidad: Optional[int] = None) -> ResultadoTurno:
        """
        Ejecuta un turno completo del combate.
        
        Args:
            accion_jugador: Acción elegida por el jugador
            indice_habilidad: Índice de habilidad si se eligió habilidad especial
            
        Returns:
            Resultado del turno
        """
        if self.estado != EstadoCombate.EN_CURSO:
            raise ValueError("El combate ya ha terminado")
        
        self.turno_actual += 1
        resultado = ResultadoTurno()
        
        # Mostrar número de turno
        print(f"\n{C.NEGRITA}{C.AMARILLO}========== TURNO {self.turno_actual} =========={C.RESET}")
        
        # 1. Determinar orden por velocidad (con variación aleatoria del 10%)
        velocidad_jugador = self.jugador.velocidad * random.uniform(0.9, 1.1)
        velocidad_ia = self.ia.velocidad * random.uniform(0.9, 1.1)
        
        # 2. Ejecutar acciones en orden
        if velocidad_jugador >= velocidad_ia:
            # Jugador actúa primero
            resultado_jugador = self._ejecutar_accion(self.jugador, self.ia, accion_jugador, indice_habilidad)
            resultado.jugador_accion = resultado_jugador.get("mensaje", "")
            self._actualizar_resultado_jugador(resultado, resultado_jugador)
            
            # Verificar si la IA murió
            if not self.ia.esta_vivo():
                resultado.ia_vida_actual = 0
                resultado.jugador_vida_actual = self.jugador.vida_actual
                resultado.jugador_energia_actual = self.jugador.energia_actual
                resultado.ia_energia_actual = self.ia.energia_actual
                resultado.mensajes.append(f"{C.ROJO_BRILLANTE}¡{self.ia.nombre} ha sido derrotado!{C.RESET}")
                self._verificar_fin_combate()
                return resultado
            
            # IA actúa
            resultado_ia = self._ejecutar_accion_ia()
            resultado.ia_accion = resultado_ia.get("mensaje", "")
            self._actualizar_resultado_ia(resultado, resultado_ia)
            
            # Verificar si el jugador murió después del ataque de la IA
            if not self.jugador.esta_vivo():
                resultado.jugador_vida_actual = 0
                resultado.ia_vida_actual = self.ia.vida_actual
                resultado.jugador_energia_actual = self.jugador.energia_actual
                resultado.ia_energia_actual = self.ia.energia_actual
                resultado.mensajes.append(f"{C.ROJO_BRILLANTE}¡{self.jugador.nombre} ha sido derrotado!{C.RESET}")
                self._verificar_fin_combate()
                return resultado
            
        else:
            # IA actúa primero
            resultado_ia = self._ejecutar_accion_ia()
            resultado.ia_accion = resultado_ia.get("mensaje", "")
            self._actualizar_resultado_ia(resultado, resultado_ia)
            
            # Verificar si el jugador murió
            if not self.jugador.esta_vivo():
                resultado.jugador_vida_actual = 0
                resultado.ia_vida_actual = self.ia.vida_actual
                resultado.jugador_energia_actual = self.jugador.energia_actual
                resultado.ia_energia_actual = self.ia.energia_actual
                resultado.mensajes.append(f"{C.ROJO_BRILLANTE}¡{self.jugador.nombre} ha sido derrotado!{C.RESET}")
                self._verificar_fin_combate()
                return resultado
            
            # Jugador actúa
            resultado_jugador = self._ejecutar_accion(self.jugador, self.ia, accion_jugador, indice_habilidad)
            resultado.jugador_accion = resultado_jugador.get("mensaje", "")
            self._actualizar_resultado_jugador(resultado, resultado_jugador)
            
            # Verificar si la IA murió después del ataque del jugador
            if not self.ia.esta_vivo():
                resultado.ia_vida_actual = 0
                resultado.jugador_vida_actual = self.jugador.vida_actual
                resultado.jugador_energia_actual = self.jugador.energia_actual
                resultado.ia_energia_actual = self.ia.energia_actual
                resultado.mensajes.append(f"{C.ROJO_BRILLANTE}¡{self.ia.nombre} ha sido derrotado!{C.RESET}")
                self._verificar_fin_combate()
                return resultado
        
        # 3. Aplicar regeneración natural
        self._aplicar_regeneracion(resultado)
        
        # 4. Evento aleatorio (15% de probabilidad)
        if random.random() < self.probabilidad_evento:
            evento_resultado = self._activar_evento_aleatorio()
            resultado.evento_aleatorio = evento_resultado
            resultado.mensajes.append(evento_resultado.get("mensaje", ""))
            self.eventos_ocurridos += 1
        
        # 5. Aplicar efectos de estados (daño continuo) y actualizar duraciones
        self._aplicar_efectos_estados(resultado)
        
        # 6. Actualizar vida y energía actual
        resultado.jugador_vida_actual = self.jugador.vida_actual
        resultado.ia_vida_actual = self.ia.vida_actual
        resultado.jugador_energia_actual = self.jugador.energia_actual
        resultado.ia_energia_actual = self.ia.energia_actual
        
        # 7. Verificar fin del combate
        self._verificar_fin_combate()
        
        # Guardar en historial
        self.historial.append(resultado)
        
        return resultado
    
    def _ejecutar_accion(self, atacante, objetivo, accion: Accion, indice_habilidad: Optional[int] = None) -> Dict[str, Any]:
        """
        Ejecuta una acción de un personaje.
        
        Args:
            atacante: Personaje que ejecuta la acción
            objetivo: Personaje objetivo
            accion: Tipo de acción
            indice_habilidad: Índice de habilidad si es habilidad especial
            
        Returns:
            Resultado de la acción
        """
        # Aplicar efectos de estados antes de la acción
        if "dormido" in atacante.estados:
            # Pierde el turno, se reduce duración automáticamente al final del turno
            return {
                "exito": False,
                "mensaje": f"{atacante.nombre} está dormido y pierde el turno.",
                "tipo": "estado",
                "dormido": True
            }
        
        if "paralizado" in atacante.estados:
            if random.random() < 0.5:  # 50% de no poder actuar
                return {
                    "exito": False,
                    "mensaje": f"{atacante.nombre} está paralizado y no puede moverse.",
                    "tipo": "estado",
                    "paralizado": True
                }
        
        if "confundido" in atacante.estados:
            if random.random() < 0.3:  # 30% de atacarse a sí mismo
                objetivo = atacante
                mensaje_confusion = f" ¡Está confundido y se ataca a sí mismo!"
            else:
                mensaje_confusion = f" (a pesar de estar confundido)"
        else:
            mensaje_confusion = ""
        
        # Ejecutar acción según tipo
        if accion == Accion.ATAQUE_BASICO:
            resultado = atacante.atacar_basico(objetivo)
            resultado["mensaje"] = f"{atacante.nombre} ataca a {objetivo.nombre}.{mensaje_confusion}"
            
        elif accion == Accion.HABILIDAD_ESPECIAL:
            if indice_habilidad is None or indice_habilidad < 0 or indice_habilidad >= len(atacante.habilidades):
                # Si la habilidad no es válida, usa ataque básico
                resultado = atacante.atacar_basico(objetivo)
                resultado["mensaje"] = f"{atacante.nombre} intenta usar una habilidad pero falla. En su lugar ataca.{mensaje_confusion}"
            else:
                resultado = atacante.usar_habilidad(indice_habilidad, objetivo)
                if resultado["exito"]:
                    habilidad = atacante.habilidades[indice_habilidad]
                    resultado["mensaje"] = f"{atacante.nombre} usa '{habilidad.nombre}' en {objetivo.nombre}.{mensaje_confusion}"
                else:
                    # Si falla (p.ej. por falta de energía), usa ataque básico
                    resultado = atacante.atacar_basico(objetivo)
                    resultado["mensaje"] = f"{atacante.nombre} intenta usar una habilidad pero falla. En su lugar ataca.{mensaje_confusion}"
        
        elif accion == Accion.DEFENDER:
            resultado = atacante.defender()
            resultado["mensaje"] = f"{atacante.nombre} se prepara para defender."
        
        elif accion == Accion.CONCENTRAR:
            resultado = atacante.concentrar()
            resultado["mensaje"] = f"{atacante.nombre} se concentra para recuperar energía."
        
        else:
            # Acción no válida, ataque básico por defecto
            resultado = atacante.atacar_basico(objetivo)
            resultado["mensaje"] = f"{atacante.nombre} no sabe qué hacer y ataca por instinto.{mensaje_confusion}"
        
        # Actualizar estadísticas de daño
        if "daño" in resultado:
            if atacante == self.jugador:
                self.daño_total_jugador += resultado["daño"]
            else:
                self.daño_total_ia += resultado["daño"]
        
        return resultado
    
    def _ejecutar_accion_ia(self) -> Dict[str, Any]:
        """
        Decide y ejecuta la acción de la IA.
        
        Returns:
            Resultado de la acción de la IA
        """
        # IA inteligente: evalúa situación y elige acción
        ia = self.ia
        jugador = self.jugador
        
        # 1. Si tiene poca energía (< 30), intenta concentrar
        if ia.energia_actual < 30:
            resultado = ia.concentrar()
            resultado["mensaje"] = f"{ia.nombre} se concentra para recuperar energía."
            return resultado
        
        # 2. Si tiene poca vida (< 40%) y tiene habilidades curativas, usa una
        if ia.vida_actual < ia.vida_maxima * 0.4:
            # Buscar habilidades curativas (marcadas con es_curacion=True)
            habilidades_curativas = []
            for i, habilidad in enumerate(ia.habilidades):
                if hasattr(habilidad, 'es_curacion') and habilidad.es_curacion:
                    habilidades_curativas.append(i)
            
            if habilidades_curativas and ia.energia_actual >= 20:
                indice = random.choice(habilidades_curativas)
                resultado = ia.usar_habilidad(indice, ia)  # Se cura a sí mismo
                if resultado.get("exito", False):
                    habilidad = ia.habilidades[indice]
                    resultado["mensaje"] = f"{ia.nombre} usa '{habilidad.nombre}' en sí mismo."
                else:
                    resultado = ia.atacar_basico(jugador)
                    resultado["mensaje"] = f"{ia.nombre} intenta curarse pero falla. Ataca en su lugar."
                return resultado
        
        # 3. Si el jugador está defendiendo, usar habilidad que ignore defensa
        if "defendiendo" in jugador.estados:
            # Buscar habilidades que afecten estados o ignoren defensa
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
        
        # 4. Si tiene energía para una habilidad potente (> 50), usarla (70% probabilidad)
        if ia.energia_actual > 50 and random.random() < 0.7:
            # Elegir habilidad ofensiva
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
        
        # 5. Ataque básico (por defecto o si no hay mejores opciones)
        resultado = ia.atacar_basico(jugador)
        resultado["mensaje"] = f"{ia.nombre} ataca a {jugador.nombre}."
        return resultado
    
    def _actualizar_resultado_jugador(self, resultado: ResultadoTurno, accion_resultado: Dict[str, Any]):
        """Actualiza el resultado con la acción del jugador."""
        if "daño" in accion_resultado:
            resultado.daño_jugador_a_ia = accion_resultado["daño"]
        if "curacion" in accion_resultado:
            resultado.curacion_jugador = accion_resultado["curacion"]
    
    def _actualizar_resultado_ia(self, resultado: ResultadoTurno, accion_resultado: Dict[str, Any]):
        """Actualiza el resultado con la acción de la IA."""
        if "daño" in accion_resultado:
            resultado.daño_ia_a_jugador = accion_resultado["daño"]
        if "curacion" in accion_resultado:
            resultado.curacion_ia = accion_resultado["curacion"]
    
    def _aplicar_regeneracion(self, resultado: ResultadoTurno):
        """Aplica regeneración natural de energía."""
        # Regeneración base de energía (10-15)
        regeneracion_jugador = random.randint(10, 15)
        regeneracion_ia = random.randint(10, 15)
        
        self.jugador.energia_actual = min(
            self.jugador.energia_maxima,
            self.jugador.energia_actual + regeneracion_jugador
        )
        self.ia.energia_actual = min(
            self.ia.energia_maxima,
            self.ia.energia_actual + regeneracion_ia
        )
        
        # Personajes específicos pueden tener regeneración especial
        self.jugador.regenerar()
        self.ia.regenerar()
    
    def _activar_evento_aleatorio(self) -> Dict[str, Any]:
        """
        Activa un evento aleatorio.
        
        Returns:
            Resultado del evento
        """
        # Decidir tipo de evento según probabilidades
        rand = random.random()
        
        if rand < 0.70:  # 70% eventos normales
            clase_evento = random.choice(EVENTOS_NORMALES)
        elif rand < 0.95:  # 25% eventos raros (70-95)
            clase_evento = random.choice(EVENTOS_RAROS)
        else:  # 5% eventos ultra raros (95-100)
            clase_evento = random.choice(EVENTOS_ULTRA_RAROS)
        
        # Crear instancia y activar evento
        evento = clase_evento()
        return evento.activar(self.jugador, self.ia, self.turno_actual)
    
    def _aplicar_efectos_estados(self, resultado: ResultadoTurno):
        """
        Aplica efectos continuos de estados y actualiza duraciones.
        """
        mensajes_estados = []
        
        # ----- Estados del jugador -----
        if "quemado" in self.jugador.estados:
            daño_quemadura = 5
            self.jugador.recibir_dano(daño_quemadura, "quemadura")
            mensajes_estados.append(f"{self.jugador.nombre} sufre {daño_quemadura} de daño por quemadura.")
        
        if "sangrando" in self.jugador.estados:
            daño_sangrado = 3
            self.jugador.recibir_dano(daño_sangrado, "sangrado")
            mensajes_estados.append(f"{self.jugador.nombre} pierde {daño_sangrado} de vida por sangrado.")
        
        if "envenenado" in self.jugador.estados:
            daño_veneno = 7
            self.jugador.recibir_dano(daño_veneno, "veneno")
            mensajes_estados.append(f"{self.jugador.nombre} sufre {daño_veneno} de daño por veneno.")
        
        if "bajon_azucar" in self.jugador.estados:
            # Reduce energía y velocidad cada turno
            perdida_energia = 10
            reduccion_velocidad = 5
            self.jugador.energia_actual = max(0, self.jugador.energia_actual - perdida_energia)
            self.jugador.velocidad = max(5, self.jugador.velocidad - reduccion_velocidad)
            mensajes_estados.append(f"{self.jugador.nombre} sufre bajón de azúcar: energía -{perdida_energia}, velocidad -{reduccion_velocidad}.")
        
        # ----- Estados de la IA -----
        if "quemado" in self.ia.estados:
            daño_quemadura = 5
            self.ia.recibir_dano(daño_quemadura, "quemadura")
            mensajes_estados.append(f"{self.ia.nombre} sufre {daño_quemadura} de daño por quemadura.")
        
        if "sangrando" in self.ia.estados:
            daño_sangrado = 3
            self.ia.recibir_dano(daño_sangrado, "sangrado")
            mensajes_estados.append(f"{self.ia.nombre} pierde {daño_sangrado} de vida por sangrado.")
        
        if "envenenado" in self.ia.estados:
            daño_veneno = 7
            self.ia.recibir_dano(daño_veneno, "veneno")
            mensajes_estados.append(f"{self.ia.nombre} sufre {daño_veneno} de daño por veneno.")
        
        if "bajon_azucar" in self.ia.estados:
            perdida_energia = 10
            reduccion_velocidad = 5
            self.ia.energia_actual = max(0, self.ia.energia_actual - perdida_energia)
            self.ia.velocidad = max(5, self.ia.velocidad - reduccion_velocidad)
            mensajes_estados.append(f"{self.ia.nombre} sufre bajón de azúcar: energía -{perdida_energia}, velocidad -{reduccion_velocidad}.")
        
        # ----- Actualizar duraciones de estados -----
        self.jugador.actualizar_estados()
        self.ia.actualizar_estados()
        
        # Eliminar estados temporales que ya no deberían persistir (defendiendo, etc.)
        # Nota: actualizar_estados ya se encarga de eliminar los expirados.
        
        # Añadir mensajes al resultado
        if mensajes_estados:
            resultado.mensajes.extend(mensajes_estados)
    
    def _verificar_fin_combate(self):
        """Verifica si el combate ha terminado."""
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
        """
        Obtiene el resultado final del combate.
        
        Returns:
            Resultado final del combate
        """
        resultado = ResultadoCombate()
        resultado.estado = self.estado
        resultado.turnos_totales = self.turno_actual
        resultado.daño_total_jugador = self.daño_total_jugador
        resultado.daño_total_ia = self.daño_total_ia
        resultado.eventos_ocurridos = self.eventos_ocurridos
        
        # Determinar ganador y perdedor
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
        """Calcula la experiencia ganada por el jugador."""
        # Base: nivel del enemigo * 10
        base = 100
        
        # Bonus por rapidez (menos turnos = más experiencia)
        if self.turno_actual < 10:
            bonus_rapidez = 50
        elif self.turno_actual < 20:
            bonus_rapidez = 30
        elif self.turno_actual < 30:
            bonus_rapidez = 15
        else:
            bonus_rapidez = 0
        
        # Bonus por eventos (cada evento da 5xp)
        bonus_eventos = self.eventos_ocurridos * 5
        
        # Bonus por daño infligido (cada 10 puntos de daño = 1xp)
        bonus_daño = self.daño_total_jugador // 10
        
        # Bonus por no recibir mucho daño (si recibió menos del 30% de su vida máxima)
        vida_perdida = self.jugador.vida_maxima - self.jugador.vida_actual
        if vida_perdida < self.jugador.vida_maxima * 0.3:
            bonus_defensa = 20
        else:
            bonus_defensa = 0
        
        experiencia_total = base + bonus_rapidez + bonus_eventos + bonus_daño + bonus_defensa
        
        return experiencia_total
    
    def mostrar_resumen_turno(self, resultado: ResultadoTurno):
        """Muestra un resumen del turno."""
        print(f"\n{C.CYAN}────────── RESUMEN DEL TURNO ──────────{C.RESET}")
        
        # Acciones
        if resultado.jugador_accion:
            print(f"{C.VERDE}- {resultado.jugador_accion}{C.RESET}")
        
        if resultado.ia_accion:
            print(f"{C.ROJO}- {resultado.ia_accion}{C.RESET}")
        
        # Daño y curación
        if resultado.daño_jugador_a_ia > 0:
            print(f"{C.VERDE}  → Daño a IA: {resultado.daño_jugador_a_ia}{C.RESET}")
        
        if resultado.daño_ia_a_jugador > 0:
            print(f"{C.ROJO}  → Daño a jugador: {resultado.daño_ia_a_jugador}{C.RESET}")
        
        if resultado.curacion_jugador > 0:
            print(f"{C.VERDE}  → Curación jugador: {resultado.curacion_jugador}{C.RESET}")
        
        if resultado.curacion_ia > 0:
            print(f"{C.ROJO}  → Curación IA: {resultado.curacion_ia}{C.RESET}")
        
        # Evento aleatorio
        if resultado.evento_aleatorio:
            print(f"\n{C.MAGENTA}¡EVENTO ALEATORIO!{C.RESET}")
            print(f"{resultado.evento_aleatorio.get('mensaje', '')}")
        
        # Mensajes adicionales
        for mensaje in resultado.mensajes:
            print(f"{C.CYAN}  {mensaje}{C.RESET}")
        
        # Estado actual
        print(f"\n{C.AMARILLO}+---------------------------------------+{C.RESET}")
        print(f"{C.AMARILLO}|        ESTADO ACTUAL                  |{C.RESET}")
        print(f"{C.AMARILLO}╠---------------------------------------╣{C.RESET}")
        
        # Barra de vida jugador
        vida_porcentaje_j = (resultado.jugador_vida_actual / self.jugador.vida_maxima) * 100
        barra_j = self._crear_barra_vida(vida_porcentaje_j)
        print(f"{C.VERDE}{self.jugador.nombre:20} {barra_j} {resultado.jugador_vida_actual:3}/{self.jugador.vida_maxima:3}{C.RESET}")
        
        # Barra de vida IA
        vida_porcentaje_i = (resultado.ia_vida_actual / self.ia.vida_maxima) * 100
        barra_i = self._crear_barra_vida(vida_porcentaje_i)
        print(f"{C.ROJO}{self.ia.nombre:20} {barra_i} {resultado.ia_vida_actual:3}/{self.ia.vida_maxima:3}{C.RESET}")
        
        # Energía
        print(f"{C.AZUL}Energía jugador: {resultado.jugador_energia_actual}/{self.jugador.energia_maxima}{C.RESET}")
        print(f"{C.AZUL}Energía IA: {resultado.ia_energia_actual}/{self.ia.energia_maxima}{C.RESET}")
        
        # Estados
        if self.jugador.estados:
            print(f"{C.MAGENTA}Estados jugador: {', '.join(self.jugador.estados)}{C.RESET}")
        if self.ia.estados:
            print(f"{C.MAGENTA}Estados IA: {', '.join(self.ia.estados)}{C.RESET}")
        
        print(f"{C.AMARILLO}+---------------------------------------+{C.RESET}")
    
    def _crear_barra_vida(self, porcentaje: float) -> str:
        """Crea una barra de vida visual."""
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
        
        barra = f"{color}[{'█' * barras_completas}{'░' * barras_vacias}]{C.RESET}"
        return barra
    
    def mostrar_estadisticas_finales(self, resultado: ResultadoCombate):
        """Muestra las estadísticas finales del combate."""
        print(f"\n{C.CYAN}+---------------------------------------------------+{C.RESET}")
        print(f"{C.CYAN}|        ESTADÍSTICAS FINALES DEL COMBATE        |{C.RESET}")
        print(f"{C.CYAN}╠---------------------------------------------------╣{C.RESET}")
        print(f"{C.CYAN}| Turnos totales: {resultado.turnos_totales:30} |{C.RESET}")
        print(f"{C.CYAN}| Daño total jugador: {resultado.daño_total_jugador:24} |{C.RESET}")
        print(f"{C.CYAN}| Daño total IA: {resultado.daño_total_ia:29} |{C.RESET}")
        print(f"{C.CYAN}| Eventos ocurridos: {resultado.eventos_ocurridos:26} |{C.RESET}")
        
        if resultado.estado == EstadoCombate.VICTORIA_JUGADOR:
            print(f"{C.CYAN}| Experiencia ganada: {resultado.experiencia_ganada:26} |{C.RESET}")
            # Aquí se podría subir de nivel al personaje
        
        print(f"{C.CYAN}+---------------------------------------------------+{C.RESET}")
        
        # Mostrar historial de eventos si hubo muchos
        if self.eventos_ocurridos > 3:
            print(f"\n{C.MAGENTA}Eventos más destacados:{C.RESET}")
            eventos_destacados = []
            for turno in self.historial:
                if turno.evento_aleatorio:
                    nombre_evento = turno.evento_aleatorio.get("tipo", "Evento")
                    eventos_destacados.append(f"Turno {self.historial.index(turno)+1}: {nombre_evento}")
            
            # Mostrar solo los primeros 5 eventos
            for evento in eventos_destacados[:5]:
                print(f"  {C.CYAN}- {evento}{C.RESET}")
            
            if len(eventos_destacados) > 5:
                print(f"  {C.CYAN}- ... y {len(eventos_destacados)-5} eventos más{C.RESET}")