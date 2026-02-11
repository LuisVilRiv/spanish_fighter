"""
Habilidades específicas del PutoAmo del Gym
Cada habilidad refleja la cultura del gym, proteínas y culturismo.
"""

from .habilidad_base import Habilidad
from utils import Colores as C
import random

class FlexionExplosiva(Habilidad):
    """Flexión Explosiva - Realiza una flexión explosiva"""
    
    def __init__(self):
        super().__init__(
            nombre="Flexión Explosiva",
            descripcion="Realiza una flexión explosiva. Daño físico y aumenta músculo.",
            costo_energia=20,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        daño_base = usuario.ataque * 2
        
        # Extra daño si el objetivo es débil físicamente
        if objetivo.defensa < 10 or "Flaquito" in objetivo.tipo:
            daño_base = int(daño_base * 1.6)
            print(f"{C.ROJO}¡Contra los débiles! +60% daño{C.RESET}")
        
        daño = objetivo.recibir_dano(daño_base, "fuerza")
        
        # Aumenta músculo
        if hasattr(usuario, '_musculo'):
            usuario._musculo = min(150, usuario._musculo + 10)
        
        print(f"{C.VERDE}¡Flexión explosiva! Músculo +10{C.RESET}")
        
        return {"exito": True, "daño": daño, "musculo_aumentado": 10}

class BatidoDeProteinas(Habilidad):
    """Batido de Proteínas - Toma un batido de proteínas"""
    
    def __init__(self):
        super().__init__(
            nombre="Batido de Proteínas",
            descripcion="Toma un batido de proteínas. Cura y aumenta stats temporalmente.",
            costo_energia=25,
            tipo="defensiva"
        )
        self.es_curacion = True
    
    def usar(self, usuario, objetivo):
        # Curación
        curacion = usuario.vida_maxima // 3
        vida_curada = usuario.recibir_curacion(curacion)
        
        # Aumenta ataque temporalmente - duración 2 turnos
        usuario.ataque += 12
        print(f"{C.VERDE}¡Batido de proteínas! Vida +{vida_curada}, Ataque +12{C.RESET}")
        
        # Registrar proteína consumida
        if hasattr(usuario, '_proteinas_consumidas'):
            usuario._proteinas_consumidas += 1
        
        # Aumenta músculo
        if hasattr(usuario, '_musculo'):
            usuario._musculo = min(150, usuario._musculo + 8)
        
        # Posible efecto secundario (10%) - duración 2 turnos
        if random.random() < 0.1:
            usuario.aplicar_estado("sobrecarga_proteica", duracion=2)
            print(f"{C.AMARILLO}¡Sobrecarga proteica!{C.RESET}")
        
        print(f"{C.CYAN}Proteínas consumidas: {getattr(usuario, '_proteinas_consumidas', 0)}{C.RESET}")
        
        return {"exito": True, "curacion": vida_curada, "ataque_aumentado": 12, "musculo_aumentado": 8}

class SelfieEnElEspejo(Habilidad):
    """Selfie en el Espejo - Se toma un selfie en el espejo del gym"""
    
    def __init__(self):
        super().__init__(
            nombre="Selfie en el Espejo",
            descripcion="Se toma un selfie en el espejo del gym. Aumenta músculo y ataque.",
            costo_energia=30,
            tipo="defensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Aumenta músculo significativamente
        if hasattr(usuario, '_musculo'):
            aumento = 15
            usuario._musculo = min(150, usuario._musculo + aumento)
        
        # Aumenta ataque (autoestima) - duración 2 turnos
        usuario.ataque += 8
        
        # Registrar selfie
        if hasattr(usuario, '_selfies_espejo'):
            usuario._selfies_espejo += 1
        
        # Posible cegamiento por flash (15%) - duración 1 turno
        if random.random() < 0.15:
            objetivo.aplicar_estado("cegado", duracion=1)
            print(f"{C.ROJO}¡Flash del selfie! Cegado.{C.RESET}")
        
        print(f"{C.MAGENTA}¡Selfie en el espejo! Músculo +15, Ataque +8. Selfies: {getattr(usuario, '_selfies_espejo', 0)}{C.RESET}")
        
        return {"exito": True, "musculo_aumentado": 15, "ataque_aumentado": 8}

class Levantamiento(Habilidad):
    """Levantamiento - Levanta peso extremo"""
    
    def __init__(self):
        super().__init__(
            nombre="Levantamiento",
            descripcion="Levanta peso extremo. Daño masivo pero puede lesionarse.",
            costo_energia=40,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Daño masivo
        daño_base = usuario.ataque * 4
        
        # Extra daño si el objetivo es ligero
        if "Flaquito" in objetivo.tipo or "Guiri" in objetivo.tipo:
            daño_base = int(daño_base * 1.5)
            print(f"{C.ROJO}¡Contra ligeros! +50% daño{C.RESET}")
        
        daño = objetivo.recibir_dano(daño_base, "fuerza")
        
        # Aumenta músculo significativamente
        if hasattr(usuario, '_musculo'):
            usuario._musculo = min(150, usuario._musculo + 25)
        
        # Registrar peso levantado
        if hasattr(usuario, '_peso_levantado'):
            peso = random.randint(100, 200)
            usuario._peso_levantado += peso
        
        # Posible lesión (30%) - duración 3 turnos
        if random.random() < 0.3:
            usuario.aplicar_estado("lesionado", duracion=3)
            print(f"{C.ROJO}¡Lesión por sobreesfuerzo!{C.RESET}")
        
        print(f"{C.VERDE_BRILLANTE}¡LEVANTAMIENTO ÉPICO! Daño: {daño}, Músculo +25. Peso total levantado: {getattr(usuario, '_peso_levantado', 0)}kg{C.RESET}")
        
        return {"exito": True, "daño": daño, "musculo_aumentado": 25}

class GritoDeGuerra(Habilidad):
    """Grito de Guerra - Da un grito motivador"""
    
    def __init__(self):
        super().__init__(
            nombre="Grito de Guerra",
            descripcion="Da un grito motivador. Aumenta todas las stats temporalmente.",
            costo_energia=35,
            tipo="defensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Aumento significativo de stats - duración 2 turnos
        usuario.ataque += 20
        usuario.defensa += 15
        usuario.velocidad += 10
        
        # Recupera energía
        usuario.energia_actual = min(usuario.energia_maxima, usuario.energia_actual + 30)
        
        # Registrar grito
        if hasattr(usuario, '_gritos_dados'):
            usuario._gritos_dados += 1
        
        # Posible aturdimiento del enemigo (40%) - duración 1 turno
        if random.random() < 0.4:
            objetivo.aplicar_estado("aturdido", duracion=1)
            print(f"{C.MAGENTA}¡Aturdido por el grito!{C.RESET}")
        
        print(f"{C.ROJO_BRILLANTE}¡¡¡GRITO DE GUERRA!!! Ataque +20, Defensa +15, Velocidad +10, Energía +30. Gritos: {getattr(usuario, '_gritos_dados', 0)}{C.RESET}")
        
        return {
            "exito": True,
            "ataque_aumentado": 20,
            "defensa_aumentada": 15,
            "velocidad_aumentada": 10,
            "energia_recuperada": 30
        }

class RutinaExtrema(Habilidad):
    """Rutina Extrema - Realiza una rutina de entrenamiento extrema"""
    
    def __init__(self):
        super().__init__(
            nombre="Rutina Extrema",
            descripcion="Realiza una rutina de entrenamiento extrema. Efectos masivos pero agotadores.",
            costo_energia=60,
            tipo="especial"
        )
        self.es_curacion = True  # Cura vida
    
    def usar(self, usuario, objetivo):
        print(f"{C.ROJO_BRILLANTE}¡{usuario.nombre} comienza una RUTINA EXTREMA!{C.RESET}")
        
        # Efectos masivos
        efectos = []
        
        # 1. Daño masivo al objetivo (entrenamiento compartido forzado)
        daño_base = usuario.ataque * 5
        daño = objetivo.recibir_dano(daño_base, "fuerza")
        efectos.append(f"Daño: {daño}")
        
        # 2. Gran aumento de músculo
        if hasattr(usuario, '_musculo'):
            usuario._musculo = min(150, usuario._musculo + 40)
            efectos.append("Músculo +40")
        
        # 3. Aumento permanente de stats
        usuario.ataque += 25
        usuario.defensa += 20
        usuario.velocidad += 15
        efectos.append("Ataque +25, Defensa +20, Velocidad +15")
        
        # 4. Curación por endorfinas
        curacion = usuario.vida_maxima // 2
        vida_curada = usuario.recibir_curacion(curacion)
        efectos.append(f"Vida +{vida_curada}")
        
        # 5. Agotamiento extremo - duración 2 turnos
        usuario.aplicar_estado("agotado", duracion=2)
        efectos.append("Agotado")
        
        # 6. Posible lesión grave (20%) - duración 4 turnos
        if random.random() < 0.2:
            usuario.aplicar_estado("lesionado_grave", duracion=4)
            efectos.append("Lesión grave")
        
        print(f"{C.AZUL}Rutina extrema efectos: {', '.join(efectos)}{C.RESET}")
        
        return {
            "exito": True,
            "efectos": efectos,
            "daño": daño,
            "curacion": vida_curada,
            "musculo_aumentado": 40
        }