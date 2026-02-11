"""
Habilidades específicas del Torero
Cada habilidad refleja el arte, tradición y riesgo de la tauromaquia.
"""

from .habilidad_base import Habilidad
from utils import Colores as C
import random

class PaseDeTorero(Habilidad):
    """Pase de Torero - Realiza un pase artístico"""
    
    def __init__(self):
        super().__init__(
            nombre="Pase de Torero",
            descripcion="Realiza un pase artístico. Aumenta arte y puede esquivar.",
            costo_energia=20,
            tipo="defensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Aumenta arte
        if hasattr(usuario, '_arte'):
            usuario._arte = min(100, usuario._arte + 10)
        
        # Esquiva el próximo ataque (50%) - duración 1 turno
        if random.random() < 0.5:
            usuario.aplicar_estado("esquivando", duracion=1)
            print(f"{C.VERDE}¡Pase artístico! Esquiva próximo ataque.{C.RESET}")
        
        # Daño leve
        daño = objetivo.recibir_dano(usuario.ataque // 2, "arte")
        
        # Pase aleatorio
        pases = ["de pecho", "de rodillas", "de muleta", "natural", "de castigo"]
        pase = random.choice(pases)
        
        print(f"{C.CYAN}¡Pase {pase}! Arte +10. Daño: {daño}{C.RESET}")
        
        return {"exito": True, "daño": daño, "arte_aumentado": 10, "pase": pase}

class Estocada(Habilidad):
    """Estocada - Golpe final del torero (BALANCEADO)"""
    
    def __init__(self):
        super().__init__(
            nombre="Estocada",
            descripcion="Golpe final del torero. Daño moderado, mayor si el arte es alto.",
            costo_energia=35,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Daño base reducido de ataque*3 a ataque*1.8
        daño_base = int(usuario.ataque * 1.8)
        
        # Bonus por arte (ahora /150 en lugar de /100)
        if hasattr(usuario, '_arte'):
            bonus = 1 + (usuario._arte / 150)
            daño_base = int(daño_base * bonus)
            print(f"{C.VERDE}¡Arte potenciado! +{int((bonus-1)*100)}%{C.RESET}")
        
        # Crítico menos frecuente y menos potente
        if hasattr(usuario, '_arte') and usuario._arte >= 70 and random.random() < 0.3:
            daño_base = int(daño_base * 1.5)  # antes 1.8
            print(f"{C.ROJO_BRILLANTE}¡ESTOCADA PRECISA! +50% daño{C.RESET}")
        
        daño = objetivo.recibir_dano(daño_base, "estocada")
        
        # Eliminada la muerte instantánea (era muy frustrante)
        
        return {"exito": True, "daño": daño, "tipo": "estocada"}

class OlesDelPublico(Habilidad):
    """Olés del Público - El público lo anima"""
    
    def __init__(self):
        super().__init__(
            nombre="Olés del Público",
            descripcion="El público lo anima. Aumenta stats y puede conseguir oreja.",
            costo_energia=25,
            tipo="defensiva"
        )
        self.es_curacion = True
    
    def usar(self, usuario, objetivo):
        # Aumento de stats por ánimo del público - duración 2 turnos
        usuario.ataque += 10
        usuario.defensa += 8
        usuario.velocidad += 6
        
        # Aumenta arte
        if hasattr(usuario, '_arte'):
            usuario._arte = min(100, usuario._arte + 15)
        
        # Registrar público entusiasmado
        if hasattr(usuario, '_publico_entusiasmado'):
            usuario._publico_entusiasmado += 1
        
        # Posible oreja (30%)
        if random.random() < 0.3:
            if hasattr(usuario, '_orejas_conseguidas'):
                usuario._orejas_conseguidas += 1
                # Beneficio extra por oreja
                vida_curada = usuario.recibir_curacion(20)
                print(f"{C.AMARILLO}¡OREJA CONSEGUIDA! Vida +{vida_curada}. Orejas: {usuario._orejas_conseguidas}{C.RESET}")
        
        print(f"{C.VERDE}¡OLÉ! Ataque +10, Defensa +8, Velocidad +6, Arte +15. Público: {getattr(usuario, '_publico_entusiasmado', 0)}{C.RESET}")
        
        return {
            "exito": True,
            "ataque_aumentado": 10,
            "defensa_aumentada": 8,
            "velocidad_aumentada": 6,
            "arte_aumentado": 15
        }

class Capote(Habilidad):
    """Capote - Usa el capote para defenderse"""
    
    def __init__(self):
        super().__init__(
            nombre="Capote",
            descripcion="Usa el capote para defenderse. Reduce drásticamente el daño recibido.",
            costo_energia=30,
            tipo="defensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Defensa aumentada significativamente (antes +25, ahora +40)
        usuario.defensa += 40
        print(f"{C.AZUL}¡Capote desplegado! Defensa +40{C.RESET}")
        
        # Estado de defensa
        usuario.aplicar_estado("defendiendo", duracion=1)
        
        # Posible contraataque (40%)
        if random.random() < 0.4:
            daño_contra = usuario.ataque // 2
            objetivo.recibir_dano(daño_contra, "contraataque")
            print(f"{C.ROJO}¡Contraataque con capote! Daño: {daño_contra}{C.RESET}")
        
        return {"exito": True, "defensa_aumentada": 40, "contraataque": random.random() < 0.4}

class Finta(Habilidad):
    """Finta - Engaña al enemigo con una finta"""
    
    def __init__(self):
        super().__init__(
            nombre="Finta",
            descripcion="Engaña al enemigo con una finta. Confunde y reduce defensa.",
            costo_energia=20,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Confunde - duración 1 turno
        objetivo.aplicar_estado("confundido", duracion=1)
        
        # Reduce defensa (está desprevenido) - duración 2 turnos
        reduccion = max(8, objetivo.defensa // 4)  # antes //3
        objetivo.defensa = max(5, objetivo.defensa - reduccion)
        
        # Aumenta arte por la finta artística
        if hasattr(usuario, '_arte'):
            usuario._arte = min(100, usuario._arte + 5)
        
        print(f"{C.MAGENTA}¡Finta magistral! Defensa enemiga -{reduccion}, Arte +5{C.RESET}")
        
        return {"exito": True, "defensa_reducida": reduccion, "arte_aumentado": 5}

class Faena(Habilidad):
    """Faena - Realiza una faena completa (BALANCEADA)"""
    
    def __init__(self):
        super().__init__(
            nombre="Faena",
            descripcion="Realiza una faena completa. Efectos múltiples basados en arte.",
            costo_energia=50,
            tipo="especial"
        )
        self.es_curacion = True
    
    def usar(self, usuario, objetivo):
        print(f"{C.AMARILLO}¡{usuario.nombre} comienza una FAENA COMPLETA!{C.RESET}")
        
        # Efectos basados en nivel de arte
        arte = getattr(usuario, '_arte', 50)
        efectos = []
        
        # 1. Daño base aumentado por arte (antes *4, ahora *2.5)
        daño_base = int(usuario.ataque * 2.5)
        bonus_arte = 1 + (arte / 150)  # antes /100
        daño_base = int(daño_base * bonus_arte)
        daño = objetivo.recibir_dano(daño_base, "faena")
        efectos.append(f"Daño: {daño} (bonus arte: +{int((bonus_arte-1)*100)}%)")
        
        # 2. Aumento de arte por la faena (más lento)
        if hasattr(usuario, '_arte'):
            aumento_arte = min(20, (100 - usuario._arte) // 4)  # antes //3
            usuario._arte = min(100, usuario._arte + aumento_arte)
            efectos.append(f"Arte +{aumento_arte}")
        
        # 3. Posible oreja (probabilidad basada en arte, pero menor)
        prob_oreja = arte / 200  # antes /100
        if random.random() < prob_oreja and hasattr(usuario, '_orejas_conseguidas'):
            usuario._orejas_conseguidas += 1
            vida_curada = usuario.recibir_curacion(25)  # antes 30
            efectos.append(f"¡Oreja! Vida +{vida_curada}. Total: {usuario._orejas_conseguidas}")
        
        # 4. Registrar faena completa
        if hasattr(usuario, '_faenas_completas'):
            usuario._faenas_completas += 1
            efectos.append(f"Faena #{usuario._faenas_completas}")
        
        # 5. Posible cornada si el arte es bajo (20% si arte < 40)
        if arte < 40 and random.random() < 0.2:
            cornada = usuario.recibir_dano(usuario.vida_maxima // 5, "cornada")  # antes //4
            if hasattr(usuario, '_cornadas_recibidas'):
                usuario._cornadas_recibidas += 1
            efectos.append(f"¡Cornada! Daño: {cornada}")
        
        print(f"{C.AZUL}Faena completa efectos: {', '.join(efectos)}{C.RESET}")
        
        return {
            "exito": True,
            "efectos": efectos,
            "daño": daño,
            "arte_aumentado": aumento_arte if 'aumento_arte' in locals() else 0
        }