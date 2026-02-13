"""
Eventos aleatorios para Batalla Cómica Española.
Cada evento tiene su propia lógica WTF y efectos en el combate.
"""

import random
from utils import Colores as C

class EventoBase:
    """Clase base para todos los eventos aleatorios."""
    
    def __init__(self, nombre, descripcion, tipo):
        """
        Inicializa un evento.
        
        Args:
            nombre: Nombre del evento
            descripcion: Descripción del evento
            tipo: 'normal', 'raro', 'ultra_raro'
        """
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo = tipo
    
    def activar(self, jugador, enemigo, turno_actual):
        """
        Activa el evento. Debe ser implementado por cada subclase.
        
        Args:
            jugador: Personaje controlado por el jugador
            enemigo: Personaje controlado por la IA
            turno_actual: Número de turno actual
            
        Returns:
            dict: Resultado del evento con mensajes y efectos
        """
        raise NotImplementedError("Cada evento debe implementar activar()")
    
    def __str__(self):
        return f"{self.nombre} ({self.tipo}): {self.descripcion}"


# ============================================================================
# EVENTOS NORMALES (70% de probabilidad cuando ocurre un evento)
# ============================================================================

class JamonVolador(EventoBase):
    """Jamón Volador - Un jamón ibérico vuela y golpea a alguien."""
    
    def __init__(self):
        super().__init__(
            nombre="🍖 JAMÓN VOLADOR",
            descripcion="Un jamón ibérico vuela y golpea a alguien. Doble daño a segarros.",
            tipo="normal"
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        # Elige un objetivo aleatorio (50/50)
        objetivo = random.choice([jugador, enemigo])
        lanzador = jugador if objetivo == enemigo else enemigo
        
        # Daño base
        daño_base = 25
        
        # Doble daño si es un segarro (alergia al jamón)
        if "Segarro" in objetivo.tipo:
            daño_base *= 2
            mensaje_daño = f"{C.ROJO}¡ALERGIA AL JAMÓN CONFIRMADA! x2 daño{C.RESET}"
        else:
            mensaje_daño = f"{C.ROJO}¡Jamón ibérico directo!{C.RESET}"
        
        # Aplicar daño
        daño_recibido = objetivo.recibir_dano(daño_base, "jamón")
        
        # Mensaje final
        mensaje = (f"{C.AMARILLO}¡JAMÓN VOLADOR!{C.RESET}\n"
                  f"Un jamón ibérico sale volando de la nada y golpea a {objetivo.nombre}.\n"
                  f"{mensaje_daño}\n"
                  f"{objetivo.nombre} recibe {daño_recibido} de daño.")
        
        return {
            "exito": True,
            "mensaje": mensaje,
            "daño": daño_recibido,
            "objetivo": objetivo.nombre,
            "tipo": "daño"
        }


class AbuelaAparece(EventoBase):
    """Abuela Aparece - Sale una abuela de la nada."""
    
    def __init__(self):
        super().__init__(
            nombre="👵 ABUELA APARECE",
            descripcion="Sale una abuela de la nada. Puede curar o dar un capón.",
            tipo="normal"
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        # Decide qué hace la abuela (50/50)
        accion = random.choice(["curar", "capón"])
        
        # Elige un objetivo aleatorio
        objetivo = random.choice([jugador, enemigo])
        
        if accion == "curar":
            # Curación
            curacion = 30
            vida_curada = objetivo.recibir_curacion(curacion)
            
            mensaje = (f"{C.VERDE}¡ABUELA APARECE!{C.RESET}\n"
                      f"Sale una abuela de la nada y le dice a {objetivo.nombre}: '¡Come, hijo!'\n"
                      f"{objetivo.nombre} recupera {vida_curada} de vida.")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "curacion": vida_curada,
                "objetivo": objetivo.nombre,
                "tipo": "curacion"
            }
        else:
            # Capón (daño)
            daño = 15
            daño_recibido = objetivo.recibir_dano(daño, "capón")
            
            mensaje = (f"{C.ROJO}¡ABUELA APARECE!{C.RESET}\n"
                      f"Sale una abuela de la nada y le da un capón a {objetivo.nombre}.\n"
                      f"{objetivo.nombre} recibe {daño_recibido} de daño.")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "daño": daño_recibido,
                "objetivo": objetivo.nombre,
                "tipo": "daño"
            }


class OleImprovisado(EventoBase):
    """Olé Improvisado - El público empieza a animar a alguien."""
    
    def __init__(self):
        super().__init__(
            nombre="👏 OLÉ IMPROVISADO",
            descripcion="El público empieza a animar a alguien. Aumenta sus estadísticas.",
            tipo="normal"
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        # Elige un objetivo aleatorio (60% jugador, 40% enemigo - favoritismo español)
        objetivo = jugador if random.random() < 0.6 else enemigo
        
        # Aumentos de estadísticas - duración 2 turnos
        aumento_ataque = 10
        aumento_defensa = 8
        aumento_velocidad = 5
        
        objetivo.ataque += aumento_ataque
        objetivo.defensa += aumento_defensa
        objetivo.velocidad += aumento_velocidad
        
        # También recupera energía
        energia_recuperada = 20
        objetivo.energia_actual = min(objetivo.energia_maxima, objetivo.energia_actual + energia_recuperada)
        
        mensaje = (f"{C.VERDE}¡OLÉ IMPROVISADO!{C.RESET}\n"
                  f"El público empieza a animar a {objetivo.nombre}.\n"
                  f"¡{objetivo.nombre} se motiva!\n"
                  f"Ataque +{aumento_ataque}, Defensa +{aumento_defensa}, Velocidad +{aumento_velocidad}, Energía +{energia_recuperada}")
        
        return {
            "exito": True,
            "mensaje": mensaje,
            "objetivo": objetivo.nombre,
            "bonus_ataque": aumento_ataque,
            "bonus_defensa": aumento_defensa,
            "bonus_velocidad": aumento_velocidad,
            "energia_recuperada": energia_recuperada,
            "tipo": "bonus"
        }


class BotellonSorpresa(EventoBase):
    """Botellón Sorpresa - Encuentras un botellón."""
    
    def __init__(self):
        super().__init__(
            nombre="🍺 BOTELLÓN SORPRESA",
            descripcion="Encuentras un botellón. Puede ser cerveza caducada o kalimotxo mágico.",
            tipo="normal"
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        # Decide qué hay en el botellón (50/50)
        contenido = random.choice(["cerveza_caducada", "kalimotxo_magico"])
        
        # Elige un objetivo aleatorio
        objetivo = random.choice([jugador, enemigo])
        
        if contenido == "cerveza_caducada":
            # Daño
            daño = 20
            daño_recibido = objetivo.recibir_dano(daño, "cerveza_caducada")
            
            # Posible estado de enfermedad (30%) - duración 2 turnos
            if random.random() < 0.3:
                objetivo.aplicar_estado("enfermo", duracion=2)
                estado_mensaje = f" y se pone enfermo"
            else:
                estado_mensaje = ""
            
            mensaje = (f"{C.ROJO}¡BOTELLÓN SORPRESA!{C.RESET}\n"
                      f"{objetivo.nombre} encuentra un botellón... ¡es cerveza caducada!\n"
                      f"{objetivo.nombre} recibe {daño_recibido} de daño{estado_mensaje}.")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "daño": daño_recibido,
                "contenido": "cerveza_caducada",
                "objetivo": objetivo.nombre,
                "tipo": "daño"
            }
        else:
            # Curación y bonus
            curacion = 25
            vida_curada = objetivo.recibir_curacion(curacion)
            
            # Bonus de energía
            energia_extra = 30
            objetivo.energia_actual = min(objetivo.energia_maxima, objetivo.energia_actual + energia_extra)
            
            # Bonus de ataque - duración 2 turnos
            objetivo.ataque += 5
            
            mensaje = (f"{C.VERDE}¡BOTELLÓN SORPRESA!{C.RESET}\n"
                      f"{objetivo.nombre} encuentra un botellón... ¡es KALIMOTXO MÁGICO!\n"
                      f"{objetivo.nombre} recupera {vida_curada} de vida, +{energia_extra} de energía y +5 de ataque.")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "curacion": vida_curada,
                "energia_extra": energia_extra,
                "ataque_extra": 5,
                "contenido": "kalimotxo_magico",
                "objetivo": objetivo.nombre,
                "tipo": "curacion"
            }


class TuristasDespistados(EventoBase):
    """Turistas Despistados - Un grupo de turistas te pide direcciones."""
    
    def __init__(self):
        super().__init__(
            nombre="🧳 TURISTAS DESPISTADOS",
            descripcion="Un grupo de turistas te pide direcciones. Pueden darte propina o enfadarse.",
            tipo="normal"
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        # Decide si ayudar o mandar a la mierda (60/40)
        accion = "ayudar" if random.random() < 0.6 else "mandar"
        
        # Siempre afecta al jugador (él es al que preguntan)
        objetivo = jugador
        
        if accion == "ayudar":
            # Ayuda bien - propina
            propina = random.randint(10, 30)
            
            # Bonus de energía (dinero)
            objetivo.energia_actual = min(objetivo.energia_maxima, objetivo.energia_actual + propina)
            
            # Posible souvenir (20%)
            if random.random() < 0.2:
                souvenir = random.choice(["imán", "llavero", "postal"])
                mensaje_souvenir = f" y un {souvenir} de recuerdo"
                tiene_souvenir = True
            else:
                mensaje_souvenir = ""
                tiene_souvenir = False
            
            mensaje = (f"{C.VERDE}¡TURISTAS DESPISTADOS!{C.RESET}\n"
                      f"Un grupo de turistas te pide direcciones y les ayudas amablemente.\n"
                      f"Te dan una propina de {propina} de energía{mensaje_souvenir}.")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "energia_ganada": propina,
                "tiene_souvenir": tiene_souvenir,
                "accion": "ayudar",
                "tipo": "beneficio"
            }
        else:
            # Manda a la mierda - se enfadan
            daño = 15
            daño_recibido = objetivo.recibir_dano(daño, "enfado_turistas")
            
            # También reduce energía (te roban)
            energia_perdida = min(20, objetivo.energia_actual)
            objetivo.energia_actual -= energia_perdida
            
            mensaje = (f"{C.ROJO}¡TURISTAS DESPISTADOS!{C.RESET}\n"
                      f"Un grupo de turistas te pide direcciones y les mandas a la mierda.\n"
                      f"Se enfadan y te atacan.\n"
                      f"Recibes {daño_recibido} de daño y pierdes {energia_perdida} de energía.")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "daño": daño_recibido,
                "energia_perdida": energia_perdida,
                "accion": "mandar",
                "tipo": "daño"
            }


# ============================================================================
# EVENTOS RAROS (25% de probabilidad cuando ocurre un evento)
# ============================================================================

class SiestaRepentina(EventoBase):
    """Siesta Repentina - A alguien le entra un sueño de la hostia."""
    
    def __init__(self):
        super().__init__(
            nombre="😴 SIESTA REPENTINA",
            descripcion="A alguien le entra un sueño de la hostia. Duerme 1-3 turnos pero se cura.",
            tipo="raro"
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        # Elige un objetivo aleatorio
        objetivo = random.choice([jugador, enemigo])
        
        # Duración de la siesta (1-3 turnos)
        duracion = random.randint(1, 3)
        
        # Aplica estado dormido
        objetivo.aplicar_estado("dormido", duracion=duracion)
        
        # Curación por la siesta
        curacion = 40
        vida_curada = objetivo.recibir_curacion(curacion)
        
        mensaje = (f"{C.CYAN}¡SIESTA REPENTINA!{C.RESET}\n"
                  f"A {objetivo.nombre} le entra un sueño de la hostia en medio del combate.\n"
                  f"Se echa una siesta de {duracion} turno{'s' if duracion > 1 else ''} y recupera {vida_curada} de vida.\n"
                  f"¡{objetivo.nombre} está DORMIDO!")
        
        return {
            "exito": True,
            "mensaje": mensaje,
            "duracion_siesta": duracion,
            "curacion": vida_curada,
            "objetivo": objetivo.nombre,
            "tipo": "estado"
        }


class ConcursoDeTapas(EventoBase):
    """Concurso de Tapas - Empieza un concurso improvisado de tapas."""
    
    def __init__(self):
        super().__init__(
            nombre="🍽️ CONCURSO DE TAPAS",
            descripcion="Empieza un concurso improvisado de tapas. El jurado decide si tu tapa está buena.",
            tipo="raro"
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        # Elige quién presenta la tapa (50/50)
        participante = random.choice([jugador, enemigo])
        
        # El jurado (un gato, una vecina y un borracho)
        jurado = ["🐱 un gato", "👵 una vecina", "🍺 un borracho"]
        
        # Cada miembro del jurado vota (33% de que a cada uno le guste)
        votos = []
        for j in jurado:
            if random.random() < 0.33:
                votos.append(True)  # Le gusta
            else:
                votos.append(False)  # No le gusta
        
        # Cuenta votos
        votos_positivos = sum(votos)
        
        # Tapa presentada (aleatoria)
        tapas = [
            "tortilla de patatas",
            "croquetas de jamón",
            "patatas bravas",
            "calamares a la romana",
            "pulpo a la gallega",
            "gambas al ajillo",
            "albóndigas en salsa",
            "chorizo a la sidra"
        ]
        tapa = random.choice(tapas)
        
        if votos_positivos >= 2:  # Mayoría
            # Éxito: 2 o 3 votos positivos
            curacion = 35
            vida_curada = participante.recibir_curacion(curacion)
            
            # Bonus de energía
            energia_extra = 25
            participante.energia_actual = min(participante.energia_maxima, participante.energia_actual + energia_extra)
            
            mensaje = (f"{C.VERDE}¡CONCURSO DE TAPAS!{C.RESET}\n"
                      f"Se organiza un concurso improvisado de tapas.\n"
                      f"{participante.nombre} presenta unas {tapa}.\n"
                      f"El jurado ({', '.join(jurado)}) aprueba la tapa ({votos_positivos}/3 votos).\n"
                      f"¡{participante.nombre} gana! Recupera {vida_curada} de vida y {energia_extra} de energía.")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "ganador": participante.nombre,
                "tapa": tapa,
                "votos": votos_positivos,
                "curacion": vida_curada,
                "energia_extra": energia_extra,
                "resultado": "gana",
                "tipo": "beneficio"
            }
        else:
            # Fracaso: 0 o 1 voto positivo
            daño = 20
            daño_recibido = participante.recibir_dano(daño, "humillacion_culinaria")
            
            # También reduce ataque (pérdida de confianza) - duración 2 turnos
            participante.ataque = max(5, participante.ataque - 8)
            
            mensaje = (f"{C.ROJO}¡CONCURSO DE TAPAS!{C.RESET}\n"
                      f"Se organiza un concurso improvisado de tapas.\n"
                      f"{participante.nombre} presenta unas {tapa}.\n"
                      f"El jurado ({', '.join(jurado)}) rechaza la tapa ({votos_positivos}/3 votos).\n"
                      f"¡{participante.nombre} pierde! Recibe {daño_recibido} de daño y -8 de ataque por la humillación.")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "perdedor": participante.nombre,
                "tapa": tapa,
                "votos": votos_positivos,
                "daño": daño_recibido,
                "ataque_perdido": 8,
                "resultado": "pierde",
                "tipo": "daño"
            }


class LlamadaDeTelefono(EventoBase):
    """Llamada de Teléfono - Te llama tu madre / el banco / una teleoperadora."""
    
    def __init__(self):
        super().__init__(
            nombre="📞 LLAMADA DE TELÉFONO",
            descripcion="Te llama tu madre / el banco / una teleoperadora. Cada una tiene efectos diferentes.",
            tipo="raro"
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        # Decide quién recibe la llamada (70% jugador, 30% enemigo)
        objetivo = jugador if random.random() < 0.7 else enemigo
        
        # Tipo de llamada
        llamadas = ["madre", "banco", "teleoperadora"]
        llamada = random.choice(llamadas)
        
        if llamada == "madre":
            # Llamada de la madre
            if random.random() < 0.6:  # 60% preocupada
                # Preocupada - cura pero distrae
                curacion = 25
                vida_curada = objetivo.recibir_curacion(curacion)
                
                # Pero reduce velocidad (está hablando) - duración 1 turno
                objetivo.velocidad = max(5, objetivo.velocidad - 10)
                
                mensaje = (f"{C.CYAN}¡LLAMADA DE TELÉFONO!{C.RESET}\n"
                          f"Te llama tu madre preocupada. '¿Has comido, hijo?'\n"
                          f"Recuperas {vida_curada} de vida por el cariño, pero velocidad -10 por estar al teléfono.")
                
                return {
                    "exito": True,
                    "mensaje": mensaje,
                    "llamada": "madre",
                    "curacion": vida_curada,
                    "velocidad_perdida": 10,
                    "objetivo": objetivo.nombre,
                    "tipo": "mixto"
                }
            else:  # 40% enfadada
                # Enfadada - daño psicológico
                daño = 30
                daño_recibido = objetivo.recibir_dano(daño, "regaño_maternal")
                
                mensaje = (f"{C.ROJO}¡LLAMADA DE TELÉFONO!{C.RESET}\n"
                          f"Te llama tu madre enfadada. '¡Limpia tu cuarto!'\n"
                          f"Recibes {daño_recibido} de daño psicológico.")
                
                return {
                    "exito": True,
                    "mensaje": mensaje,
                    "llamada": "madre_enfadada",
                    "daño": daño_recibido,
                    "objetivo": objetivo.nombre,
                    "tipo": "daño"
                }
        
        elif llamada == "banco":
            # Llamada del banco
            if random.random() < 0.4:  # 40% buena noticia
                # Buena noticia - dinero
                dinero = random.randint(20, 50)
                objetivo.energia_actual = min(objetivo.energia_maxima, objetivo.energia_actual + dinero)
                
                mensaje = (f"{C.VERDE}¡LLAMADA DE TELÉFONO!{C.RESET}\n"
                          f"Te llama el banco. 'Tiene una transferencia a su favor.'\n"
                          f"Recibes {dinero} de energía (dinero).")
                
                return {
                    "exito": True,
                    "mensaje": mensaje,
                    "llamada": "banco_bueno",
                    "energia_ganada": dinero,
                    "objetivo": objetivo.nombre,
                    "tipo": "beneficio"
                }
            else:  # 60% mala noticia
                # Mala noticia - deudas
                deuda = random.randint(15, 40)
                objetivo.energia_actual = max(0, objetivo.energia_actual - deuda)
                
                # También reduce defensa (preocupación) - duración 2 turnos
                objetivo.defensa = max(5, objetivo.defensa - 5)
                
                mensaje = (f"{C.ROJO}¡LLAMADA DE TELÉFONO!{C.RESET}\n"
                          f"Te llama el banco. 'Tiene una deuda pendiente.'\n"
                          f"Pierdes {deuda} de energía (dinero) y -5 de defensa por la preocupación.")
                
                return {
                    "exito": True,
                    "mensaje": mensaje,
                    "llamada": "banco_malo",
                    "energia_perdida": deuda,
                    "defensa_perdida": 5,
                    "objetivo": objetivo.nombre,
                    "tipo": "daño"
                }
        
        else:  # teleoperadora
            # Teleoperadora - siempre mala
            # Daño psicológico
            daño = 15
            daño_recibido = objetivo.recibir_dano(daño, "teleoperadora")
            
            # También reduce energía (pérdida de tiempo)
            energia_perdida = min(10, objetivo.energia_actual)
            objetivo.energia_actual -= energia_perdida
            
            productos = ["seguro", "fibra óptica", "curso milagroso", "tarjeta de crédito"]
            producto = random.choice(productos)
            
            mensaje = (f"{C.MAGENTA}¡LLAMADA DE TELÉFONO!{C.RESET}\n"
                      f"Te llama una teleoperadora. '¿Le interesa un {producto}?'\n"
                      f"Recibes {daño_recibido} de daño psicológico y pierdes {energia_perdida} de energía (tiempo).")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "llamada": "teleoperadora",
                "producto": producto,
                "daño": daño_recibido,
                "energia_perdida": energia_perdida,
                "objetivo": objetivo.nombre,
                "tipo": "daño"
            }


class QueTiempoMasRaro(EventoBase):
    """Qué Tiempo Más Raro - Cambia el tiempo bruscamente."""
    
    def __init__(self):
        super().__init__(
            nombre="🌦️ QUÉ TIEMPO MÁS RARO",
            descripcion="Cambia el tiempo bruscamente. Granizo, calor extremo o sol de justicia.",
            tipo="raro"
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        # Tipo de tiempo
        tiempos = [
            ("granizo", "hielo"),
            ("calor_extremo", "fuego"),
            ("sol_de_justicia", "sol"),
            ("lluvia_torrencial", "agua"),
            ("viento_hurracanado", "viento")
        ]
        tiempo, tipo_daño = random.choice(tiempos)
        
        # Efectos según el tiempo
        if tiempo == "granizo":
            # Daño a ambos pero más al que no tiene protección
            daño_jugador = 20 if "protegido_frio" not in jugador.estados else 5
            daño_enemigo = 20 if "protegido_frio" not in enemigo.estados else 5
            
            daño_recibido_j = jugador.recibir_dano(daño_jugador, "hielo")
            daño_recibido_e = enemigo.recibir_dano(daño_enemigo, "hielo")
            
            mensaje = (f"{C.AZUL}¡QUÉ TIEMPO MÁS RARO!{C.RESET}\n"
                      f"Empieza a caer granizo del tamaño de pelotas de golf.\n"
                      f"{jugador.nombre} recibe {daño_recibido_j} de daño.\n"
                      f"{enemigo.nombre} recibe {daño_recibido_e} de daño.")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "tiempo": "granizo",
                "daño_jugador": daño_recibido_j,
                "daño_enemigo": daño_recibido_e,
                "tipo": "daño_multi"
            }
        
        elif tiempo == "calor_extremo":
            # Daño por calor y posible quemadura
            daño = 25
            daño_j = jugador.recibir_dano(daño, "fuego")
            daño_e = enemigo.recibir_dano(daño, "fuego")
            
            # Posible quemadura (40% cada uno) - duración 2 turnos
            if random.random() < 0.4:
                jugador.aplicar_estado("quemado", duracion=2)
                quemado_j = True
            else:
                quemado_j = False
            
            if random.random() < 0.4:
                enemigo.aplicar_estado("quemado", duracion=2)
                quemado_e = True
            else:
                quemado_e = False
            
            mensaje_quemado = ""
            if quemado_j or quemado_e:
                quemados = []
                if quemado_j:
                    quemados.append(jugador.nombre)
                if quemado_e:
                    quemados.append(enemigo.nombre)
                mensaje_quemado = f"\n{' y '.join(quemados)} {'se' if len(quemados) == 1 else 'se'} quema{'n' if len(quemados) > 1 else ''}."
            
            mensaje = (f"{C.ROJO}¡QUÉ TIEMPO MÁS RARO!{C.RESET}\n"
                      f"El calor es extremo, parece un horno.\n"
                      f"{jugador.nombre} recibe {daño_j} de daño.\n"
                      f"{enemigo.nombre} recibe {daño_e} de daño.{mensaje_quemado}")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "tiempo": "calor_extremo",
                "daño_jugador": daño_j,
                "daño_enemigo": daño_e,
                "quemado_jugador": quemado_j,
                "quemado_enemigo": quemado_e,
                "tipo": "daño_multi"
            }
        
        elif tiempo == "sol_de_justicia":
            # Beneficia a algunos, perjudica a otros
            # Beneficia a personajes de playa/verano, perjudica a otros
            beneficiosos = ["🏖️ Flaquito Playero", "🐂 El Fatal Torero"]
            
            if jugador.tipo in beneficiosos:
                # Cura al jugador
                curacion_j = 30
                vida_curada_j = jugador.recibir_curacion(curacion_j)
                bonus_j = f"{jugador.nombre} disfruta del sol y recupera {vida_curada_j} de vida."
                tipo_j = "curacion"
            else:
                # Daña al jugador
                daño_j = 20
                daño_recibido_j = jugador.recibir_dano(daño_j, "sol")
                bonus_j = f"{jugador.nombre} sufre el sol y recibe {daño_recibido_j} de daño."
                tipo_j = "daño"
            
            if enemigo.tipo in beneficiosos:
                # Cura al enemigo
                curacion_e = 30
                vida_curada_e = enemigo.recibir_curacion(curacion_e)
                bonus_e = f"{enemigo.nombre} disfruta del sol y recupera {vida_curada_e} de vida."
                tipo_e = "curacion"
            else:
                # Daña al enemigo
                daño_e = 20
                daño_recibido_e = enemigo.recibir_dano(daño_e, "sol")
                bonus_e = f"{enemigo.nombre} sufre el sol y recibe {daño_recibido_e} de daño."
                tipo_e = "daño"
            
            mensaje = (f"{C.AMARILLO}¡QUÉ TIEMPO MÁS RARO!{C.RESET}\n"
                      f"Sale un sol de justicia que derrite el asfalto.\n"
                      f"{bonus_j}\n"
                      f"{bonus_e}")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "tiempo": "sol_de_justicia",
                "efecto_jugador": tipo_j,
                "efecto_enemigo": tipo_e,
                "tipo": "mixto_multi"
            }
        
        elif tiempo == "lluvia_torrencial":
            # Mojado a todos, posible resfriado
            # Estado mojado a ambos - duración 3 turnos
            jugador.aplicar_estado("mojado", duracion=3)
            enemigo.aplicar_estado("mojado", duracion=3)
            
            # Posible resfriado (30% cada uno) - duración 3 turnos
            if random.random() < 0.3:
                jugador.aplicar_estado("resfriado", duracion=3)
                resfriado_j = True
            else:
                resfriado_j = False
            
            if random.random() < 0.3:
                enemigo.aplicar_estado("resfriado", duracion=3)
                resfriado_e = True
            else:
                resfriado_e = False
            
            mensaje_resfriado = ""
            if resfriado_j or resfriado_e:
                resfriados = []
                if resfriado_j:
                    resfriados.append(jugador.nombre)
                if resfriado_e:
                    resfriados.append(enemigo.nombre)
                mensaje_resfriado = f"\n{' y '.join(resfriados)} {'se' if len(resfriados) == 1 else 'se'} resfría{'n' if len(resfriados) > 1 else ''}."
            
            mensaje = (f"{C.AZUL}¡QUÉ TIEMPO MÁS RARO!{C.RESET}\n"
                      f"Comienza una lluvia torrencial.\n"
                      f"¡Ambos están MOJADOS!{mensaje_resfriado}")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "tiempo": "lluvia_torrencial",
                "mojado_jugador": True,
                "mojado_enemigo": True,
                "resfriado_jugador": resfriado_j,
                "resfriado_enemigo": resfriado_e,
                "tipo": "estado_multi"
            }
        
        else:  # viento_hurracanado
            # Aleatorio - puede mover personajes, dañar, o nada
            efectos = []
            
            # 50% de que mueva al jugador
            if random.random() < 0.5:
                direccion = random.choice(["izquierda", "derecha", "arriba", "abajo"])
                efectos.append(f"{jugador.nombre} es arrastrado {direccion}.")
            
            # 50% de que mueva al enemigo
            if random.random() < 0.5:
                direccion = random.choice(["izquierda", "derecha", "arriba", "abajo"])
                efectos.append(f"{enemigo.nombre} es arrastrado {direccion}.")
            
            # 30% de daño a ambos
            if random.random() < 0.3:
                daño = 15
                jugador.recibir_dano(daño, "viento")
                enemigo.recibir_dano(daño, "viento")
                efectos.append(f"Ambos reciben {daño} de daño por los objetos voladores.")
            
            if not efectos:
                efectos.append("Afortunadamente, nadie sale volando.")
            
            mensaje = (f"{C.CYAN}¡QUÉ TIEMPO MÁS RARO!{C.RESET}\n"
                      f"Un viento huracanado arrasa el campo de batalla.\n"
                      f"{' '.join(efectos)}")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "tiempo": "viento_hurracanado",
                "efectos": efectos,
                "tipo": "aleatorio"
            }


# ============================================================================
# EVENTOS ULTRA RAROS (5% de probabilidad cuando ocurre un evento)
# ============================================================================

class FurgonetaBlanca(EventoBase):
    """Furgoneta Blanca - Aparece LA FURGONETA."""
    
    def __init__(self):
        super().__init__(
            nombre="🚐 FURGONETA BLANCA",
            descripcion="Aparece LA FURGONETA. Todos corren. Daño masivo y posibilidad de secuestro.",
            tipo="ultra_raro"
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        print(f"{C.ROJO_BRILLANTE}¡¡¡FURGONETA BLANCA!!!{C.RESET}")
        
        # Daño masivo a ambos
        daño_masivo = 50
        daño_j = jugador.recibir_dano(daño_masivo, "furgoneta")
        daño_e = enemigo.recibir_dano(daño_masivo, "furgoneta")
        
        # Posibilidad de secuestro (10% cada uno)
        secuestro_j = random.random() < 0.1
        secuestro_e = random.random() < 0.1
        
        mensaje_secuestro = ""
        if secuestro_j or secuestro_e:
            secuestrados = []
            if secuestro_j:
                secuestrados.append(jugador.nombre)
                jugador.vida_actual = 0  # Eliminado del combate
            if secuestro_e:
                secuestrados.append(enemigo.nombre)
                enemigo.vida_actual = 0  # Eliminado del combate
            
            mensaje_secuestro = (f"\n{C.ROJO_BRILLANTE}¡SECUESTRO! "
                               f"{' y '.join(secuestrados)} {'es' if len(secuestrados) == 1 else 'son'} secuestrado{'s' if len(secuestrados) > 1 else ''} "
                               f"por la furgoneta blanca.{C.RESET}")
        
        mensaje = (f"{C.ROJO_BRILLANTE}¡¡¡FURGONETA BLANCA!!!{C.RESET}\n"
                  f"De la nada aparece LA FURGONETA BLANCA. ¡TODOS CORREN!\n"
                  f"Daño masivo por el pánico:\n"
                  f"{jugador.nombre} recibe {daño_j} de daño.\n"
                  f"{enemigo.nombre} recibe {daño_e} de daño."
                  f"{mensaje_secuestro}")
        
        return {
            "exito": True,
            "mensaje": mensaje,
            "daño_jugador": daño_j,
            "daño_enemigo": daño_e,
            "secuestro_jugador": secuestro_j,
            "secuestro_enemigo": secuestro_e,
            "tipo": "catastrofico"
        }


class ConspiracionTortillera(EventoBase):
    """Conspiración Tortillera - Se descubre la verdad sobre la tortilla de patatas."""
    
    def __init__(self):
        super().__init__(
            nombre="🥔 CONSPIRACIÓN TORTILLERA",
            descripcion="Se descubre la verdad sobre la tortilla de patatas. Debes elegir: ¿CON CEBOLLA O SIN CEBOLLA?",
            tipo="ultra_raro"
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        print(f"{C.AMARILLO_BRILLANTE}¡¡¡CONSPIRACIÓN TORTILLERA!!!{C.RESET}")
        
        # Este evento requiere interacción del jugador
        # En un juego real, aquí habría una pausa para que el jugador elija
        # Por ahora, elegimos aleatoriamente
        
        eleccion = random.choice(["con cebolla", "sin cebolla"])
        
        if eleccion == "con cebolla":
            # Los que eligen con cebolla se curan
            curacion = 60
            vida_curada_j = jugador.recibir_curacion(curacion)
            vida_curada_e = enemigo.recibir_curacion(curacion)  # Enemigo también elige con cebolla por simplicidad
            
            # Bonus de ataque (confianza en la elección correcta) - duración 3 turnos
            jugador.ataque += 20
            enemigo.ataque += 20
            
            mensaje = (f"{C.AMARILLO_BRILLANTE}¡¡¡CONSPIRACIÓN TORTILLERA!!!{C.RESET}\n"
                      f"Se descubre la VERDAD sobre la tortilla de patatas.\n"
                      f"Eliges: {eleccion.upper()} (la respuesta correcta).\n"
                      f"¡Revelación gastronómica! Ambos recuperan {vida_curada_j} de vida y +20 de ataque por la certeza.")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "eleccion": eleccion,
                "curacion_jugador": vida_curada_j,
                "curacion_enemigo": vida_curada_e,
                "ataque_extra": 20,
                "correcto": True,
                "tipo": "eleccion"
            }
        else:
            # Los que eligen sin cebolla sufren
            daño = 40
            daño_j = jugador.recibir_dano(daño, "herejia_culinaria")
            daño_e = enemigo.recibir_dano(daño, "herejia_culinaria")
            
            # Reducción de defensa (culpa por elegir mal) - duración 3 turnos
            jugador.defensa = max(5, jugador.defensa - 15)
            enemigo.defensa = max(5, enemigo.defensa - 15)
            
            mensaje = (f"{C.AMARILLO_BRILLANTE}¡¡¡CONSPIRACIÓN TORTILLERA!!!{C.RESET}\n"
                      f"Se descubre la VERDAD sobre la tortilla de patatas.\n"
                      f"Eliges: {eleccion.upper()} (la respuesta INCORRECTA).\n"
                      f"¡Herejía culinaria! Ambos reciben {daño_j} de daño y -15 de defensa por la vergüenza.")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "eleccion": eleccion,
                "daño_jugador": daño_j,
                "daño_enemigo": daño_e,
                "defensa_perdida": 15,
                "correcto": False,
                "tipo": "eleccion"
            }


class RatalectricaFalsa(EventoBase):
    """Ratalectrica Falsa - Aparece una Ratalectrica pirata de ImportExpress."""
    
    def __init__(self):
        super().__init__(
            nombre="[!] RATALECTRICA FALSA",
            descripcion="Aparece una Ratalectrica pirata de ImportExpress. Explota el 70% de las veces.",
            tipo="ultra_raro"
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        print(f"{C.AMARILLO_BRILLANTE}¡¡¡RATALECTRICA FALSA!!!{C.RESET}")
        
        # 70% de probabilidad de explosión
        explota = random.random() < 0.7
        
        if explota:
            # Explosión - daño masivo aleatorio
            daño = random.randint(30, 80)
            
            # Elige un objetivo aleatorio (o ambos)
            objetivo = random.choice(["jugador", "enemigo", "ambos"])
            
            if objetivo == "jugador":
                daño_recibido = jugador.recibir_dano(daño, "explosion_ratalectrica")
                mensaje_daño = f"{jugador.nombre} recibe {daño_recibido} de daño por la explosión."
            elif objetivo == "enemigo":
                daño_recibido = enemigo.recibir_dano(daño, "explosion_ratalectrica")
                mensaje_daño = f"{enemigo.nombre} recibe {daño_recibido} de daño por la explosión."
            else:  # ambos
                daño_j = jugador.recibir_dano(daño, "explosion_ratalectrica")
                daño_e = enemigo.recibir_dano(daño, "explosion_ratalectrica")
                mensaje_daño = f"Ambos reciben {daño_j}/{daño_e} de daño por la explosión."
            
            mensaje = (f"{C.AMARILLO_BRILLANTE}¡¡¡RATALECTRICA FALSA!!!{C.RESET}\n"
                      f"Aparece una Ratalectrica pirata de ImportExpress...\n"
                      f"¡EXPLOTA! (70% de probabilidad)\n"
                      f"{mensaje_daño}")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "explota": True,
                "daño": daño,
                "objetivo": objetivo,
                "tipo": "explosion"
            }
        else:
            # No explota - efectos aleatorios
            efectos = random.choice([
                "te cura un poco",
                "da un choque eléctrico leve",
                "hace un truco gracioso",
                "se convierte en un Copión"
            ])
            
            if efectos == "te cura un poco":
                curacion = 40
                vida_curada = jugador.recibir_curacion(curacion)
                mensaje_efecto = f"La Ratalectrica falsa cura a {jugador.nombre} por {vida_curada} de vida."
            elif efectos == "da un choque eléctrico leve":
                daño = 10
                objetivo = random.choice([jugador, enemigo])
                daño_recibido = objetivo.recibir_dano(daño, "choque_ratalectrica")
                mensaje_efecto = f"La Ratalectrica falsa da un choque a {objetivo.nombre} por {daño_recibido} de daño."
            elif efectos == "hace un truco gracioso":
                # Aumenta la energía de ambos por la risa
                energia = 25
                jugador.energia_actual = min(jugador.energia_maxima, jugador.energia_actual + energia)
                enemigo.energia_actual = min(enemigo.energia_maxima, enemigo.energia_actual + energia)
                mensaje_efecto = f"La Ratalectrica falsa hace un truco gracioso. Ambos recuperan {energia} de energía por la risa."
            else:  # se convierte en un Copión
                # Copia temporalmente las stats del más fuerte - duración 2 turnos
                if jugador.ataque > enemigo.ataque:
                    enemigo.ataque = jugador.ataque
                    mensaje_efecto = f"¡Se convierte en Copión y copia a {jugador.nombre}! {enemigo.nombre} ahora tiene el mismo ataque."
                else:
                    jugador.ataque = enemigo.ataque
                    mensaje_efecto = f"¡Se convierte en Copión y copia a {enemigo.nombre}! {jugador.nombre} ahora tiene el mismo ataque."
            
            mensaje = (f"{C.AMARILLO_BRILLANTE}¡¡¡RATALECTRICA FALSA!!!{C.RESET}\n"
                      f"Aparece una Ratalectrica pirata de ImportExpress...\n"
                      f"No explota (30% de probabilidad)\n"
                      f"{mensaje_efecto}")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "explota": False,
                "efecto": efectos,
                "tipo": "aleatorio"
            }


class EspirituDeLaFeria(EventoBase):
    """Espíritu de la Feria - El fantasma de la feria te ofrece una oreja de feria."""
    
    def __init__(self):
        super().__init__(
            nombre="👻 ESPÍRITU DE LA FERIA",
            descripcion="El fantasma de la feria te ofrece una oreja de feria o te monta en un Refresco de cola.",
            tipo="ultra_raro"
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        print(f"{C.MAGENTA_BRILLANTE}¡¡¡ESPÍRITU DE LA FERIA!!!{C.RESET}")
        
        # El espíritu ofrece una de dos cosas
        oferta = random.choice(["oreja_feria", "refresco_cola"])
        
        if oferta == "oreja_feria":
            # Oreja de feria - curación masiva
            curacion = 75
            vida_curada_j = jugador.recibir_curacion(curacion)
            vida_curada_e = enemigo.recibir_curacion(curacion)  # El espíritu es generoso
            
            # Bonus extra por la magia de la feria - duración 2 turnos
            jugador.ataque += 15
            enemigo.ataque += 15
            
            mensaje = (f"{C.MAGENTA_BRILLANTE}¡¡¡ESPÍRITU DE LA FERIA!!!{C.RESET}\n"
                      f"Aparece el fantasma de la feria y te ofrece una OREJA DE FERIA.\n"
                      f"¡Magia ferial! Ambos recuperan {vida_curada_j} de vida y +15 de ataque.")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "oferta": "oreja_feria",
                "curacion_jugador": vida_curada_j,
                "curacion_enemigo": vida_curada_e,
                "ataque_extra": 15,
                "tipo": "beneficio"
            }
        else:
            # Monta en Refresco de cola - efectos locos
            # Daño por mareo
            daño_mareo = 30
            daño_j = jugador.recibir_dano(daño_mareo, "mareo_cocacola")
            daño_e = enemigo.recibir_dano(daño_mareo, "mareo_cocacola")
            
            # Estado mareado - duración 2 turnos
            jugador.aplicar_estado("mareado", duracion=2)
            enemigo.aplicar_estado("mareado", duracion=2)
            
            # Pero también diversión (energía)
            energia_extra = 40
            jugador.energia_actual = min(jugador.energia_maxima, jugador.energia_actual + energia_extra)
            enemigo.energia_actual = min(enemigo.energia_maxima, enemigo.energia_actual + energia_extra)
            
            mensaje = (f"{C.MAGENTA_BRILLANTE}¡¡¡ESPÍRITU DE LA FERIA!!!{C.RESET}\n"
                      f"Aparece el fantasma de la feria y te monta en REFRESCO DE COLA.\n"
                      f"¡Viaje salvaje! Ambos reciben {daño_j} de daño por el mareo, "
                      f"pero recuperan {energia_extra} de energía por la diversión. ¡Están MAREADOS!")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "oferta": "refresco_cola",
                "daño_jugador": daño_j,
                "daño_enemigo": daño_e,
                "energia_extra": energia_extra,
                "mareado": True,
                "tipo": "mixto"
            }


class MocoEnElDedo(EventoBase):
    """Moco en el Dedo - Encuentras un moco."""
    
    def __init__(self):
        super().__init__(
            nombre="💧 MOCO EN EL DEDO",
            descripcion="Encuentras un moco. Puedes: mirarlo detenidamente, lanzarlo al oponente, o comértelo.",
            tipo="ultra_raro"
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        print(f"{C.VERDE_BRILLANTE}¡¡¡MOCO EN EL DEDO!!!{C.RESET}")
        
        # Tres opciones posibles
        opciones = ["mirar", "lanzar", "comer"]
        opcion = random.choice(opciones)
        
        if opcion == "mirar":
            # Mirarlo detenidamente - revelación científica
            # Cura por el asco superado
            curacion = 20
            vida_curada = jugador.recibir_curacion(curacion)
            
            # Aumenta sabiduría (si el personaje tiene ese atributo)
            if hasattr(jugador, '_sabiduria'):
                jugador._sabiduria = min(150, getattr(jugador, '_sabiduria', 0) + 10)
                mensaje_sabiduria = f" y gana 10 de sabiduría"
            else:
                mensaje_sabiduria = ""
            
            mensaje = (f"{C.VERDE_BRILLANTE}¡¡¡MOCO EN EL DEDO!!!{C.RESET}\n"
                      f"Encuentras un moco y lo miras detenidamente.\n"
                      f"¡Revelación científica! {jugador.nombre} recupera {vida_curada} de vida{mensaje_sabiduria}.")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "opcion": "mirar",
                "curacion": vida_curada,
                "sabiduria_extra": 10 if hasattr(jugador, '_sabiduria') else 0,
                "tipo": "beneficio"
            }
        
        elif opcion == "lanzar":
            # Lanzarlo al oponente - daño y asco
            daño = 25
            daño_recibido = enemigo.recibir_dano(daño, "moco")
            
            # Estado asqueado - duración 2 turnos
            enemigo.aplicar_estado("asqueado", duracion=2)
            
            # Reduce defensa del enemigo por el asco - duración 2 turnos
            enemigo.defensa = max(5, enemigo.defensa - 10)
            
            mensaje = (f"{C.VERDE_BRILLANTE}¡¡¡MOCO EN EL DEDO!!!{C.RESET}\n"
                      f"Encuentras un moco y se lo lanzas a {enemigo.nombre}.\n"
                      f"¡Impacto directo! {enemigo.nombre} recibe {daño_recibido} de daño, "
                      f"-10 de defensa por el asco y está ASQUEADO.")
            
            return {
                "exito": True,
                "mensaje": mensaje,
                "opcion": "lanzar",
                "daño": daño_recibido,
                "defensa_perdida": 10,
                "objetivo": enemigo.nombre,
                "tipo": "daño"
            }
        
        else:  # comer
            # Comérselo - efectos aleatorios extremos
            efectos = random.choice([
                "curacion_masiva",
                "enfermedad_grave",
                "poder_oculto",
                "transformacion"
            ])
            
            if efectos == "curacion_masiva":
                curacion = 100
                vida_curada = jugador.recibir_curacion(curacion)
                mensaje = (f"{C.VERDE_BRILLANTE}¡¡¡MOCO EN EL DEDO!!!{C.RESET}\n"
                          f"Encuentras un moco y te lo comes.\n"
                          f"¡SABOR SECRETO! {jugador.nombre} recupera {vida_curada} de vida. ¿Era caramelizado?")
                return {
                    "exito": True,
                    "mensaje": mensaje,
                    "opcion": "comer",
                    "efecto": "curacion_masiva",
                    "curacion": vida_curada,
                    "tipo": "beneficio"
                }
            
            elif efectos == "enfermedad_grave":
                daño = 50
                daño_recibido = jugador.recibir_dano(daño, "enfermedad_moco")
                # Estado grave - duración 3 turnos
                jugador.aplicar_estado("enfermo_grave", duracion=3)
                mensaje = (f"{C.ROJO_BRILLANTE}¡¡¡MOCO EN EL DEDO!!!{C.RESET}\n"
                          f"Encuentras un moco y te lo comes.\n"
                          f"¡ERROR GRAVE! {jugador.nombre} recibe {daño_recibido} de daño y contrae una enfermedad grave.")
                return {
                    "exito": True,
                    "mensaje": mensaje,
                    "opcion": "comer",
                    "efecto": "enfermedad_grave",
                    "daño": daño_recibido,
                    "enfermedad": True,
                    "tipo": "daño"
                }
            
            elif efectos == "poder_oculto":
                # Descubre un poder oculto - duración 3 turnos
                jugador.ataque += 30
                jugador.defensa += 20
                jugador.velocidad += 15
                mensaje = (f"{C.VERDE_BRILLANTE}¡¡¡MOCO EN EL DEDO!!!{C.RESET}\n"
                          f"Encuentras un moco y te lo comes.\n"
                          f"¡PODER OCULTO! {jugador.nombre} descubre habilidades místicas. "
                          f"Ataque +30, Defensa +20, Velocidad +15.")
                return {
                    "exito": True,
                    "mensaje": mensaje,
                    "opcion": "comer",
                    "efecto": "poder_oculto",
                    "ataque_extra": 30,
                    "defensa_extra": 20,
                    "velocidad_extra": 15,
                    "tipo": "beneficio"
                }
            
            else:  # transformacion
                # Se transforma temporalmente - duración 2 turnos
                jugador.aplicar_estado("transformado", duracion=2)
                mensaje = (f"{C.MAGENTA_BRILLANTE}¡¡¡MOCO EN EL DEDO!!!{C.RESET}\n"
                          f"Encuentras un moco y te lo comes.\n"
                          f"¡TRANSFORMACIÓN! {jugador.nombre} sufre una transformación temporal. "
                          f"Está TRANSFORMADO y sus habilidades cambian.")
                return {
                    "exito": True,
                    "mensaje": mensaje,
                    "opcion": "comer",
                    "efecto": "transformacion",
                    "transformado": True,
                    "tipo": "estado"
                }