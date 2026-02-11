"""
PutoAmo del Gym - El tío del gym que solo habla de proteínas
Cultor del físico y la autoestima muscular

Estadísticas:
- Vida: 90
- Ataque: 25
- Defensa: 8
- Velocidad: 55
- Energía: 110
"""

from .personaje_base import Personaje
from habilidades.habilidades_putamo import (
    FlexionExplosiva,
    BatidoDeProteinas,
    SelfieEnElEspejo,
    Levantamiento,
    GritoDeGuerra,
    RutinaExtrema
)
from utils import Colores as C
import random

class PutoAmo(Personaje):
    """
    Personaje: PutoAmo del Gym
    El tío del gym que solo habla de proteínas.
    Cultor del físico y la autoestima muscular.
    """
    
    def __init__(self, nombre_personalizado: str = None):
        super().__init__(
            nombre=nombre_personalizado if nombre_personalizado else "Máximo Pump",
            tipo="💪 PutoAmo del Gym",
            vida_base=90,
            ataque_base=25,
            defensa_base=8,
            velocidad_base=55,
            energia_base=110
        )
        
        # Sistema de tipos y efectividades
        self.debilidades = ["inteligencia", "cardio", "flexibilidad", "astucia"]
        self.fortalezas = ["fuerza", "proteina", "musculo", "testosterona"]
        self.inmunidades = ["dolor", "cansancio"]  # No siente dolor por las agujetas
        
        # Estadísticas especiales del putamo
        self._proteinas_consumidas = 0
        self._selfies_espejo = 0
        self._peso_levantado = 0  # en kg
        self._gritos_dados = 0
        self._musculo = 100  # Nivel muscular (0-100)
        
        # Frases típicas de putamo
        self._frases_putamo = [
            "¡Una más!",
            "¡Vamos, que puedes!",
            "¡Proteínas!",
            "¡No pain, no gain!",
            "¡Dale duro!",
            "¡Vamos a por todas!",
            "¡Crecimiento!",
            "¡Pump!"
        ]
        
        # Ejercicios favoritos
        self._ejercicios = [
            "press de banca",
            "sentadillas",
            "peso muerto",
            "curl de bíceps",
            "dominadas",
            "press militar",
            "fondos",
            "remo"
        ]
        
        # Suplementos
        self._suplementos = [
            "proteína de suero",
            "creatina",
            "pre-entreno",
            "BCAA",
            "glutamina",
            "termogénicos",
            "vitaminas",
            "omega-3"
        ]
        
        # Inicializar habilidades
        self.inicializar_habilidades()
    
    @classmethod
    def descripcion(cls):
        return ("El tío del gym que solo habla de proteínas. "
                "Cultor del físico y la autoestima muscular. "
                "Extremadamente fuerte pero no muy listo.")
    
    def inicializar_habilidades(self):
        """Inicializa las 6 habilidades únicas del PutoAmo."""
        self.habilidades = [
            FlexionExplosiva(),   # Habilidad 1: Flexión poderosa
            BatidoDeProteinas(),  # Habilidad 2: Batido de proteínas
            SelfieEnElEspejo(),   # Habilidad 3: Selfie muscular
            Levantamiento(),      # Habilidad 4: Levanta peso
            GritoDeGuerra(),      # Habilidad 5: Grito motivador
            RutinaExtrema()       # Habilidad 6: Rutina completa
        ]
    
    def mostrar_stats(self):
        """Muestra estadísticas con estilo putamo."""
        print(f"\n{C.NEGRITA}{C.ROJO}┌───── PUTAMO DEL GYM ─────┐{C.RESET}")
        super().mostrar_stats()
        
        # Mostrar estadísticas especiales
        print(f"\n{C.AMARILLO}┌───── ESTADÍSTICAS MUSCULARES ─────┐{C.RESET}")
        print(f"{C.CYAN}│ Proteínas consumidas: {self._proteinas_consumidas:3} │{C.RESET}")
        print(f"{C.CYAN}│ Selfies en espejo: {self._selfies_espejo:3}      │{C.RESET}")
        print(f"{C.CYAN}│ Peso levantado: {self._peso_levantado:4}kg    │{C.RESET}")
        print(f"{C.CYAN}│ Gritos dados: {self._gritos_dados:3}         │{C.RESET}")
        print(f"{C.CYAN}│ Nivel muscular: {self._musculo:3}         │{C.RESET}")
        print(f"{C.AMARILLO}└──────────────────────────────────┘{C.RESET}")
    
    def recibir_dano(self, dano: int, tipo_dano: str = "normal", critico: bool = False) -> int:
        """Recibir daño con modificadores especiales para PutoAmo."""
        # La inteligencia lo confunde
        if tipo_dano == "inteligencia":
            dano = int(dano * 1.8)
            print(f"{C.ROJO_BRILLANTE}¡NO ENTIENDE! +80% daño{C.RESET}")
            
            # Posible confusión
            if random.random() < 0.4:
                self.estados.append("confundido")
                print(f"{C.MAGENTA}¡Se confunde! Estado: confundido{C.RESET}")
        
        # El cardio lo agota
        elif tipo_dano == "cardio":
            dano = int(dano * 1.5)
            print(f"{C.ROJO}¡El cardio duele! +50% daño{C.RESET}")
            
            # Pierde energía extra
            energia_perdida = min(20, self.energia_actual)
            self.energia_actual -= energia_perdida
            print(f"{C.ROJO}¡Pierde {energia_perdida} de energía por el cardio!{C.RESET}")
        
        # Inmune al dolor
        elif tipo_dano == "dolor":
            print(f"{C.AZUL}¡No siente dolor! Inmune.{C.RESET}")
            return 0
        
        # Aumenta músculo con cada golpe (adaptación)
        self._musculo = min(150, self._musculo + 2)
        
        return super().recibir_dano(dano, tipo_dano, critico)
    
    def regenerar(self):
        """Regeneración del putamo."""
        super().regenerar()
        
        # Toma proteínas (40%)
        if random.random() < 0.4:
            self._proteinas_consumidas += 1
            suplemento = random.choice(self._suplementos)
            
            # Beneficios de las proteínas
            curacion_proteina = random.randint(10, 25)
            self.vida_actual = min(self.vida_maxima, self.vida_actual + curacion_proteina)
            self._musculo = min(150, self._musculo + 5)
            
            print(f"{C.CYAN}» Toma {suplemento}. Vida +{curacion_proteina}, Músculo +5. Proteínas: {self._proteinas_consumidas}{C.RESET}")
        
        # Se toma un selfie (25%)
        if random.random() < 0.25:
            self._selfies_espejo += 1
            
            # Sube ataque temporalmente
            self.ataque += 3
            self._musculo = min(150, self._musculo + 3)
            
            print(f"{C.MAGENTA}¡Selfie en el espejo! Ataque +3, Músculo +3. Selfies: {self._selfies_espejo}{C.RESET}")
    
    def levantar_peso(self, peso: int):
        """Levanta peso."""
        self._peso_levantado += peso
        
        # Beneficios por levantar peso
        self.ataque += 2
        self._musculo = min(150, self._musculo + 10)
        
        print(f"{C.VERDE}¡Levanta {peso}kg! Ataque +2, Músculo +10. Total: {self._peso_levantado}kg{C.RESET}")
    
    def dar_grito(self):
        """Da un grito de guerra."""
        self._gritos_dados += 1
        
        # Beneficios del grito
        self.ataque += 5
        self.velocidad += 3
        self.energia_actual = min(self.energia_maxima, self.energia_actual + 20)
        
        print(f"{C.ROJO_BRILLANTE}¡¡¡GRITO DE GUERRA!!! Ataque +5, Velocidad +3, Energía +20. Gritos: {self._gritos_dados}{C.RESET}")