"""
Habilidades específicas de la Choni de Barrio
Cada habilidad refleja la actitud, chismes y estilo de vida choni.
"""

from .habilidad_base import Habilidad
from utils import Colores as C
import random

class TacónEnElPie(Habilidad):
    """Tacón en el Pie - Golpea con el tacón"""
    
    def __init__(self):
        super().__init__(
            nombre="Tacón en el Pie",
            descripcion="Golpea con el tacón. Daño extra si el objetivo es 'fino'.",
            costo_energia=15,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        daño_base = usuario.ataque
        
        # Extra daño a objetivos "finos" o "educados"
        if any(tipo in objetivo.tipo for tipo in ["� Católica Conservadora", "� Político Prometedor", "�️ Super Sacerdote"]):
            daño_base = int(daño_base * 1.7)
            print(f"{C.ROJO}¡Le duele a los finos! +70% daño{C.RESET}")
        
        daño = objetivo.recibir_dano(daño_base, "fisico")
        
        # Posible rotura de tacón (10%)
        if random.random() < 0.1 and hasattr(usuario, '_uñas_rotas'):
            usuario._uñas_rotas += 1  # Bueno, es tacón, pero usamos el mismo contador
            print(f"{C.AMARILLO}¡Se le rompe un tacón! Uñas/Tacones rotos: {usuario._uñas_rotas}{C.RESET}")
        
        return {"exito": True, "daño": daño, "tipo": "fisico"}

class MiradaDeHielo(Habilidad):
    """Mirada de Hielo - Una mirada que congela"""
    
    def __init__(self):
        super().__init__(
            nombre="Mirada de Hielo",
            descripcion="Una mirada que congela. Reduce velocidad y puede paralizar.",
            costo_energia=20,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Reduce velocidad significativamente - duración 2 turnos
        reduccion = max(10, objetivo.velocidad // 3)
        objetivo.velocidad = max(5, objetivo.velocidad - reduccion)
        
        # Posible paralización (30%) - duración 1 turno
        if random.random() < 0.3:
            objetivo.aplicar_estado("paralizado", duracion=1)
            print(f"{C.CYAN}¡Paralizado por la mirada!{C.RESET}")
        
        print(f"{C.AZUL}¡Mirada de hielo! Velocidad -{reduccion}{C.RESET}")
        
        return {"exito": True, "velocidad_reducida": reduccion}

class SelfieConFiltro(Habilidad):
    """Selfie con Filtro - Se toma un selfie con filtro"""
    
    def __init__(self):
        super().__init__(
            nombre="Selfie con Filtro",
            descripcion="Se toma un selfie con filtro. Aumenta actitud y puede cegar al enemigo.",
            costo_energia=25,
            tipo="defensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Aumenta actitud
        if hasattr(usuario, '_actitud'):
            aumento = 15
            usuario._actitud = min(100, usuario._actitud + aumento)
        
        # Registrar selfie
        if hasattr(usuario, '_selfies_tomadas'):
            usuario._selfies_tomadas += 1
        
        # Posible cegamiento por flash (25%) - duración 1 turno
        if random.random() < 0.25:
            objetivo.aplicar_estado("cegado", duracion=1)
            print(f"{C.ROJO}¡Flash del selfie! Cegado.{C.RESET}")
        
        # Filtro aleatorio
        filtros = ["perrito", "corazones", "flores", "arcoíris", "estrellas"]
        filtro = random.choice(filtros)
        
        print(f"{C.MAGENTA}¡Selfie con filtro de {filtro}! Actitud +{aumento}. Selfies: {getattr(usuario, '_selfies_tomadas', 0)}{C.RESET}")
        
        return {"exito": True, "actitud_aumentada": aumento, "filtro": filtro}

class Uñazo(Habilidad):
    """Uñazo - Araña con las uñas largas"""
    
    def __init__(self):
        super().__init__(
            nombre="Uñazo",
            descripcion="Araña con las uñas largas. Daño extra y posible sangrado.",
            costo_energia=30,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        daño_base = usuario.ataque * 2
        
        # Daño extra si el objetivo no tiene protección
        if objetivo.defensa < 14:
            daño_base = int(daño_base * 1.4)
            print(f"{C.ROJO}¡Sin protección contra uñas! +40% daño{C.RESET}")
        
        daño = objetivo.recibir_dano(daño_base, "fisico")
        
        # Posible sangrado (40%) - duración 3 turnos
        if random.random() < 0.4:
            objetivo.aplicar_estado("sangrando", duracion=3)
            print(f"{C.ROJO}¡Arañazo profundo! Sangrado.{C.RESET}")
        
        # Posible rotura de uñas (20%)
        if random.random() < 0.2 and hasattr(usuario, '_uñas_rotas'):
            usuario._uñas_rotas += 1
            print(f"{C.AMARILLO}¡Se le rompe una uña! Total rotas: {usuario._uñas_rotas}{C.RESET}")
        
        return {"exito": True, "daño": daño, "tipo": "fisico"}

class Chismorreo(Habilidad):
    """Chismorreo - Cuenta un chisme jugoso"""
    
    def __init__(self):
        super().__init__(
            nombre="Chismorreo",
            descripcion="Cuenta un chisme jugoso. Daño psicológico y reduce defensa.",
            costo_energia=35,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Daño psicológico
        daño_base = usuario.ataque
        daño = objetivo.recibir_dano(daño_base, "psicologico")
        
        # Reduce defensa (se siente expuesto) - duración 3 turnos
        reduccion = max(8, objetivo.defensa // 4)
        objetivo.defensa = max(5, objetivo.defensa - reduccion)
        
        # Registrar chisme
        if hasattr(usuario, '_chismes_contados'):
            usuario._chismes_contados += 1
        
        # Chisme aleatorio
        chismes = [
            f"{objetivo.nombre} engañó a su pareja",
            f"{objetivo.nombre} debe dinero",
            f"{objetivo.nombre} se operó la nariz",
            f"{objetivo.nombre} fue a la cárcel",
            f"{objetivo.nombre} tiene un hijo secreto"
        ]
        chisme = random.choice(chismes)
        
        print(f"{C.MAGENTA}¡Chismorreo: \"{chisme}\"! Defensa -{reduccion}. Chismes: {getattr(usuario, '_chismes_contados', 0)}{C.RESET}")
        
        return {"exito": True, "daño": daño, "defensa_reducida": reduccion, "chisme": chisme}

class FiestaDelPueblo(Habilidad):
    """Fiesta del Pueblo - Se va de fiesta"""
    
    def __init__(self):
        super().__init__(
            nombre="Fiesta del Pueblo",
            descripcion="Se va de fiesta. Grandes beneficios pero posibles consecuencias.",
            costo_energia=50,
            tipo="especial"
        )
        self.es_curacion = True  # Cura vida
    
    def usar(self, usuario, objetivo):
        # Grandes beneficios
        curacion = usuario.vida_maxima // 3
        vida_curada = usuario.recibir_curacion(curacion)
        energia_recuperada = 50
        aumento_actitud = 25
        
        usuario.energia_actual = min(usuario.energia_maxima, usuario.energia_actual + energia_recuperada)
        
        if hasattr(usuario, '_actitud'):
            usuario._actitud = min(100, usuario._actitud + aumento_actitud)
        
        if hasattr(usuario, '_fiestas_asistidas'):
            usuario._fiestas_asistidas += 1
        
        # Posibles consecuencias (30%)
        if random.random() < 0.3:
            consecuencias = ["resaca", "vergüenza_ajena", "perdida_dinero"]
            consecuencia = random.choice(consecuencias)
            
            if consecuencia == "resaca":
                usuario.aplicar_estado("resaca", duracion=2)
                print(f"{C.ROJO}¡Resaca monumental!{C.RESET}")
            elif consecuencia == "vergüenza_ajena":
                # El objetivo se avergüenza por ella
                objetivo.aplicar_estado("avergonzado", duracion=2)
                print(f"{C.AMARILLO}¡Vergüenza ajena!{C.RESET}")
            else:
                # Pierde energía (dinero)
                perdida = min(20, usuario.energia_actual)
                usuario.energia_actual -= perdida
                print(f"{C.ROJO}¡Gasta demasiado! Energía -{perdida}{C.RESET}")
        
        print(f"{C.VERDE_BRILLANTE}¡FIESTA DEL PUEBLO! Vida +{vida_curada}, Energía +{energia_recuperada}, Actitud +{aumento_actitud}. Fiestas: {getattr(usuario, '_fiestas_asistidas', 0)}{C.RESET}")
        
        return {
            "exito": True,
            "curacion": vida_curada,
            "energia_recuperada": energia_recuperada,
            "actitud_aumentada": aumento_actitud
        }