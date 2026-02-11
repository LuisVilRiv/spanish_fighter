"""
Habilidades específicas de Maripili Católica.
Cada habilidad refleja la piedad, tradición y juicio moral típicos.
"""

from .habilidad_base import Habilidad
from utils import Colores as C
import random

class RezarRosario(Habilidad):
    """Rezar el Rosario - Cura y aumenta defensa"""
    
    def __init__(self):
        super().__init__(
            nombre="Rezar el Rosario",
            descripcion="Reza el rosario con devoción. Se cura y aumenta su defensa.",
            costo_energia=25,
            tipo="defensiva"
        )
        self.es_curacion = True
    
    def usar(self, usuario, objetivo):
        # Curación
        curacion = usuario.vida_maxima // 4
        vida_curada = usuario.recibir_curacion(curacion)
        
        # Aumenta defensa - duración 2 turnos
        usuario.defensa += 10
        print(f"{C.VERDE}¡Defensa aumentada en 10!{C.RESET}")
        
        # Daño a segarros (les duele lo religioso)
        if "🎮 Amego Segarro" in objetivo.tipo:
            dano_extra = objetivo.recibir_dano(20, "religioso")
            print(f"{C.ROJO}¡El segarro sufre daño extra por blasfemia!{C.RESET}")
        
        return {"exito": True, "curacion": vida_curada, "tipo": "defensiva"}

class AguaBendita(Habilidad):
    """Agua Bendita - Daño extra a impuros"""
    
    def __init__(self):
        super().__init__(
            nombre="Agua Bendita",
            descripcion="Riega agua bendita. Daño extra a impuros.",
            costo_energia=20,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        dano_base = usuario.ataque // 2
        
        # Doble daño a segarros y turistas borrachos
        tipos_impuros = ["🎮 Amego Segarro", "🧳 Guiri Turista", "💅 Choni de Barrio"]
        if any(tipo in objetivo.tipo for tipo in tipos_impuros):
            dano_base *= 2
            print(f"{C.ROJO}¡Super efectivo contra impuros! x2{C.RESET}")
        
        dano = objetivo.recibir_dano(dano_base, "religioso")
        
        # Posible curación de estados negativos (50% de eliminar un estado)
        if random.random() < 0.5 and usuario.estados:
            estado_eliminado = usuario.estados[0]  # elimina el primero
            usuario.eliminar_estado(estado_eliminado)
            print(f"{C.VERDE}¡Estado '{estado_eliminado}' eliminado!{C.RESET}")
        
        return {"exito": True, "daño": dano, "tipo": "religioso"}

class SermonDominical(Habilidad):
    """Sermón Dominical - Aburre al enemigo hasta dormirlo"""
    
    def __init__(self):
        super().__init__(
            nombre="Sermón Dominical",
            descripcion="Da un sermón aburrido que puede dormir al enemigo.",
            costo_energia=30,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Intenta dormir al objetivo (60% de probabilidad) - duración 1-3 turnos
        if random.random() < 0.6:
            duracion = random.randint(1, 3)
            objetivo.aplicar_estado("dormido", duracion=duracion)
            print(f"{C.CYAN}¡{objetivo.nombre} se ha dormido por {duracion} turno(s)!{C.RESET}")
        
        # Daño por aburrimiento
        dano = objetivo.recibir_dano(usuario.ataque // 3, "aburrimiento")
        
        return {"exito": True, "daño": dano, "tipo": "aburrimiento"}

class MiradaJuzgadora(Habilidad):
    """Mirada Juzgadora - Una mirada que hace sentir culpable"""
    
    def __init__(self):
        super().__init__(
            nombre="Mirada Juzgadora",
            descripcion="Una mirada que hace sentir culpable. Reduce ataque.",
            costo_energia=15,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Reduce ataque por culpa - duración 2 turnos
        reduccion = max(5, objetivo.ataque // 5)
        objetivo.ataque = max(10, objetivo.ataque - reduccion)
        
        # Más efectivo contra católicos y abuelas
        if any(tipo in objetivo.tipo for tipo in ["📿 Católica Conservadora", "👵 Abuela Española"]):
            reduccion *= 2
            print(f"{C.ROJO}¡Se siente muy culpable! x2{C.RESET}")
        
        print(f"{C.AMARILLO}Ataque de {objetivo.nombre} reducido en {reduccion}{C.RESET}")
        
        return {"exito": True, "efecto": "ataque_reducido", "tipo": "psicologico"}

class ViernesSanto(Habilidad):
    """Viernes Santo - No come carne y potencia habilidades religiosas"""
    
    def __init__(self):
        super().__init__(
            nombre="Viernes Santo",
            descripcion="No come carne y potencia habilidades religiosas.",
            costo_energia=40,
            tipo="especial"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Potencia todas las habilidades religiosas temporalmente - duración 3 turnos
        usuario.aplicar_estado("viernes_santo", duracion=3)
        
        # Aumenta ataque y defensa
        usuario.ataque += 15
        usuario.defensa += 10
        
        # Daño a quien coma jamón (segarros especialmente)
        if "🎮 Amego Segarro" in objetivo.tipo:
            dano = objetivo.recibir_dano(40, "religioso")
            print(f"{C.ROJO}¡El segarro sufre por comer jamón en Viernes Santo!{C.RESET}")
        else:
            dano = objetivo.recibir_dano(25, "religioso")
        
        print(f"{C.NEGRITA}{C.BLANCO}¡Viernes Santo! Poder religioso aumentado{C.RESET}")
        
        return {"exito": True, "daño": dano, "tipo": "religioso"}

class Excomulgar(Habilidad):
    """Excomulgar - Expulsa temporalmente del combate"""
    
    def __init__(self):
        super().__init__(
            nombre="Excomulgar",
            descripcion="Expulsa al enemigo temporalmente del combate.",
            costo_energia=50,
            tipo="especial"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Solo funciona contra no creyentes
        tipos_creyentes = ["📿 Católica Conservadora", "✝️ Super Sacerdote"]
        
        if objetivo.tipo in tipos_creyentes:
            print(f"{C.AMARILLO}¡No puede excomulgar a un creyente!{C.RESET}")
            return {"exito": False, "mensaje": "No funciona contra creyentes"}
        
        # Expulsión temporal (pierde un turno) - duración 1 turno
        objetivo.aplicar_estado("excomulgado", duracion=1)
        
        # Daño psicológico
        dano = objetivo.recibir_dano(usuario.ataque // 2, "religioso")
        
        print(f"{C.ROJO_BRILLANTE}¡{objetivo.nombre} ha sido excomulgado! Pierde un turno.{C.RESET}")
        
        return {"exito": True, "daño": dano, "efecto": "excomulgado", "tipo": "religioso"}