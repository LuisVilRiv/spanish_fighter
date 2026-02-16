import os
from PIL import Image, ImageDraw, ImageFont

def crear_carpetas():
    carpetas = [
        "img/personajes",
        "img/botones",
        "img/fondos"
    ]
    for carpeta in carpetas:
        os.makedirs(carpeta, exist_ok=True)

def generar_personaje(nombre, color_fondo, color_texto, texto):
    img = Image.new('RGB', (100, 100), color=color_fondo)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()
    draw.rectangle([0, 0, 99, 99], outline=(255,255,255), width=2)
    bbox = draw.textbbox((0,0), texto, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (100 - text_width) // 2
    y = (100 - text_height) // 2
    draw.text((x, y), texto, fill=color_texto, font=font)
    img.save(f"img/personajes/{nombre}.png")

def generar_boton(nombre, color, texto):
    img = Image.new('RGBA', (200, 60), color=(0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0,0,199,59], radius=10, fill=color, outline=(255,255,255), width=2)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0,0), texto, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (200 - text_width) // 2
    y = (60 - text_height) // 2
    draw.text((x, y), texto, fill=(255,255,255), font=font)
    img.save(f"img/botones/{nombre}.png")

def generar_fondo(nombre, color):
    img = Image.new('RGB', (1024, 768), color=color)
    draw = ImageDraw.Draw(img)
    for i in range(0, 1024, 50):
        draw.line([(i,0), (i-50,768)], fill=(100,100,100), width=1)
    for i in range(0, 768, 50):
        draw.line([(0,i), (1024,i-50)], fill=(100,100,100), width=1)
    img.save(f"img/fondos/{nombre}.png")

def generar_icono():
    img = Image.new('RGB', (32, 32), color=(255,0,0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([8,8,24,24], fill=(255,255,0), outline=(0,0,0))
    img.save("img/icono.png")

if __name__ == "__main__":
    crear_carpetas()

    # Personajes
    personajes = [
        ("segarro", (0,100,0), (255,255,255), "SEG"),
        ("catolico", (100,0,100), (255,255,255), "CAT"),
        ("sacerdote", (150,150,0), (0,0,0), "SAC"),
        ("turista", (0,100,150), (255,255,255), "TUR"),
        ("abuela", (150,0,0), (255,255,255), "ABU"),
        ("politico", (50,50,50), (255,255,0), "POL"),
        ("torero", (200,50,50), (255,255,255), "TOR"),
        ("flaquito", (255,200,100), (0,0,0), "FLA"),
        ("choni", (255,0,200), (0,0,0), "CHO"),
        ("putamo", (255,100,0), (0,0,0), "PUT"),
        ("barrendero", (0,150,150), (255,255,255), "BAR")
    ]
    for nombre, color, text_color, texto in personajes:
        generar_personaje(nombre, color, text_color, texto)

    # Botones (incluyendo aceptar, nueva partida, etc.)
    botones = [
        ("ataque", (150,50,50), "ATAQUE"),
        ("defender", (50,50,150), "DEFENDER"),
        ("concentrar", (50,150,50), "CONCENTRAR"),
        ("habilidad", (150,150,50), "HABILIDAD"),
        ("volver", (100,100,100), "VOLVER"),
        ("aceptar", (0,150,0), "ACEPTAR"),
        ("nueva_partida", (0,100,200), "NUEVA"),
        ("cargar_partida", (100,100,0), "CARGAR"),
        ("personajes", (150,0,150), "PERSONAJES"),
        ("instrucciones", (0,150,150), "INSTRUCCIONES")
    ]
    for nombre, color, texto in botones:
        generar_boton(nombre, color, texto)

    # Fondos
    fondos = ["menu", "combate", "eula"]
    colores = [(30,30,70), (70,30,30), (30,70,30)]
    for nombre, color in zip(fondos, colores):
        generar_fondo(nombre, color)

    # Icono
    generar_icono()

    print("✅ Imágenes placeholder generadas en la carpeta img/")