"""
Habilidades específicas del Super Sacerdote
Exorcismos, bendiciones, milagros y castigos divinos
"""

from .habilidad_base import Habilidad
from utils import Colores as C
import random
import time

class Exorcismo(Habilidad):
    """Exorcismo - Expulsa demonios y espíritus malignos"""
    
    def __init__(self):
        super().__init__(
            nombre="Exorcismo",
            descripcion="Expulsa demonios y espíritus malignos. Daño masivo a impuros.",
            costo_energia=45,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        print(f"{C.MAGENTA}¡{usuario.nombre} comienza un exorcismo!{C.RESET}")
        time.sleep(0.5)
        
        # Daño base
        dano_base = int(usuario.ataque * 1.5)
        
        # Efectivo contra demonios, segarros y pecadores
        es_impuro = any(tipo in objetivo.tipo for tipo in ["� Amego Segarro", "� Choni de Barrio", "� Guiri Turista"])
        es_demonio = "demonio" in objetivo.tipo.lower() if hasattr(objetivo, 'tipo') else False
        
        if es_impuro or es_demonio:
            dano_base = int(dano_base * 2)
            print(f"{C.ROJO_BRILLANTE}¡EXORCISMO SUPEREFECTIVO! x2 daño{C.RESET}")
            
            # Expulsión forzada (30%) - duración 1 turno
            if random.random() < 0.3:
                objetivo.aplicar_estado("exorcizado", duracion=1)
                print(f"{C.VERDE_BRILLANTE}¡{objetivo.nombre} ha sido exorcizado!{C.RESET}")
        
        # Aplicar daño
        dano = objetivo.recibir_dano(dano_base, "divino")
        
        # Registrar exorcismo
        if hasattr(usuario, '_exorcismos_realizados'):
            usuario._exorcismos_realizados += 1
        
        # Ganar fe
        if hasattr(usuario, '_fe_acumulada'):
            usuario._fe_acumulada = min(getattr(usuario, '_fe_maxima', 300), 
                                       usuario._fe_acumulada + 20)
        
        return {
            "exito": True,
            "dano": dano,
            "tipo": "divino",
            "exorcismo": True,
            "mensaje": f"Exorciza a {objetivo.nombre}"
        }

class BendicionDivina(Habilidad):
    """Bendición Divina - Bendice y cura aliados"""
    
    def __init__(self):
        super().__init__(
            nombre="Bendición Divina",
            descripcion="Bendice y cura a aliados. Aumenta defensa y cura estados.",
            costo_energia=35,
            tipo="defensiva"
        )
        self.es_curacion = True
    
    def usar(self, usuario, objetivo):
        print(f"{C.AZUL}¡{usuario.nombre} pronuncia una bendición divina!{C.RESET}")
        time.sleep(0.5)
        
        # Curación poderosa
        curacion = usuario.vida_maxima // 3
        vida_curada = objetivo.recibir_curacion(curacion)
        
        # Aumenta defensa - duración 2 turnos
        aumento_defensa = max(4, objetivo.defensa // 4)
        objetivo.defensa += aumento_defensa
        
        # Cura estados negativos
        estados_curables = ["quemado", "envenenado", "maldito", "poseído"]
        estados_eliminados = []
        
        for estado in estados_curables:
            if estado in objetivo.estados:
                objetivo.eliminar_estado(estado)
                estados_eliminados.append(estado)
        
        print(f"{C.VERDE}¡Bendición! Defensa +{aumento_defensa}{C.RESET}")
        
        if estados_eliminados:
            print(f"{C.VERDE}Estados curados: {', '.join(estados_eliminados)}{C.RESET}")
        
        # Ganar fe
        if hasattr(usuario, '_fe_acumulada'):
            usuario._fe_acumulada = min(getattr(usuario, '_fe_maxima', 300), 
                                       usuario._fe_acumulada + 15)
        
        return {
            "exito": True,
            "curacion": vida_curada,
            "defensa_aumentada": aumento_defensa,
            "estados_eliminados": estados_eliminados,
            "tipo": "defensiva",
            "mensaje": f"Bendición divina cura a {objetivo.nombre}"
        }

class AguaBenditaAvanzada(Habilidad):
    """Agua Bendita Avanzada - Agua bendita potenciada por la fe"""
    
    def __init__(self):
        super().__init__(
            nombre="Agua Bendita Avanzada",
            descripcion="Agua bendita potenciada por la fe. Purifica y daña.",
            costo_energia=30,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        print(f"{C.CYAN}¡{usuario.nombre} lanza agua bendita avanzada!{C.RESET}")
        time.sleep(0.5)
        
        # Daño base aumentado por fe
        dano_base = usuario.ataque
        
        if hasattr(usuario, '_fe_acumulada'):
            bonus_fe = 1 + (usuario._fe_acumulada / 200)  # Hasta 50% extra
            dano_base = int(dano_base * bonus_fe)
            print(f"{C.VERDE}¡Potenciado por la fe! +{int((bonus_fe-1)*100)}%{C.RESET}")
        
        # Super efectivo contra impuros
        if "impuro" in objetivo.tipo.lower() or "Segarro" in objetivo.tipo:
            dano_base *= 2
            print(f"{C.ROJO}¡Purificación total! x2 daño{C.RESET}")
        
        dano = objetivo.recibir_dano(dano_base, "divino")
        
        # Purifica estados - duración 2 turnos
        if random.random() < 0.5:
            objetivo.aplicar_estado("purificado", duracion=2)
            print(f"{C.VERDE}¡{objetivo.nombre} ha sido purificado!{C.RESET}")
        
        return {
            "exito": True,
            "dano": dano,
            "tipo": "divino",
            "purificado": True,
            "mensaje": f"Agua bendita avanzada purifica a {objetivo.nombre}"
        }

class SermonEterno(Habilidad):
    """Sermón Eterno - Sermón tan largo que cansa al enemigo"""
    
    def __init__(self):
        super().__init__(
            nombre="Sermón Eterno",
            descripcion="Sermón tan largo que cansa al enemigo. Reduce velocidad y ataque.",
            costo_energia=25,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        print(f"{C.MAGENTA}¡{usuario.nombre} comienza un sermón eterno...{C.RESET}")
        time.sleep(1)
        
        # Reducciones - duración 2 turnos
        reduccion_velocidad = max(10, objetivo.velocidad // 3)
        reduccion_ataque = max(5, objetivo.ataque // 4)
        
        objetivo.velocidad = max(5, objetivo.velocidad - reduccion_velocidad)
        objetivo.ataque = max(5, objetivo.ataque - reduccion_ataque)
        
        # Posible sueño (40%) - duración 1-2 turnos
        if random.random() < 0.4:
            duracion = random.randint(1, 2)
            objetivo.aplicar_estado("dormido", duracion=duracion)
            print(f"{C.CYAN}¡{objetivo.nombre} se ha dormido por {duracion} turno(s)!{C.RESET}")
        
        print(f"{C.AMARILLO}Velocidad -{reduccion_velocidad}, Ataque -{reduccion_ataque}{C.RESET}")
        
        return {
            "exito": True,
            "velocidad_reducida": reduccion_velocidad,
            "ataque_reducido": reduccion_ataque,
            "tipo": "estado",
            "mensaje": f"Sermón eterno agota a {objetivo.nombre}"
        }

class MilagroDivino(Habilidad):
    """Milagro Divino - Realiza un milagro con efectos aleatorios"""
    
    def __init__(self):
        super().__init__(
            nombre="Milagro Divino",
            descripcion="Realiza un milagro. Efectos aleatorios potentes.",
            costo_energia=60,
            tipo="especial"
        )
        self.es_curacion = True
    
    def usar(self, usuario, objetivo):
        print(f"{C.VERDE_BRILLANTE}¡{usuario.nombre} invoca un milagro divino!{C.RESET}")
        time.sleep(1)
        
        milagros = [
            self._milagro_curacion,
            self._milagro_dano,
            self._milagro_resurreccion,
            self._milagro_bendicion,
            self._milagro_castigo,
            self._milagro_transfiguracion
        ]
        
        milagro = random.choice(milagros)
        return milagro(usuario, objetivo)
    
    def _milagro_curacion(self, usuario, objetivo):
        curacion = usuario.vida_maxima // 2
        vida_curada = usuario.recibir_curacion(curacion)
        estados_antes = usuario.estados.copy()
        usuario.estados = [estado for estado in usuario.estados if estado not in ["quemado", "envenenado", "maldito"]]
        print(f"{C.VERDE_BRILLANTE}¡MILAGRO DE CURACI�N! Vida +{vida_curada}{C.RESET}")
        if hasattr(usuario, '_milagros_realizados'):
            usuario._milagros_realizados += 1
        return {"exito": True, "milagro": "curacion", "curacion": vida_curada, "estados_eliminados": estados_antes, "mensaje": "Milagro de curación realizado"}
    
    def _milagro_dano(self, usuario, objetivo):
        dano = objetivo.vida_maxima // 3
        dano_recibido = objetivo.recibir_dano(dano, "divino")
        print(f"{C.ROJO_BRILLANTE}¡MILAGRO DE DESTRUCCI�N! Daño: {dano_recibido}{C.RESET}")
        return {"exito": True, "milagro": "dano", "dano": dano_recibido, "mensaje": "Milagro de destrucción realizado"}
    
    def _milagro_resurreccion(self, usuario, objetivo):
        if not usuario.esta_vivo():
            usuario.vida_actual = usuario.vida_maxima // 2
            print(f"{C.VERDE_BRILLANTE}¡RESURRECCI�N MILAGROSA! Revive con mitad de vida.{C.RESET}")
        if random.random() < 0.5:
            curacion = objetivo.vida_maxima // 4
            vida_curada = objetivo.recibir_curacion(curacion)
        return {"exito": True, "milagro": "resurreccion", "resucitado": not usuario.esta_vivo(), "mensaje": "Milagro de resurrección"}
    
    def _milagro_bendicion(self, usuario, objetivo):
        aum_atk = max(5, usuario.ataque // 3)
        aum_def = max(4, usuario.defensa // 3)
        aum_vel = max(3, usuario.velocidad // 6)
        usuario.ataque += aum_atk
        usuario.defensa += aum_def
        usuario.velocidad += aum_vel
        print(f"{C.AZUL}¡MILAGRO DE BENDICI�N! Stats mejoradas.{C.RESET}")
        return {"exito": True, "milagro": "bendicion", "ataque_mejorado": 20, "defensa_mejorada": 15, "velocidad_mejorada": 10, "mensaje": "Bendición potenciada aplicada"}
    
    def _milagro_castigo(self, usuario, objetivo):
        objetivo.ataque = max(1, objetivo.ataque // 2)
        objetivo.defensa = max(1, objetivo.defensa // 2)
        objetivo.velocidad = max(1, objetivo.velocidad // 2)
        print(f"{C.ROJO}¡MILAGRO DE CASTIGO! Todas las stats del enemigo reducidas a la mitad.{C.RESET}")
        return {"exito": True, "milagro": "castigo", "mensaje": "Castigo divino aplicado"}
    
    def _milagro_transfiguracion(self, usuario, objetivo):
        objetivo.aplicar_estado("transfigurado", duracion=2)
        if random.random() < 0.33:
            objetivo.aplicar_estado("sin_habilidades", duracion=2)
            print(f"{C.MAGENTA}¡TRANSFIGURACI�N! {objetivo.nombre} pierde temporalmente sus habilidades.{C.RESET}")
        return {"exito": True, "milagro": "transfiguracion", "mensaje": "Transfiguración divina realizada"}

class CastigoDivino(Habilidad):
    """Castigo Divino - Castigo de Dios sobre los pecadores (BALANCEADO)"""
    
    def __init__(self):
        super().__init__(
            nombre="Castigo Divino",
            descripcion="Castigo de Dios sobre los pecadores. Daño masivo y efectos duraderos.",
            costo_energia=70,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        print(f"{C.ROJO_BRILLANTE}¡{usuario.nombre} invoca el CASTIGO DIVINO!{C.RESET}")
        time.sleep(0.5)
        
        # Daño masivo reducido de *3 a *2.2
        dano_base = int(usuario.ataque * 2.2)
        
        # Extra contra pecadores (reducido de *2 a *1.5)
        es_pecador = any(tipo in objetivo.tipo for tipo in ["� Amego Segarro", "� Choni de Barrio", "� Político Prometedor"])
        if es_pecador:
            dano_base = int(dano_base * 1.5)
            print(f"{C.ROJO_BRILLANTE}¡PECADOR DETECTADO! +50% daño{C.RESET}")
        
        dano = objetivo.recibir_dano(dano_base, "divino")
        
        # Efectos secundarios - menos probables y de menor duración
        efectos = ["maldito", "paralizado", "confundido", "debilitado"]
        for efecto in efectos:
            if random.random() < 0.2:  # antes 0.3
                objetivo.aplicar_estado(efecto, duracion=1)  # antes 2
        
        # Reducción permanente de stats (menos probable y menos severa)
        if random.random() < 0.05:  # antes 0.1
            objetivo.ataque = max(1, objetivo.ataque - max(2, objetivo.ataque // 8))
            objetivo.defensa = max(1, objetivo.defensa - max(1, objetivo.defensa // 8))
            print(f"{C.ROJO}¡Reducción permanente leve de stats!{C.RESET}")
        
        return {
            "exito": True,
            "dano": dano,
            "tipo": "divino",
            "castigo": True,
            "mensaje": f"{usuario.nombre} invoca el CASTIGO DIVINO contra {objetivo.nombre}!"
        }