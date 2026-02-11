"""
juego.py - Lógica principal del combate y selección de personajes.
Extraído de main.py original para modularizar.
"""

import os
import sys
import random
from combate import Combate, Accion, EstadoCombate
from personajes import (
    Segarro, Catolico, Sacerdote, Turista, Abuela,
    Politico, Torero, Flaquito, Choni, PutoAmo, Barrendero
)
from utils import Colores as C
from sistema_guardado import GestorGuardado, crear_datos_jugador

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa_para_continuar(mensaje="Presiona Enter para continuar..."):
    input(f"\n{C.CYAN}{mensaje}{C.RESET}")

class JuegoBatallaComica:
    """Clase principal del juego (combate, selección)."""

    def __init__(self):
        self.personajes_disponibles = [
            Segarro, Catolico, Sacerdote, Turista, Abuela,
            Politico, Torero, Flaquito, Choni, PutoAmo, Barrendero
        ]
        self.personaje_jugador = None
        self.personaje_cpu = None
        self.combate_actual = None
        self.gestor_guardado = GestorGuardado()

    def mostrar_titulo(self):
        limpiar_pantalla()
        print(f"\n{C.NEGRITA}{C.ROJO_BRILLANTE}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}║       BATALLA CÓMICA ESPAÑOLA - v1.0             ║{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}║          Jugador vs CPU                         ║{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}╚═══════════════════════════════════════════════════╝{C.RESET}")
        print(f"{C.CYAN}¡Prepárate para el combate más surrealista y español!{C.RESET}\n")

    def seleccionar_personaje_jugador(self):
        """Permite al jugador seleccionar su personaje."""
        limpiar_pantalla()
        self.mostrar_titulo()

        print(f"\n{C.VERDE}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.VERDE}║       SELECCIONA TU PERSONAJE                    ║{C.RESET}")
        print(f"{C.VERDE}╠═══════════════════════════════════════════════════╣{C.RESET}")

        for i, personaje_clase in enumerate(self.personajes_disponibles, 1):
            try:
                instancia = personaje_clase()
                print(f"{C.VERDE}║ {i:2}. {personaje_clase.__name__:20} {C.RESET}", end="")
                print(f"{instancia.tipo[:20]:20} ║{C.RESET}")
                print(f"{C.VERDE}║    Vida: {instancia.vida_maxima:3}  Ataque: {instancia.ataque_base:3}  ", end="")
                print(f"Defensa: {instancia.defensa_base:3}  Velocidad: {instancia.velocidad_base:3} ║{C.RESET}")
                print(f"{C.VERDE}║    {instancia.descripcion()[:40]:40} ║{C.RESET}")
            except:
                print(f"{C.VERDE}║ {i:2}. {personaje_clase.__name__:20} {'Personaje disponible':20} ║{C.RESET}")

        print(f"{C.VERDE}║ 0. {C.ROJO}Volver al menú principal{C.VERDE}               ║{C.RESET}")
        print(f"{C.VERDE}╚═══════════════════════════════════════════════════╝{C.RESET}")

        while True:
            try:
                opcion = int(input(f"\n{C.AZUL}Elige tu personaje (0 para volver): {C.RESET}"))
                if opcion == 0:
                    return None
                if 1 <= opcion <= len(self.personajes_disponibles):
                    personaje_clase = self.personajes_disponibles[opcion - 1]
                    self.personaje_jugador = personaje_clase()

                    nombre_personalizado = input(f"{C.AZUL}¿Quieres un nombre personalizado? (deja vacío para usar el predeterminado): {C.RESET}")
                    if nombre_personalizado.strip():
                        try:
                            self.personaje_jugador = personaje_clase(nombre_personalizado.strip())
                        except TypeError:
                            print(f"{C.AMARILLO}Este personaje no acepta nombre personalizado. Usando nombre predeterminado.{C.RESET}")

                    limpiar_pantalla()
                    print(f"\n{C.VERDE_BRILLANTE}¡Has seleccionado a {self.personaje_jugador.nombre}!{C.RESET}")
                    self.personaje_jugador.mostrar_stats()
                    pausa_para_continuar()
                    return True
                else:
                    print(f"{C.ROJO}Opción no válida. Intenta de nuevo.{C.RESET}")
            except ValueError:
                print(f"{C.ROJO}Por favor, ingresa un número.{C.RESET}")

    def seleccionar_personaje_cpu(self, excluir_jugador=True):
        """Selecciona un personaje para la CPU."""
        limpiar_pantalla()
        self.mostrar_titulo()

        print(f"\n{C.ROJO}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.ROJO}║       SELECCIONA EL PERSONAJE DE LA CPU          ║{C.RESET}")
        print(f"{C.ROJO}╠═══════════════════════════════════════════════════╣{C.RESET}")

        personajes_cpu = self.personajes_disponibles.copy()
        if excluir_jugador and self.personaje_jugador:
            jugador_clase = type(self.personaje_jugador)
            personajes_cpu = [p for p in personajes_cpu if p != jugador_clase]

        for i, personaje_clase in enumerate(personajes_cpu, 1):
            try:
                instancia = personaje_clase()
                print(f"{C.ROJO}║ {i:2}. {personaje_clase.__name__:20} {C.RESET}", end="")
                print(f"{instancia.tipo[:20]:20} ║{C.RESET}")
            except:
                print(f"{C.ROJO}║ {i:2}. {personaje_clase.__name__:20} {'Personaje disponible':20} ║{C.RESET}")

        print(f"{C.ROJO}║ 0. {C.ROJO}Aleatorio (CPU elige){C.ROJO}                   ║{C.RESET}")
        print(f"{C.ROJO}║ 99. {C.ROJO}Volver al menú principal{C.ROJO}              ║{C.RESET}")
        print(f"{C.ROJO}╚═══════════════════════════════════════════════════╝{C.RESET}")

        while True:
            try:
                opcion = int(input(f"\n{C.AZUL}Elige el personaje de la CPU (0 para aleatorio, 99 para volver): {C.RESET}"))
                if opcion == 99:
                    return None
                if opcion == 0:
                    personaje_clase = random.choice(personajes_cpu)
                    self.personaje_cpu = personaje_clase()
                    limpiar_pantalla()
                    print(f"\n{C.ROJO_BRILLANTE}¡La CPU ha seleccionado a {self.personaje_cpu.nombre}!{C.RESET}")
                    self.personaje_cpu.mostrar_stats()
                    pausa_para_continuar()
                    return True
                if 1 <= opcion <= len(personajes_cpu):
                    personaje_clase = personajes_cpu[opcion - 1]
                    self.personaje_cpu = personaje_clase()
                    limpiar_pantalla()
                    print(f"\n{C.ROJO_BRILLANTE}¡La CPU será {self.personaje_cpu.nombre}!{C.RESET}")
                    self.personaje_cpu.mostrar_stats()
                    pausa_para_continuar()
                    return True
                else:
                    print(f"{C.ROJO}Opción no válida. Intenta de nuevo.{C.RESET}")
            except ValueError:
                print(f"{C.ROJO}Por favor, ingresa un número.{C.RESET}")

    def iniciar_nuevo_combate(self, partida_cargada=False, slot_actual=None, datos_cargados=None):
        """Inicia un nuevo combate jugador vs CPU.
        
        Args:
            partida_cargada: Indica si se ha cargado una partida existente.
            slot_actual: Slot de guardado actual (None si no se guarda).
            datos_cargados: Datos de la partida cargada (para actualizar tras combate).
        """
        # Si no hay personaje jugador (partida nueva) lo selecciona
        if not self.personaje_jugador:
            if not self.seleccionar_personaje_jugador():
                return

        # Seleccionar personaje CPU
        if not self.personaje_cpu:
            if not self.seleccionar_personaje_cpu():
                return

        # Confirmación
        limpiar_pantalla()
        self.mostrar_titulo()

        print(f"\n{C.NEGRITA}{C.AMARILLO}══════════ CONFIRMACIÓN DEL COMBATE ══════════{C.RESET}")
        print(f"{C.VERDE}JUGADOR: {self.personaje_jugador.nombre} {self.personaje_jugador.tipo}{C.RESET}")
        print(f"{C.ROJO}CPU: {self.personaje_cpu.nombre} {self.personaje_cpu.tipo}{C.RESET}")

        confirmar = input(f"\n{C.AZUL}¿Iniciar combate? (s/n): {C.RESET}").lower()
        if confirmar != 's':
            print(f"{C.AMARILLO}Combate cancelado.{C.RESET}")
            pausa_para_continuar()
            return

        # Crear combate
        self.combate_actual = Combate(self.personaje_jugador, self.personaje_cpu)

        # Bucle principal del combate
        while self.combate_actual.estado == EstadoCombate.EN_CURSO:
            limpiar_pantalla()
            self.combate_actual.mostrar_intro_combate()
            self.mostrar_opciones_turno()

            accion_valida = False
            while not accion_valida:
                try:
                    opcion = int(input(f"\n{C.AZUL}Elige una acción (1-4, 9 para stats, 0 para rendirse): {C.RESET}"))
                    if opcion == 1:
                        resultado = self.combate_actual.ejecutar_turno(Accion.ATAQUE_BASICO)
                        accion_valida = True
                    elif opcion == 2:
                        indice_habilidad = self.seleccionar_habilidad()
                        if indice_habilidad is not None:
                            resultado = self.combate_actual.ejecutar_turno(Accion.HABILIDAD_ESPECIAL, indice_habilidad)
                            accion_valida = True
                        else:
                            limpiar_pantalla()
                            self.combate_actual.mostrar_intro_combate()
                            self.mostrar_opciones_turno()
                    elif opcion == 3:
                        resultado = self.combate_actual.ejecutar_turno(Accion.DEFENDER)
                        accion_valida = True
                    elif opcion == 4:
                        resultado = self.combate_actual.ejecutar_turno(Accion.CONCENTRAR)
                        accion_valida = True
                    elif opcion == 0:
                        rendirse = input(f"{C.ROJO}¿Estás seguro de que quieres rendirte? (s/n): {C.RESET}").lower()
                        if rendirse == 's':
                            self.personaje_jugador.vida_actual = 0
                            self.combate_actual.estado = EstadoCombate.VICTORIA_IA
                            accion_valida = True
                        else:
                            limpiar_pantalla()
                            self.combate_actual.mostrar_intro_combate()
                            self.mostrar_opciones_turno()
                    elif opcion == 9:
                        self.mostrar_stats_completos()
                        pausa_para_continuar("Presiona Enter para volver al combate...")
                        limpiar_pantalla()
                        self.combate_actual.mostrar_intro_combate()
                        self.mostrar_opciones_turno()
                    else:
                        print(f"{C.ROJO}Opción no válida. Intenta de nuevo.{C.RESET}")
                except ValueError:
                    print(f"{C.ROJO}Por favor, ingresa un número.{C.RESET}")

            if 'resultado' in locals():
                limpiar_pantalla()
                self.combate_actual.mostrar_intro_combate()
                self.combate_actual.mostrar_resumen_turno(resultado)
                pausa_para_continuar("Presiona Enter para continuar...")

        # Combate terminado
        limpiar_pantalla()
        self.mostrar_fin_combate()

        # --- Guardado automático al final del combate ---
        if slot_actual is not None and self.personaje_jugador.esta_vivo():
            datos = crear_datos_jugador(self.personaje_jugador)
            # Actualizar progreso: si ganó, incrementar partidas_ganadas
            if self.combate_actual.estado == EstadoCombate.VICTORIA_JUGADOR:
                datos["progreso"]["partidas_ganadas"] = getattr(self.personaje_jugador, '_partidas_ganadas', 0) + 1
            self.gestor_guardado.guardar_partida(datos, slot_actual)
        elif slot_actual is not None and not self.personaje_jugador.esta_vivo():
            print(f"{C.AMARILLO}Has perdido. No se guarda el progreso.{C.RESET}")

        self.preguntar_revancha(slot_actual)

    def mostrar_opciones_turno(self):
        """Muestra las opciones disponibles para el turno actual."""
        jugador = self.combate_actual.jugador
        print(f"\n{C.NEGRITA}{C.VERDE}══════════ TU TURNO ══════════{C.RESET}")
        print(f"{C.VERDE}Vida: {jugador.vida_actual}/{jugador.vida_maxima}   Energía: {jugador.energia_actual}/{jugador.energia_maxima}{C.RESET}")

        if jugador.estados:
            print(f"{C.MAGENTA}Estados: {', '.join(jugador.estados)}{C.RESET}")

        print(f"\n{C.CYAN}OPCIONES:{C.RESET}")
        print(f"  {C.VERDE}1. Ataque Básico{C.RESET} - No gasta energía, daño normal")
        print(f"  {C.VERDE}2. Habilidad Especial{C.RESET} - Gasta energía, efectos únicos")
        print(f"  {C.AZUL}3. Defender{C.RESET} - Te cubres, recibes menos daño")
        print(f"  {C.AZUL}4. Concentrar{C.RESET} - Recuperas energía extra")
        print(f"  {C.AMARILLO}9. Ver stats completos{C.RESET}")
        print(f"  {C.ROJO}0. Rendirse{C.RESET}")

    def seleccionar_habilidad(self):
        """Permite al jugador seleccionar una habilidad."""
        limpiar_pantalla()
        self.combate_actual.mostrar_intro_combate()

        jugador = self.combate_actual.jugador
        print(f"\n{C.CYAN}══════════ HABILIDADES DISPONIBLES ══════════{C.RESET}")
        print(f"{C.VERDE}Energía disponible: {jugador.energia_actual}/{jugador.energia_maxima}{C.RESET}\n")

        for i, habilidad in enumerate(jugador.habilidades, 1):
            energia_suficiente = jugador.energia_actual >= habilidad.costo_energia
            color = C.VERDE if energia_suficiente else C.ROJO
            print(f"  {color}{i}. {habilidad.nombre} ({habilidad.costo_energia}E){C.RESET}")
            print(f"     {habilidad.descripcion}")
            if not energia_suficiente:
                print(f"     {C.ROJO}¡Energía insuficiente!{C.RESET}")
            print()

        print(f"  {C.AMARILLO}0. Volver al combate{C.RESET}")

        while True:
            try:
                opcion = int(input(f"\n{C.AZUL}Elige una habilidad (1-{len(jugador.habilidades)}, 0 para volver): {C.RESET}"))
                if opcion == 0:
                    return None
                if 1 <= opcion <= len(jugador.habilidades):
                    habilidad = jugador.habilidades[opcion - 1]
                    if jugador.energia_actual >= habilidad.costo_energia:
                        return opcion - 1
                    else:
                        print(f"\n{C.ROJO}No tienes suficiente energía para usar '{habilidad.nombre}'.{C.RESET}")
                        continuar = input(f"{C.AZUL}¿Elegir otra habilidad? (s/n): {C.RESET}").lower()
                        if continuar != 's':
                            return None
                        limpiar_pantalla()
                        self.combate_actual.mostrar_intro_combate()
                        print(f"\n{C.CYAN}══════════ HABILIDADES DISPONIBLES ══════════{C.RESET}")
                        print(f"{C.VERDE}Energía disponible: {jugador.energia_actual}/{jugador.energia_maxima}{C.RESET}\n")
                        for j, hab in enumerate(jugador.habilidades, 1):
                            color = C.VERDE if jugador.energia_actual >= hab.costo_energia else C.ROJO
                            print(f"  {color}{j}. {hab.nombre} ({hab.costo_energia}E){C.RESET}")
                            print(f"     {hab.descripcion}")
                            if not jugador.energia_actual >= hab.costo_energia:
                                print(f"     {C.ROJO}¡Energía insuficiente!{C.RESET}")
                            print()
                        print(f"  {C.AMARILLO}0. Volver al combate{C.RESET}")
                else:
                    print(f"{C.ROJO}Opción no válida.{C.RESET}")
            except ValueError:
                print(f"{C.ROJO}Por favor, ingresa un número.{C.RESET}")

    def mostrar_stats_completos(self):
        """Muestra las stats completas de ambos personajes."""
        limpiar_pantalla()
        self.combate_actual.mostrar_intro_combate()

        print(f"\n{C.CYAN}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.CYAN}║         ESTADÍSTICAS COMPLETAS                   ║{C.RESET}")
        print(f"{C.CYAN}╠═══════════════════════════════════════════════════╣{C.RESET}")

        print(f"{C.CYAN}║ {C.VERDE}JUGADOR: {self.combate_actual.jugador.nombre}{C.CYAN}                     ║{C.RESET}")
        self.combate_actual.jugador.mostrar_stats()

        print(f"{C.CYAN}╠═══════════════════════════════════════════════════╣{C.RESET}")

        print(f"{C.CYAN}║ {C.ROJO}CPU: {self.combate_actual.ia.nombre}{C.CYAN}                           ║{C.RESET}")
        self.combate_actual.ia.mostrar_stats()

        print(f"{C.CYAN}╚═══════════════════════════════════════════════════╝{C.RESET}")

    def mostrar_fin_combate(self):
        """Muestra el resultado final del combate."""
        resultado = self.combate_actual.obtener_resultado_final()

        print(f"\n{C.NEGRITA}{C.AMARILLO}══════════ FIN DEL COMBATE ══════════{C.RESET}")
        print(resultado.mensaje_final)

        self.combate_actual.mostrar_estadisticas_finales(resultado)

        if resultado.estado == EstadoCombate.VICTORIA_JUGADOR:
            print(f"\n{C.VERDE}¡Enhorabuena! Has ganado {resultado.experiencia_ganada} puntos de experiencia.{C.RESET}")
            self.personaje_jugador.ganar_experiencia(resultado.experiencia_ganada)
            # Actualizar contador de victorias
            if not hasattr(self.personaje_jugador, '_partidas_ganadas'):
                self.personaje_jugador._partidas_ganadas = 0
            self.personaje_jugador._partidas_ganadas += 1
            print(f"{C.VERDE}¡Eres más español que un chotis en San Isidro!{C.RESET}")
        elif resultado.estado == EstadoCombate.VICTORIA_IA:
            print(f"\n{C.ROJO}¡La CPU te ha derrotado!{C.RESET}")
            print(f"{C.ROJO}No pasa nada, hasta el mejor segarro tiene malos días.{C.RESET}")
        else:
            print(f"\n{C.AMARILLO}¡Empate técnico!{C.RESET}")
            print(f"{C.AMARILLO}Ambos sois igual de españoles, lo cual es mucho decir.{C.RESET}")

    def preguntar_revancha(self, slot_actual=None):
        """Pregunta al jugador si quiere una revancha."""
        print(f"\n{C.CYAN}══════════ ¿QUÉ QUIERES HACER AHORA? ══════════{C.RESET}")
        print(f"  1. {C.VERDE}Revancha (mismos personajes){C.RESET}")
        print(f"  2. {C.AZUL}Nuevo combate (elegir nuevos personajes){C.RESET}")
        print(f"  3. {C.AMARILLO}Volver al menú principal{C.RESET}")

        while True:
            try:
                opcion = int(input(f"\n{C.AZUL}Elige una opción (1-3): {C.RESET}"))
                if opcion == 1:
                    # Revancha - reiniciar personajes
                    self.personaje_jugador.vida_actual = self.personaje_jugador.vida_maxima
                    self.personaje_jugador.energia_actual = self.personaje_jugador.energia_maxima
                    self.personaje_jugador.estados = []
                    self.personaje_jugador.estados_duracion = {}

                    self.personaje_cpu.vida_actual = self.personaje_cpu.vida_maxima
                    self.personaje_cpu.energia_actual = self.personaje_cpu.energia_maxima
                    self.personaje_cpu.estados = []
                    self.personaje_cpu.estados_duracion = {}

                    self.iniciar_nuevo_combate(partida_cargada=False, slot_actual=slot_actual)
                    break
                elif opcion == 2:
                    # Nuevo combate - resetear personajes
                    self.personaje_jugador = None
                    self.personaje_cpu = None
                    self.iniciar_nuevo_combate(partida_cargada=False, slot_actual=slot_actual)
                    break
                elif opcion == 3:
                    # Volver al menú principal
                    break
                else:
                    print(f"{C.ROJO}Opción no válida.{C.RESET}")
            except ValueError:
                print(f"{C.ROJO}Por favor, ingresa un número.{C.RESET}")