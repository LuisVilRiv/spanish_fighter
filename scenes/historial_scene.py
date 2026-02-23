# scenes/historial_scene.py
"""
HistorialView — muestra el historial de combate con tarjetas visuales.

Cada entrada se renderiza como una tarjeta con panel de fondo y
color codificado según el tipo:
  🎮  Verde   — acción del jugador humano
  🤖  Morado  — acción de la IA
  ⚡  Amarillo — evento aleatorio
  📋  Azul    — turno 1v1 (ResultadoTurno)
"""
import re as _re
import arcade
from scenes.base_view import BaseView
from gui.widgets import ImageButton, RetroLabel

# ── Cuántas tarjetas por página ───────────────────────────────────────────
CARDS_POR_PAGINA = 5

# ── Paletas por tipo de tarjeta ───────────────────────────────────────────
# (fill_body, border, fill_header, color_titulo)
CARD_JUGADOR = (
    (18, 38, 18, 215),
    (65, 170, 65, 200),
    (30, 65, 30),
    (140, 240, 140),
)
CARD_IA = (
    (30, 18, 40, 215),
    (150, 65, 180, 200),
    (55, 30, 70),
    (220, 150, 255),
)
CARD_EVENTO = (
    (42, 36, 8, 215),
    (210, 175, 30, 200),
    (75, 62, 12),
    (255, 230, 80),
)
CARD_1V1 = (
    (18, 24, 42, 215),
    (70, 105, 190, 200),
    (28, 42, 75),
    (140, 185, 255),
)

# Panel header/footer (igual que otras escenas)
COL_PANEL_BG     = (15, 17, 28, 220)
COL_PANEL_BORDER = (60, 65, 95, 200)


def _limpiar_ansi(texto: str) -> str:
    return _re.sub(r'\x1b\[[0-9;]*m', '', texto)


class HistorialView(BaseView):
    def __init__(self, app, historial: list, on_back=None):
        super().__init__(app)
        self.historial        = historial
        self.on_back_callback = on_back
        self.current_page     = 0

        self._card_data: list = []   # datos de rectángulos para on_draw
        self.ui_elements      = []
        self._w = app.width
        self._h = app.height
        self._setup_ui()

    # ── Configuración de UI ───────────────────────────────────────────────

    def _setup_ui(self):
        self.ui_elements.clear()
        self._card_data.clear()

        w, h = self.app.width, self.app.height
        self._w, self._h = w, h
        self.background_color = (22, 26, 38)

        # ── Zonas proporcionales (mismo patrón que characters_info_scene) ──
        HEADER_H   = max(52, int(h * 0.095))
        BTN_H      = max(36, int(h * 0.055))
        BTN_GAP    = max(8,  int(h * 0.012))
        MARGIN_BOT = max(12, int(h * 0.018))
        FOOTER_H   = MARGIN_BOT + BTN_H + BTN_GAP + BTN_H + MARGIN_BOT

        self._header_h = HEADER_H
        self._footer_h = FOOTER_H

        content_top = h - HEADER_H
        content_bot = FOOTER_H
        content_h   = content_top - content_bot

        # ── Header: título + contadores ────────────────────────────────────
        title_sz = max(18, int(HEADER_H * 0.42))
        self.ui_elements.append(RetroLabel(
            "HISTORIAL DEL COMBATE",
            w // 2, h - HEADER_H // 2,
            font_size=title_sz, color=(255, 220, 150),
            anchor_x='center', anchor_y='center'
        ))

        pag_sz     = max(11, int(HEADER_H * 0.22))
        total_pags = self._total_paginas()
        self.lbl_pagina = RetroLabel(
            f"Pág. {self.current_page + 1} / {total_pags}",
            w - int(w * 0.025), h - HEADER_H // 2,
            font_size=pag_sz, color=(160, 165, 195),
            anchor_x='right', anchor_y='center'
        )
        self.ui_elements.append(self.lbl_pagina)

        self.ui_elements.append(RetroLabel(
            f"{len(self.historial)} acciones",
            int(w * 0.025), h - HEADER_H // 2,
            font_size=max(10, int(HEADER_H * 0.20)),
            color=(110, 115, 145),
            anchor_x='left', anchor_y='center'
        ))

        # ── Footer: dos filas de botones ───────────────────────────────────
        nav_w   = int(min(w * 0.19, 180))
        back_w  = int(min(w * 0.23, 215))
        GAP_BTN = int(w * 0.020)

        # Fila 1 (más arriba): ANTERIOR | SIGUIENTE
        nav_y = MARGIN_BOT + BTN_H + BTN_GAP
        self.ui_elements.extend([
            ImageButton(
                x=w // 2 - nav_w - GAP_BTN, y=nav_y,
                width=nav_w, height=BTN_H,
                text="◀ ANTERIOR",
                normal_color=(75, 80, 115), hover_color=(105, 110, 160),
                callback=self.prev_page
            ),
            ImageButton(
                x=w // 2 + GAP_BTN, y=nav_y,
                width=nav_w, height=BTN_H,
                text="SIGUIENTE ▶",
                normal_color=(75, 80, 115), hover_color=(105, 110, 160),
                callback=self.next_page
            ),
        ])

        # Fila 2 (abajo): VOLVER
        self.ui_elements.append(ImageButton(
            x=w // 2 - back_w // 2, y=MARGIN_BOT,
            width=back_w, height=BTN_H,
            text="VOLVER",
            normal_color=(100, 105, 130), hover_color=(135, 140, 175),
            callback=self.back
        ))

        # ── Tarjetas de contenido ──────────────────────────────────────────
        CARD_GAP = max(6, int(content_h * 0.012))
        PAD_X    = int(w * 0.035)

        n_cards = CARDS_POR_PAGINA
        card_h  = (content_h - (n_cards + 1) * CARD_GAP) // n_cards
        card_w  = w - 2 * PAD_X

        start = self.current_page * CARDS_POR_PAGINA
        page  = self.historial[start:start + CARDS_POR_PAGINA]

        for idx, entrada in enumerate(page):
            card_y = content_top - CARD_GAP - (idx + 1) * card_h - idx * CARD_GAP
            self._build_card(
                entrada, start + idx + 1,
                PAD_X, card_y, card_w, card_h
            )

        # Sin entradas
        if not self.historial:
            self.ui_elements.append(RetroLabel(
                "No hay entradas en el historial.",
                w // 2, content_bot + content_h // 2,
                font_size=max(14, int(h * 0.025)),
                color=(140, 140, 160),
                anchor_x='center', anchor_y='center'
            ))

    def _build_card(self, entrada, numero: int,
                    cx: int, cy: int, cw: int, ch: int):
        """Construye una tarjeta visual: rect + etiquetas de texto."""
        _tipo, palette, lineas = self._parse_entrada(numero, entrada)

        fill, border, hdr_fill, hdr_color = palette

        HDR_H      = max(20, int(ch * 0.30))
        BODY_PAD_X = 14
        BODY_PAD_Y = 5
        body_h     = ch - HDR_H

        # Guardar rect para on_draw
        self._card_data.append({
            'cx': cx, 'cy': cy, 'cw': cw, 'ch': ch,
            'hdr_h': HDR_H, 'body_h': body_h,
            'fill': fill, 'border': border, 'hdr_fill': hdr_fill,
        })

        # ── Cabecera de la tarjeta ─────────────────────────────────────────
        titulo    = lineas[0] if len(lineas) > 0 else ""
        subtitulo = lineas[1] if len(lineas) > 1 else ""

        hdr_cy   = cy + body_h + HDR_H // 2
        title_sz = max(9, int(HDR_H * 0.40))
        sub_sz   = max(8, int(HDR_H * 0.32))

        if titulo:
            self.ui_elements.append(RetroLabel(
                titulo,
                cx + BODY_PAD_X, hdr_cy,
                font_size=title_sz, color=hdr_color,
                anchor_x='left', anchor_y='center'
            ))
        if subtitulo:
            self.ui_elements.append(RetroLabel(
                subtitulo,
                cx + cw - BODY_PAD_X, hdr_cy,
                font_size=sub_sz, color=(195, 195, 215),
                anchor_x='right', anchor_y='center'
            ))

        # ── Cuerpo de la tarjeta ───────────────────────────────────────────
        body_lines = lineas[2:]
        if not body_lines:
            return

        usable_h = body_h - 2 * BODY_PAD_Y
        line_h   = usable_h / max(len(body_lines), 1)
        font_sz  = max(8, int(min(line_h * 0.54, 13)))

        for i, line in enumerate(body_lines):
            if not line.strip():
                continue
            lx = cx + BODY_PAD_X + (14 if line.startswith("  ") else 0)
            ly = cy + body_h - BODY_PAD_Y - int(i * line_h) - int(line_h * 0.5)
            self.ui_elements.append(RetroLabel(
                line.strip(),
                lx, ly,
                font_size=font_sz,
                color=self._line_color(line),
                anchor_x='left', anchor_y='center'
            ))

    # ── Colores por tipo de línea ─────────────────────────────────────────

    @staticmethod
    def _line_color(line: str) -> tuple:
        s = line.strip()
        if s.startswith("⚔"):
            return (255, 115, 95)
        if s.startswith("💚"):
            return (95, 230, 125)
        if s.startswith("⚠"):
            return (255, 195, 70)
        if s.startswith("🎮"):
            return (130, 230, 130)
        if s.startswith("🤖"):
            return (210, 150, 255)
        if s.startswith("⚡"):
            return (255, 230, 80)
        return (190, 195, 215)

    # ── Parser de entradas ────────────────────────────────────────────────

    def _parse_entrada(self, numero: int, entrada) -> tuple:
        """
        Devuelve (tipo, palette, lineas).
        lineas[0] = titulo header   ej: '#1  🎮 Segarro [Eq.1]'
        lineas[1] = subtitulo       ej: '→ El Fatal [Eq.2]'
        lineas[2:] = cuerpo
        """
        # ── ResultadoAccion (modo equipo) ─────────────────────────────────
        if hasattr(entrada, 'descripcion'):
            actor_nom = getattr(entrada, 'actor_nombre', '') or ''
            es_evento = actor_nom.startswith("⚡")

            if es_evento:
                titulo = f"#{numero}  ⚡ EVENTO ALEATORIO"
                body   = [f"  {entrada.descripcion}"] + [
                    f"  {_limpiar_ansi(m)}"
                    for m in getattr(entrada, 'mensajes_extra', [])[:4]
                ]
                return 'evento', CARD_EVENTO, [titulo, ""] + body

            # Acción de personaje
            es_ia    = getattr(entrada, 'es_ia', False)
            eq_actor = getattr(entrada, 'actor_equipo', '')
            eq_obj   = getattr(entrada, 'objetivo_equipo', '')
            obj_nom  = getattr(entrada, 'objetivo_nombre', '') or ''
            ctrl     = "🤖" if es_ia else "🎮"
            eq_tag   = f" [Eq.{eq_actor}]" if eq_actor else ""
            palette  = CARD_IA if es_ia else CARD_JUGADOR

            titulo    = f"#{numero}  {ctrl} {actor_nom}{eq_tag}"
            subtitulo = (f"→ {obj_nom} [Eq.{eq_obj}]" if obj_nom else "")

            body = [f"  {entrada.descripcion}"]
            daño = getattr(entrada, 'daño', 0)
            cur  = getattr(entrada, 'curacion', 0)
            if daño:
                body.append(f"  ⚔ Daño: {daño}")
            if cur:
                body.append(f"  💚 Curación: {cur}")
            for m in getattr(entrada, 'mensajes_extra', [])[:3]:
                body.append(f"  ⚠ {_limpiar_ansi(m)}")

            tipo = 'ia' if es_ia else 'jugador'
            return tipo, palette, [titulo, subtitulo] + body

        # ── ResultadoTurno (modo 1v1) ─────────────────────────────────────
        jac = getattr(entrada, 'jugador_accion', '') or ''
        iac = getattr(entrada, 'ia_accion', '') or ''
        dj  = getattr(entrada, 'daño_jugador_a_ia', 0)
        de  = getattr(entrada, 'daño_ia_a_jugador', 0)
        cj  = getattr(entrada, 'curacion_jugador', 0)
        ci  = getattr(entrada, 'curacion_ia', 0)
        ev  = getattr(entrada, 'evento_aleatorio', None)

        titulo = f"#{numero}  📋 Turno 1v1"
        body   = []
        if jac:
            body.append(f"  🎮 {jac}")
        if iac:
            body.append(f"  🤖 {iac}")
        if dj:
            body.append(f"  ⚔ Daño a IA: {dj}")
        if de:
            body.append(f"  ⚔ Daño recibido: {de}")
        if cj:
            body.append(f"  💚 Cur. jugador: {cj}")
        if ci:
            body.append(f"  💚 Cur. IA: {ci}")
        if ev:
            nombre_ev = ev.get('nombre', 'Evento')
            body.append(f"  ⚡ {nombre_ev}")
            msg = _limpiar_ansi(ev.get('mensaje', ''))
            for l in msg.splitlines()[:2]:
                if l.strip():
                    body.append(f"    {l.strip()}")

        return '1v1', CARD_1V1, [titulo, ""] + body

    # ── Paginación ────────────────────────────────────────────────────────

    def _total_paginas(self) -> int:
        return max(1, (len(self.historial) + CARDS_POR_PAGINA - 1) // CARDS_POR_PAGINA)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._setup_ui()

    def next_page(self):
        if self.current_page < self._total_paginas() - 1:
            self.current_page += 1
            self._setup_ui()

    def back(self):
        if self.on_back_callback:
            self.on_back_callback()
        else:
            self.app.pop_view()

    # ── Render ────────────────────────────────────────────────────────────

    def on_draw(self):
        self.clear()
        w, h = self._w, self._h

        # Fondo base
        arcade.draw_rect_filled(
            arcade.XYWH(w // 2, h // 2, w, h),
            self.background_color
        )

        # Banda de header
        arcade.draw_rect_filled(
            arcade.LBWH(0, h - self._header_h, w, self._header_h),
            COL_PANEL_BG
        )
        arcade.draw_line(
            0, h - self._header_h,
            w, h - self._header_h,
            COL_PANEL_BORDER[:3], 1
        )

        # Banda de footer
        arcade.draw_rect_filled(
            arcade.LBWH(0, 0, w, self._footer_h),
            COL_PANEL_BG
        )
        arcade.draw_line(
            0, self._footer_h,
            w, self._footer_h,
            COL_PANEL_BORDER[:3], 1
        )

        # Tarjetas
        for cd in self._card_data:
            cx, cy, cw, ch   = cd['cx'], cd['cy'], cd['cw'], cd['ch']
            hdr_h            = cd['hdr_h']
            body_h           = cd['body_h']

            # Fondo cuerpo
            arcade.draw_rect_filled(
                arcade.LBWH(cx, cy, cw, body_h),
                cd['fill']
            )
            # Fondo cabecera
            arcade.draw_rect_filled(
                arcade.LBWH(cx, cy + body_h, cw, hdr_h),
                cd['hdr_fill']
            )
            # Borde exterior
            arcade.draw_rect_outline(
                arcade.LBWH(cx, cy, cw, ch),
                cd['border'], 2
            )
            # Línea divisoria cabecera/cuerpo
            arcade.draw_line(
                cx,      cy + body_h,
                cx + cw, cy + body_h,
                cd['border'][:3], 1
            )

        # Etiquetas y botones
        for elem in self.ui_elements:
            if hasattr(elem, 'draw'):
                elem.draw()

    # ── Eventos de entrada ────────────────────────────────────────────────

    def on_mouse_press(self, x, y, button, modifiers):
        # Bloquear el primer press (es el mismo click que abrió la vista)
        if self._block_next_press:
            return False
        return super().on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        super().on_mouse_motion(x, y, dx, dy)
        for elem in self.ui_elements:
            if hasattr(elem, 'on_mouse_motion'):
                elem.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.prev_page()
        elif symbol == arcade.key.RIGHT:
            self.next_page()
        elif symbol == arcade.key.ESCAPE:
            self.back()

    def on_resize(self, width, height):
        self._setup_ui()