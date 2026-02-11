"""
Habilidades específicas del Político Prometedor
Cada habilidad refleja la demagogia, promesas vacías y artimañas políticas.
"""

from .habilidad_base import Habilidad
from utils import Colores as C
import random

class DiscursoVacio(Habilidad):
    """Discurso Vacío - Da un discurso sin contenido"""
    
    def __init__(self):
        super().__init__(
            nombre="Discurso Vacío",
            descripcion="Da un discurso sin contenido. Aburre al enemigo y recupera popularidad.",
            costo_energia=20,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Aburre al objetivo (posible sueño) - duración 1-2 turnos
        if random.random() < 0.4:
            duracion = random.randint(1, 2)
            objetivo.aplicar_estado("dormido", duracion=duracion)
            print(f"{C.CYAN}¡El discurso es tan aburrido que se duerme por {duracion} turno(s)!{C.RESET}")
        
        # Daño psicológico leve
        daño = objetivo.recibir_dano(usuario.ataque // 3, "aburrimiento")
        
        # Aumenta popularidad
        if hasattr(usuario, '_popularidad'):
            usuario._popularidad = min(100, usuario._popularidad + 10)
        
        # Registrar discurso
        if hasattr(usuario, '_discursos_vacios'):
            usuario._discursos_vacios += 1
        
        print(f"{C.AZUL}¡Discurso vacío! Popularidad +10. Discursos: {getattr(usuario, '_discursos_vacios', 0)}{C.RESET}")
        
        return {"exito": True, "daño": daño, "popularidad_aumentada": 10}

class PromesaFalsa(Habilidad):
    """Promesa Falsa - Promete algo que nunca cumplirá"""
    
    def __init__(self):
        super().__init__(
            nombre="Promesa Falsa",
            descripcion="Promete algo que nunca cumplirá. Confunde y desmoraliza.",
            costo_energia=25,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Confusión (creerá la promesa) - duración 2 turnos
        objetivo.aplicar_estado("confundido", duracion=2)
        
        # Reduce ataque (desmoralización) - duración 2 turnos
        reduccion = max(5, objetivo.ataque // 4)
        objetivo.ataque = max(5, objetivo.ataque - reduccion)
        
        # Registrar promesa
        if hasattr(usuario, '_promesas_incumplidas'):
            usuario._promesas_incumplidas += 1
        
        # Promesa aleatoria
        promesas = [
            "bajar los impuestos",
            "mejorar la sanidad",
            "crear empleo",
            "subir las pensiones",
            "arreglar las carreteras",
            "combatir la corrupción"
        ]
        promesa = random.choice(promesas)
        
        print(f"{C.MAGENTA}¡Promete {promesa}! Ataque -{reduccion}. Promesas incumplidas: {getattr(usuario, '_promesas_incumplidas', 0)}{C.RESET}")
        
        return {"exito": True, "ataque_reducido": reduccion, "promesa": promesa}

class FotoConBebe(Habilidad):
    """Foto con Bebé - Se fotografía con un bebé para ganar popularidad"""
    
    def __init__(self):
        super().__init__(
            nombre="Foto con Bebé",
            descripcion="Se fotografía con un bebé para ganar popularidad. Cura y aumenta stats.",
            costo_energia=30,
            tipo="defensiva"
        )
        self.es_curacion = True
    
    def usar(self, usuario, objetivo):
        # Curación
        curacion = usuario.vida_maxima // 4
        vida_curada = usuario.recibir_curacion(curacion)
        
        # Aumenta popularidad significativamente
        if hasattr(usuario, '_popularidad'):
            aumento = 20
            usuario._popularidad = min(100, usuario._popularidad + aumento)
        
        # Registrar foto
        if hasattr(usuario, '_fotos_con_bebes'):
            usuario._fotos_con_bebes += 1
        
        # Posible llanto del bebé (25% de daño al objetivo)
        if random.random() < 0.25:
            daño = objetivo.recibir_dano(15, "llanto")
            print(f"{C.ROJO}¡El bebé llora y molesta al enemigo! Daño: {daño}{C.RESET}")
        
        print(f"{C.VERDE}¡Foto con bebé! Vida +{vida_curada}, Popularidad +20. Fotos: {getattr(usuario, '_fotos_con_bebes', 0)}{C.RESET}")
        
        return {"exito": True, "curacion": vida_curada, "popularidad_aumentada": 20}

class DesviarAtencion(Habilidad):
    """Desviar Atención - Cambia de tema hábilmente"""
    
    def __init__(self):
        super().__init__(
            nombre="Desviar Atención",
            descripcion="Cambia de tema hábilmente. El enemigo pierde su turno.",
            costo_energia=35,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # El objetivo pierde su próximo turno - duración 1 turno
        objetivo.aplicar_estado("distraído", duracion=1)
        
        # Tema aleatorio al que desvía
        temas = [
            "el tiempo",
            "el fútbol",
            "la última polémica",
            "un escándalo ajeno",
            "las vacaciones",
            "la economía global"
        ]
        tema = random.choice(temas)
        
        print(f"{C.CYAN}¡Desvía la atención hacia {tema}! El enemigo perderá su próximo turno.{C.RESET}")
        
        return {"exito": True, "estado": "distraído", "tema": tema}

class SubirImpuestos(Habilidad):
    """Subir Impuestos - Sube los impuestos para obtener recursos"""
    
    def __init__(self):
        super().__init__(
            nombre="Subir Impuestos",
            descripcion="Sube los impuestos para obtener recursos. Gana energía pero pierde popularidad.",
            costo_energia=40,
            tipo="especial"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Gran ganancia de energía (dinero)
        energia_ganada = 60
        usuario.energia_actual = min(usuario.energia_maxima, usuario.energia_actual + energia_ganada)
        
        # Pierde popularidad
        if hasattr(usuario, '_popularidad'):
            perdida = 25
            usuario._popularidad = max(0, usuario._popularidad - perdida)
        
        # Registrar subida de impuestos
        if hasattr(usuario, '_impuestos_subidos'):
            usuario._impuestos_subidos += 1
        
        # Daño al objetivo (le suben los impuestos)
        daño = objetivo.recibir_dano(usuario.ataque, "impuestos")
        
        print(f"{C.ROJO}¡Subida de impuestos! Energía +{energia_ganada}, Popularidad -25, Daño: {daño}. Impuestos subidos: {getattr(usuario, '_impuestos_subidos', 0)}{C.RESET}")
        
        return {
            "exito": True,
            "energia_ganada": energia_ganada,
            "popularidad_perdida": 25,
            "daño": daño
        }

class CampanaElectoral(Habilidad):
    """Campaña Electoral - Lanza una campaña electoral completa"""
    
    def __init__(self):
        super().__init__(
            nombre="Campaña Electoral",
            descripcion="Lanza una campaña electoral completa. Efectos masivos pero costosos.",
            costo_energia=70,
            tipo="especial"
        )
        self.es_curacion = True  # Cura vida
    
    def usar(self, usuario, objetivo):
        print(f"{C.VERDE_BRILLANTE}¡{usuario.nombre} lanza una CAMPAÑA ELECTORAL!{C.RESET}")
        
        # Efectos masivos
        efectos = []
        
        # 1. Gran aumento de popularidad
        if hasattr(usuario, '_popularidad'):
            usuario._popularidad = min(100, usuario._popularidad + 40)
            efectos.append("Popularidad +40")
        
        # 2. Curación significativa
        curacion = usuario.vida_maxima // 2
        vida_curada = usuario.recibir_curacion(curacion)
        efectos.append(f"Vida +{vida_curada}")
        
        # 3. Aumento de stats - duración 3 turnos
        usuario.ataque += 15
        usuario.defensa += 10
        usuario.velocidad += 5
        efectos.append("Ataque +15, Defensa +10, Velocidad +5")
        
        # 4. Daño masivo al enemigo (crítica mediática)
        daño_base = usuario.ataque * 4
        daño = objetivo.recibir_dano(daño_base, "mediatico")
        efectos.append(f"Daño mediático: {daño}")
        
        # 5. Posible victoria automática si la popularidad es muy alta (5%)
        if hasattr(usuario, '_popularidad') and usuario._popularidad >= 90 and random.random() < 0.05:
            objetivo.vida_actual = 0
            print(f"{C.VERDE_BRILLANTE}¡VICTORIA ELECTORAL APLASTANTE! El enemigo se rinde.{C.RESET}")
            efectos.append("Victoria electoral")
        
        # Gran costo de energía
        print(f"{C.AZUL}Campaña electoral efectos: {', '.join(efectos)}{C.RESET}")
        
        return {
            "exito": True,
            "efectos": efectos,
            "daño": daño,
            "curacion": vida_curada
        }