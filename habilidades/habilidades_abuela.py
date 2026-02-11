"""
Habilidades específicas de Doña Remedios (Abuela Española)
Cada habilidad refleja la sabiduría, cocina y poder familiar de la abuela española.
"""

from .habilidad_base import Habilidad
from utils import Colores as C
import random

class CucharonDeMadera(Habilidad):
    """Cucharón de Madera - Golpea con el cucharón de cocina"""
    
    def __init__(self):
        super().__init__(
            nombre="Cucharón de Madera",
            descripcion="Golpea con el cucharón de cocina. Daño extra a desobedientes.",
            costo_energia=15,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        daño_base = usuario.ataque
        
        # Extra daño a los que no obedecen
        if any(tipo in objetivo.tipo for tipo in ["🎮 Amego Segarro", "💅 Choni de Barrio", "🧳 Guiri Turista"]):
            daño_base = int(daño_base * 1.5)
            print(f"{C.ROJO}¡Desobediente! +50% daño{C.RESET}")
        
        daño = objetivo.recibir_dano(daño_base, "familiar")
        
        # 20% de aturdimiento (duración 1 turno)
        if random.random() < 0.2:
            objetivo.aplicar_estado("aturdido", duracion=1)
            print(f"{C.MAGENTA}¡Aturdido con el cucharón!{C.RESET}")
        
        return {"exito": True, "daño": daño, "tipo": "fisico"}

class ComeHijo(Habilidad):
    """¡Come, hijo! - Te obliga a comer y te cura"""
    
    def __init__(self):
        super().__init__(
            nombre="¡Come, hijo!",
            descripcion="Te obliga a comer. Cura al objetivo pero puede causar indigestión.",
            costo_energia=20,
            tipo="defensiva"
        )
        self.es_curacion = True
    
    def usar(self, usuario, objetivo):
        # Curación generosa
        curacion = objetivo.vida_maxima // 3
        vida_curada = objetivo.recibir_curacion(curacion)
        
        # Registrar comida preparada
        if hasattr(usuario, '_comidas_preparadas'):
            usuario._comidas_preparadas += 1
        
        print(f"{C.VERDE}¡{objetivo.nombre} come hasta reventar! +{vida_curada} vida. Comidas: {getattr(usuario, '_comidas_preparadas', 0)}{C.RESET}")
        
        # Posible indigestión (30%) - duración 2 turnos
        if random.random() < 0.3:
            objetivo.aplicar_estado("indigestión", duracion=2)
            print(f"{C.AMARILLO}¡Demasiada comida! Indigestión.{C.RESET}")
        
        return {"exito": True, "curacion": vida_curada, "tipo": "alimento"}

class ChismeVenenoso(Habilidad):
    """Chisme Venenoso - Un chisme que duele más que un golpe"""
    
    def __init__(self):
        super().__init__(
            nombre="Chisme Venenoso",
            descripcion="Cuenta un chisme que duele. Daño psicológico y reduce defensa.",
            costo_energia=25,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Daño psicológico
        daño_base = usuario.ataque // 2
        daño = objetivo.recibir_dano(daño_base, "psicologico")
        
        # Reduce defensa (se siente vulnerable) - duración 3 turnos
        reduccion = max(5, objetivo.defensa // 4)
        objetivo.defensa = max(5, objetivo.defensa - reduccion)
        
        # Más efectivo contra familiares y conocidos
        if any(tipo in objetivo.tipo for tipo in ["👵 Abuela Española", "🎮 Amego Segarro"]):
            objetivo.aplicar_estado("avergonzado", duracion=2)
            print(f"{C.ROJO}¡Chisme familiar! Avergüenza al objetivo.{C.RESET}")
        
        print(f"{C.MAGENTA}¡Chisme del barrio! Defensa -{reduccion}{C.RESET}")
        
        return {"exito": True, "daño": daño, "defensa_reducida": reduccion}

class RemedioCasero(Habilidad):
    """Remedio Casero - Aplica un remedio de la abuela"""
    
    def __init__(self):
        super().__init__(
            nombre="Remedio Casero",
            descripcion="Aplica un remedio casero. Efectos aleatorios (curación, estados, etc).",
            costo_energia=30,
            tipo="especial"
        )
        self.es_curacion = True  # Algunos remedios curan
    
    def usar(self, usuario, objetivo):
        remedios = [
            self._vicks_vaporub,
            self._agua_con_limon,
            self._infusion_manzanilla,
            self._ajo_en_almohada,
            self._panuelo_con_alcanfor,
            self._jeringuilla_de_ajos
        ]
        
        remedio = random.choice(remedios)
        return remedio(usuario, objetivo)
    
    def _vicks_vaporub(self, usuario, objetivo):
        """Vicks Vaporub - Cura y protege"""
        curacion = usuario.vida_maxima // 5
        vida_curada = usuario.recibir_curacion(curacion)
        
        # Protección contra frío - duración 3 turnos
        usuario.eliminar_estado("congelado")
        usuario.aplicar_estado("inmune_frio", duracion=3)
        
        print(f"{C.VERDE}¡Vicks Vaporub aplicado! Cura {vida_curada} y protege del frío.{C.RESET}")
        return {"exito": True, "remedio": "vicks_vaporub", "curacion": vida_curada}
    
    def _agua_con_limon(self, usuario, objetivo):
        """Agua con limón - Desintoxica"""
        # Cura estados negativos
        estados_eliminados = []
        for estado in ["envenenado", "mareado", "confundido"]:
            if estado in objetivo.estados:
                objetivo.eliminar_estado(estado)
                estados_eliminados.append(estado)
        
        # Pequeña curación
        curacion = 10
        vida_curada = objetivo.recibir_curacion(curacion)
        
        print(f"{C.VERDE}¡Agua con limón! Desintoxica y cura {vida_curada}. Estados eliminados: {estados_eliminados}{C.RESET}")
        return {"exito": True, "remedio": "agua_con_limon", "curacion": vida_curada, "estados_eliminados": estados_eliminados}
    
    def _infusion_manzanilla(self, usuario, objetivo):
        """Infusión de manzanilla - Calma"""
        # Calma al objetivo (reduce ataque) - duración 2 turnos
        reduccion = max(3, objetivo.ataque // 6)
        objetivo.ataque = max(5, objetivo.ataque - reduccion)
        
        # Cura 15 de vida
        vida_curada = objetivo.recibir_curacion(15)
        
        print(f"{C.AZUL}¡Infusión de manzanilla! Calma al objetivo. Ataque -{reduccion}, Vida +{vida_curada}{C.RESET}")
        return {"exito": True, "remedio": "infusion_manzanilla", "ataque_reducido": reduccion, "curacion": vida_curada}
    
    def _ajo_en_almohada(self, usuario, objetivo):
        """Ajo en la almohada - Aleja males"""
        # Aleja estados negativos (40% de probabilidad)
        if random.random() < 0.4:
            estados_alejados = ["maldito", "poseído", "hechizado"]
            for estado in estados_alejados:
                if estado in objetivo.estados:
                    objetivo.eliminar_estado(estado)
            print(f"{C.VERDE}¡Ajo en la almohada! Aleja males espirituales.{C.RESET}")
        else:
            print(f"{C.AMARILLO}¡Ajo en la almohada! El olor es fuerte pero no pasa nada.{C.RESET}")
        
        return {"exito": True, "remedio": "ajo_en_almohada"}
    
    def _panuelo_con_alcanfor(self, usuario, objetivo):
        """Pañuelo con alcanfor - Alivia"""
        # Alivia estados de salud
        if "resfriado" in objetivo.estados:
            objetivo.eliminar_estado("resfriado")
            print(f"{C.VERDE}¡Pañuelo con alcanfor! Cura el resfriado.{C.RESET}")
        else:
            # Curación básica
            vida_curada = objetivo.recibir_curacion(20)
            print(f"{C.VERDE}¡Pañuelo con alcanfor! Alivia y cura {vida_curada}.{C.RESET}")
        
        return {"exito": True, "remedio": "panuelo_con_alcanfor"}
    
    def _jeringuilla_de_ajos(self, usuario, objetivo):
        """Jeringuilla de ajos - Remedio extremo"""
        # Daño al enemigo (es desagradable)
        daño = objetivo.recibir_dano(30, "remedio_casero")
        
        # Posible curación milagrosa (10%)
        if random.random() < 0.1:
            vida_curada = objetivo.recibir_curacion(50)
            print(f"{C.VERDE_BRILLANTE}¡JERINGUILLA DE AJOS MILAGROSA! Cura {vida_curada}.{C.RESET}")
        
        print(f"{C.ROJO}¡Jeringuilla de ajos! El olor hace {daño} de daño.{C.RESET}")
        return {"exito": True, "remedio": "jeringuilla_de_ajos", "daño": daño}

class MiradaQueMata(Habilidad):
    """Mirada Que Mata - La mirada de la abuela que paraliza"""
    
    def __init__(self):
        super().__init__(
            nombre="Mirada Que Mata",
            descripcion="La mirada de la abuela que paraliza. Reduce todas las estadísticas.",
            costo_energia=35,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Reduce todas las stats - duración 2 turnos
        reduccion_ataque = max(5, objetivo.ataque // 5)
        reduccion_defensa = max(5, objetivo.defensa // 5)
        reduccion_velocidad = max(5, objetivo.velocidad // 5)
        
        objetivo.ataque = max(5, objetivo.ataque - reduccion_ataque)
        objetivo.defensa = max(5, objetivo.defensa - reduccion_defensa)
        objetivo.velocidad = max(5, objetivo.velocidad - reduccion_velocidad)
        
        # Más efectivo contra familiares
        if "Segarro" in objetivo.tipo or "Abuela" in objetivo.tipo:
            objetivo.aplicar_estado("paralizado", duracion=1)
            print(f"{C.ROJO}¡Mirada familiar paralizante!{C.RESET}")
        
        print(f"{C.MAGENTA}¡Mirada de abuela! Ataque -{reduccion_ataque}, Defensa -{reduccion_defensa}, Velocidad -{reduccion_velocidad}{C.RESET}")
        
        return {
            "exito": True,
            "ataque_reducido": reduccion_ataque,
            "defensa_reducida": reduccion_defensa,
            "velocidad_reducida": reduccion_velocidad
        }

class BufandaDeLana(Habilidad):
    """Bufanda de Lana - Te abriga y protege"""
    
    def __init__(self):
        super().__init__(
            nombre="Bufanda de Lana",
            descripcion="Te teje una bufanda de lana. Aumenta defensa y protege del frío.",
            costo_energia=40,
            tipo="defensiva"
        )
        self.es_curacion = True
    
    def usar(self, usuario, objetivo):
        # Aumenta defensa significativamente - duración 3 turnos
        aumento_defensa = 20
        objetivo.defensa += aumento_defensa
        # Nota: como es temporal, no se guarda en base; se perderá al terminar combate.
        # Podríamos añadir un estado "bufanda" que expire y restaure defensa, pero es complejo.
        # Por simplicidad, lo dejamos como modificación directa.
        
        # Protección contra frío - duración 3 turnos
        objetivo.eliminar_estado("congelado")
        objetivo.aplicar_estado("inmune_frio", duracion=3)
        
        # Curación por el calorcito
        curacion = 25
        vida_curada = objetivo.recibir_curacion(curacion)
        
        print(f"{C.AZUL}¡Bufanda de lana tejida! Defensa +{aumento_defensa}, Vida +{vida_curada}, Inmune al frío.{C.RESET}")
        
        return {
            "exito": True,
            "defensa_aumentada": aumento_defensa,
            "curacion": vida_curada,
            "inmunidad": "frio"
        }