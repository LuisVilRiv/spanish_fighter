"""
Clase base abstracta para todas las habilidades del juego.
Cada habilidad hereda de esta clase y define su comportamiento único.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import random

class Habilidad(ABC):
    """
    Clase base para todas las habilidades.
    
    Atributos:
        nombre (str): Nombre de la habilidad
        descripcion (str): Descripción de lo que hace
        costo_energia (int): Energía necesaria para usar la habilidad
        tipo (str): Tipo de habilidad (ofensiva, defensiva, especial, estado)
        es_curacion (bool): Indica si la habilidad tiene efectos curativos
    """
    
    def __init__(self, nombre: str, descripcion: str, costo_energia: int, tipo: str):
        """
        Inicializa una nueva habilidad.
        
        Args:
            nombre: Nombre de la habilidad
            descripcion: Descripción de lo que hace
            costo_energia: Energía necesaria
            tipo: Tipo de habilidad
        """
        self.nombre = nombre
        self.descripcion = descripcion
        self.costo_energia = costo_energia
        self.tipo = tipo  # "ofensiva", "defensiva", "especial", "estado"
        self.es_curacion = False  # Por defecto, no es curativa
    
    @abstractmethod
    def usar(self, usuario, objetivo) -> Dict[str, Any]:
        """
        Método abstracto que debe implementar cada habilidad.
        
        Args:
            usuario: Personaje que usa la habilidad
            objetivo: Personaje objetivo
            
        Returns:
            Diccionario con el resultado de la habilidad
        """
        pass
    
    def __str__(self) -> str:
        """
        Representación en string de la habilidad.
        
        Returns:
            String con información básica
        """
        return f"{self.nombre} ({self.costo_energia}E): {self.descripcion}"