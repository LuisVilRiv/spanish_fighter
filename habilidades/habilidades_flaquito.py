"""
Habilidades específicas del Flaquito Playero
Cada habilidad refleja la fragilidad, agilidad y situaciones playeras del flaquito.
"""

from .habilidad_base import Habilidad
from utils import Colores as C
import random

class ArenaEnLosOjos(Habilidad):
    """Arena en los Ojos - Lanza arena a los ojos"""
    
    def __init__(self):
        super().__init__(
            nombre="Arena en los Ojos",
            descripcion="Lanza arena a los ojos. Ciega y reduce precisión.",
            costo_energia=15,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Cegamiento (alta probabilidad) - duración 1 turno
        if random.random() < 0.7:  # 70% de éxito
            objetivo.aplicar_estado("cegado", duracion=1)
            print(f"{C.ROJO}¡Arena en los ojos! Cegado.{C.RESET}")
        
        # Daño leve
        daño = objetivo.recibir_dano(usuario.ataque // 3, "arena")
        
        # Reduce velocidad (se frota los ojos) - duración 1 turno
        objetivo.velocidad = max(5, objetivo.velocidad - 5)
        
        print(f"{C.AMARILLO}¡Arena playera! Velocidad -5{C.RESET}")
        
        return {"exito": True, "daño": daño, "cegado": True}

class SurfearOla(Habilidad):
    """Surfear Ola - Surfea una ola para esquivar y atacar"""
    
    def __init__(self):
        super().__init__(
            nombre="Surfear Ola",
            descripcion="Surfea una ola para esquivar y atacar. Aumenta velocidad y daño.",
            costo_energia=25,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Aumenta velocidad temporalmente - duración 1 turno
        usuario.velocidad += 20
        print(f"{C.AZUL}¡Surfeando una ola! Velocidad +20{C.RESET}")
        
        # Daño con bonus de velocidad
        daño_base = usuario.ataque + (usuario.velocidad // 10)
        daño = objetivo.recibir_dano(daño_base, "agua")
        
        # Registrar ola surfeada
        if hasattr(usuario, '_olas_surfeadas'):
            usuario._olas_surfeadas += 1
        
        # Posible caída (15%)
        if random.random() < 0.15:
            usuario.recibir_dano(10, "caida")
            print(f"{C.ROJO}¡Se cae de la ola! Daño autoinfligido: 10{C.RESET}")
        
        print(f"{C.CYAN}Olas surfeadas: {getattr(usuario, '_olas_surfeadas', 0)}{C.RESET}")
        
        return {"exito": True, "daño": daño, "velocidad_aumentada": 20}

class BronceadoExpress(Habilidad):
    """Bronceado Express - Se pone moreno rápidamente"""
    
    def __init__(self):
        super().__init__(
            nombre="Bronceado Express",
            descripcion="Se pone moreno rápidamente. Aumenta defensa pero puede quemarse.",
            costo_energia=20,
            tipo="defensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Aumenta defensa (piel morena = más dura?) - duración 3 turnos
        aumento_defensa = 15
        usuario.defensa += aumento_defensa
        
        # Posible quemadura (40%) - duración 2 turnos
        if random.random() < 0.4:
            usuario.aplicar_estado("quemado", duracion=2)
            if hasattr(usuario, '_quemaduras_solares'):
                usuario._quemaduras_solares += 1
            print(f"{C.ROJO}¡Demasiado sol! Quemadura solar.{C.RESET}")
        else:
            # Beneficio adicional si no se quema
            usuario.ataque += 5
            print(f"{C.VERDE}¡Bronceado perfecto! Ataque +5{C.RESET}")
        
        print(f"{C.AMARILLO}¡Bronceado express! Defensa +{aumento_defensa}{C.RESET}")
        
        return {"exito": True, "defensa_aumentada": aumento_defensa}

class Esquivel(Habilidad):
    """Esquivel - Esquiva un ataque de forma espectacular"""
    
    def __init__(self):
        super().__init__(
            nombre="Esquivel",
            descripcion="Esquiva un ataque de forma espectacular. Aumenta evasión temporalmente.",
            costo_energia=30,
            tipo="defensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Aumenta evasión (representado como estado) - duración 1 turno
        usuario.aplicar_estado("esquivando", duracion=1)
        
        # Aumenta suerte temporalmente - duración 1 turno
        if hasattr(usuario, '_suerte'):
            usuario._suerte = min(0.6, usuario._suerte + 0.15)
        
        # Recupera un poco de energía por el movimiento ágil
        usuario.energia_actual = min(usuario.energia_maxima, usuario.energia_actual + 20)
        
        print(f"{C.VERDE}¡Esquive espectacular! Suerte +15%, Energía +20, Estado: esquivando{C.RESET}")
        
        return {
            "exito": True,
            "suerte_aumentada": 0.15,
            "energia_recuperada": 20,
            "estado": "esquivando"
        }

class PalizaDeToalla(Habilidad):
    """Paliza de Toalla - Golpea con una toalla mojada"""
    
    def __init__(self):
        super().__init__(
            nombre="Paliza de Toalla",
            descripcion="Golpea con una toalla mojada. Daño extra y posible mareo.",
            costo_energia=35,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        daño_base = usuario.ataque * 2
        
        # Extra daño si el objetivo está mojado
        if "mojado" in objetivo.estados:
            daño_base = int(daño_base * 1.8)
            print(f"{C.ROJO}¡Toalla mojada sobre mojado! +80% daño{C.RESET}")
        
        daño = objetivo.recibir_dano(daño_base, "fisico")
        
        # Posible mareo por el golpe (30%) - duración 1 turno
        if random.random() < 0.3:
            objetivo.aplicar_estado("mareado", duracion=1)
            print(f"{C.MAGENTA}¡Mareado por la toalla!{C.RESET}")
        
        # Posible pérdida de toalla (10%)
        if random.random() < 0.1:
            print(f"{C.AMARILLO}¡Se le escapa la toalla al viento!{C.RESET}")
        
        return {"exito": True, "daño": daño, "tipo": "fisico"}

class RefrescoAzucarado(Habilidad):
    """Refresco Azucarado - Bebe un refresco lleno de azúcar"""
    
    def __init__(self):
        super().__init__(
            nombre="Refresco Azucarado",
            descripcion="Bebe un refresco lleno de azúcar. Energía rápida pero posible bajón.",
            costo_energia=10,
            tipo="defensiva"
        )
        self.es_curacion = False  # No cura vida, da energía
    
    def usar(self, usuario, objetivo):
        # Gran aumento de energía
        energia_recuperada = 40
        usuario.energia_actual = min(usuario.energia_maxima, usuario.energia_actual + energia_recuperada)
        
        # Aumento temporal de velocidad (azúcar) - duración 1 turno
        usuario.velocidad += 10
        print(f"{C.VERDE}¡Subidón de azúcar! Energía +{energia_recuperada}, Velocidad +10{C.RESET}")
        
        # Registrar refresco bebido
        if hasattr(usuario, '_refrescos_bebidos'):
            usuario._refrescos_bebidos += 1
        
        # Posible bajón de azúcar después (50%) - duración 2 turnos
        if random.random() < 0.5:
            usuario.aplicar_estado("bajon_azucar", duracion=2)
            print(f"{C.AMARILLO}¡Bajón de azúcar inminente!{C.RESET}")
        
        print(f"{C.CYAN}Refrescos bebidos: {getattr(usuario, '_refrescos_bebidos', 0)}{C.RESET}")
        
        return {
            "exito": True,
            "energia_recuperada": energia_recuperada,
            "velocidad_aumentada": 10
        }