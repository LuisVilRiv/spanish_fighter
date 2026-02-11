"""
Habilidades específicas del Guiri Turista
Cada habilidad refleja la confusión, torpeza y suerte del turista perdido.
"""

from .habilidad_base import Habilidad
from utils import Colores as C
import random

class PedirDirecciones(Habilidad):
    """Pedir Direcciones - Pide direcciones a alguien"""
    
    def __init__(self):
        super().__init__(
            nombre="Pedir Direcciones",
            descripcion="Pide direcciones a alguien. Puede obtener ayuda o ser ignorado.",
            costo_energia=15,
            tipo="especial"
        )
        self.es_curacion = False  # Depende del resultado
    
    def usar(self, usuario, objetivo):
        # Resultado aleatorio
        resultados = [
            self._direcciones_correctas,
            self._direcciones_equivocadas,
            self._ignorado,
            self._ayuda_extrema,
            self._robo
        ]
        
        resultado = random.choice(resultados)
        return resultado(usuario, objetivo)
    
    def _direcciones_correctas(self, usuario, objetivo):
        """Obtiene direcciones correctas"""
        # Curación y energía (encontró el camino)
        curacion = 20
        energia = 25
        
        vida_curada = usuario.recibir_curacion(curacion)
        usuario.energia_actual = min(usuario.energia_maxima, usuario.energia_actual + energia)
        
        print(f"{C.VERDE}¡Alguien le da direcciones correctas! Vida +{vida_curada}, Energía +{energia}{C.RESET}")
        return {"exito": True, "resultado": "direcciones_correctas", "curacion": vida_curada, "energia": energia}
    
    def _direcciones_equivocadas(self, usuario, objetivo):
        """Le dan direcciones equivocadas"""
        # Daño a sí mismo (se pierde más)
        daño = usuario.vida_maxima // 10
        usuario.recibir_dano(daño, "perdido")
        
        # Pierde energía
        perdida_energia = min(15, usuario.energia_actual)
        usuario.energia_actual -= perdida_energia
        
        print(f"{C.ROJO}¡Le dan direcciones equivocadas! Vida -{daño}, Energía -{perdida_energia}{C.RESET}")
        return {"exito": True, "resultado": "direcciones_equivocadas", "daño": daño, "energia_perdida": perdida_energia}
    
    def _ignorado(self, usuario, objetivo):
        """Es ignorado"""
        print(f"{C.AMARILLO}Nadie le hace caso. No pasa nada.{C.RESET}")
        return {"exito": True, "resultado": "ignorado"}
    
    def _ayuda_extrema(self, usuario, objetivo):
        """Recibe ayuda extrema"""
        # Gran curación
        curacion = usuario.vida_maxima // 2
        vida_curada = usuario.recibir_curacion(curacion)
        
        # Aumenta suerte
        if hasattr(usuario, '_suerte'):
            usuario._suerte = min(0.5, usuario._suerte + 0.1)
        
        # Dinero encontrado
        if hasattr(usuario, '_dinero_gastado'):
            usuario._dinero_gastado -= 50  # Encuentra dinero
        
        print(f"{C.VERDE_BRILLANTE}¡Un buen samaritano le ayuda enormemente! Vida +{vida_curada}, Suerte +10%, Dinero encontrado{C.RESET}")
        return {"exito": True, "resultado": "ayuda_extrema", "curacion": vida_curada, "suerte_aumentada": 0.1}
    
    def _robo(self, usuario, objetivo):
        """Lo roban"""
        # Daño significativo
        daño = usuario.vida_maxima // 4
        usuario.recibir_dano(daño, "robo")
        
        # Pierde mucha energía (dinero)
        perdida_energia = min(40, usuario.energia_actual)
        usuario.energia_actual -= perdida_energia
        
        # Pierde dinero
        if hasattr(usuario, '_dinero_gastado'):
            usuario._dinero_gastado += 100
        
        print(f"{C.ROJO_BRILLANTE}¡LO ROBAN! Vida -{daño}, Energía -{perdida_energia}, Dinero perdido{C.RESET}")
        return {"exito": True, "resultado": "robo", "daño": daño, "energia_perdida": perdida_energia}

class FotoTuristica(Habilidad):
    """Foto Turística - Toma una foto turística"""
    
    def __init__(self):
        super().__init__(
            nombre="Foto Turística",
            descripcion="Toma una foto turística. Aumenta suerte y puede cegar.",
            costo_energia=20,
            tipo="defensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Aumenta suerte
        if hasattr(usuario, '_suerte'):
            usuario._suerte = min(0.5, usuario._suerte + 0.05)
        
        # Registrar foto
        if hasattr(usuario, '_fotos_tomadas'):
            usuario._fotos_tomadas += 1
        
        # Posible cegamiento por flash (20%) - duración 1 turno
        if random.random() < 0.2:
            objetivo.aplicar_estado("cegado", duracion=1)
            print(f"{C.ROJO}¡Flash! Cegado.{C.RESET}")
        
        # Sujeto fotografiado aleatorio
        sujetos = ["un monumento", "una paloma", "su comida", "un local extraño", "su propio reflejo"]
        sujeto = random.choice(sujetos)
        
        print(f"{C.CYAN}¡Foto de {sujeto}! Suerte +5%. Fotos: {getattr(usuario, '_fotos_tomadas', 0)}{C.RESET}")
        
        return {"exito": True, "suerte_aumentada": 0.05, "sujeto": sujeto}

class ComprarSouvenir(Habilidad):
    """Comprar Souvenir - Compra un souvenir inútil"""
    
    def __init__(self):
        super().__init__(
            nombre="Comprar Souvenir",
            descripcion="Compra un souvenir inútil. Gasta dinero pero obtiene efectos aleatorios.",
            costo_energia=25,
            tipo="especial"
        )
        self.es_curacion = False  # Depende del souvenir
    
    def usar(self, usuario, objetivo):
        # Gasta dinero
        costo = random.randint(10, 30)
        if hasattr(usuario, '_dinero_gastado'):
            usuario._dinero_gastado += costo
        
        # Efecto aleatorio del souvenir
        souvenirs = [
            self._souvenir_curativo,
            self._souvenir_ofensivo,
            self._souvenir_defensivo,
            self._souvenir_inutil,
            self._souvenir_magico
        ]
        
        souvenir = random.choice(souvenirs)
        return souvenir(usuario, objetivo, costo)
    
    def _souvenir_curativo(self, usuario, objetivo, costo):
        """Souvenir curativo"""
        curacion = 30
        vida_curada = usuario.recibir_curacion(curacion)
        
        # Registrar souvenir
        if hasattr(usuario, '_souvenirs_inutiles'):
            usuario._souvenirs_inutiles += 1
        
        print(f"{C.VERDE}¡Compra una 'piedra curativa'! Vida +{vida_curada}. Costo: {costo}€{C.RESET}")
        return {"exito": True, "souvenir": "curativo", "curacion": vida_curada, "costo": costo}
    
    def _souvenir_ofensivo(self, usuario, objetivo, costo):
        """Souvenir ofensivo"""
        daño = objetivo.recibir_dano(25, "souvenir")
        
        # Registrar souvenir
        if hasattr(usuario, '_souvenirs_inutiles'):
            usuario._souvenirs_inutiles += 1
        
        print(f"{C.ROJO}¡Compra una 'figura de toro enfadado'! Daño: {daño}. Costo: {costo}€{C.RESET}")
        return {"exito": True, "souvenir": "ofensivo", "daño": daño, "costo": costo}
    
    def _souvenir_defensivo(self, usuario, objetivo, costo):
        """Souvenir defensivo - duración 2 turnos"""
        usuario.defensa += 15
        
        # Registrar souvenir
        if hasattr(usuario, '_souvenirs_inutiles'):
            usuario._souvenirs_inutiles += 1
        
        print(f"{C.AZUL}¡Compra un 'pañuelo protector'! Defensa +15. Costo: {costo}€{C.RESET}")
        return {"exito": True, "souvenir": "defensivo", "defensa_aumentada": 15, "costo": costo}
    
    def _souvenir_inutil(self, usuario, objetivo, costo):
        """Souvenir completamente inútil"""
        # Registrar souvenir
        if hasattr(usuario, '_souvenirs_inutiles'):
            usuario._souvenirs_inutiles += 1
        
        objetos = ["imán feo", "llavero roto", "postal mojada", "figura de plástico"]
        objeto = random.choice(objetos)
        
        print(f"{C.AMARILLO}¡Compra un {objeto} completamente inútil! Costo: {costo}€{C.RESET}")
        return {"exito": True, "souvenir": "inutil", "objeto": objeto, "costo": costo}
    
    def _souvenir_magico(self, usuario, objetivo, costo):
        """Souvenir mágico (raro)"""
        # Efecto aleatorio potente
        if random.random() < 0.5:
            # Efecto positivo
            usuario.vida_actual = usuario.vida_maxima
            print(f"{C.VERDE_BRILLANTE}¡Compra un 'amuleto de la suerte'! Curación completa. Costo: {costo}€{C.RESET}")
            efecto = "curacion_completa"
        else:
            # Efecto negativo
            usuario.recibir_dano(usuario.vida_maxima // 3, "souvenir_maldito")
            print(f"{C.ROJO_BRILLANTE}¡Compra un 'ídolo maldito'! Daño masivo. Costo: {costo}€{C.RESET}")
            efecto = "daño_masivo"
        
        # Registrar souvenir
        if hasattr(usuario, '_souvenirs_inutiles'):
            usuario._souvenirs_inutiles += 1
        
        return {"exito": True, "souvenir": "magico", "efecto": efecto, "costo": costo}

class Perderse(Habilidad):
    """Perderse - Se pierde (de nuevo)"""
    
    def __init__(self):
        super().__init__(
            nombre="Perderse",
            descripcion="Se pierde (de nuevo). Efectos aleatorios de perderse.",
            costo_energia=0,  # No cuesta, es algo que le pasa
            tipo="especial"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Registrar que se perdió
        if hasattr(usuario, '_veces_perdido'):
            usuario._veces_perdido += 1
        
        # Resultados aleatorios de perderse
        resultados = [
            self._perderse_en_lugar_bueno,
            self._perderse_en_lugar_malo,
            self._perderse_y_encontrar_dinero,
            self._perderse_y_sufrir_daño,
            self._perderse_y_encontrar_atajo
        ]
        
        resultado = random.choice(resultados)
        return resultado(usuario, objetivo)
    
    def _perderse_en_lugar_bueno(self, usuario, objetivo):
        """Se pierde en un lugar bueno"""
        curacion = 25
        vida_curada = usuario.recibir_curacion(curacion)
        
        lugar = random.choice(["un parque bonito", "un mirador", "una tienda de chuches", "un bar con wifi gratis"])
        
        print(f"{C.VERDE}¡Se pierde en {lugar}! Vida +{vida_curada}. Veces perdido: {getattr(usuario, '_veces_perdido', 0)}{C.RESET}")
        return {"exito": True, "resultado": "lugar_bueno", "curacion": vida_curada, "lugar": lugar}
    
    def _perderse_en_lugar_malo(self, usuario, objetivo):
        """Se pierde en un lugar malo"""
        daño = 20
        usuario.recibir_dano(daño, "perdido")
        
        lugar = random.choice(["un callejón oscuro", "una obra", "un barrio peligroso", "el metro equivocado"])
        
        print(f"{C.ROJO}¡Se pierde en {lugar}! Vida -{daño}. Veces perdido: {getattr(usuario, '_veces_perdido', 0)}{C.RESET}")
        return {"exito": True, "resultado": "lugar_malo", "daño": daño, "lugar": lugar}
    
    def _perderse_y_encontrar_dinero(self, usuario, objetivo):
        """Se pierde pero encuentra dinero"""
        dinero = random.randint(5, 20)
        if hasattr(usuario, '_dinero_gastado'):
            usuario._dinero_gastado -= dinero  # Encuentra dinero
        
        print(f"{C.AMARILLO}¡Se pierde pero encuentra {dinero}€ en el suelo! Veces perdido: {getattr(usuario, '_veces_perdido', 0)}{C.RESET}")
        return {"exito": True, "resultado": "encontrar_dinero", "dinero": dinero}
    
    def _perderse_y_sufrir_daño(self, usuario, objetivo):
        """Se pierde y sufre daño"""
        daño = usuario.vida_maxima // 5
        usuario.recibir_dano(daño, "perdido")
        
        # También pierde energía
        perdida_energia = min(25, usuario.energia_actual)
        usuario.energia_actual -= perdida_energia
        
        print(f"{C.ROJO}¡Se pierde gravemente! Vida -{daño}, Energía -{perdida_energia}. Veces perdido: {getattr(usuario, '_veces_perdido', 0)}{C.RESET}")
        return {"exito": True, "resultado": "sufrir_daño", "daño": daño, "energia_perdida": perdida_energia}
    
    def _perderse_y_encontrar_atajo(self, usuario, objetivo):
        """Se pierde pero encuentra un atajo"""
        # Recupera energía por el atajo
        energia = 30
        usuario.energia_actual = min(usuario.energia_maxima, usuario.energia_actual + energia)
        
        # Aumenta velocidad temporalmente - duración 1 turno
        usuario.velocidad += 10
        
        print(f"{C.VERDE}¡Se pierde pero encuentra un atajo! Energía +{energia}, Velocidad +10. Veces perdido: {getattr(usuario, '_veces_perdido', 0)}{C.RESET}")
        return {"exito": True, "resultado": "encontrar_atajo", "energia_recuperada": energia, "velocidad_aumentada": 10}

class HablarInglesAlto(Habilidad):
    """Hablar Inglés Alto - Habla inglés muy alto para hacerse entender"""
    
    def __init__(self):
        super().__init__(
            nombre="Hablar Inglés Alto",
            descripcion="Habla inglés muy alto para hacerse entender. Aturde y confunde.",
            costo_energia=30,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Aturdimiento (alta probabilidad) - duración 1 turno
        if random.random() < 0.8:
            objetivo.aplicar_estado("aturdido", duracion=1)
        
        # Confusión (40%) - duración 1 turno
        if random.random() < 0.4:
            objetivo.aplicar_estado("confundido", duracion=1)
        
        # Daño psicológico
        daño = objetivo.recibir_dano(usuario.ataque // 2, "psicologico")
        
        # Frase en inglés aleatoria
        frases = [
            "WHERE IS THE BEACH?",
            "HOW MUCH IS THIS?",
            "I NEED A DOCTOR!",
            "TAXI! TAXI!",
            "I LOVE SPAIN!",
            "DO YOU SPEAK ENGLISH?",
            "VERY GOOD!",
            "TOO EXPENSIVE!"
        ]
        frase = random.choice(frases)
        
        print(f"{C.MAGENTA}¡{frase}! Daño: {daño}, Aturdido y posiblemente confundido{C.RESET}")
        
        return {"exito": True, "daño": daño, "frase": frase}

class BuscarWifi(Habilidad):
    """Buscar Wifi - Busca desesperadamente wifi"""
    
    def __init__(self):
        super().__init__(
            nombre="Buscar Wifi",
            descripcion="Busca desesperadamente wifi. Puede encontrar o no.",
            costo_energia=35,
            tipo="defensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Probabilidad de encontrar wifi (60%)
        if random.random() < 0.6:
            # Encuentra wifi
            energia_recuperada = 40
            usuario.energia_actual = min(usuario.energia_maxima, usuario.energia_actual + energia_recuperada)
            
            # Posible subida de stats por felicidad - duración 1 turno
            usuario.ataque += 5
            usuario.velocidad += 5
            
            print(f"{C.VERDE}¡ENCUENTRA WIFI GRATIS! Energía +{energia_recuperada}, Ataque +5, Velocidad +5{C.RESET}")
            
            return {
                "exito": True,
                "wifi": True,
                "energia_recuperada": energia_recuperada,
                "ataque_aumentado": 5,
                "velocidad_aumentada": 5
            }
        else:
            # No encuentra wifi
            # Pierde energía por la búsqueda
            perdida = min(20, usuario.energia_actual)
            usuario.energia_actual -= perdida
            
            # Posible frustración (daño a sí mismo)
            if random.random() < 0.4:
                usuario.recibir_dano(15, "frustracion")
                print(f"{C.ROJO}¡NO ENCUENTRA WIFI! Energía -{perdida}, Vida -15 por frustración{C.RESET}")
                return {"exito": True, "wifi": False, "energia_perdida": perdida, "daño": 15}
            else:
                print(f"{C.AMARILLO}¡No encuentra wifi! Energía -{perdida}{C.RESET}")
                return {"exito": True, "wifi": False, "energia_perdida": perdida}