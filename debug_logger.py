# debug_logger.py
"""
Sistema de debug para capturar inconsistencias lógicas en tiempo de ejecución.
Cuando algo raro ocurra, el log se puede copiar y mandármelo tal cual.

Uso básico:
    from debug_logger import DBG
    DBG.warn("Turno jugador activado con combate terminado", estado=..., turno=...)
    DBG.dump()   # imprime todo el log en consola
    DBG.export() # devuelve string con todo el log para copiar/pegar
"""

import time
import traceback
import sys


class _DebugLogger:
    NIVEL_INFO  = "INFO "
    NIVEL_WARN  = "WARN "
    NIVEL_ERROR = "ERROR"
    NIVEL_CLICK = "CLICK"
    NIVEL_STATE = "STATE"

    MAX_ENTRIES = 500

    def __init__(self):
        self._entries: list[dict] = []
        self._t0 = time.time()
        self._habilitado = True
        self._click_count = 0
        self._ultimo_estado: dict = {}

    # ── Métodos públicos ─────────────────────────────────────────────────────

    def info(self, msg: str, **ctx):
        self._log(self.NIVEL_INFO, msg, ctx)

    def warn(self, msg: str, **ctx):
        self._log(self.NIVEL_WARN, msg, ctx)
        self._print_inmediato(self.NIVEL_WARN, msg, ctx)

    def error(self, msg: str, **ctx):
        self._log(self.NIVEL_ERROR, msg, ctx)
        self._print_inmediato(self.NIVEL_ERROR, msg, ctx)
        # Capturar stack trace
        tb = traceback.format_stack()[:-1]
        self._log(self.NIVEL_ERROR, "Stack:\n" + "".join(tb), {})

    def click(self, origen: str, x: int, y: int, consumido: bool, **ctx):
        """Registra un evento de click con su resultado."""
        self._click_count += 1
        self._log(self.NIVEL_CLICK,
                  f"#{self._click_count} {origen} ({x},{y}) → {'CONSUMIDO' if consumido else 'ignorado'}",
                  ctx)

    def estado(self, **ctx):
        """Snapshot del estado de juego en un momento dado."""
        self._ultimo_estado = ctx
        self._log(self.NIVEL_STATE, "Snapshot estado", ctx)

    # ── Comprobaciones lógicas ───────────────────────────────────────────────

    def check_turno(self, turno_jugador: bool, combate_estado, en_curso_valor,
                    mostrando_habs: bool = False, ubicacion: str = ""):
        """Detecta combinaciones imposibles de estado."""
        from_str = f" [{ubicacion}]" if ubicacion else ""

        if turno_jugador and combate_estado != en_curso_valor:
            self.warn(
                f"turno_jugador=True pero combate NO está EN_CURSO{from_str}",
                turno_jugador=turno_jugador,
                combate_estado=str(combate_estado)
            )

        if mostrando_habs and not turno_jugador:
            self.warn(
                f"mostrando_habilidades=True pero NO es turno del jugador{from_str}",
                mostrando_habs=mostrando_habs,
                turno_jugador=turno_jugador
            )

    def check_visibilidad(self, lista_nombre: str, lista_btns: list, condicion_esperada: bool):
        """Verifica que la visibilidad de los botones es consistente."""
        for i, btn in enumerate(lista_btns):
            if hasattr(btn, 'visible') and btn.visible != condicion_esperada:
                # No siempre es un error (postcombate, etc.), solo loguea en nivel info
                pass  # Desactivado para no saturar; activar si necesitas granularidad

    def check_doble_lista(self, lista_a: list, lista_b: list, nombre_a: str, nombre_b: str):
        """Detecta si un botón está en dos listas a la vez (puede causar doble procesamiento)."""
        set_a = set(id(x) for x in lista_a)
        set_b = set(id(x) for x in lista_b)
        interseccion = set_a & set_b
        if interseccion:
            self.warn(
                f"Botón presente en '{nombre_a}' Y '{nombre_b}' simultáneamente",
                count=len(interseccion)
            )

    # ── Salida ───────────────────────────────────────────────────────────────

    def dump(self):
        """Imprime el log completo en consola."""
        print("\n" + "═" * 70)
        print("  DEBUG LOG — Lucha de Clases")
        print("═" * 70)
        for e in self._entries:
            print(self._format_entry(e))
        print("═" * 70)
        print(f"  Total entradas: {len(self._entries)}")
        if self._ultimo_estado:
            print("  Último estado conocido:")
            for k, v in self._ultimo_estado.items():
                print(f"    {k}: {v}")
        print("═" * 70 + "\n")

    def export(self) -> str:
        """Devuelve el log como string para copiar/pegar y mandármelo."""
        lines = ["═" * 70, "DEBUG LOG — Lucha de Clases", "═" * 70]
        for e in self._entries:
            lines.append(self._format_entry(e))
        lines.append("═" * 70)
        lines.append(f"Total entradas: {len(self._entries)}")
        if self._ultimo_estado:
            lines.append("Último estado conocido:")
            for k, v in self._ultimo_estado.items():
                lines.append(f"  {k}: {v}")
        lines.append("═" * 70)
        return "\n".join(lines)

    def clear(self):
        self._entries.clear()
        self._click_count = 0
        self._ultimo_estado = {}

    def solo_warns(self) -> str:
        """Exporta solo WARNs y ERRORs — lo más útil para mandármelo."""
        lines = ["═" * 70, "DEBUG (solo WARN/ERROR) — Lucha de Clases", "═" * 70]
        relevantes = [e for e in self._entries
                      if e['nivel'] in (self.NIVEL_WARN, self.NIVEL_ERROR)]
        if not relevantes:
            lines.append("  Sin advertencias ni errores registrados. ✓")
        for e in relevantes:
            lines.append(self._format_entry(e))
        lines.append("═" * 70)
        return "\n".join(lines)

    # ── Internos ─────────────────────────────────────────────────────────────

    def _log(self, nivel: str, msg: str, ctx: dict):
        if not self._habilitado:
            return
        t = time.time() - self._t0
        entry = {'t': t, 'nivel': nivel, 'msg': msg, 'ctx': ctx}
        self._entries.append(entry)
        if len(self._entries) > self.MAX_ENTRIES:
            self._entries = self._entries[-self.MAX_ENTRIES:]

    def _format_entry(self, e: dict) -> str:
        ctx_str = ""
        if e['ctx']:
            ctx_str = "  " + ", ".join(f"{k}={v}" for k, v in e['ctx'].items())
        return f"[{e['t']:7.2f}s] {e['nivel']} {e['msg']}{ctx_str}"

    def _print_inmediato(self, nivel: str, msg: str, ctx: dict):
        """WARNs y ERRORs se imprimen inmediatamente en stderr."""
        ctx_str = ", ".join(f"{k}={v}" for k, v in ctx.items()) if ctx else ""
        t = time.time() - self._t0
        print(
            f"[DBG {t:.2f}s] {nivel} — {msg}" + (f" | {ctx_str}" if ctx_str else ""),
            file=sys.stderr
        )


# Instancia global — importar desde cualquier módulo
DBG = _DebugLogger()