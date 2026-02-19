"""
Clase base abstracta para todas las habilidades del juego.
Cada habilidad hereda de esta clase y define su comportamiento Ãºnico.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import random

class Habilidad(ABC):
    """
    Clase base para todas las habilidades.
    
    Atributos:
        nombre (str): Nombre de la habilidad
        descripcion (str): DescripciÃ³n de lo que hace
        costo_energia (int): EnergÃ­a necesaria para usar la habilidad
        tipo (str): Tipo de habilidad (ofensiva, defensiva, especial, estado)
        es_curacion (bool): Indica si la habilidad tiene efectos curativos
    """
    
    def __init__(self, nombre: str, descripcion: str, costo_energia: int, tipo: str):
        """
        Inicializa una nueva habilidad.
        
        Args:
            nombre: Nombre de la habilidad
            descripcion: DescripciÃ³n de lo que hace
            costo_energia: EnergÃ­a necesaria
            tipo: Tipo de habilidad
        """
        self.nombre = nombre
        self.descripcion = descripcion
        self.costo_energia = costo_energia
        self.tipo = tipo  # "ofensiva", "defensiva", "especial", "estado"
        self.es_curacion = False  # Por defecto, no es curativa
        # En combate de equipos, las habilidades con es_curacion=True
        # SOLO pueden aplicarse a compañeros del mismo equipo.
        self.cura_aliados = True
    
    @abstractmethod
    def usar(self, usuario, objetivo) -> Dict[str, Any]:
        """
        MÃ©todo abstracto que debe implementar cada habilidad.
        
        Args:
            usuario: Personaje que usa la habilidad
            objetivo: Personaje objetivo
            
        Returns:
            Diccionario con el resultado de la habilidad
        """
        pass
    
    def __str__(self) -> str:
        """
        RepresentaciÃ³n en string de la habilidad.
        
        Returns:
            String con informaciÃ³n bÃ¡sica
        """
        return f"{self.nombre} ({self.costo_energia}E): {self.descripcion}"