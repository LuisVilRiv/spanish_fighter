"""
Batalla Cómica Española - Juego Principal
Sistema de combate por turnos: Jugador vs CPU
Con sistema de guardado/carga JSON.
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
from utils.sistema_guardado import SistemaGuardado, SAVE_DIR, MAX_SLOTS

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa_para_continuar(mensaje="Presiona Enter para continuar..."):
    input(f"\n{C.CYAN}{mensaje}{C.RESET}")

class JuegoBatallaComica:
    def __init__(self):
        self.personajes_disponibles = [
            Segarro, Catolico, Sacerdote, Turista, Abuela,
            Politico, Torero, Flaquito, Choni, PutoAmo, Barrendero
        ]
        self.personaje_jugador = None
        self.personaje_cpu = None
        self.combate_actual = None
        self.slot_actual = None  # Slot de guardado activo
        SistemaGuardado.inicializar()
    
    def mostrar_titulo(self):
        limpiar_pantalla()
        print(f"\n{C.NEGRITA}{C.ROJO_BRILLANTE}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}║       BATALLA CÓMICA ESPAÑOLA - v1.0             ║{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}║          Jugador vs CPU                         ║{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}╚═══════════════════════════════════════════════════╝{C.RESET}")
        print(f"{C.CYAN}¡Prepárate para el combate más surrealista y español!{C.RESET}\n")
    
    def mostrar_menu_principal(self):
        limpiar_pantalla()
        self.mostrar_titulo()
        
        print(f"{C.VERDE}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.VERDE}║               MENÚ PRINCIPAL                     ║{C.RESET}")
        print(f"{C.VERDE}╠═══════════════════════════════════════════════════╣{C.RESET}")
        print(f"{C.VERDE}║   1. {C.AZUL}Nuevo Combate (Nueva Partida){C.VERDE}           ║{C.RESET}")
        print(f"{C.VERDE}║   2. {C.AZUL}Cargar Partida{C.VERDE}                          ║{C.RESET}")
        print(f"{C.VERDE}║   3. {C.AZUL}Ver Personajes Disponibles{C.VERDE}                ║{C.RESET}")
        print(f"{C.VERDE}║   4. {C.AZUL}Instrucciones del Juego{C.VERDE}                   ║{C.RESET}")
        print(f"{C.VERDE}║   5. {C.AZUL}Gestionar Partidas Guardadas{C.VERDE}             ║{C.RESET}")
        print(f"{C.VERDE}║   6. {C.AZUL}Salir del Juego{C.VERDE}                          ║{C.RESET}")
        print(f"{C.VERDE}╚═══════════════════════════════════════════════════╝{C.RESET}")
    
    # ---------- Menús de gestión de partidas ----------
    def menu_gestion_partidas(self):
        """Menú para ver y eliminar partidas guardadas."""
        while True:
            limpiar_pantalla()
            self.mostrar_titulo()
            print(f"\n{C.AMARILLO}╔═══════════════════════════════════════════════════╗{C.RESET}")
            print(f"{C.AMARILLO}║         GESTIÓN DE PARTIDAS GUARDADAS            ║{C.RESET}")
            print(f"{C.AMARILLO}╠═══════════════════════════════════════════════════╣{C.RESET}")
            
            slots_info = SistemaGuardado.obtener_info_slots()
            if not slots_info:
                print(f"{C.AMARILLO}║   No hay partidas guardadas.                      ║{C.RESET}")
            else:
                for slot_str, info in slots_info.items():
                    print(f"{C.AMARILLO}║   Slot {slot_str}: {info['nombre_personaje']} - {info['modo']} - {info['timestamp'][:10]}{C.RESET}")
            
            print(f"{C.AMARILLO}╠═══════════════════════════════════════════════════╣{C.RESET}")
            print(f"{C.AMARILLO}║   1. Eliminar una partida                        ║{C.RESET}")
            print(f"{C.AMARILLO}║   0. Volver al menú principal                    ║{C.RESET}")
            print(f"{C.AMARILLO}╚═══════════════════════════════════════════════════╝{C.RESET}")
            
            try:
                opcion = int(input(f"\n{C.AZUL}Elige una opción: {C.RESET}"))
                if opcion == 0:
                    return
                elif opcion == 1:
                    self.eliminar_partida_interactivo()
                else:
                    print(f"{C.ROJO}Opción no válida.{C.RESET}")
                    pausa_para_continuar()
            except ValueError:
                print(f"{C.ROJO}Por favor, ingresa un número.{C.RESET}")
                pausa_para_continuar()
    
    def eliminar_partida_interactivo(self):
        """Permite al usuario elegir qué slot eliminar."""
        limpiar_pantalla()
        self.mostrar_titulo()
        print(f"\n{C.ROJO}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.ROJO}║           ELIMINAR PARTIDA                        ║{C.RESET}")
        print(f"{C.ROJO}╠═══════════════════════════════════════════════════╣{C.RESET}")
        
        slots_info = SistemaGuardado.obtener_info_slots()
        if not slots_info:
            print(f"{C.ROJO}║   No hay partidas para eliminar.                 ║{C.RESET}")
            print(f"{C.ROJO}╚═══════════════════════════════════════════════════╝{C.RESET}")
            pausa_para_continuar()
            return
        
        for slot_str, info in slots_info.items():
            print(f"{C.ROJO}║   {slot_str}. {info['nombre_personaje']} - {info['timestamp'][:10]}     ║{C.RESET}")
        print(f"{C.ROJO}║   0. Cancelar                                     ║{C.RESET}")
        print(f"{C.ROJO}╚═══════════════════════════════════════════════════╝{C.RESET}")
        
        try:
            slot = int(input(f"\n{C.AZUL}¿Qué slot quieres eliminar? (0 para cancelar): {C.RESET}"))
            if slot == 0:
                return
            if SistemaGuardado.slot_ocupado(slot):
                confirmar = input(f"{C.ROJO}¿Estás seguro de eliminar la partida del slot {slot}? (s/n): {C.RESET}").lower()
                if confirmar == 's':
                    SistemaGuardado.eliminar_partida(slot)
                    if self.slot_actual == slot:
                        self.slot_actual = None
                        self.personaje_jugador = None
                pausa_para_continuar()
            else:
                print(f"{C.ROJO}El slot {slot} no tiene partida guardada.{C.RESET}")
                pausa_para_continuar()
        except ValueError:
            print(f"{C.ROJO}Por favor, ingresa un número.{C.RESET}")
            pausa_para_continuar()
    
    # ---------- Selección de slot ----------
    def seleccionar_slot(self, accion="guardar") -> int:
        """
        Muestra los slots disponibles y pide al usuario que elija uno.
        Retorna el número de slot seleccionado, o None si cancela.
        """
        while True:
            limpiar_pantalla()
            self.mostrar_titulo()
            print(f"\n{C.CYAN}╔═══════════════════════════════════════════════════╗{C.RESET}")
            print(f"{C.CYAN}║           SELECCIÓN DE SLOT                       ║{C.RESET}")
            print(f"{C.CYAN}╠═══════════════════════════════════════════════════╣{C.RESET}")
            
            slots_info = SistemaGuardado.obtener_info_slots()
            for i in range(MAX_SLOTS):
                if str(i) in slots_info:
                    info = slots_info[str(i)]
                    print(f"{C.CYAN}║   Slot {i}: {info['nombre_personaje']} - {info['timestamp'][:10]}   ║{C.RESET}")
                else:
                    print(f"{C.CYAN}║   Slot {i}: Vacío                               ║{C.RESET}")
            
            print(f"{C.CYAN}╠═══════════════════════════════════════════════════╣{C.RESET}")
            print(f"{C.CYAN}║   0. Cancelar                                    ║{C.RESET}")
            print(f"{C.CYAN}╚═══════════════════════════════════════════════════╝{C.RESET}")
            
            try:
                slot = int(input(f"\n{C.AZUL}Elige un slot (0-{MAX_SLOTS-1}, 0 para cancelar): {C.RESET}"))
                if slot == 0:
                    return None
                if 0 <= slot < MAX_SLOTS:
                    if accion == "cargar" and not SistemaGuardado.slot_ocupado(slot):
                        print(f"{C.ROJO}El slot {slot} está vacío. Elige otro.{C.RESET}")
                        pausa_para_continuar()
                        continue
                    if accion == "guardar" and SistemaGuardado.slot_ocupado(slot):
                        sobreescribir = input(f"{C.AMARILLO}El slot {slot} ya tiene una partida. ¿Sobrescribir? (s/n): {C.RESET}").lower()
                        if sobreescribir != 's':
                            continue
                    return slot
                else:
                    print(f"{C.ROJO}Slot no válido. Debe ser entre 0 y {MAX_SLOTS-1}.{C.RESET}")
                    pausa_para_continuar()
            except ValueError:
                print(f"{C.ROJO}Por favor, ingresa un número.{C.RESET}")
                pausa_para_continuar()
    
    # ---------- Guardar y cargar partida ----------
    def guardar_partida_actual(self):
        """Guarda la partida actual en el slot activo."""
        if self.personaje_jugador is None:
            print(f"{C.ROJO}No hay personaje para guardar.{C.RESET}")
            return False
        
        if self.slot_actual is None:
            slot = self.seleccionar_slot("guardar")
            if slot is None:
                print(f"{C.AMARILLO}Guardado cancelado.{C.RESET}")
                return False
            self.slot_actual = slot
        
        datos_jugador = SistemaGuardado.serializar_personaje(self.personaje_jugador)
        # Aquí se pueden añadir más datos del modo historia en el futuro
        SistemaGuardado.guardar_partida(self.slot_actual, datos_jugador, modo="normal")
        return True
    
    def cargar_partida_interactivo(self):
        """Permite al usuario cargar una partida desde un slot."""
        slot = self.seleccionar_slot("cargar")
        if slot is None:
            return False
        
        partida = SistemaGuardado.cargar_partida(slot)
        if partida:
            self.personaje_jugador = SistemaGuardado.deserializar_personaje(partida["jugador"])
            self.slot_actual = slot
            print(f"{C.VERDE_BRILLANTE}¡Partida cargada! Bienvenido de nuevo, {self.personaje_jugador.nombre}.{C.RESET}")
            self.personaje_jugador.mostrar_stats()
            pausa_para_continuar()
            return True
        return False
    
    # ---------- Flujo principal ----------
    def iniciar_nuevo_combate(self, desde_carga=False):
        """
        Inicia un nuevo combate.
        Si desde_carga es True, se usa el personaje ya cargado.
        Si no, se selecciona personaje nuevo.
        """
        if not desde_carga:
            if not self.seleccionar_personaje_jugador():
                return
            # Al crear personaje nuevo, se asigna slot después del combate o ahora?
            self.slot_actual = None  # Forzar elegir slot al guardar
        
        if not self.personaje_cpu:
            if not self.seleccionar_personaje_cpu():
                return
        
        # Confirmación de combate
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
            
            # Mostrar resumen y pausa
            if 'resultado' in locals():
                limpiar_pantalla()
                self.combate_actual.mostrar_intro_combate()
                self.combate_actual.mostrar_resumen_turno(resultado)
                pausa_para_continuar("Presiona Enter para continuar...")
        
        # Combate terminado
        limpiar_pantalla()
        self.mostrar_fin_combate()
        
        # Guardar partida después del combate (si se ganó o incluso si se perdió, para mantener progreso)
        if self.personaje_jugador.esta_vivo() or True:  # Siempre guardamos el estado actual
            guardar = input(f"\n{C.AZUL}¿Quieres guardar la partida? (s/n): {C.RESET}").lower()
            if guardar == 's':
                self.guardar_partida_actual()
        
        self.preguntar_revancha()
    
    # ---------- Métodos auxiliares (sin cambios, excepto integración de guardado) ----------
    def mostrar_opciones_turno(self):
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
                        # Re-muestra las habilidades
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
    
    def mostrar_personajes(self):
        limpiar_pantalla()
        self.mostrar_titulo()
        print(f"\n{C.CYAN}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.CYAN}║          PERSONAJES DISPONIBLES                  ║{C.RESET}")
        print(f"{C.CYAN}╠═══════════════════════════════════════════════════╣{C.RESET}")
        for i, personaje_clase in enumerate(self.personajes_disponibles, 1):
            print(f"{C.CYAN}║ {i:2}. {personaje_clase.__name__:20} {C.RESET}", end="")
            try:
                instancia = personaje_clase()
                tipo = instancia.tipo.split()[0] if hasattr(instancia, 'tipo') else ""
                print(f"{tipo:4} {instancia.descripcion()[:30]:30} ║{C.RESET}")
            except:
                print(f"{' ':4} {'Personaje disponible':30} ║{C.RESET}")
        print(f"{C.CYAN}╚═══════════════════════════════════════════════════╝{C.RESET}")
    
    def mostrar_instrucciones(self):
        limpiar_pantalla()
        self.mostrar_titulo()
        print(f"\n{C.AMARILLO}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.AMARILLO}║           INSTRUCCIONES DEL JUEGO                ║{C.RESET}")
        print(f"{C.AMARILLO}╠═══════════════════════════════════════════════════╣{C.RESET}")
        print(f"{C.AMARILLO}║ {C.NEGRITA}CÓMO JUGAR:{C.RESET}{C.AMARILLO}                                      ║{C.RESET}")
        print(f"{C.AMARILLO}║ 1. Elige tu personaje                            ║{C.RESET}")
        print(f"{C.AMARILLO}║ 2. Enfréntate a la CPU                           ║{C.RESET}")
        print(f"{C.AMARILLO}║ 3. Combate por turnos hasta que uno caiga        ║{C.RESET}")
        print(f"{C.AMARILLO}║                                                  ║{C.RESET}")
        print(f"{C.AMARILLO}║ {C.NEGRITA}ACCIONES POR TURNO:{C.RESET}{C.AMARILLO}                              ║{C.RESET}")
        print(f"{C.AMARILLO}║ 1. {C.VERDE}Ataque Básico{C.AMARILLO} - No gasta energía           ║{C.RESET}")
        print(f"{C.AMARILLO}║ 2. {C.VERDE}Habilidad Especial{C.AMARILLO} - Gasta energía         ║{C.RESET}")
        print(f"{C.AMARILLO}║ 3. {C.AZUL}Defender{C.AMARILLO} - Reduces daño recibido          ║{C.RESET}")
        print(f"{C.AMARILLO}║ 4. {C.AZUL}Concentrar{C.AMARILLO} - Recuperas energía            ║{C.RESET}")
        print(f"{C.AMARILLO}║                                                  ║{C.RESET}")
        print(f"{C.AMARILLO}║ {C.NEGRITA}EVENTOS ALEATORIOS:{C.RESET}{C.AMARILLO}                              ║{C.RESET}")
        print(f"{C.AMARILLO}║ Cada turno hay un 15% de probabilidad de que     ║{C.RESET}")
        print(f"{C.AMARILLO}║ ocurra algo WTF (Jamón volador, abuela, etc.)   ║{C.RESET}")
        print(f"{C.AMARILLO}╚═══════════════════════════════════════════════════╝{C.RESET}")
    
    def seleccionar_personaje_jugador(self):
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
    
    def mostrar_stats_completos(self):
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
        resultado = self.combate_actual.obtener_resultado_final()
        print(f"\n{C.NEGRITA}{C.AMARILLO}══════════ FIN DEL COMBATE ══════════{C.RESET}")
        print(resultado.mensaje_final)
        self.combate_actual.mostrar_estadisticas_finales(resultado)
        if resultado.estado == EstadoCombate.VICTORIA_JUGADOR:
            print(f"\n{C.VERDE}¡Enhorabuena! Has ganado {resultado.experiencia_ganada} puntos de experiencia.{C.RESET}")
            self.personaje_jugador.ganar_experiencia(resultado.experiencia_ganada)
            print(f"{C.VERDE}¡Eres más español que un chotis en San Isidro!{C.RESET}")
        elif resultado.estado == EstadoCombate.VICTORIA_IA:
            print(f"\n{C.ROJO}¡La CPU te ha derrotado!{C.RESET}")
            print(f"{C.ROJO}No pasa nada, hasta el mejor segarro tiene malos días.{C.RESET}")
        else:
            print(f"\n{C.AMARILLO}¡Empate técnico!{C.RESET}")
            print(f"{C.AMARILLO}Ambos sois igual de españoles, lo cual es mucho decir.{C.RESET}")
    
    def preguntar_revancha(self):
        print(f"\n{C.CYAN}══════════ ¿QUÉ QUIERES HACER AHORA? ══════════{C.RESET}")
        print(f"  1. {C.VERDE}Revancha (mismos personajes){C.RESET}")
        print(f"  2. {C.AZUL}Nuevo combate (elegir nuevos personajes){C.RESET}")
        print(f"  3. {C.AMARILLO}Volver al menú principal{C.RESET}")
        while True:
            try:
                opcion = int(input(f"\n{C.AZUL}Elige una opción (1-3): {C.RESET}"))
                if opcion == 1:
                    self.personaje_jugador.vida_actual = self.personaje_jugador.vida_maxima
                    self.personaje_jugador.energia_actual = self.personaje_jugador.energia_maxima
                    self.personaje_jugador.estados = []
                    self.personaje_jugador.estados_duracion = {}
                    self.personaje_cpu.vida_actual = self.personaje_cpu.vida_maxima
                    self.personaje_cpu.energia_actual = self.personaje_cpu.energia_maxima
                    self.personaje_cpu.estados = []
                    self.personaje_cpu.estados_duracion = {}
                    self.iniciar_nuevo_combate(desde_carga=True)
                    break
                elif opcion == 2:
                    self.personaje_jugador = None
                    self.personaje_cpu = None
                    self.slot_actual = None
                    self.iniciar_nuevo_combate(desde_carga=False)
                    break
                elif opcion == 3:
                    break
                else:
                    print(f"{C.ROJO}Opción no válida.{C.RESET}")
            except ValueError:
                print(f"{C.ROJO}Por favor, ingresa un número.{C.RESET}")
    
    def ejecutar(self):
        self.mostrar_titulo()
        while True:
            self.mostrar_menu_principal()
            try:
                opcion = int(input(f"\n{C.AZUL}Elige una opción (1-6): {C.RESET}"))
                if opcion == 1:
                    # Nueva partida
                    self.personaje_jugador = None
                    self.personaje_cpu = None
                    self.slot_actual = None
                    self.iniciar_nuevo_combate(desde_carga=False)
                elif opcion == 2:
                    # Cargar partida
                    if self.cargar_partida_interactivo():
                        # Una vez cargado el personaje, ofrecer combate
                        self.personaje_cpu = None
                        self.iniciar_nuevo_combate(desde_carga=True)
                elif opcion == 3:
                    self.mostrar_personajes()
                    pausa_para_continuar()
                elif opcion == 4:
                    self.mostrar_instrucciones()
                    pausa_para_continuar()
                elif opcion == 5:
                    self.menu_gestion_partidas()
                elif opcion == 6:
                    # Guardar antes de salir si hay partida activa
                    if self.personaje_jugador is not None and self.personaje_jugador.esta_vivo():
                        guardar = input(f"{C.AZUL}¿Quieres guardar la partida antes de salir? (s/n): {C.RESET}").lower()
                        if guardar == 's':
                            self.guardar_partida_actual()
                    limpiar_pantalla()
                    print(f"\n{C.VERDE}¡Gracias por jugar a Batalla Cómica Española!{C.RESET}")
                    print(f"{C.VERDE}¡Hasta la próxima, crack!{C.RESET}")
                    break
                else:
                    print(f"{C.ROJO}Opción no válida. Intenta de nuevo.{C.RESET}")
                    pausa_para_continuar()
            except ValueError:
                print(f"{C.ROJO}Por favor, ingresa un número.{C.RESET}")
                pausa_para_continuar()
            except KeyboardInterrupt:
                print(f"\n\n{C.ROJO}¡Juego interrumpido!{C.RESET}")
                break
            except Exception as e:
                print(f"\n{C.ROJO}Error inesperado: {e}{C.RESET}")
                import traceback
                traceback.print_exc()
                pausa_para_continuar()

def main():
    try:
        juego = JuegoBatallaComica()
        juego.ejecutar()
    except KeyboardInterrupt:
        print(f"\n\n{C.ROJO}¡Juego interrumpido por el usuario!{C.RESET}")
    except Exception as e:
        print(f"\n{C.ROJO}Error crítico: {e}{C.RESET}")
        import traceback
        traceback.print_exc()
    finally:
        print(f"\n{C.CYAN}─────────────────────────────────────────────────{C.RESET}")
        print(f"{C.CYAN}Batalla Cómica Española se ha cerrado.{C.RESET}")

if __name__ == "__main__":
    main()