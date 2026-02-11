"""
Habilidades específicas del Amego Segarro.
Cada habilidad refleja la personalidad del segarro español típico.
"""

from .habilidad_base import Habilidad
from utils import Colores as C
import random

class DameCartera(Habilidad):
    """¡Dame la Cartera! - Pide dinero prestado que nunca devolverá"""
    
    def __init__(self):
        super().__init__(
            nombre="¡Dame la Cartera!",
            descripcion="Pide dinero prestado que nunca devolverá. Roba energía del enemigo.",
            costo_energia=20,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Daño base
        dano_base = usuario.ataque // 2
        
        # Más efectivo contra amigos
        if objetivo.tipo in ["🎮 Amego Segarro", "🏖️ Flaquito Playero"]:
            dano_base *= 2
            print(f"{C.ROJO}¡Se aprovecha de la confianza! x2{C.RESET}")
        
        # Aplicar daño
        daño = objetivo.recibir_dano(dano_base, "verborrea")
        
        # 30% de robar energía
        if random.random() < 0.3:
            energia_robada = min(15, objetivo.energia_actual)
            objetivo.energia_actual -= energia_robada
            usuario.energia_actual = min(usuario.energia_maxima, usuario.energia_actual + energia_robada)
            print(f"{C.AMARILLO}¡Robó {energia_robada} de energía!{C.RESET}")
        
        return {"exito": True, "daño": daño, "tipo": "verborrea"}

class PedirSigarrito(Habilidad):
    """¿Me Das un Siga? - Pide un cigarro y reduce la defensa del enemigo"""
    
    def __init__(self):
        super().__init__(
            nombre="¿Me Das un Siga?",
            descripcion="Pide un cigarro y reduce la defensa del enemigo.",
            costo_energia=15,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Reduce defensa - duración 2 turnos
        reduccion = max(5, objetivo.defensa // 4)
        objetivo.defensa = max(10, objetivo.defensa - reduccion)
        
        # Pequeño daño
        daño = objetivo.recibir_dano(usuario.ataque // 4, "verborrea")
        
        print(f"{C.AMARILLO}{objetivo.nombre} baja la guardia. Defensa -{reduccion}{C.RESET}")
        
        return {"exito": True, "daño": daño, "efecto": "defensa_reducida"}

class SuperMeca(Habilidad):
    """Super Meca del Móvil - Se pone a jugar al móvil y se cura"""
    
    def __init__(self):
        super().__init__(
            nombre="Super Meca del Móvil",
            descripcion="Se pone a jugar al móvil y se cura.",
            costo_energia=25,
            tipo="defensiva"
        )
        self.es_curacion = True
    
    def usar(self, usuario, objetivo):
        # Curación
        curacion = usuario.vida_maxima // 3
        vida_curada = usuario.recibir_curacion(curacion)
        
        # Regenera energía extra
        usuario.energia_actual = min(usuario.energia_maxima, usuario.energia_actual + 10)
        
        print(f"{C.VERDE}¡Se cura {vida_curada} HP jugando al Candy Crush!{C.RESET}")
        
        return {"exito": True, "curacion": vida_curada}

class CriticaConstructiva(Habilidad):
    """Crítica 'Constructiva' - Critica todo lo que haces mal"""
    
    def __init__(self):
        super().__init__(
            nombre="Crítica 'Constructiva'",
            descripcion="Critica todo lo que haces mal. Daño extra contra perfeccionistas.",
            costo_energia=30,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        dano_base = usuario.ataque
        
        # Daño extra si el objetivo es perfeccionista
        if objetivo.tipo in ["💪 PutoAmo del Gym", "📿 Católica Conservadora"]:
            dano_base = int(dano_base * 1.5)
            print(f"{C.ROJO}¡Le duele en el ego! +50%{C.RESET}")
        
        daño = objetivo.recibir_dano(dano_base, "verborrea")
        
        # Posible confusión (40%) - duración 1 turno
        if random.random() < 0.4:
            objetivo.aplicar_estado("confundido", duracion=1)
            print(f"{C.MAGENTA}¡{objetivo.nombre} se ha confundido!{C.RESET}")
        
        return {"exito": True, "daño": daño}

class ToPelma(Habilidad):
    """To Pelma - Te cuenta su vida aburrida por horas"""
    
    def __init__(self):
        super().__init__(
            nombre="To Pelma",
            descripcion="Te cuenta su vida aburrida por horas. Reduce velocidad y ataque.",
            costo_energia=35,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Reduce velocidad y ataque - duración 2 turnos
        objetivo.velocidad = max(10, objetivo.velocidad - 15)
        objetivo.ataque = max(10, objetivo.ataque - 10)
        
        # Daño psicológico
        daño = objetivo.recibir_dano(usuario.ataque // 3, "aburrimiento")
        
        print(f"{C.CYAN}¡{objetivo.nombre} está aburridísimo! Velocidad y ataque reducidos{C.RESET}")
        
        return {"exito": True, "daño": daño, "efecto": "estadisticas_reducidas"}

class PedirFavor(Habilidad):
    """Pedir Favor - Pide un favor imposible y obtiene efectos aleatorios"""
    
    def __init__(self):
        super().__init__(
            nombre="Pedir Favor",
            descripcion="Pide un favor imposible. Efecto aleatorio que puede ser bueno o malo.",
            costo_energia=40,
            tipo="especial"
        )
        self.es_curacion = False  # Depende del efecto
    
    def usar(self, usuario, objetivo):
        print(f"{C.MAGENTA}{usuario.nombre} pide un favor completamente imposible...{C.RESET}")
        
        # Efectos aleatorios (ruleta rusa de favores)
        efectos = [
            self._efecto_curar,
            self._efecto_danar,
            self._efecto_robar_energia,
            self._efecto_confundir,
            self._efecto_mejorar_stats,
            self._efecto_empeorar_stats,
            self._efecto_nada,
            self._efecto_critico
        ]
        
        efecto_elegido = random.choice(efectos)
        return efecto_elegido(usuario, objetivo)
    
    def _efecto_curar(self, usuario, objetivo):
        """Efecto: Se cura a sí mismo"""
        curacion = usuario.vida_maxima // 4
        vida_curada = usuario.recibir_curacion(curacion)
        
        mensaje = f"¡El favor funciona! {usuario.nombre} se cura {vida_curada}."
        print(f"{C.VERDE}{mensaje}{C.RESET}")
        
        return {"exito": True, "efecto": "curar", "curacion": vida_curada}
    
    def _efecto_danar(self, usuario, objetivo):
        """Efecto: Daña al objetivo"""
        daño = objetivo.vida_maxima // 5
        daño_recibido = objetivo.recibir_dano(daño, "verborrea")
        
        mensaje = f"¡El favor sale mal! {objetivo.nombre} pierde {daño_recibido} de vida."
        print(f"{C.ROJO}{mensaje}{C.RESET}")
        
        return {"exito": True, "efecto": "dañar", "daño": daño_recibido}
    
    def _efecto_robar_energia(self, usuario, objetivo):
        """Efecto: Roba energía"""
        energia_robada = min(30, objetivo.energia_actual)
        objetivo.energia_actual -= energia_robada
        usuario.energia_actual = min(usuario.energia_maxima, usuario.energia_actual + energia_robada)
        
        mensaje = f"¡Consigue energía! Roba {energia_robada} de {objetivo.nombre}."
        print(f"{C.AZUL}{mensaje}{C.RESET}")
        
        return {"exito": True, "efecto": "robar_energia", "energia_robada": energia_robada}
    
    def _efecto_confundir(self, usuario, objetivo):
        """Efecto: Confunde al objetivo - duración 2 turnos"""
        objetivo.aplicar_estado("confundido", duracion=2)
        
        mensaje = f"¡Confusión total! {objetivo.nombre} no sabe qué hacer."
        print(f"{C.MAGENTA}{mensaje}{C.RESET}")
        
        return {"exito": True, "efecto": "confundir", "estado_aplicado": "confundido"}
    
    def _efecto_mejorar_stats(self, usuario, objetivo):
        """Efecto: Mejora las stats del usuario - duración 2 turnos"""
        usuario.ataque += 10
        usuario.defensa += 5
        usuario.velocidad += 5
        
        mensaje = f"¡Auto-mejora! Ataque +10, Defensa +5, Velocidad +5."
        print(f"{C.VERDE}{mensaje}{C.RESET}")
        
        return {"exito": True, "efecto": "mejorar_stats"}
    
    def _efecto_empeorar_stats(self, usuario, objetivo):
        """Efecto: Empeora las stats del usuario - duración 2 turnos"""
        usuario.ataque = max(10, usuario.ataque - 5)
        usuario.defensa = max(5, usuario.defensa - 3)
        
        mensaje = f"¡Le sale el tiro por la culata! Ataque -5, Defensa -3."
        print(f"{C.ROJO}{mensaje}{C.RESET}")
        
        return {"exito": True, "efecto": "empeorar_stats"}
    
    def _efecto_nada(self, usuario, objetivo):
        """Efecto: No pasa nada"""
        mensaje = "Nadie le hace caso. No pasa nada."
        print(f"{C.AMARILLO}{mensaje}{C.RESET}")
        
        return {"exito": True, "efecto": "nada"}
    
    def _efecto_critico(self, usuario, objetivo):
        """Efecto: Daño crítico masivo"""
        daño = objetivo.vida_maxima // 3
        daño_recibido = objetivo.recibir_dano(daño, "verborrea")
        
        mensaje = f"¡FAVOR ÉPICO! {objetivo.nombre} pierde {daño_recibido} de vida."
        print(f"{C.ROJO_BRILLANTE}{mensaje}{C.RESET}")
        
        return {"exito": True, "efecto": "critico", "daño": daño_recibido}