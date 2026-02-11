"""
eula.py - Gestión de aceptación del Acuerdo de Licencia.
"""

import os
import sys
from utils import Colores as C

EULA_FILE = "eula_accepted.txt"

EULA_TEXT = """
═══════════════════════════════════════════════════════════════════════
                     ACUERDO DE LICENCIA DE USUARIO FINAL (EULA)
                          Batalla Cómica Española
                    Copyright (c) 2026 Luis Villegas Rivera
═══════════════════════════════════════════════════════════════════════

Este software se proporciona bajo una licencia limitada, no exclusiva
e intransferible para su uso personal y no comercial.

✅ TÉRMINOS PERMITIDOS:
   • Jugar y disfrutar el juego.
   • Crear y distribuir modificaciones (mods) gratuitas siempre que:
       - No incluyan el juego base completo.
       - No se vendan ni moneticen.
       - Atribuyan crédito al autor original.

❌ TÉRMINOS PROHIBIDOS:
   • Vender, alquilar o distribuir el juego sin autorización.
   • Realizar ingeniería inversa o descompilar el código.
   • Eliminar avisos de copyright.
   • Usar el software con fines ilegales.

⚠️ SIN GARANTÍA:
   El software se entrega "tal cual", sin garantías de ningún tipo.
   El autor no será responsable de daños derivados de su uso.

Al hacer clic en "Aceptar", usted confirma que ha leído y acepta
todos los términos y condiciones de esta licencia.

═══════════════════════════════════════════════════════════════════════
"""

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def verificar_eula() -> bool:
    """
    Verifica si el usuario ya aceptó el EULA.
    Si no, lo muestra y pide aceptación.
    Retorna True si acepta, False si no (sale del juego).
    """
    if os.path.exists(EULA_FILE):
        return True

    limpiar_pantalla()
    print(EULA_TEXT)
    print()
    respuesta = input(f"{C.AZUL}¿Aceptas los términos de la licencia? (s/n): {C.RESET}").lower()
    if respuesta == 's':
        with open(EULA_FILE, 'w', encoding='utf-8') as f:
            f.write("aceptado")
        print(f"{C.VERDE}✅ Licencia aceptada. ¡Bienvenido!{C.RESET}")
        input(f"{C.CYAN}Presiona Enter para continuar...{C.RESET}")
        return True
    else:
        print(f"{C.ROJO}❌ Debes aceptar la licencia para jugar.{C.RESET}")
        input(f"{C.CYAN}Presiona Enter para salir...{C.RESET}")
        sys.exit(0)
        return False