"""
Batalla Cómica Española - Punto de entrada principal.
"""

import sys
from menu_principal import MenuPrincipal
from utils import Colores as C

def main():
    try:
        menu = MenuPrincipal()
        menu.ejecutar()
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