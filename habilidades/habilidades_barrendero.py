"""
Habilidades específicas del Barrendero Filósofo
Cada habilidad refleja la sabiduría callejera y la filosofía del barrendero.
"""

from .habilidad_base import Habilidad
from utils import Colores as C
import random

class BarridoExistencial(Habilidad):
    """Barrido Existencial - Barre mientras reflexiona sobre la vida"""
    
    def __init__(self):
        super().__init__(
            nombre="Barrido Existencial",
            descripcion="Barre mientras reflexiona sobre la vida. Daño y posible confusión.",
            costo_energia=20,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        daño_base = usuario.ataque
        
        # Aumenta daño con sabiduría
        if hasattr(usuario, '_sabiduria'):
            bonus = 1 + (usuario._sabiduria / 200)  # Hasta +50%
            daño_base = int(daño_base * bonus)
        
        daño = objetivo.recibir_dano(daño_base, "filosofico")
        
        # Posible confusión existencial (40%) - duración 2 turnos
        if random.random() < 0.4:
            objetivo.aplicar_estado("confundido", duracion=2)
            print(f"{C.MAGENTA}¡Confusión existencial!{C.RESET}")
        
        # Registrar calle barrida
        if hasattr(usuario, '_calles_barridas'):
            usuario._calles_barridas += 1
        
        print(f"{C.CYAN}Barre mientras piensa en el sentido de la vida... Calles: {getattr(usuario, '_calles_barridas', 0)}{C.RESET}")
        
        return {"exito": True, "daño": daño, "tipo": "filosofico"}

class FregonaDeLaVerdad(Habilidad):
    """Fregona de la Verdad - Friega con la verdad absoluta"""
    
    def __init__(self):
        super().__init__(
            nombre="Fregona de la Verdad",
            descripcion="Friega con la verdad absoluta. Daño extra a mentirosos.",
            costo_energia=25,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        daño_base = usuario.ataque * 2
        
        # Super efectivo contra mentirosos (políticos, segarros)
        if any(tipo in objetivo.tipo for tipo in ["� Político Prometedor", "� Amego Segarro"]):
            daño_base = int(daño_base * 1.8)
            print(f"{C.ROJO}¡La verdad duele a los mentirosos! +80% daño{C.RESET}")
        
        daño = objetivo.recibir_dano(daño_base, "verdad")
        
        # Revela debilidades (30%) - duración 3 turnos
        if random.random() < 0.3:
            objetivo.aplicar_estado("revelado", duracion=3)
            print(f"{C.VERDE}¡Debilidades reveladas!{C.RESET}")
        
        return {"exito": True, "daño": daño, "tipo": "verdad"}

class CuboDeLaSabiduria(Habilidad):
    """Cubo de la Sabiduría - Lanza el cubo lleno de conocimiento"""
    
    def __init__(self):
        super().__init__(
            nombre="Cubo de la Sabiduría",
            descripcion="Lanza el cubo lleno de conocimiento. Daño y posible sabiduría.",
            costo_energia=30,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        daño_base = usuario.ataque * 2
        
        # Daño extra si el objetivo es ignorante
        if "Guiri Turista" in objetivo.tipo or "Choni" in objetivo.tipo:
            daño_base = int(daño_base * 1.5)
            print(f"{C.ROJO}¡La ignorancia duele! +50% daño{C.RESET}")
        
        daño = objetivo.recibir_dano(daño_base, "sabiduria")
        
        # Posible ganancia de sabiduría para el usuario (25%)
        if random.random() < 0.25 and hasattr(usuario, '_sabiduria'):
            usuario._sabiduria = min(150, usuario._sabiduria + 10)
            print(f"{C.VERDE}¡Aprende del ataque! Sabiduría +10.{C.RESET}")
        
        return {"exito": True, "daño": daño, "tipo": "sabiduria"}

class MeditacionCallejera(Habilidad):
    """Meditación Callejera - Medita en medio de la calle"""
    
    def __init__(self):
        super().__init__(
            nombre="Meditación Callejera",
            descripcion="Medita en medio de la calle. Recupera vida, energía y sabiduría.",
            costo_energia=0,  # No cuesta energía, más bien la regenera
            tipo="defensiva"
        )
        self.es_curacion = True
    
    def usar(self, usuario, objetivo):
        # Recuperación significativa
        curacion = usuario.vida_maxima // 4
        vida_curada = usuario.recibir_curacion(curacion)
        energia_recuperada = 40
        sabiduria_recuperada = 15
        
        usuario.energia_actual = min(usuario.energia_maxima, usuario.energia_actual + energia_recuperada)
        
        if hasattr(usuario, '_sabiduria'):
            usuario._sabiduria = min(150, usuario._sabiduria + sabiduria_recuperada)
        
        # Posible iluminación (10%) - duración 3 turnos
        if random.random() < 0.1:
            usuario.aplicar_estado("iluminado", duracion=3)
            print(f"{C.VERDE_BRILLANTE}¡ILUMINACI�N!{C.RESET}")
        
        print(f"{C.AZUL}¡Meditación callejera! Vida +{vida_curada}, Energía +{energia_recuperada}, Sabiduría +{sabiduria_recuperada}{C.RESET}")
        
        return {
            "exito": True,
            "curacion": vida_curada,
            "energia_recuperada": energia_recuperada,
            "sabiduria_recuperada": sabiduria_recuperada
        }

class FilosofiaDeBar(Habilidad):
    """Filosofía de Bar - Comparte sabiduría de bar"""
    
    def __init__(self):
        super().__init__(
            nombre="Filosofía de Bar",
            descripcion="Comparte sabiduría de bar. Efectos aleatorios basados en filosofías.",
            costo_energia=35,
            tipo="especial"
        )
        self.es_curacion = False  # Algunas filosofías pueden curar, pero no siempre
    
    def usar(self, usuario, objetivo):
        filosofias = [
            self._filosofia_existencialista,
            self._filosofia_absurda,
            self._filosofia_hedonista,
            self._filosofia_estoica,
            self._filosofia_nihilista,
            self._filosofia_pragmatica
        ]
        
        filosofia = random.choice(filosofias)
        return filosofia(usuario, objetivo)
    
    def _filosofia_existencialista(self, usuario, objetivo):
        """Existencialismo - Enfrentamiento con la nada"""
        daño = objetivo.recibir_dano(usuario.ataque * 2, "existencial")
        
        # Posible crisis existencial - duración 2 turnos
        if random.random() < 0.4:
            objetivo.aplicar_estado("crisis_existencial", duracion=2)
            print(f"{C.MAGENTA}¡Crisis existencial!{C.RESET}")
        
        print(f"{C.CYAN}«La vida es absurda, pero hay que vivirla». Daño: {daño}{C.RESET}")
        return {"exito": True, "filosofia": "existencialismo", "daño": daño}
    
    def _filosofia_absurda(self, usuario, objetivo):
        """Absurdo - Todo carece de sentido"""
        # Confunde fuertemente - duración 2 turnos
        objetivo.aplicar_estado("confundido", duracion=2)
        
        # Reduce ataque y defensa - duración 2 turnos
        reduccion_atk = max(4, objetivo.ataque // 5)
        reduccion_def = max(3, objetivo.defensa // 5)
        objetivo.ataque = max(5, objetivo.ataque - reduccion_atk)
        objetivo.defensa = max(5, objetivo.defensa - reduccion_def)
        
        print(f"{C.CYAN}«Nada tiene sentido, así que ¿por qué preocuparse?». Ataque -{reduccion_atk}, Defensa -{reduccion_def}{C.RESET}")
        return {"exito": True, "filosofia": "absurdo", "ataque_reducido": 10, "defensa_reducida": 8}
    
    def _filosofia_hedonista(self, usuario, objetivo):
        """Hedonismo - Busca el placer"""
        # Cura a ambos (el placer es compartido)
        curacion_usuario = usuario.vida_maxima // 6
        curacion_objetivo = objetivo.vida_maxima // 8
        
        vida_curada_usuario = usuario.recibir_curacion(curacion_usuario)
        vida_curada_objetivo = objetivo.recibir_curacion(curacion_objetivo)
        
        print(f"{C.VERDE}«El placer es el único bien». Ambos curan: tú +{vida_curada_usuario}, él +{vida_curada_objetivo}{C.RESET}")
        return {"exito": True, "filosofia": "hedonismo", "curacion_usuario": vida_curada_usuario, "curacion_objetivo": vida_curada_objetivo}
    
    def _filosofia_estoica(self, usuario, objetivo):
        """Estoicismo - Acepta lo inevitable"""
        # Aumenta defensa significativamente - duración 2 turnos
        aumento_defensa = max(8, usuario.defensa // 3)
        usuario.defensa += aumento_defensa
        
        # Resistencia a estados negativos - duración 2 turnos
        usuario.aplicar_estado("resistente", duracion=2)
        
        print(f"{C.AZUL}«Acepta lo que no puedes cambiar». Defensa +{aumento_defensa}, Resistente{C.RESET}")
        return {"exito": True, "filosofia": "estoicismo", "defensa_aumentada": aumento_defensa}
    
    def _filosofia_nihilista(self, usuario, objetivo):
        """Nihilismo - Nada importa"""
        # Daño a ambos (nada importa)
        daño_usuario = usuario.vida_maxima // 10
        daño_objetivo = objetivo.vida_maxima // 6
        
        usuario.recibir_dano(daño_usuario, "nihilista")
        objetivo.recibir_dano(daño_objetivo, "nihilista")
        
        print(f"{C.ROJO}«Nada importa, ni siquiera esto». Ambos daño: tú -{daño_usuario}, él -{daño_objetivo}{C.RESET}")
        return {"exito": True, "filosofia": "nihilismo", "daño_usuario": daño_usuario, "daño_objetivo": daño_objetivo}
    
    def _filosofia_pragmatica(self, usuario, objetivo):
        """Pragmatismo - Lo útil es lo verdadero"""
        # Beneficios prácticos
        usuario.energia_actual = min(usuario.energia_maxima, usuario.energia_actual + 30)
        aumento_atk = max(3, usuario.ataque // 5)
        usuario.ataque += aumento_atk
        
        if hasattr(usuario, '_sabiduria'):
            usuario._sabiduria = min(150, usuario._sabiduria + 5)
        
        print(f"{C.VERDE}«Lo útil es lo verdadero». Energía +30, Ataque +{aumento_atk}, Sabiduría +5{C.RESET}")
        return {"exito": True, "filosofia": "pragmatismo", "energia_recuperada": 30, "ataque_aumentado": 8}

class LimpiezaProfunda(Habilidad):
    """Limpieza Profunda - Limpieza total física y espiritual"""
    
    def __init__(self):
        super().__init__(
            nombre="Limpieza Profunda",
            descripcion="Limpieza total física y espiritual. Elimina estados negativos y daña.",
            costo_energia=50,
            tipo="especial"
        )
        self.es_curacion = True  # Porque elimina estados negativos
    
    def usar(self, usuario, objetivo):
        # Elimina estados negativos del usuario
        estados_negativos = ["envenenado", "confundido", "quemado", "congelado", "maldito", "paralizado"]
        estados_eliminados = []
        
        for estado in estados_negativos:
            if estado in usuario.estados:
                usuario.eliminar_estado(estado)
                estados_eliminados.append(estado)
        
        # Daño al objetivo (la "suciedad")
        daño_base = usuario.ataque * 2
        
        # Extra daño si el objetivo es "sucio" (Segarro, Choni, etc.)
        if any(tipo in objetivo.tipo for tipo in ["� Amego Segarro", "� Choni de Barrio"]):
            daño_base = int(daño_base * 1.5)
            print(f"{C.ROJO}¡Limpieza profunda de suciedad! +50% daño{C.RESET}")
        
        daño = objetivo.recibir_dano(daño_base, "limpieza")
        
        # Aumenta sabiduría por la limpieza
        if hasattr(usuario, '_sabiduria'):
            usuario._sabiduria = min(150, usuario._sabiduria + 20)
        
        print(f"{C.CYAN}¡Limpieza profunda! Estados eliminados: {estados_eliminados}. Daño: {daño}. Sabiduría +20{C.RESET}")
        
        return {
            "exito": True,
            "estados_eliminados": estados_eliminados,
            "daño": daño,
            "sabiduria_aumentada": 20
        }