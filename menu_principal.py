"""
menu_principal.py - Menú principal con sistema de guardado/carga.
"""

import os
import sys
from typing import Optional

from utils import Colores as C
from sistema_guardado import GestorGuardado, crear_datos_jugador, restaurar_personaje, slot_disponible
from personajes import (
    Segarro, Catolico, Sacerdote, Turista, Abuela,
    Politico, Torero, Flaquito, Choni, PutoAmo, Barrendero
)
from juego import JuegoBatallaComica
from eula import verificar_eula

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa():
    input(f"\n{C.CYAN}Presiona Enter para continuar...{C.RESET}")

class MenuPrincipal:
    def __init__(self):
        self.gestor_guardado = GestorGuardado()
        self.juego = None

    def mostrar_titulo(self):
        limpiar_pantalla()
        print(f"\n{C.NEGRITA}{C.ROJO_BRILLANTE}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}║       BATALLA CÓMICA ESPAÑOLA - v1.0             ║{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}║          Sistema de Guardado Cifrado            ║{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}╚═══════════════════════════════════════════════════╝{C.RESET}")
        print(f"{C.CYAN}¡Prepárate para el combate más surrealista y español!{C.RESET}\n")

    def mostrar_menu(self):
        self.mostrar_titulo()
        print(f"{C.VERDE}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.VERDE}║               MENÚ PRINCIPAL                     ║{C.RESET}")
        print(f"{C.VERDE}╠═══════════════════════════════════════════════════╣{C.RESET}")
        print(f"{C.VERDE}║   1. {C.AZUL}Nueva Partida{C.VERDE}                             ║{C.RESET}")
        print(f"{C.VERDE}║   2. {C.AZUL}Cargar Partida{C.VERDE}                            ║{C.RESET}")
        print(f"{C.VERDE}║   3. {C.AZUL}Ver Personajes{C.VERDE}                            ║{C.RESET}")
        print(f"{C.VERDE}║   4. {C.AZUL}Instrucciones{C.VERDE}                             ║{C.RESET}")
        print(f"{C.VERDE}║   5. {C.AZUL}Salir{C.VERDE}                                     ║{C.RESET}")
        print(f"{C.VERDE}╚═══════════════════════════════════════════════════╝{C.RESET}")

    def seleccionar_slot(self, accion: str) -> Optional[int]:
        """Muestra los slots disponibles y pide elegir uno."""
        slots = self.gestor_guardado.listar_partidas()
        print(f"\n{C.AMARILLO}📁 Slots disponibles: {slots if slots else 'Ninguno'}{C.RESET}")
        print(f"{C.CYAN}   • 0: Volver{C.RESET}")
        try:
            slot = int(input(f"\n{C.AZUL}Elige un slot (1-9, 0 para volver): {C.RESET}"))
            if slot == 0:
                return None
            if 1 <= slot <= 9:
                return slot
            else:
                print(f"{C.ROJO}Slot no válido.{C.RESET}")
                return self.seleccionar_slot(accion)
        except ValueError:
            print(f"{C.ROJO}Por favor, ingresa un número.{C.RESET}")
            return self.seleccionar_slot(accion)

    def nueva_partida(self):
        """Inicia una nueva partida (elige personaje y guarda)."""
        self.juego = JuegoBatallaComica()
        if not self.juego.seleccionar_personaje_jugador():
            return

        # Elegir slot
        slot = slot_disponible(self.gestor_guardado)
        print(f"\n{C.CYAN}Se usará el slot {slot} para guardar la partida.{C.RESET}")

        # Guardar datos iniciales
        datos = crear_datos_jugador(self.juego.personaje_jugador)
        if self.gestor_guardado.guardar_partida(datos, slot):
            self.juego.iniciar_nuevo_combate(partida_cargada=False, slot_actual=slot)
        else:
            print(f"{C.ROJO}No se pudo guardar la partida. ¿Continuar sin guardar?{C.RESET}")
            if input("s/n: ").lower() == 's':
                self.juego.iniciar_nuevo_combate(partida_cargada=False, slot_actual=None)

    def cargar_partida(self):
        """Carga una partida existente."""
        slots = self.gestor_guardado.listar_partidas()
        if not slots:
            print(f"\n{C.AMARILLO}No hay partidas guardadas.{C.RESET}")
            pausa()
            return

        slot = self.seleccionar_slot("cargar")
        if slot is None:
            return

        datos = self.gestor_guardado.cargar_partida(slot)
        if not datos:
            pausa()
            return

        # Mapeo de nombres de clase a clases reales
        personajes_map = {
            "Segarro": Segarro,
            "Catolico": Catolico,
            "Sacerdote": Sacerdote,
            "Turista": Turista,
            "Abuela": Abuela,
            "Politico": Politico,
            "Torero": Torero,
            "Flaquito": Flaquito,
            "Choni": Choni,
            "PutoAmo": PutoAmo,
            "Barrendero": Barrendero
        }
        nombre_clase = datos["tipo"].split(" ")[1] if " " in datos["tipo"] else datos["tipo"]
        clase = personajes_map.get(nombre_clase)
        if not clase:
            print(f"{C.ROJO}Error: personaje '{datos['tipo']}' no encontrado.{C.RESET}")
            pausa()
            return

        personaje = clase()
        restaurar_personaje(personaje, datos)

        # Iniciar juego con personaje cargado
        self.juego = JuegoBatallaComica()
        self.juego.personaje_jugador = personaje
        self.juego.iniciar_nuevo_combate(partida_cargada=True, slot_actual=slot, datos_cargados=datos)

    def ver_personajes(self):
        from personajes import __all__ as lista_personajes
        limpiar_pantalla()
        self.mostrar_titulo()
        print(f"\n{C.CYAN}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.CYAN}║          PERSONAJES DISPONIBLES                  ║{C.RESET}")
        print(f"{C.CYAN}╠═══════════════════════════════════════════════════╣{C.RESET}")
        for i, nombre_clase in enumerate(lista_personajes, 1):
            clase = globals()[nombre_clase]
            instancia = clase()
            print(f"{C.CYAN}║ {i:2}. {nombre_clase:20} {C.RESET}{instancia.tipo[:20]:20} ║{C.RESET}")
        print(f"{C.CYAN}╚═══════════════════════════════════════════════════╝{C.RESET}")
        pausa()

    def instrucciones(self):
        limpiar_pantalla()
        self.mostrar_titulo()
        print(f"\n{C.AMARILLO}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.AMARILLO}║           INSTRUCCIONES DEL JUEGO                ║{C.RESET}")
        print(f"{C.AMARILLO}╠═══════════════════════════════════════════════════╣{C.RESET}")
        print(f"{C.AMARILLO}║ • Sistema de guardado cifrado                    ║{C.RESET}")
        print(f"{C.AMARILLO}║ • 3 slots de partida independientes              ║{C.RESET}")
        print(f"{C.AMARILLO}║ • El progreso se guarda automáticamente          ║{C.RESET}")
        print(f"{C.AMARILLO}║ • Los archivos .dat están cifrados con AES      ║{C.RESET}")
        print(f"{C.AMARILLO}║ • No se puede editar manualmente                ║{C.RESET}")
        print(f"{C.AMARILLO}╚═══════════════════════════════════════════════════╝{C.RESET}")
        pausa()

    def ejecutar(self):
        # Verificar EULA
        if not verificar_eula():
            return

        while True:
            self.mostrar_menu()
            try:
                opcion = int(input(f"\n{C.AZUL}Elige una opción (1-5): {C.RESET}"))
                if opcion == 1:
                    self.nueva_partida()
                elif opcion == 2:
                    self.cargar_partida()
                elif opcion == 3:
                    self.ver_personajes()
                elif opcion == 4:
                    self.instrucciones()
                elif opcion == 5:
                    print(f"\n{C.VERDE}¡Gracias por jugar!{C.RESET}")
                    break
                else:
                    print(f"{C.ROJO}Opción no válida.{C.RESET}")
                    pausa()
            except ValueError:
                print(f"{C.ROJO}Por favor, ingresa un número.{C.RESET}")
                pausa()