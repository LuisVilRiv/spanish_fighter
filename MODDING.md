# 🧩 Guía de Modding – Batalla Cómica Española

**Versión:** 1.0  
**Fecha:** 2026  
**Autor:** Luis Villegas Rivera  
**Licencia:** Todos los derechos reservados (con excepción para mods gratuitos).  

Esta guía te enseñará a crear modificaciones (mods) para *Batalla Cómica Española*.  
Los mods pueden incluir nuevos personajes, habilidades, eventos, diálogos, arte ASCII y ajustes de balance.  

---

## 📋 Índice

1. [¿Qué es un mod?](#-qué-es-un-mod)
2. [Estructura del proyecto](#-estructura-del-proyecto)
3. [Requisitos](#-requisitos)
4. [Crear un nuevo personaje](#-crear-un-nuevo-personaje)
5. [Crear nuevas habilidades](#-crear-nuevas-habilidades)
6. [Crear nuevos eventos aleatorios](#-crear-nuevos-eventos-aleatorios)
7. [Modificar personajes existentes](#-modificar-personajes-existentes)
8. [Arte ASCII y sprites de texto](#-arte-ascii-y-sprites-de-texto)
9. [Diálogos y descripciones](#-diálogos-y-descripciones)
10. [Ejemplo completo: El Botellón Humano](#-ejemplo-completo-el-botellón-humano)
11. [Buenas prácticas y advertencias](#-buenas-prácticas-y-advertencias)
12. [Distribución de mods](#-distribución-de-mods)

---

## 🎮 ¿Qué es un mod?

Un **mod** (modificación) es cualquier cambio no oficial realizado por la comunidad.  
Puedes:

- ✅ **Crear personajes nuevos** con estadísticas y habilidades únicas.
- ✅ **Añadir habilidades** a personajes existentes.
- ✅ **Inventar eventos aleatorios** que ocurran durante el combate.
- ✅ **Cambiar descripciones, diálogos o nombres**.
- ✅ **Ajustar estadísticas** (vida, ataque, defensa, velocidad).
- ✅ **Añadir arte ASCII** para personalizar la presentación.

**NO puedes:**

- ❌ Vender tu mod o exigir pago por él.
- ❌ Distribuir el juego base completo dentro de tu mod.
- ❌ Eliminar o modificar los créditos del autor original.
- ❌ Usar el mod para fines ilegales o que dañen la imagen del juego.

*(Consulta el archivo `LICENSE.txt` para términos completos.)*

---

## 📁 Estructura del proyecto

Antes de modificar, familiarízate con las carpetas clave:

```
BatallaComicaEspanola/
│
├── personajes/               # Todos los personajes
│   ├── personaje_base.py     # Clase base Personaje (no modificar directamente)
│   ├── segarro.py
│   ├── catolico.py
│   └── ... (más personajes)
│
├── habilidades/              # Todas las habilidades
│   ├── habilidad_base.py     # Clase base Habilidad
│   ├── habilidades_segarro.py
│   ├── habilidades_abuela.py
│   └── ...
│
├── eventos/                  # Eventos aleatorios
│   ├── __init__.py
│   └── eventos_aleatorios.py
│
├── utils/                    # Utilidades (colores, etc.)
│   └── colores.py
│
├── combate/                  # Sistema de combate
│   └── sistema_combate.py
│
├── saves/                    # Partidas guardadas (se genera automáticamente)
│
├── main.py                   # Punto de entrada
└── menu_principal.py         # Menú y gestión de guardado
```

**IMPORTANTE:** No modifiques `personaje_base.py`, `habilidad_base.py` ni los archivos del sistema de combate a menos que sepas exactamente lo que haces. Podrías romper el juego. Crea tus propios archivos y personajes en las carpetas correspondientes.

---

## 🛠️ Requisitos

- Conocimientos básicos de Python 3.8+.
- Editor de código (VS Code, PyCharm, etc.).
- El juego descargado y funcionando.
- (Opcional) Git para control de versiones.

---

## 👤 Crear un nuevo personaje

### Paso 1: Crear el archivo del personaje

Dentro de la carpeta `personajes/`, crea un archivo con el nombre de tu personaje, por ejemplo:  
`personajes/botellon.py`

### Paso 2: Importar la clase base

```python
from .personaje_base import Personaje
from utils import Colores as C
import random
```

### Paso 3: Definir la clase

Tu personaje debe heredar de `Personaje` e implementar:

- `__init__` – define nombre, tipo, estadísticas base, debilidades, fortalezas.
- `inicializar_habilidades` – asigna las habilidades.
- `descripcion` – método de clase que devuelve una descripción.

**Ejemplo mínimo:**

```python
class Botellon(Personaje):
    def __init__(self, nombre_personalizado: str = None):
        super().__init__(
            nombre=nombre_personalizado if nombre_personalizado else "El Botellón",
            tipo="🍺 Botellón Humano",
            vida_base=80,
            ataque_base=15,
            defensa_base=4,
            velocidad_base=50,
            energia_base=90
        )
        # Sistema de tipos (opcional)
        self.debilidades = ["autoridad", "madrugar"]
        self.fortalezas = ["alcohol", "fiesta"]
        self.inmunidades = ["resaca"]  # jeje
        
        # Estadísticas especiales (propias del personaje)
        self._litros_bebidos = 0
        self._popularidad = 50
        
        self.inicializar_habilidades()
    
    @classmethod
    def descripcion(cls):
        return ("El alma de la fiesta, siempre trae bebida. "
                "Débil contra la autoridad, pero nunca tiene resaca.")
    
    def inicializar_habilidades(self):
        from habilidades.habilidades_botellon import (
            BotellinCompartido,     # H1
            CanciónDesafinada,      # H2
            CalimotxoMagico,        # H3
            HieloTraicionero,       # H4
            LlamadaAlTaxi,          # H5
            UltimoVaso             # H6
        )
        self.habilidades = [
            BotellinCompartido(),
            CanciónDesafinada(),
            CalimotxoMagico(),
            HieloTraicionero(),
            LlamadaAlTaxi(),
            UltimoVaso()
        ]
```

### Paso 4: Registrar el personaje en `personajes/__init__.py`

```python
from .botellon import Botellon

__all__ = [
    # ... (personajes existentes)
    'Botellon',
]
```

### Paso 5: Añadir al menú de selección

En `menu_principal.py`, dentro del diccionario `personajes_map`, añade tu personaje:

```python
personajes_map = {
    # ...
    "Botellon": Botellon,
}
```

¡Ya puedes seleccionar tu personaje desde el menú!

---

## ⚔️ Crear nuevas habilidades

### Paso 1: Crear el archivo de habilidades

Dentro de `habilidades/`, crea un archivo para tu personaje:  
`habilidades/habilidades_botellon.py`

### Paso 2: Importar la clase base

```python
from .habilidad_base import Habilidad
from utils import Colores as C
import random
```

### Paso 3: Definir cada habilidad

Cada habilidad hereda de `Habilidad` y debe:

- Definir `__init__` con nombre, descripción, costo_energía, tipo.
- Definir `es_curacion = True` si la habilidad cura (útil para la IA).
- Implementar `usar(usuario, objetivo)` que devuelve un diccionario.

**Ejemplo de habilidad ofensiva:**

```python
class BotellinCompartido(Habilidad):
    def __init__(self):
        super().__init__(
            nombre="Botellín Compartido",
            descripcion="Invita a un botellín. El enemigo baja la guardia (defensa -10).",
            costo_energia=15,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        # Daño leve
        daño = objetivo.recibir_dano(usuario.ataque // 3, "alcohol")
        # Reduce defensa durante 2 turnos
        objetivo.defensa = max(5, objetivo.defensa - 10)
        objetivo.aplicar_estado("confiado", duracion=2)
        print(f"{C.AMARILLO}¡Salud! {objetivo.nombre} baja la guardia.{C.RESET}")
        return {"exito": True, "daño": daño, "defensa_reducida": 10}
```

**Ejemplo de habilidad curativa:**

```python
class CalimotxoMagico(Habilidad):
    def __init__(self):
        super().__init__(
            nombre="Calimotxo Mágico",
            descripcion="Bebida ancestral que cura 30 de vida y da energía extra.",
            costo_energia=25,
            tipo="defensiva"
        )
        self.es_curacion = True
    
    def usar(self, usuario, objetivo):
        vida_curada = usuario.recibir_curacion(30)
        usuario.energia_actual = min(usuario.energia_maxima, usuario.energia_actual + 20)
        print(f"{C.VERDE}¡Calimotxo mágico! +{vida_curada} vida, +20 energía.{C.RESET}")
        return {"exito": True, "curacion": vida_curada, "energia_recuperada": 20}
```

### Paso 4: Registrar habilidades en `habilidades/__init__.py`

```python
from .habilidades_botellon import (
    BotellinCompartido,
    CanciónDesafinada,
    CalimotxoMagico,
    HieloTraicionero,
    LlamadaAlTaxi,
    UltimoVaso
)

__all__ = [
    # ... (habilidades existentes)
    'BotellinCompartido',
    'CanciónDesafinada',
    'CalimotxoMagico',
    'HieloTraicionero',
    'LlamadaAlTaxi',
    'UltimoVaso',
]
```

---

## 🌟 Crear nuevos eventos aleatorios

### Paso 1: Editar `eventos/eventos_aleatorios.py`

Añade tu evento al final del archivo, antes de las listas de clasificación.

### Paso 2: Heredar de `EventoBase`

```python
class BotellonSorpresaMejorado(EventoBase):
    def __init__(self):
        super().__init__(
            nombre="🍾 BOTELLÓN SORPRESA MEJORADO",
            descripcion="Aparece un botellón de categoría. Todos beben y se divierten.",
            tipo="raro"  # normal, raro, ultra_raro
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        # Cura a ambos pero los marea
        curacion_j = jugador.recibir_curacion(25)
        curacion_e = enemigo.recibir_curacion(25)
        jugador.aplicar_estado("mareado", duracion=2)
        enemigo.aplicar_estado("mareado", duracion=2)
        
        mensaje = (f"{C.VERDE}¡BOTELLÓN SORPRESA MEJORADO!{C.RESET}\n"
                   f"Todos beben y se divierten.\n"
                   f"{jugador.nombre} recupera {curacion_j} de vida.\n"
                   f"{enemigo.nombre} recupera {curacion_e} de vida.\n"
                   f"¡Ambos están MAREADOS!")
        
        return {
            "exito": True,
            "mensaje": mensaje,
            "tipo": "mixto"
        }
```

### Paso 3: Añadir el evento a la lista correspondiente

```python
EVENTOS_NORMALES = [ ... ]
EVENTOS_RAROS = [ ... ]   # ← añade aquí tu evento si es raro
EVENTOS_ULTRA_RAROS = [ ... ]
TODOS_LOS_EVENTOS = EVENTOS_NORMALES + EVENTOS_RAROS + EVENTOS_ULTRA_RAROS
```

¡Ya aparecerá aleatoriamente en los combates!

---

## ⚖️ Modificar personajes existentes

Si solo quieres cambiar las estadísticas de un personaje (por ejemplo, hacer al Segarro más rápido):

1. Abre el archivo del personaje (`personajes/segarro.py`).
2. Modifica los valores en `super().__init__(..., vida_base=..., ataque_base=..., etc.)`.
3. Guarda el archivo.

**No olvides respetar el balance general del juego.**  
Prueba tus cambios antes de distribuirlos.

---

## 🎨 Arte ASCII y sprites de texto

Puedes personalizar la presentación de tu personaje o habilidades usando arte ASCII.  
Por ejemplo, al inicio del combate, podrías mostrar un dibujo.

### Método recomendado: añadir un atributo `ascii_art` en la clase del personaje.

```python
class Botellon(Personaje):
    ascii_art = """
    ⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⣠⡴⠟⠛⠛⠻⢿⣦⠀⠀⠀⠀⠀
    ⠀⠀⠀⢀⡾⠋⠀⠀⠀⠀⠀⠀⠙⢷⡀⠀⠀⠀
    ⠀⠀⢠⡟⠀⠀⣠⣴⣶⣦⣄⠀⠀⠈⣇⠀⠀⠀
    ⠀⢠⡟⠀⠀⢰⣿⣿⣿⣿⣿⡆⠀⠀⢹⡀⠀⠀
    ⠀⣾⠁⠀⠀⠈⠻⠿⠿⠟⠋⠀⠀⠀⠀⣧⠀⠀
    ⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀
    ⠀⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡟⠀⠀
    ⠀⠈⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠁⠀⠀
    ⠀⠀⠈⢿⣦⣀⠀⠀⠀⠀⠀⣀⣴⡿⠁⠀⠀⠀
    ⠀⠀⠀⠀⠙⠻⠿⠿⠿⠿⠿⠟⠋⠀⠀⠀⠀⠀
    🍾 EL BOTELLÓN HUMANO 🍾
    """
    
    def mostrar_arte(self):
        from utils import Colores as C
        print(f"{C.AMARILLO}{self.ascii_art}{C.RESET}")
```

Luego puedes llamar a `personaje.mostrar_arte()` en la introducción del combate (modificando `sistema_combate.py` o desde tu propio menú).  
**Nota:** Modificar `sistema_combate.py` requiere cuidado; mejor crear un método en tu personaje y llamarlo manualmente.

---

## 💬 Diálogos y descripciones

Puedes cambiar las frases típicas de un personaje modificando las listas internas (ej. `self._frases_segarro`).  
También puedes añadir nuevos diálogos en las habilidades.

**Ejemplo (dentro de una habilidad):**

```python
class CriticaConstructiva(Habilidad):
    def usar(self, usuario, objetivo):
        frases_criticonas = [
            "¡Eso no se hace así!",
            "¿En qué estabas pensando?",
            "Mi abuela lo haría mejor."
        ]
        frase = random.choice(frases_criticonas)
        print(f"{C.MAGENTA}{usuario.nombre}: \"{frase}\"{C.RESET}")
        # ... resto del código
```

---

## 🧪 Ejemplo completo: El Botellón Humano

Vamos a crear un personaje completo con 6 habilidades y 1 evento.

### Archivo `personajes/botellon.py`

```python
from .personaje_base import Personaje
from utils import Colores as C
import random

class Botellon(Personaje):
    def __init__(self, nombre_personalizado: str = None):
        super().__init__(
            nombre=nombre_personalizado if nombre_personalizado else "El Botellón",
            tipo="🍺 Botellón Humano",
            vida_base=80,
            ataque_base=15,
            defensa_base=4,
            velocidad_base=50,
            energia_base=90
        )
        self.debilidades = ["autoridad", "madrugar"]
        self.fortalezas = ["alcohol", "fiesta"]
        self.inmunidades = ["resaca"]
        self._litros_bebidos = 0
        self._popularidad = 50
        self.inicializar_habilidades()
    
    @classmethod
    def descripcion(cls):
        return "El alma de la fiesta, siempre trae bebida. Débil contra la autoridad, pero nunca tiene resaca."
    
    def inicializar_habilidades(self):
        from habilidades.habilidades_botellon import (
            BotellinCompartido,
            CancionDesafinada,
            CalimotxoMagico,
            HieloTraicionero,
            LlamadaAlTaxi,
            UltimoVaso
        )
        self.habilidades = [
            BotellinCompartido(),
            CancionDesafinada(),
            CalimotxoMagico(),
            HieloTraicionero(),
            LlamadaAlTaxi(),
            UltimoVaso()
        ]
    
    def regenerar(self):
        super().regenerar()
        # El Botellón bebe solo y recupera energía extra
        if random.random() < 0.3:
            self.energia_actual = min(self.energia_maxima, self.energia_actual + 15)
            self._litros_bebidos += 1
            print(f"{C.AZUL}¡{self.nombre} se bebe una birra! Energía +15. Litros: {self._litros_bebidos}{C.RESET}")
```

### Archivo `habilidades/habilidades_botellon.py`

```python
from .habilidad_base import Habilidad
from utils import Colores as C
import random

class BotellinCompartido(Habilidad):
    def __init__(self):
        super().__init__(
            nombre="Botellín Compartido",
            descripcion="Invita a un botellín. El enemigo baja la guardia (defensa -10) y recibe daño.",
            costo_energia=15,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        daño = objetivo.recibir_dano(usuario.ataque // 3, "alcohol")
        objetivo.defensa = max(5, objetivo.defensa - 10)
        objetivo.aplicar_estado("confiado", duracion=2)
        print(f"{C.AMARILLO}¡Salud! {objetivo.nombre} baja la guardia.{C.RESET}")
        return {"exito": True, "daño": daño, "defensa_reducida": 10}

class CancionDesafinada(Habilidad):
    def __init__(self):
        super().__init__(
            nombre="Canción Desafinada",
            descripcion="Canta horrible. Puede confundir al enemigo.",
            costo_energia=20,
            tipo="estado"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        daño = objetivo.recibir_dano(usuario.ataque // 2, "ruido")
        if random.random() < 0.5:
            objetivo.aplicar_estado("confundido", duracion=1)
            print(f"{C.MAGENTA}¡{objetivo.nombre} se confunde con la desafinación!{C.RESET}")
        return {"exito": True, "daño": daño}

class CalimotxoMagico(Habilidad):
    def __init__(self):
        super().__init__(
            nombre="Calimotxo Mágico",
            descripcion="Bebida ancestral que cura 30 de vida y da energía extra.",
            costo_energia=25,
            tipo="defensiva"
        )
        self.es_curacion = True
    
    def usar(self, usuario, objetivo):
        vida_curada = usuario.recibir_curacion(30)
        usuario.energia_actual = min(usuario.energia_maxima, usuario.energia_actual + 20)
        print(f"{C.VERDE}¡Calimotxo mágico! +{vida_curada} vida, +20 energía.{C.RESET}")
        return {"exito": True, "curacion": vida_curada, "energia_recuperada": 20}

class HieloTraicionero(Habilidad):
    def __init__(self):
        super().__init__(
            nombre="Hielo Traicionero",
            descripcion="Lanza un hielo del botellón. Daño y posibilidad de congelar.",
            costo_energia=30,
            tipo="ofensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        daño = objetivo.recibir_dano(usuario.ataque * 2, "hielo")
        if random.random() < 0.3:
            objetivo.aplicar_estado("congelado", duracion=1)
            print(f"{C.CYAN}¡{objetivo.nombre} queda congelado!{C.RESET}")
        return {"exito": True, "daño": daño}

class LlamadaAlTaxi(Habilidad):
    def __init__(self):
        super().__init__(
            nombre="Llamada al Taxi",
            descripcion="Pide un taxi y huye del peligro. Aumenta velocidad y defensa.",
            costo_energia=35,
            tipo="defensiva"
        )
        self.es_curacion = False
    
    def usar(self, usuario, objetivo):
        usuario.velocidad += 20
        usuario.defensa += 15
        print(f"{C.AZUL}¡Taxi! Velocidad +20, Defensa +15 (1 turno).{C.RESET}")
        return {"exito": True, "velocidad_aumentada": 20, "defensa_aumentada": 15}

class UltimoVaso(Habilidad):
    def __init__(self):
        super().__init__(
            nombre="Último Vaso",
            descripcion="Se toma el último vaso. Recupera toda la vida pero se emborracha.",
            costo_energia=50,
            tipo="especial"
        )
        self.es_curacion = True
    
    def usar(self, usuario, objetivo):
        vida_curada = usuario.vida_maxima - usuario.vida_actual
        usuario.vida_actual = usuario.vida_maxima
        usuario.aplicar_estado("borracho", duracion=3)
        print(f"{C.VERDE_BRILLANTE}¡Último vaso! Vida restaurada al máximo. ¡Está BORRACHO!{C.RESET}")
        return {"exito": True, "curacion": vida_curada, "estado": "borracho"}
```

### Archivo `eventos/eventos_aleatorios.py` (fragmento)

```python
class BotellonSorpresaMejorado(EventoBase):
    def __init__(self):
        super().__init__(
            nombre="🍾 BOTELLÓN SORPRESA MEJORADO",
            descripcion="Aparece un botellón de categoría. Todos beben y se divierten.",
            tipo="raro"
        )
    
    def activar(self, jugador, enemigo, turno_actual):
        curacion_j = jugador.recibir_curacion(25)
        curacion_e = enemigo.recibir_curacion(25)
        jugador.aplicar_estado("mareado", duracion=2)
        enemigo.aplicar_estado("mareado", duracion=2)
        mensaje = (f"{C.VERDE}¡BOTELLÓN SORPRESA MEJORADO!{C.RESET}\n"
                   f"Todos beben y se divierten.\n"
                   f"{jugador.nombre} recupera {curacion_j} de vida.\n"
                   f"{enemigo.nombre} recupera {curacion_e} de vida.\n"
                   f"¡Ambos están MAREADOS!")
        return {"exito": True, "mensaje": mensaje, "tipo": "mixto"}

# Añadir a EVENTOS_RAROS
EVENTOS_RAROS.append(BotellonSorpresaMejorado)
```

**¡Ya tienes tu primer mod funcional!**

---

## 🧹 Buenas prácticas y advertencias

1. **No modifiques los archivos originales si no es necesario.**  
   Siempre que puedas, crea archivos nuevos y añade tu código mediante imports.

2. **Usa nombres únicos.**  
   Evita sobrescribir clases existentes. Si tu personaje se llama `Segarro`, el juego se romperá. Prefijo recomendado: `MiSegarro`, `SegarroPlus`, etc.

3. **Prueba tu mod en un entorno separado.**  
   Haz una copia del juego y prueba allí antes de distribuirlo.

4. **Documenta tu mod.**  
   Incluye un archivo `README.md` dentro de tu mod explicando qué hace, cómo instalarlo y los créditos.

5. **Respeta la licencia.**  
   No elimines los créditos del autor original. Añade los tuyos, pero conserva los existentes.

6. **Cuidado con el balance.**  
   Un personaje con 999 de vida y ataque infinito no es divertido. Busca el equilibrio.

7. **Mantén la coherencia con el estilo del juego.**  
   Humor español, situaciones absurdas y referencias culturales son bienvenidas.

---

## 📦 Distribución de mods

Puedes distribuir tu mod como:

- **Archivo comprimido (.zip)** con los archivos modificados y una guía de instalación.
- **Script de instalación** que copie los archivos a las carpetas correspondientes.
- **Publicación en foros** (ej. Discord del juego, Reddit, itch.io).

**NO** incluyas el juego completo. Solo los archivos que has creado o modificado.

---

## ❓ ¿Dudas o sugerencias?

Si tienes preguntas sobre el modding, puedes contactar con el creador original o abrir un issue en el repositorio oficial (si está disponible).

**¡Esperamos ver tus creaciones!**  
Que la fuerza del jamón te acompañe. 🍖🇪🇸

---

© 2026 Luis Villegas Rivera. Esta guía se distribuye bajo la misma licencia que el juego.  
Permitida su reproducción y modificación para uso no comercial, manteniendo los créditos.