"""
Sistema de colores ANSI para la terminal.
Permite mostrar el juego con colores vivos y estilos diferentes.
"""

class Colores:
    """
    Clase con constantes para colores y estilos de terminal.
    Todos los colores usan códigos ANSI.
    """
    
    # Colores básicos (30-37)
    NEGRO = '\033[30m'
    ROJO = '\033[31m'
    VERDE = '\033[32m'
    AMARILLO = '\033[33m'
    AZUL = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    BLANCO = '\033[37m'
    
    # Colores brillantes (90-97)
    ROJO_BRILLANTE = '\033[91m'
    VERDE_BRILLANTE = '\033[92m'
    AMARILLO_BRILLANTE = '\033[93m'
    AZUL_BRILLANTE = '\033[94m'
    MAGENTA_BRILLANTE = '\033[95m'
    CYAN_BRILLANTE = '\033[96m'
    BLANCO_BRILLANTE = '\033[97m'
    
    # Colores adicionales (256-color mode)
    NARANJA = '\033[38;5;208m'
    
    # Estilos de texto
    NEGRITA = '\033[1m'
    SUBRAYADO = '\033[4m'
    INVERTIDO = '\033[7m'
    OCULTO = '\033[8m'
    TACHADO = '\033[9m'
    
    # Reset (vuelve a los valores por defecto)
    RESET = '\033[0m'
    
    # Fondos (40-47)
    FONDO_NEGRO = '\033[40m'
    FONDO_ROJO = '\033[41m'
    FONDO_VERDE = '\033[42m'
    FONDO_AMARILLO = '\033[43m'
    FONDO_AZUL = '\033[44m'
    FONDO_MAGENTA = '\033[45m'
    FONDO_CYAN = '\033[46m'
    FONDO_BLANCO = '\033[47m'
    
    # Fondos brillantes (100-107)
    FONDO_ROJO_BRILLANTE = '\033[101m'
    FONDO_VERDE_BRILLANTE = '\033[102m'
    FONDO_AMARILLO_BRILLANTE = '\033[103m'
    FONDO_AZUL_BRILLANTE = '\033[104m'
    FONDO_MAGENTA_BRILLANTE = '\033[105m'
    FONDO_CYAN_BRILLANTE = '\033[106m'
    FONDO_BLANCO_BRILLANTE = '\033[107m'
    
    @staticmethod
    def limpiar_pantalla():
        """Limpia la pantalla de la terminal."""
        print("\033[H\033[J", end="")
    
    @staticmethod
    def mostrar_barra(porcentaje: float, ancho: int = 30, color_lleno: str = VERDE, color_vacio: str = ROJO):
        """
        Genera una barra de progreso visual.
        
        Args:
            porcentaje (float): Porcentaje de 0 a 1
            ancho (int): Ancho de la barra en caracteres
            color_lleno (str): Color para la parte llena
            color_vacio (str): Color para la parte vacía
            
        Returns:
            str: Barra formateada
        """
        lleno = int(porcentaje * ancho)
        vacio = ancho - lleno
        return f"{color_lleno}{'█' * lleno}{color_vacio}{'░' * vacio}{RESET}"
    
    @staticmethod
    def centrar_texto(texto: str, ancho: int = 50, relleno: str = " "):
        """
        Centra texto en un ancho dado.
        
        Args:
            texto (str): Texto a centrar
            ancho (int): Ancho total
            relleno (str): Carácter de relleno
            
        Returns:
            str: Texto centrado
        """
        return texto.center(ancho, relleno)
    
    @staticmethod
    def crear_caja(texto: str, color_borde: str = AZUL, color_texto: str = BLANCO):
        """
        Crea una caja decorada alrededor del texto.
        
        Args:
            texto (str): Texto a enmarcar
            color_borde (str): Color del borde
            color_texto (str): Color del texto
            
        Returns:
            str: Texto enmarcado
        """
        lineas = texto.split('\n')
        ancho = max(len(linea) for linea in lineas) + 4
        
        resultado = []
        resultado.append(f"{color_borde}╔{'═' * ancho}╗{RESET}")
        
        for linea in lineas:
            espacios = ancho - len(linea) - 3
            resultado.append(f"{color_borde}║ {color_texto}{linea}{' ' * espacios}{color_borde} ║{RESET}")
        
        resultado.append(f"{color_borde}╚{'═' * ancho}╝{RESET}")
        return '\n'.join(resultado)


# Alias global para facilitar el uso
C = Colores
RESET = Colores.RESET