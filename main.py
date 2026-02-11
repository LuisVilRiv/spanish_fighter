"""
Batalla Cómica Española - Juego Principal
Sistema de combate por turnos: Jugador vs CPU
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

def limpiar_pantalla():
    """Limpia la pantalla de la terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa_para_continuar(mensaje="Presiona Enter para continuar..."):
    """Muestra un mensaje y espera a que el usuario presione Enter."""
    input(f"\n{C.CYAN}{mensaje}{C.RESET}")

class JuegoBatallaComica:
    """Clase principal del juego."""
    
    def __init__(self):
        """Inicializa el juego."""
        self.personajes_disponibles = [
            Segarro, Catolico, Sacerdote, Turista, Abuela,
            Politico, Torero, Flaquito, Choni, PutoAmo, Barrendero
        ]
        self.personaje_jugador = None
        self.personaje_cpu = None
        self.combate_actual = None
        
    def mostrar_titulo(self):
        """Muestra el título del juego."""
        limpiar_pantalla()
        print(f"\n{C.NEGRITA}{C.ROJO_BRILLANTE}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}║       BATALLA CÓMICA ESPAÑOLA - v1.0             ║{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}║          Jugador vs CPU                         ║{C.RESET}")
        print(f"{C.NEGRITA}{C.ROJO_BRILLANTE}╚═══════════════════════════════════════════════════╝{C.RESET}")
        print(f"{C.CYAN}¡Prepárate para el combate más surrealista y español!{C.RESET}\n")
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal."""
        limpiar_pantalla()
        self.mostrar_titulo()
        
        print(f"{C.VERDE}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.VERDE}║               MENÚ PRINCIPAL                     ║{C.RESET}")
        print(f"{C.VERDE}╠═══════════════════════════════════════════════════╣{C.RESET}")
        print(f"{C.VERDE}║   1. {C.AZUL}Nuevo Combate (Jugador vs CPU){C.VERDE}             ║{C.RESET}")
        print(f"{C.VERDE}║   2. {C.AZUL}Ver Personajes Disponibles{C.VERDE}                ║{C.RESET}")
        print(f"{C.VERDE}║   3. {C.AZUL}Instrucciones del Juego{C.VERDE}                   ║{C.RESET}")
        print(f"{C.VERDE}║   4. {C.AZUL}Salir del Juego{C.VERDE}                          ║{C.RESET}")
        print(f"{C.VERDE}╚═══════════════════════════════════════════════════╝{C.RESET}")
    
    def mostrar_personajes(self):
        """Muestra todos los personajes disponibles."""
        limpiar_pantalla()
        self.mostrar_titulo()
        
        print(f"\n{C.CYAN}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.CYAN}║          PERSONAJES DISPONIBLES                  ║{C.RESET}")
        print(f"{C.CYAN}╠═══════════════════════════════════════════════════╣{C.RESET}")
        
        for i, personaje_clase in enumerate(self.personajes_disponibles, 1):
            print(f"{C.CYAN}║ {i:2}. {personaje_clase.__name__:20} {C.RESET}", end="")
            
            # Crear instancia temporal para mostrar descripción
            try:
                instancia = personaje_clase()
                # Mostrar emoji si está disponible
                tipo = instancia.tipo.split()[0] if hasattr(instancia, 'tipo') else ""
                print(f"{tipo:4} {instancia.descripcion()[:30]:30} ║{C.RESET}")
            except:
                print(f"{' ':4} {'Personaje disponible':30} ║{C.RESET}")
        
        print(f"{C.CYAN}╚═══════════════════════════════════════════════════╝{C.RESET}")
    
    def mostrar_instrucciones(self):
        """Muestra las instrucciones del juego."""
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
        """Permite al jugador seleccionar su personaje."""
        limpiar_pantalla()
        self.mostrar_titulo()
        
        print(f"\n{C.VERDE}╔═══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.VERDE}║       SELECCIONA TU PERSONAJE                    ║{C.RESET}")
        print(f"{C.VERDE}╠═══════════════════════════════════════════════════╣{C.RESET}")
        
        for i, personaje_clase in enumerate(self.personajes_disponibles, 1):
            # Crear instancia temporal para mostrar stats básicas
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
                    
                    # Preguntar si quiere nombre personalizado
                    nombre_personalizado = input(f"{C.AZUL}¿Quieres un nombre personalizado? (deja vacío para usar el predeterminado): {C.RESET}")
                    if nombre_personalizado.strip():
                        # Intentar crear con nombre personalizado
                        try:
                            self.personaje_jugador = personaje_clase(nombre_personalizado.strip())
                        except TypeError:
                            # Si el personaje no acepta nombre personalizado, usar predeterminado
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
        
        # Filtrar personajes si se debe excluir el del jugador
        personajes_cpu = self.personajes_disponibles.copy()
        if excluir_jugador and self.personaje_jugador:
            # Encontrar la clase del personaje del jugador
            jugador_clase = type(self.personaje_jugador)
            # Crear nueva lista excluyendo esa clase
            personajes_cpu = [p for p in personajes_cpu if p != jugador_clase]
        
        for i, personaje_clase in enumerate(personajes_cpu, 1):
            # Crear instancia temporal para mostrar stats básicas
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
                    # Selección aleatoria
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
    
    def iniciar_nuevo_combate(self):
        """Inicia un nuevo combate jugador vs CPU."""
        # Paso 1: Seleccionar personaje del jugador
        if not self.personaje_jugador:
            if not self.seleccionar_personaje_jugador():
                return  # El jugador decidió volver
        
        # Paso 2: Seleccionar personaje de la CPU
        if not self.personaje_cpu:
            if not self.seleccionar_personaje_cpu():
                return  # El jugador decidió volver
        
        # Paso 3: Confirmar combate
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
        
        # Paso 4: Crear y ejecutar combate
        self.combate_actual = Combate(self.personaje_jugador, self.personaje_cpu)
        
        # Bucle principal del combate
        while self.combate_actual.estado == EstadoCombate.EN_CURSO:
            limpiar_pantalla()
            self.combate_actual.mostrar_intro_combate()
            self.mostrar_opciones_turno()
            
            # Obtener acción del jugador
            accion_valida = False
            while not accion_valida:
                try:
                    opcion = int(input(f"\n{C.AZUL}Elige una acción (1-4, 9 para stats, 0 para rendirse): {C.RESET}"))
                    
                    if opcion == 1:
                        # Ataque básico
                        resultado = self.combate_actual.ejecutar_turno(Accion.ATAQUE_BASICO)
                        accion_valida = True
                    
                    elif opcion == 2:
                        # Habilidad especial
                        indice_habilidad = self.seleccionar_habilidad()
                        if indice_habilidad is not None:
                            resultado = self.combate_actual.ejecutar_turno(Accion.HABILIDAD_ESPECIAL, indice_habilidad)
                            accion_valida = True
                        else:
                            # El jugador decidió volver, mostrar opciones nuevamente
                            limpiar_pantalla()
                            self.combate_actual.mostrar_intro_combate()
                            self.mostrar_opciones_turno()
                    
                    elif opcion == 3:
                        # Defender
                        resultado = self.combate_actual.ejecutar_turno(Accion.DEFENDER)
                        accion_valida = True
                    
                    elif opcion == 4:
                        # Concentrar
                        resultado = self.combate_actual.ejecutar_turno(Accion.CONCENTRAR)
                        accion_valida = True
                    
                    elif opcion == 0:
                        # Rendirse
                        rendirse = input(f"{C.ROJO}¿Estás seguro de que quieres rendirte? (s/n): {C.RESET}").lower()
                        if rendirse == 's':
                            self.personaje_jugador.vida_actual = 0
                            self.combate_actual.estado = EstadoCombate.VICTORIA_IA
                            accion_valida = True
                        else:
                            # Mostrar opciones nuevamente
                            limpiar_pantalla()
                            self.combate_actual.mostrar_intro_combate()
                            self.mostrar_opciones_turno()
                    
                    elif opcion == 9:
                        # Ver stats
                        self.mostrar_stats_completos()
                        # No marca accion_valida como True, así que vuelve a pedir acción
                        pausa_para_continuar("Presiona Enter para volver al combate...")
                        limpiar_pantalla()
                        self.combate_actual.mostrar_intro_combate()
                        self.mostrar_opciones_turno()
                    
                    else:
                        print(f"{C.ROJO}Opción no válida. Intenta de nuevo.{C.RESET}")
                
                except ValueError:
                    print(f"{C.ROJO}Por favor, ingresa un número.{C.RESET}")
            
            # Mostrar resultado del turno
            if 'resultado' in locals():
                limpiar_pantalla()
                self.combate_actual.mostrar_intro_combate()
                self.combate_actual.mostrar_resumen_turno(resultado)
                
                # Pequeña pausa para que el jugador pueda leer
                if self.combate_actual.estado == EstadoCombate.EN_CURSO:
                    pausa_para_continuar("Presiona Enter para continuar al siguiente turno...")
        
        # Combate terminado
        limpiar_pantalla()
        self.mostrar_fin_combate()
        
        # Preguntar si quiere revancha
        self.preguntar_revancha()
    
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
            print()  # Línea en blanco entre habilidades
        
        print(f"  {C.AMARILLO}0. Volver al combate{C.RESET}")
        
        while True:
            try:
                opcion = int(input(f"\n{C.AZUL}Elige una habilidad (1-{len(jugador.habilidades)}, 0 para volver): {C.RESET}"))
                
                if opcion == 0:
                    return None
                
                if 1 <= opcion <= len(jugador.habilidades):
                    habilidad = jugador.habilidades[opcion - 1]
                    
                    if jugador.energia_actual >= habilidad.costo_energia:
                        return opcion - 1  # Retorna el índice
                    else:
                        print(f"\n{C.ROJO}No tienes suficiente energía para usar '{habilidad.nombre}'.{C.RESET}")
                        print(f"{C.ROJO}Energía necesaria: {habilidad.costo_energia}, Energía actual: {jugador.energia_actual}{C.RESET}")
                        # Preguntar si quiere elegir otra habilidad
                        continuar = input(f"{C.AZUL}¿Elegir otra habilidad? (s/n): {C.RESET}").lower()
                        if continuar != 's':
                            return None
                        # Limpiar y mostrar habilidades nuevamente
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
        
        # Stats del jugador
        print(f"{C.CYAN}║ {C.VERDE}JUGADOR: {self.combate_actual.jugador.nombre}{C.CYAN}                     ║{C.RESET}")
        self.combate_actual.jugador.mostrar_stats()
        
        print(f"{C.CYAN}╠═══════════════════════════════════════════════════╣{C.RESET}")
        
        # Stats de la CPU
        print(f"{C.CYAN}║ {C.ROJO}CPU: {self.combate_actual.ia.nombre}{C.CYAN}                           ║{C.RESET}")
        self.combate_actual.ia.mostrar_stats()
        
        print(f"{C.CYAN}╚═══════════════════════════════════════════════════╝{C.RESET}")
    
    def mostrar_fin_combate(self):
        """Muestra el resultado final del combate."""
        resultado = self.combate_actual.obtener_resultado_final()
        
        print(f"\n{C.NEGRITA}{C.AMARILLO}══════════ FIN DEL COMBATE ══════════{C.RESET}")
        print(resultado.mensaje_final)
        
        # Mostrar estadísticas finales
        self.combate_actual.mostrar_estadisticas_finales(resultado)
        
        # Mensaje adicional según resultado
        if resultado.estado == EstadoCombate.VICTORIA_JUGADOR:
            print(f"\n{C.VERDE}¡Enhorabuena! Has ganado {resultado.experiencia_ganada} puntos de experiencia.{C.RESET}")
            # Aplicar experiencia al personaje del jugador
            self.personaje_jugador.ganar_experiencia(resultado.experiencia_ganada)
            print(f"{C.VERDE}¡Eres más español que un chotis en San Isidro!{C.RESET}")
        
        elif resultado.estado == EstadoCombate.VICTORIA_IA:
            print(f"\n{C.ROJO}¡La CPU te ha derrotado!{C.RESET}")
            print(f"{C.ROJO}No pasa nada, hasta el mejor segarro tiene malos días.{C.RESET}")
        
        else:  # Empate
            print(f"\n{C.AMARILLO}¡Empate técnico!{C.RESET}")
            print(f"{C.AMARILLO}Ambos sois igual de españoles, lo cual es mucho decir.{C.RESET}")
    
    def preguntar_revancha(self):
        """Pregunta al jugador si quiere una revancha."""
        print(f"\n{C.CYAN}══════════ ¿QUÉ QUIERES HACER AHORA? ══════════{C.RESET}")
        print(f"  1. {C.VERDE}Revancha (mismos personajes){C.RESET}")
        print(f"  2. {C.AZUL}Nuevo combate (elegir nuevos personajes){C.RESET}")
        print(f"  3. {C.AMARILLO}Volver al menú principal{C.RESET}")
        
        while True:
            try:
                opcion = int(input(f"\n{C.AZUL}Elige una opción (1-3): {C.RESET}"))
                
                if opcion == 1:
                    # Revancha - reiniciar personajes y combate
                    self.personaje_jugador.vida_actual = self.personaje_jugador.vida_maxima
                    self.personaje_jugador.energia_actual = self.personaje_jugador.energia_maxima
                    self.personaje_jugador.estados = []
                    
                    self.personaje_cpu.vida_actual = self.personaje_cpu.vida_maxima
                    self.personaje_cpu.energia_actual = self.personaje_cpu.energia_maxima
                    self.personaje_cpu.estados = []
                    
                    self.iniciar_nuevo_combate()
                    break
                
                elif opcion == 2:
                    # Nuevo combate - resetear personajes
                    self.personaje_jugador = None
                    self.personaje_cpu = None
                    self.iniciar_nuevo_combate()
                    break
                
                elif opcion == 3:
                    # Volver al menú principal
                    break
                
                else:
                    print(f"{C.ROJO}Opción no válida.{C.RESET}")
            
            except ValueError:
                print(f"{C.ROJO}Por favor, ingresa un número.{C.RESET}")
    
    def ejecutar(self):
        """Método principal que ejecuta el juego."""
        self.mostrar_titulo()
        
        while True:
            self.mostrar_menu_principal()
            
            try:
                opcion = int(input(f"\n{C.AZUL}Elige una opción (1-4): {C.RESET}"))
                
                if opcion == 1:
                    # Nuevo combate
                    self.iniciar_nuevo_combate()
                
                elif opcion == 2:
                    # Ver personajes
                    self.mostrar_personajes()
                    pausa_para_continuar()
                
                elif opcion == 3:
                    # Instrucciones
                    self.mostrar_instrucciones()
                    pausa_para_continuar()
                
                elif opcion == 4:
                    # Salir
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
                print(f"{C.ROJO}Por favor, reporta este error.{C.RESET}")
                pausa_para_continuar()


def main():
    """Función principal del juego."""
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