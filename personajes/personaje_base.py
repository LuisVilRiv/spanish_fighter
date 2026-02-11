"""
Clase base abstracta para todos los personajes del juego.
Define la estructura común y métodos abstractos que cada personaje debe implementar.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TYPE_CHECKING
import random

# Importación condicional para evitar import circular
if TYPE_CHECKING:
    from habilidades.habilidad_base import Habilidad

class Personaje(ABC):
    """
    Clase base para todos los personajes del juego.
    
    Atributos:
        nombre (str): Nombre del personaje
        tipo (str): Tipo/Clase del personaje con emoji
        nivel (int): Nivel actual
        experiencia (int): Experiencia acumulada
        experiencia_necesaria (int): Exp necesaria para subir de nivel
        vida_maxima (int): Vida máxima
        vida_actual (int): Vida actual
        ataque_base (int): Ataque base
        defensa_base (int): Defensa base
        velocidad_base (int): Velocidad base
        ataque (int): Ataque actual (puede tener modificadores)
        defensa (int): Defensa actual (puede tener modificadores)
        velocidad (int): Velocidad actual (puede tener modificadores)
        energia_maxima (int): Energía máxima
        energia_actual (int): Energía actual
        estados (List[str]): Estados alterados activos
        estados_duracion (Dict[str, int]): Duración restante de cada estado (turnos)
        es_ia (bool): Si es controlado por la IA
        debilidades (List[str]): Tipos que hacen x2 daño
        fortalezas (List[str]): Tipos que hacen x0.5 daño
        inmunidades (List[str]): Tipos que no hacen daño
        habilidades (List[Habilidad]): Habilidades del personaje
    """
    
    def __init__(self, nombre: str, tipo: str, vida_base: int, ataque_base: int, 
                 defensa_base: int, velocidad_base: int, energia_base: int = 100):
        """
        Inicializa un nuevo personaje.
        
        Args:
            nombre: Nombre del personaje
            tipo: Tipo/Clase con emoji
            vida_base: Vida máxima inicial
            ataque_base: Ataque base inicial
            defensa_base: Defensa base inicial
            velocidad_base: Velocidad base inicial
            energia_base: Energía máxima inicial
        """
        # Información básica
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = 1
        self.experiencia = 0
        self.experiencia_necesaria = 100
        
        # Estadísticas base
        self.vida_maxima = vida_base
        self.vida_actual = vida_base
        self.ataque_base = ataque_base
        self.defensa_base = defensa_base
        self.velocidad_base = velocidad_base
        
        # Estadísticas actuales (pueden tener modificadores)
        self.ataque = ataque_base
        self.defensa = defensa_base
        self.velocidad = velocidad_base
        
        # Sistema de energía
        self.energia_maxima = energia_base
        self.energia_actual = energia_base
        
        # Estados y efectos
        self.estados = []
        self.estados_duracion = {}   # estado -> turnos restantes
        self.es_ia = False
        
        # Sistema de tipos (como Pokémon)
        self.debilidades = []
        self.fortalezas = []
        self.inmunidades = []
        
        # Habilidades (se inicializan en el método abstracto)
        self.habilidades = []
        
        # Inicializar habilidades específicas
        self.inicializar_habilidades()
    
    @abstractmethod
    def inicializar_habilidades(self) -> None:
        """
        Método abstracto: cada personaje debe definir sus habilidades únicas.
        """
        pass
    
    def regenerar(self) -> None:
        """
        Regeneración especial del personaje (puede ser sobrescrito por subclases).
        Por defecto, no hace nada. Los personajes pueden sobrescribir para tener regeneración especial.
        """
        pass
    
    @classmethod
    @abstractmethod
    def descripcion(cls) -> str:
        """
        Método abstracto: descripción del personaje para menús.
        
        Returns:
            Descripción del personaje
        """
        return "Personaje base sin descripción"
    
    def mostrar_stats(self) -> None:
        """
        Muestra las estadísticas del personaje de forma visual.
        """
        from utils import Colores as C
        
        print(f"\n{C.NEGRITA}{C.AZUL}┌───── ESTADÍSTICAS ──────────────────────┐{C.RESET}")
        print(f"{C.CYAN} Nombre: {C.NEGRITA}{self.nombre}{C.RESET}")
        print(f"{C.CYAN} Tipo:   {self.tipo}{C.RESET}")
        print(f"{C.CYAN} Nivel:  {self.nivel}{C.RESET}")
        print(f"{C.VERDE} Vida:   {self.vida_actual}/{self.vida_maxima}{C.RESET}")
        print(f"{C.ROJO} Ataque: {self.ataque}{C.RESET}")
        print(f"{C.AMARILLO} Defensa:{self.defensa}{C.RESET}")
        print(f"{C.MAGENTA} Veloc.: {self.velocidad}{C.RESET}")
        print(f"{C.AZUL} Energía:{self.energia_actual}/{self.energia_maxima}{C.RESET}")
        
        # Mostrar estados si los hay
        if self.estados:
            print(f"{C.CYAN} Estados: {', '.join(self.estados)}{C.RESET}")
        
        # Mostrar habilidades
        print(f"\n{C.CYAN}Habilidades:{C.RESET}")
        for i, habilidad in enumerate(self.habilidades, 1):
            costo = f"({habilidad.costo_energia}E)" if hasattr(habilidad, 'costo_energia') else ""
            print(f"  {i}. {habilidad.nombre} {costo}")
            print(f"     {habilidad.descripcion}")
        
        print(f"{C.AZUL}└─────────────────────────────────────────┘{C.RESET}")
    
    def recibir_dano(self, dano: int, tipo_dano: str = "normal", critico: bool = False) -> int:
        """
        Recibe daño aplicando modificadores de tipo.
        
        Args:
            dano: Daño base a recibir
            tipo_dano: Tipo del daño
            critico: Si es un ataque crítico (opcional)
            
        Returns:
            Daño realmente recibido
        """
        from utils import Colores as C
        
        # Aplicar modificadores de tipo
        multiplicador = 1.0
        
        if tipo_dano in self.debilidades:
            multiplicador = 2.0
            print(f"{C.ROJO}¡EFECTO SUPEREFECTIVO! x2{C.RESET}")
        
        elif tipo_dano in self.fortalezas:
            multiplicador = 0.5
            print(f"{C.VERDE}¡RESISTENCIA! /2{C.RESET}")
        
        elif tipo_dano in self.inmunidades:
            multiplicador = 0.0
            print(f"{C.AZUL}¡INMUNE!{C.RESET}")
        
        # Calcular daño final
        dano_final = int(dano * multiplicador)
        
        # Aplicar defensa (mejorada: //3 en lugar de //4)
        dano_final = max(1, dano_final - (self.defensa // 3))
        
        # Aplicar bonificación si está defendiendo (más potente: 35% en lugar de 50%)
        if "defendiendo" in self.estados:
            dano_final = int(dano_final * 0.35)
            print(f"{C.AZUL}¡Defensa activa! Daño reducido a un 35%{C.RESET}")
        
        # Reducir vida
        self.vida_actual = max(0, self.vida_actual - dano_final)
        
        print(f"{C.ROJO}{self.nombre} recibe {dano_final} de daño. Salud: {self.vida_actual}/{self.vida_maxima}{C.RESET}")
        
        if self.vida_actual <= 0:
            self.morir()
        
        return dano_final
    
    def recibir_curacion(self, curacion: int) -> int:
        """
        Recibe curación.
        
        Args:
            curacion: Cantidad de vida a curar
            
        Returns:
            Vida realmente curada
        """
        from utils import Colores as C
        
        vida_antes = self.vida_actual
        self.vida_actual = min(self.vida_maxima, self.vida_actual + curacion)
        vida_curada = self.vida_actual - vida_antes
        
        print(f"{C.VERDE}{self.nombre} recupera {vida_curada} de vida.{C.RESET}")
        
        return vida_curada
    
    def usar_habilidad(self, indice: int, objetivo: 'Personaje') -> Dict[str, Any]:
        """
        Usa una habilidad específica.
        
        Args:
            indice: Índice de la habilidad en la lista
            objetivo: Personaje objetivo
            
        Returns:
            Resultado de la habilidad
        """
        from utils import Colores as C
        
        # Validar índice
        if indice < 0 or indice >= len(self.habilidades):
            return {"exito": False, "mensaje": "Habilidad no válida"}
        
        habilidad = self.habilidades[indice]
        
        # Verificar energía
        if self.energia_actual < habilidad.costo_energia:
            return {"exito": False, "mensaje": "Energía insuficiente"}
        
        # Gastar energía
        self.energia_actual -= habilidad.costo_energia
        
        # Usar habilidad
        resultado = habilidad.usar(self, objetivo)
        
        return resultado
    
    def atacar_basico(self, objetivo: 'Personaje') -> Dict[str, Any]:
        """
        Realiza un ataque básico sin gastar energía.
        
        Args:
            objetivo: Personaje objetivo
            
        Returns:
            Resultado del ataque
        """
        from utils import Colores as C
        
        # Calcular daño básico
        dano = max(1, self.ataque // 2)
        
        # Aplicar daño
        dano_recibido = objetivo.recibir_dano(dano)
        
        # Posibilidad de crítico (15%)
        if random.random() < 0.15:
            dano_extra = dano_recibido // 2
            objetivo.recibir_dano(dano_extra)
            print(f"{C.ROJO}¡ATAQUE CRÍTICO! Daño extra: {dano_extra}{C.RESET}")
            dano_recibido += dano_extra
        
        return {
            "exito": True,
            "daño": dano_recibido,
            "tipo": "basico",
            "mensaje": f"{self.nombre} ataca a {objetivo.nombre}"
        }
    
    def defender(self) -> Dict[str, Any]:
        """
        Se defiende reduciendo el daño recibido.
        
        Returns:
            Resultado de la defensa
        """
        from utils import Colores as C
        
        self.aplicar_estado("defendiendo", duracion=1)
        
        print(f"{C.AZUL}{self.nombre} se prepara para defender.{C.RESET}")
        
        return {
            "exito": True,
            "tipo": "defensa",
            "mensaje": f"{self.nombre} se defiende"
        }
    
    def concentrar(self) -> Dict[str, Any]:
        """
        Se concentra para recuperar energía.
        
        Returns:
            Resultado de la concentración
        """
        from utils import Colores as C
        
        # Recuperar energía
        energia_recuperada = 25
        self.energia_actual = min(self.energia_maxima, self.energia_actual + energia_recuperada)
        
        print(f"{C.AZUL}{self.nombre} se concentra y recupera {energia_recuperada} de energía.{C.RESET}")
        
        return {
            "exito": True,
            "tipo": "concentracion",
            "energia_recuperada": energia_recuperada,
            "mensaje": f"{self.nombre} se concentra"
        }
    
    def regenerar_energia(self, cantidad: int = 15) -> None:
        """
        Regenera energía naturalmente.
        
        Args:
            cantidad: Cantidad de energía a regenerar
        """
        self.energia_actual = min(self.energia_maxima, self.energia_actual + cantidad)
    
    def morir(self) -> None:
        """
        Marca al personaje como muerto.
        """
        from utils import Colores as C
        
        print(f"{C.ROJO_BRILLANTE}*** {self.nombre} ha sido derrotado! ***{C.RESET}")
    
    def esta_vivo(self) -> bool:
        """
        Verifica si el personaje está vivo.
        
        Returns:
            True si está vivo, False si no
        """
        return self.vida_actual > 0
    
    def ganar_experiencia(self, experiencia: int) -> None:
        """
        Gana experiencia y sube de nivel si es necesario.
        
        Args:
            experiencia: Cantidad de experiencia a ganar
        """
        from utils import Colores as C
        
        self.experiencia += experiencia
        print(f"{C.CYAN}{self.nombre} ganó {experiencia} puntos de experiencia.{C.RESET}")
        
        while self.experiencia >= self.experiencia_necesaria:
            self.subir_nivel()
    
    def subir_nivel(self) -> None:
        """
        Sube de nivel aumentando estadísticas, preservando modificadores temporales.
        """
        from utils import Colores as C
        
        # Guardar modificadores actuales (buffs/debuffs)
        mod_ataque = self.ataque - self.ataque_base
        mod_defensa = self.defensa - self.defensa_base
        mod_velocidad = self.velocidad - self.velocidad_base
        
        self.nivel += 1
        self.experiencia -= self.experiencia_necesaria
        self.experiencia_necesaria = int(self.experiencia_necesaria * 1.1)
        
        # Aumentar estadísticas
        aumento_vida = int(self.vida_maxima * 0.1)
        aumento_ataque = int(self.ataque_base * 0.05)
        aumento_defensa = int(self.defensa_base * 0.05)
        aumento_velocidad = int(self.velocidad_base * 0.05)
        
        self.vida_maxima += aumento_vida
        self.vida_actual += aumento_vida
        self.ataque_base += aumento_ataque
        self.defensa_base += aumento_defensa
        self.velocidad_base += aumento_velocidad
        
        # Restaurar estadísticas con los modificadores preservados
        self.ataque = self.ataque_base + mod_ataque
        self.defensa = self.defensa_base + mod_defensa
        self.velocidad = self.velocidad_base + mod_velocidad
        
        print(f"{C.VERDE_BRILLANTE}¡{self.nombre} ha subido a nivel {self.nivel}!{C.RESET}")
        print(f"{C.VERDE}Vida: +{aumento_vida} | Ataque: +{aumento_ataque} | Defensa: +{aumento_defensa} | Velocidad: +{aumento_velocidad}{C.RESET}")
    
    # ---------- Sistema de estados con duración ----------
    def aplicar_estado(self, estado: str, duracion: int = 1) -> None:
        """
        Aplica un estado alterado con una duración determinada (en turnos).
        Si el estado ya existe, se renueva con la duración más larga.
        
        Args:
            estado: Nombre del estado
            duracion: Turnos que dura el estado
        """
        if estado not in self.estados:
            self.estados.append(estado)
            self.estados_duracion[estado] = duracion
        else:
            # Renovar solo si la nueva duración es mayor
            duracion_actual = self.estados_duracion.get(estado, 0)
            if duracion > duracion_actual:
                self.estados_duracion[estado] = duracion
    
    def eliminar_estado(self, estado: str) -> None:
        """
        Elimina un estado manualmente.
        
        Args:
            estado: Nombre del estado a eliminar
        """
        if estado in self.estados:
            self.estados.remove(estado)
        if estado in self.estados_duracion:
            del self.estados_duracion[estado]
    
    def actualizar_estados(self) -> None:
        """
        Decrementa la duración de los estados y elimina aquellos que han expirado.
        Debe llamarse al final de cada turno.
        """
        expirados = []
        for estado, duracion in self.estados_duracion.items():
            nueva_duracion = duracion - 1
            if nueva_duracion <= 0:
                expirados.append(estado)
            else:
                self.estados_duracion[estado] = nueva_duracion
        
        for estado in expirados:
            if estado in self.estados:
                self.estados.remove(estado)
            del self.estados_duracion[estado]
    
    def __str__(self) -> str:
        """
        Representación en string del personaje.
        
        Returns:
            String con información básica
        """
        estado = "VIVO" if self.esta_vivo() else "DERROTADO"
        return f"{self.nombre} [{self.tipo}] - {estado} - Vida: {self.vida_actual}/{self.vida_maxima}"