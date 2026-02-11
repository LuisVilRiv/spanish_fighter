"""
sistema_guardado.py - Sistema de guardado/cifrado para Batalla Cómica Española.
Utiliza cifrado Fernet (AES-128 + HMAC) y doble verificación de integridad.
"""

import os
import json
import base64
import hashlib
from typing import Any, Dict, Optional, List
from datetime import datetime

# Dependencia: cryptography
try:
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives import hashes, hmac
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    print("ADVERTENCIA: Biblioteca 'cryptography' no instalada. El guardado será inseguro (JSON plano).")
    print("Instala con: pip install cryptography")

from utils import Colores as C

# Constantes - NO CAMBIAR después de lanzar el juego
VERSION_SAVE = 1
SECRET_PASSPHRASE = b"BatallaComicaEspanola2026-LuisVillegas"
SALT = b"sal_para_derivacion_clave_1234"

class CifradoError(Exception):
    """Excepción lanzada cuando hay errores de cifrado/descifrado."""
    pass

class GestorGuardado:
    """
    Gestiona el guardado y carga de partidas con cifrado autenticado.
    Escalable para múltiples slots y futuro modo historia.
    """

    def __init__(self, directorio: str = "saves"):
        """
        Args:
            directorio: Carpeta donde se almacenan los archivos de guardado.
        """
        self.directorio = directorio
        self.fernet: Optional[Fernet] = None
        self.hmac_key: Optional[bytes] = None

        if not CRYPTOGRAPHY_AVAILABLE:
            print(f"{C.AMARILLO}⚠️ Modo inseguro: guardado sin cifrado.{C.RESET}")
            return

        self._derivar_claves()

    def _derivar_claves(self):
        """Deriva una clave Fernet (32 bytes) y una clave HMAC (32 bytes) usando Scrypt."""
        kdf = Scrypt(
            salt=SALT,
            length=64,  # 64 bytes: 32 para Fernet + 32 para HMAC
            n=2**14,
            r=8,
            p=1,
        )
        clave_completa = kdf.derive(SECRET_PASSPHRASE)
        clave_fernet = base64.urlsafe_b64encode(clave_completa[:32])
        self.fernet = Fernet(clave_fernet)
        self.hmac_key = clave_completa[32:]

    def _generar_hmac(self, datos: bytes) -> str:
        """Genera HMAC-SHA256 de los datos."""
        if not self.hmac_key:
            return ""
        h = hmac.HMAC(self.hmac_key, hashes.SHA256())
        h.update(datos)
        return h.finalize().hex()

    def _cifrar(self, datos: Dict[str, Any]) -> str:
        """
        Cifra un diccionario y devuelve un string base64.
        Incluye un hash HMAC para verificación extra.
        """
        if not CRYPTOGRAPHY_AVAILABLE or self.fernet is None:
            # Modo inseguro: guardar como JSON plano ofuscado en base64
            json_str = json.dumps(datos, indent=2, ensure_ascii=False)
            return base64.b64encode(json_str.encode('utf-8')).decode('ascii')

        # Serializar a JSON
        json_str = json.dumps(datos, ensure_ascii=False)
        datos_bytes = json_str.encode('utf-8')

        # Generar HMAC y añadirlo al payload
        hmac_val = self._generar_hmac(datos_bytes)
        payload = {
            "data": base64.b64encode(datos_bytes).decode('ascii'),
            "hmac": hmac_val,
            "version": VERSION_SAVE
        }
        payload_json = json.dumps(payload, ensure_ascii=False)

        # Cifrar el payload completo
        token = self.fernet.encrypt(payload_json.encode('utf-8'))
        return token.decode('ascii')

    def _descifrar(self, contenido_cifrado: str) -> Dict[str, Any]:
        """
        Descifra un string y devuelve el diccionario original.
        Lanza CifradoError si la integridad falla o el formato es inválido.
        """
        if not CRYPTOGRAPHY_AVAILABLE or self.fernet is None:
            try:
                # Modo inseguro: asumimos base64
                json_str = base64.b64decode(contenido_cifrado.encode('ascii')).decode('utf-8')
                return json.loads(json_str)
            except Exception as e:
                raise CifradoError(f"No se pudo descifrar (modo inseguro): {e}")

        try:
            # Descifrar Fernet
            payload_json = self.fernet.decrypt(contenido_cifrado.encode('ascii'))
            payload = json.loads(payload_json.decode('utf-8'))

            # Verificar versión
            if payload.get("version") != VERSION_SAVE:
                raise CifradoError(f"Versión de guardado incompatible: {payload.get('version')}")

            # Extraer datos y HMAC
            datos_b64 = payload.get("data")
            hmac_esperado = payload.get("hmac", "")
            if not datos_b64:
                raise CifradoError("Payload corrupto: falta 'data'")

            datos_bytes = base64.b64decode(datos_b64.encode('ascii'))

            # Verificar HMAC
            if self.hmac_key:
                hmac_calculado = self._generar_hmac(datos_bytes)
                if hmac_calculado != hmac_esperado:
                    raise CifradoError("¡Integridad comprometida! El archivo de guardado ha sido modificado.")

            # Cargar JSON original
            return json.loads(datos_bytes.decode('utf-8'))

        except (InvalidToken, json.JSONDecodeError, KeyError, base64.binascii.Error) as e:
            raise CifradoError(f"Error al descifrar: {e}")

    def _ruta_archivo(self, slot: int = 1) -> str:
        """Devuelve la ruta del archivo de guardado para un slot."""
        if not os.path.exists(self.directorio):
            os.makedirs(self.directorio, exist_ok=True)
        return os.path.join(self.directorio, f"save_{slot}.dat")

    # ------------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------------

    def guardar_partida(self, datos: Dict[str, Any], slot: int = 1) -> bool:
        """
        Guarda la partida en el slot indicado.
        Retorna True si éxito, False si error.
        """
        try:
            # Añadir metadatos
            datos_save = datos.copy()
            datos_save["_metadata"] = {
                "version": VERSION_SAVE,
                "timestamp": datetime.now().isoformat(),
                "slot": slot
            }

            contenido_cifrado = self._cifrar(datos_save)
            ruta = self._ruta_archivo(slot)

            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(contenido_cifrado)

            print(f"{C.VERDE}💾 Partida guardada correctamente en slot {slot}.{C.RESET}")
            return True
        except Exception as e:
            print(f"{C.ROJO}❌ Error al guardar partida: {e}{C.RESET}")
            return False

    def cargar_partida(self, slot: int = 1) -> Optional[Dict[str, Any]]:
        """
        Carga la partida del slot indicado.
        Retorna el diccionario de datos o None si no existe/error.
        """
        ruta = self._ruta_archivo(slot)
        if not os.path.exists(ruta):
            print(f"{C.AMARILLO}⚠️ No existe partida guardada en slot {slot}.{C.RESET}")
            return None

        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido_cifrado = f.read()

            datos_save = self._descifrar(contenido_cifrado)
            print(f"{C.VERDE}📂 Partida cargada correctamente desde slot {slot}.{C.RESET}")
            return datos_save
        except CifradoError as e:
            print(f"{C.ROJO}🔒 Error de integridad: {e}. La partida podría estar corrupta o haber sido modificada.{C.RESET}")
            return None
        except Exception as e:
            print(f"{C.ROJO}❌ Error al cargar partida: {e}{C.RESET}")
            return None

    def listar_partidas(self) -> List[int]:
        """Devuelve una lista de slots disponibles."""
        if not os.path.exists(self.directorio):
            return []
        slots = []
        for f in os.listdir(self.directorio):
            if f.startswith("save_") and f.endswith(".dat"):
                try:
                    slot = int(f[5:-4])
                    slots.append(slot)
                except:
                    continue
        return sorted(slots)

    def eliminar_partida(self, slot: int = 1) -> bool:
        """Elimina la partida del slot indicado."""
        ruta = self._ruta_archivo(slot)
        if os.path.exists(ruta):
            try:
                os.remove(ruta)
                print(f"{C.VERDE}🗑️ Partida en slot {slot} eliminada.{C.RESET}")
                return True
            except Exception as e:
                print(f"{C.ROJO}❌ Error al eliminar partida: {e}{C.RESET}")
                return False
        return False


# ============================================================================
# Funciones de utilidad para integrar con el juego
# ============================================================================

def crear_datos_jugador(heroe) -> Dict[str, Any]:
    """
    Convierte un objeto Personaje en un diccionario serializable.
    Escalable: aquí se añadirán más campos para modo historia.
    """
    return {
        "nombre": heroe.nombre,
        "tipo": heroe.tipo,
        "nivel": heroe.nivel,
        "experiencia": heroe.experiencia,
        "vida_maxima": heroe.vida_maxima,
        "vida_actual": heroe.vida_actual,
        "ataque_base": heroe.ataque_base,
        "defensa_base": heroe.defensa_base,
        "velocidad_base": heroe.velocidad_base,
        "energia_maxima": heroe.energia_maxima,
        "energia_actual": heroe.energia_actual,
        # No guardamos estados ni buffs temporales
        "habilidades": [h.nombre for h in heroe.habilidades],
        # Datos de progreso (escalable para modo historia)
        "progreso": {
            "partidas_ganadas": getattr(heroe, '_partidas_ganadas', 0),
            "enemigos_derrotados": getattr(heroe, '_enemigos_derrotados', 0),
            "mundo": 1,
            "capitulo": 1,
            "misiones_completadas": []
        }
    }

def restaurar_personaje(personaje, datos: Dict[str, Any]):
    """
    Restaura el estado de un personaje a partir de los datos guardados.
    Solo restaura estadísticas base y progreso; los buffs temporales se pierden (intencionado).
    """
    personaje.nivel = datos.get("nivel", 1)
    personaje.experiencia = datos.get("experiencia", 0)
    personaje.vida_maxima = datos.get("vida_maxima", personaje.vida_maxima)
    personaje.vida_actual = datos.get("vida_actual", personaje.vida_maxima)
    personaje.ataque_base = datos.get("ataque_base", personaje.ataque_base)
    personaje.defensa_base = datos.get("defensa_base", personaje.defensa_base)
    personaje.velocidad_base = datos.get("velocidad_base", personaje.velocidad_base)
    personaje.energia_maxima = datos.get("energia_maxima", personaje.energia_maxima)
    personaje.energia_actual = datos.get("energia_actual", personaje.energia_maxima)

    # Recalcular stats actuales (sin buffs)
    personaje.ataque = personaje.ataque_base
    personaje.defensa = personaje.defensa_base
    personaje.velocidad = personaje.velocidad_base
    personaje.estados = []
    personaje.estados_duracion = {}

    # Progreso (atributos dinámicos)
    progreso = datos.get("progreso", {})
    personaje._partidas_ganadas = progreso.get("partidas_ganadas", 0)
    personaje._enemigos_derrotados = progreso.get("enemigos_derrotados", 0)

def slot_disponible(gestor: GestorGuardado) -> int:
    """Devuelve el primer slot libre (1,2,3...). Útil para nuevo juego."""
    slots = gestor.listar_partidas()
    if not slots:
        return 1
    for i in range(1, max(slots) + 2):
        if i not in slots:
            return i
    return len(slots) + 1