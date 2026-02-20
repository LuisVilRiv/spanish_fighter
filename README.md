# 🥊 Batalla Cómica Española

> Juego de combate por turnos con personajes surrealistas del imaginario español. Hecho con Python y [arcade](https://api.arcade.academy/).

---

## 🎮 ¿Qué es esto?

Elige a tu luchador entre una plantilla de personajes variopintos —la abuela, el torero, el político corrupto, el flaquito del barrio— y enfréntate en combates por turnos llenos de habilidades absurdas y eventos aleatorios sacados de la España más profunda.

Puedes jugar en solitario contra la IA, o montar equipos de hasta 4 personajes en batallas épicas.

---

## ✨ Características actuales

**Modos de juego**
- 1 vs 1, 2 vs 2, 3 vs 3 y 4 vs 4
- Cada slot de personaje es configurable como **Jugador** o **IA** de forma independiente
- Partidas completamente contra IA, completamente manuales, o cualquier mezcla

**Sistema de combate**
- Turno por turno con orden de actuación por velocidad (+ varianza aleatoria)
- 4 acciones básicas: **Atacar**, **Defender**, **Concentrar** (recuperar energía), **Habilidad especial**
- Cada personaje tiene **6 habilidades únicas** con coste de energía
- Sistema de tipos: debilidades, fortalezas e inmunidades
- Estados alterados: dormido, paralizado, confundido, quemado, sangrando, envenenado, bajón de azúcar
- Regeneración de vida/energía entre rounds
- Historial de combate navegable tras cada batalla

**Eventos aleatorios**
- Se activan aleatoriamente al final de cada round
- Tres raridades: normales, raros y ultra-raros
- Incluyen consecuencias absurdas: la vecina del 3B, la huelga general, la siesta repentina, el concurso de tapas, la furgoneta blanca, y muchos más

**Interfaz gráfica**
- GUI completa con arcade (ventana redimensionable, F11 para pantalla completa)
- Sprites de personaje, barras de vida/energía, log de combate en tiempo real
- Pantalla de información de personajes con estadísticas y descripción
- Pantalla de instrucciones

**Sistema de guardado** *(modo 1v1)*
- 3 slots de partida independientes
- Guardado cifrado con **AES-128 (Fernet) + HMAC-SHA256** — archivos `.dat` no legibles ni modificables externamente

**Extras**
- EULA obligatorio en el primer arranque
- Soporte para mods (ver `MODDING.md`)
- Logger de debug interno (`debug_logger.py`)

---

## 🧑‍🤝‍🧑 Plantilla de personajes

| Personaje | Tipo |
|---|---|
| Segarro | El Buscavidas |
| Católico | El Devoto |
| Sacerdote | El Hombre de Dios |
| Turista | El Guiri Perdido |
| Abuela | La Matriarca |
| Político | El Prometedor |
| Torero | El Arte |
| Flaquito | El del Barrio |
| Choni | La Guerrera |
| El Puto Amo | El Infalible |
| Barrendero | El Invisible |

---

## 📁 Estructura del proyecto

```
spanish_fighter/
│
├── main.py                        # Punto de entrada
│
├── scenes/                        # Pantallas de la aplicación
│   ├── base_view.py               # Clase base de todas las vistas
│   ├── eula_scene.py              # EULA (primer arranque)
│   ├── menu_scene.py              # Menú principal
│   ├── mode_select_scene.py       # Selección de modo (1v1 … 4v4)
│   ├── character_select_scene.py  # Selección de personaje (modo 1v1)
│   ├── team_select_scene.py       # Selección de equipo (modo equipo)
│   ├── combat_scene.py            # Combate 1v1
│   ├── combat_team_scene.py       # Combate por equipos
│   ├── historial_scene.py         # Historial de combate post-batalla
│   ├── characters_info_scene.py   # Ficha de cada personaje
│   ├── instructions_scene.py      # Instrucciones
│   └── save_slot_scene.py         # Gestión de slots de guardado
│
├── combate/
│   ├── sistema_combate.py         # Motor de combate 1v1
│   └── sistema_combate_equipo.py  # Motor de combate por equipos
│
├── personajes/
│   ├── personaje_base.py          # Clase base abstracta
│   ├── segarro.py
│   ├── catolico.py
│   ├── sacerdote.py
│   ├── turista.py
│   ├── abuela.py
│   ├── politico.py
│   ├── torero.py
│   ├── flaquito.py
│   ├── choni.py
│   ├── putamo.py
│   └── barrendero.py
│
├── habilidades/
│   ├── habilidad_base.py          # Clase base abstracta
│   └── habilidades_*.py           # Habilidades de cada personaje
│
├── eventos/
│   └── eventos_aleatorios.py      # Pool de eventos (normal / raro / ultra-raro)
│
├── gui/
│   └── widgets.py                 # ImageButton, RetroLabel, HealthBar
│
├── img/
│   ├── personajes/                # Sprites PNG de cada personaje
│   └── fondos/                    # Imágenes de fondo
│
├── saves/                         # Partidas guardadas (.dat) — generado automáticamente
│
├── sistema_guardado.py            # Cifrado AES + HMAC para los saves
├── debug_logger.py                # Logger interno de depuración
├── utils/                         # Colores de consola y utilidades
│
├── MODDING.md                     # Guía para crear personajes y eventos propios
├── requirements.txt
└── README.md
```

---

## 📦 Instalación

**Requisitos:** Python 3.10 o superior.

```bash
# 1. Clona el repositorio
git clone https://github.com/tu-usuario/spanish_fighter.git
cd spanish_fighter

# 2. (Recomendado) Crea un entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 3. Instala las dependencias
pip install -r requirements.txt
```

`requirements.txt` incluye:
- `arcade` — motor gráfico
- `cryptography>=42.0.0` — cifrado de partidas guardadas

---

## ▶️ Arrancar el juego

```bash
python main.py
```

En el primer arranque aparecerá el EULA. Una vez aceptado, se accede al menú principal.

**Atajos de teclado:**
- `F11` — alternar pantalla completa / ventana
- `←` `→` — navegar páginas en el historial de combate

---

## 🕹️ Cómo se juega

1. Desde el menú principal elige **Nueva Partida** o **Combate Rápido**.
2. Selecciona el **modo** (1v1, 2v2, 3v3 o 4v4).
3. Elige tu **personaje** (y el de la IA en modo 1v1, o configura cada slot en modo equipo).
4. En tu turno dispones de cuatro acciones:

| Acción | Efecto |
|---|---|
| ⚔️ **Atacar** | Golpe básico. Daño = ataque - defensa rival |
| 🛡️ **Defender** | Reduce el daño del siguiente golpe recibido |
| ⚡ **Concentrar** | Recupera energía para usar habilidades |
| ✨ **Habilidad** | Activa una de tus 6 habilidades especiales |

5. Al terminar el combate puedes ver el **Historial** completo (acción por acción, con eventos incluidos), pedir **Revancha** o volver al **Menú**.

---

## 🧩 Modding

¿Quieres crear tu propio personaje o evento? Consulta la guía detallada en [`MODDING.md`](MODDING.md). Incluye ejemplos completos de personaje, habilidades y eventos aleatorios.

---

## 📄 Licencia

Todos los derechos reservados. Se permite crear y distribuir mods gratuitos, siempre que no se eliminen los créditos originales ni se redistribuya el juego base completo. Consulta `LICENSE.txt` para los términos completos.

**Autor:** Luis Villegas Rivera · 2026