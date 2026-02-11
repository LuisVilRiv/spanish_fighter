"""
Sistema de guardado y carga para Batalla Cómica Española.
Utiliza JSON para almacenar datos del jugador, permitiendo múltiples slots
y escalabilidad futura (modo historia, inventario, logros, etc.).
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

from utils import Colores as C

# Directorio base de guardado (usando el directorio del juego /save)
SAVE_DIR = Path("save")
SAVE_DIR.mkdir(exist_ok=True)

# Archivo de metadatos: guarda información de todos los slots
METADATA_FILE = SAVE_DIR / "metadata.json"

# Número máximo de slots
MAX_SLOTS = 3

class SistemaGuardado:
    """Clase estática para gestionar guardado/carga."""

    @staticmethod
    def inicializar():
        """Crea la estructura de guardado si no existe."""
        if not METADATA_FILE.exists():
            metadata = {
                "slots": {},
                "ultimo_slot": None,
                "version": "1.0"
            }
            with open(METADATA_FILE, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4, ensure_ascii=False)

    @staticmethod
    def slot_ocupado(slot: int) -> bool:
        """Verifica si un slot tiene partida guardada."""
        if not METADATA_FILE.exists():
            return False
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        return str(slot) in metadata["slots"]

    @staticmethod
    def obtener_info_slots() -> Dict[str, Dict]:
        """Devuelve la información de todos los slots."""
        if not METADATA_FILE.exists():
            return {}
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        return metadata["slots"]

    @staticmethod
    def guardar_partida(slot: int, datos_jugador: Dict[str, Any], modo: str = "normal", 
                       historia: Optional[Dict] = None) -> bool:
        """
        Guarda la partida en el slot especificado.
        
        Args:
            slot: Número de slot (0,1,2...)
            datos_jugador: Diccionario con datos serializados del personaje
            modo: "normal", "historia", etc.
            historia: Datos adicionales del modo historia
        
        Returns:
            True si se guardó correctamente
        """
        # Preparar datos completos de la partida
        timestamp = datetime.now().isoformat()
        
        partida = {
            "slot": slot,
            "timestamp": timestamp,
            "modo": modo,
            "jugador": datos_jugador,
            "historia": historia or {},
            "version": "1.0"
        }
        
        # Guardar archivo de slot
        slot_file = SAVE_DIR / f"slot_{slot}.json"
        with open(slot_file, "w", encoding="utf-8") as f:
            json.dump(partida, f, indent=4, ensure_ascii=False)
        
        # Actualizar metadatos
        SistemaGuardado._actualizar_metadata(slot, timestamp, modo, datos_jugador.get("nombre", "Sin nombre"))
        
        print(f"{C.VERDE}✓ Partida guardada en slot {slot}.{C.RESET}")
        return True

    @staticmethod
    def _actualizar_metadata(slot: int, timestamp: str, modo: str, nombre_personaje: str):
        """Actualiza el archivo de metadatos con la información del slot."""
        metadata = {}
        if METADATA_FILE.exists():
            with open(METADATA_FILE, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        
        if "slots" not in metadata:
            metadata["slots"] = {}
        
        metadata["slots"][str(slot)] = {
            "timestamp": timestamp,
            "modo": modo,
            "nombre_personaje": nombre_personaje
        }
        metadata["ultimo_slot"] = slot
        
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)

    @staticmethod
    def cargar_partida(slot: int) -> Optional[Dict[str, Any]]:
        """
        Carga una partida desde el slot especificado.
        
        Returns:
            Diccionario con todos los datos de la partida, o None si no existe.
        """
        slot_file = SAVE_DIR / f"slot_{slot}.json"
        if not slot_file.exists():
            print(f"{C.ROJO}No hay partida guardada en el slot {slot}.{C.RESET}")
            return None
        
        with open(slot_file, "r", encoding="utf-8") as f:
            partida = json.load(f)
        
        # Actualizar último slot en metadatos
        if "timestamp" in partida:
            SistemaGuardado._actualizar_metadata(
                slot, 
                partida["timestamp"], 
                partida.get("modo", "normal"),
                partida.get("jugador", {}).get("nombre", "Desconocido")
            )
        
        print(f"{C.VERDE}✓ Partida cargada desde slot {slot}.{C.RESET}")
        return partida

    @staticmethod
    def eliminar_partida(slot: int) -> bool:
        """Elimina la partida de un slot."""
        slot_file = SAVE_DIR / f"slot_{slot}.json"
        if slot_file.exists():
            os.remove(slot_file)
        
        # Actualizar metadatos
        if METADATA_FILE.exists():
            with open(METADATA_FILE, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            if str(slot) in metadata["slots"]:
                del metadata["slots"][str(slot)]
            if metadata.get("ultimo_slot") == slot:
                metadata["ultimo_slot"] = None
            with open(METADATA_FILE, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4, ensure_ascii=False)
        
        print(f"{C.AMARILLO}🗑️ Partida en slot {slot} eliminada.{C.RESET}")
        return True

    @staticmethod
    def serializar_personaje(personaje) -> Dict[str, Any]:
        """
        Convierte un objeto Personaje en un diccionario serializable JSON.
        Incluye estadísticas base, nivel, experiencia, estados, etc.
        """
        # Atributos básicos
        data = {
            "clase": personaje.__class__.__name__,
            "nombre": personaje.nombre,
            "tipo": personaje.tipo,
            "nivel": personaje.nivel,
            "experiencia": personaje.experiencia,
            "experiencia_necesaria": personaje.experiencia_necesaria,
            "vida_maxima": personaje.vida_maxima,
            "vida_actual": personaje.vida_actual,
            "ataque_base": personaje.ataque_base,
            "defensa_base": personaje.defensa_base,
            "velocidad_base": personaje.velocidad_base,
            "ataque": personaje.ataque,
            "defensa": personaje.defensa,
            "velocidad": personaje.velocidad,
            "energia_maxima": personaje.energia_maxima,
            "energia_actual": personaje.energia_actual,
            "estados": personaje.estados,
            "estados_duracion": personaje.estados_duracion,
            "debilidades": personaje.debilidades,
            "fortalezas": personaje.fortalezas,
            "inmunidades": personaje.inmunidades,
        }
        
        # Atributos específicos de cada personaje (ej. _arte, _musculo, etc.)
        # Los guardamos todos los que empiecen por '_' y sean serializables.
        for attr in dir(personaje):
            if attr.startswith("_") and not attr.startswith("__"):
                valor = getattr(personaje, attr)
                # Solo guardamos tipos básicos y listas/dicts
                if isinstance(valor, (int, float, str, bool, list, dict, tuple)) or valor is None:
                    data[attr] = valor
        
        return data

    @staticmethod
    def deserializar_personaje(data: Dict[str, Any]):
        """
        Reconstruye un objeto Personaje a partir de su representación serializada.
        Retorna la instancia del personaje.
        """
        from personajes import (Segarro, Catolico, Sacerdote, Turista, Abuela,
                               Politico, Torero, Flaquito, Choni, PutoAmo, Barrendero)
        
        # Mapeo de nombres de clase a constructores
        clases = {
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
            "Barrendero": Barrendero,
        }
        
        clase = clases.get(data["clase"])
        if not clase:
            raise ValueError(f"Clase de personaje desconocida: {data['clase']}")
        
        # Crear instancia con el nombre guardado
        personaje = clase(nombre_personalizado=data["nombre"])
        
        # Restaurar atributos
        personaje.nivel = data["nivel"]
        personaje.experiencia = data["experiencia"]
        personaje.experiencia_necesaria = data["experiencia_necesaria"]
        personaje.vida_maxima = data["vida_maxima"]
        personaje.vida_actual = data["vida_actual"]
        personaje.ataque_base = data["ataque_base"]
        personaje.defensa_base = data["defensa_base"]
        personaje.velocidad_base = data["velocidad_base"]
        personaje.ataque = data["ataque"]
        personaje.defensa = data["defensa"]
        personaje.velocidad = data["velocidad"]
        personaje.energia_maxima = data["energia_maxima"]
        personaje.energia_actual = data["energia_actual"]
        personaje.estados = data["estados"]
        personaje.estados_duracion = data["estados_duracion"]
        personaje.debilidades = data["debilidades"]
        personaje.fortalezas = data["fortalezas"]
        personaje.inmunidades = data["inmunidades"]
        
        # Restaurar atributos específicos (los que empiezan por '_')
        for key, value in data.items():
            if key.startswith("_") and hasattr(personaje, key):
                setattr(personaje, key, value)
        
        return personaje