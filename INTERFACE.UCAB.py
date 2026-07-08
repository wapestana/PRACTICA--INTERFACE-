from tkinter import *
from PIL import Image, ImageTk
import os

# ---------------- Configuración ----------------
BG = "#3DA5dc"
UCAB_YELLOW = "#f9c32b"
UCAB_BLUE = "#0072CE"
UCAB_GREEN = "#008343"
TEXT_DARK = "#131514"
TEXT_LIGHT = "#ffffff"
HOVER_FACTOR = 0.92

# Ruta de la imagen de fondo: pon el nombre exacto o ruta absoluta
FONDO_RUTA = "fondo.ucab.png"

# ---------------- Ventana principal ----------------
root = Tk()
root.title("El Ucabista - Desafío Digital")
root.geometry("960x640")
root.minsize(640, 420)
root.resizable(True, True)

# ---------------- Canvas principal ----------------
main_canvas = Canvas(root, highlightthickness=0)
main_canvas.pack(fill="both", expand=True)

# Variables para la imagen de fondo
fondo_pil = None
bg_photo = None
darkness_factor = 0.45
resize_timer = None

def cargar_imagen_fondo(ruta):
    if not os.path.exists(ruta):
        print(f"No se encontró el archivo de fondo: {ruta}")
        return None
    try:
        img = Image.open(ruta).convert("RGBA")
        return img
    except Exception as e:
        print("No se pudo cargar imagen de fondo:", e)
        return None

fondo_pil = cargar_imagen_fondo(FONDO_RUTA)

def aplicar_oscurecimiento(img_pil, factor):
    if factor <= 0:
        return img_pil
    overlay = Image.new("RGBA", img_pil.size, (0, 0, 0, int(255 * factor)))
    base = img_pil.copy()
    return Image.alpha_composite(base, overlay)

def actualizar_fondo_cover():
    global bg_photo
    if fondo_pil is None:
        main_canvas.config(bg=BG)
        return

    W = max(1, main_canvas.winfo_width())
    H = max(1, main_canvas.winfo_height())

    img_w, img_h = fondo_pil.size
    scale = max(W / img_w, H / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    img_resized = fondo_pil.resize((new_w, new_h), Image.Resampling.LANCZOS)

    left = (new_w - W) // 2
    top = (new_h - H) // 2
    img_cropped = img_resized.crop((left, top, left + W, top + H))

    img_dark = aplicar_oscurecimiento(img_cropped, darkness_factor)

    bg_photo = ImageTk.PhotoImage(img_dark)
    if getattr(main_canvas, "bg_id", None):
        main_canvas.itemconfig(main_canvas.bg_id, image=bg_photo)
    else:
        main_canvas.bg_id = main_canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        main_canvas.tag_lower(main_canvas.bg_id)

# ---------------- UI dibujada sobre el canvas ----------------

entrada_widget = Entry(
    root,
    font=("Arial", 12),
    justify="center",
    width=24,
    bd=1,
    relief="solid",
    bg=TEXT_LIGHT,
    fg=TEXT_DARK,
    highlightthickness=1,
    highlightbackground="#aaaaaa",
    highlightcolor=UCAB_BLUE
)
entrada_widget.config(insertbackground=TEXT_DARK)

def cargar_logo(ruta, ancho_max):
    try:
        if not os.path.exists(ruta):
            return None
        img = Image.open(ruta)
        ancho = min(ancho_max, img.size[0])
        w_porcent = ancho / float(img.size[0])
        h_size = int(float(img.size[1]) * w_porcent)
        img = img.resize((ancho, h_size), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print("No se pudo cargar logo:", e)
        return None

logo_img = cargar_logo("Logo_UCAB.png", 160)

# ---------------- Utilidades y prismas ----------------
def clamp(v, a=0, b=255):
    return max(a, min(b, int(v)))

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0,2,4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def adjust_brightness(hexcol, factor):
    r,g,b = hex_to_rgb(hexcol)
    r = clamp(r * factor); g = clamp(g * factor); b = clamp(b * factor)
    return rgb_to_hex((r,g,b))

# NUEVA FORMA: 12 puntos para simular el hexágono con colitas horizontales
def prisma_points(xc, yc, w, h):
    tail_w = w * 0.12      # Largo de las colitas laterales
    tail_h = h * 0.12      # Grosor de las colitas
    chamfer = w * 0.12     # Inclinación de los cortes del hexágono
    body_w = w - (2 * tail_w)
    
    half_body = body_w / 2
    half_h = h / 2
    half_tail_h = tail_h / 2
    half_w = w / 2

    return [
        xc - half_body + chamfer, yc - half_h,          # Arriba Izquierda
        xc + half_body - chamfer, yc - half_h,          # Arriba Derecha
        xc + half_body, yc - half_tail_h,               # Intersección Cola Derecha (Arriba)
        xc + half_w, yc - half_tail_h,                  # Punta Cola Derecha (Arriba)
        xc + half_w, yc + half_tail_h,                  # Punta Cola Derecha (Abajo)
        xc + half_body, yc + half_tail_h,               # Intersección Cola Derecha (Abajo)
        xc + half_body - chamfer, yc + half_h,          # Abajo Derecha
        xc - half_body + chamfer, yc + half_h,          # Abajo Izquierda
        xc - half_body, yc + half_tail_h,               # Intersección Cola Izquierda (Abajo)
        xc - half_w, yc + half_tail_h,                  # Punta Cola Izquierda (Abajo)
        xc - half_w, yc - half_tail_h,                  # Punta Cola Izquierda (Arriba)
        xc - half_body, yc - half_tail_h                # Intersección Cola Izquierda (Arriba)
    ]

def nombre_usuario(*args):
    texto_actual = entrada_widget.get()
    texto_limpio = "".join(letra.upper() for letra in texto_actual if letra.isalpha())
    if texto_actual != texto_limpio:
        var_nombre.set(texto_limpio)

def abrir_ventana_apensar():
    n = nombre_usuario()
    v = Toplevel(root)
    v.title("Apensar - UCAB")
    v.geometry("480x360")
    v.config(bg=UCAB_YELLOW)
    Label(v, text="¡Bienvenido al juego de Apensar,", font=("Arial", 16, "bold"),
          bg=UCAB_YELLOW, fg=TEXT_DARK).pack(pady=(40,4))
    Label(v, text=n, font=("Arial", 16, "bold"), bg=UCAB_YELLOW, fg=TEXT_DARK).pack(pady=(0,20))
    Button(v, text="Cerrar", command=v.destroy, bg=TEXT_DARK, fg=TEXT_LIGHT,
           font=("Arial", 11, "bold"), padx=12, pady=6).pack(pady=8)

def abrir_ventana_trivia():
    n = nombre_usuario()
    v = Toplevel(root)
    v.title("Trivia - UCAB")
    v.geometry("480x360")
    v.config(bg=UCAB_BLUE)
    Label(v, text="¡Bienvenido al juego de Trivia,", font=("Arial", 16, "bold"),
          bg=UCAB_BLUE, fg=TEXT_LIGHT).pack(pady=(40,4))
    Label(v, text=n, font=("Arial", 16, "bold"), bg=UCAB_BLUE, fg=TEXT_LIGHT).pack(pady=(0,20))
    Button(v, text="Cerrar", command=v.destroy, bg=TEXT_LIGHT, fg=UCAB_BLUE,
           font=("Arial", 11, "bold"), padx=12, pady=6).pack(pady=8)

def abrir_ventana_wordle():
    n = nombre_usuario()
    v = Toplevel(root)
    v.title("Wordle - UCAB")
    v.geometry("480x360")
    v.config(bg=UCAB_GREEN)
    Label(v, text="¡Bienvenido al juego de Wordle,", font=("Arial", 16, "bold"),
          bg=UCAB_GREEN, fg=TEXT_LIGHT).pack(pady=(40,4))
    Label(v, text=n, font=("Arial", 16, "bold"), bg=UCAB_GREEN, fg=TEXT_LIGHT).pack(pady=(0,20))
    Button(v, text="Cerrar", command=v.destroy, bg=TEXT_LIGHT, fg=UCAB_GREEN,
           font=("Arial", 11, "bold"), padx=12, pady=6).pack(pady=8)

def create_text_with_shadow(canvas, x, y, text, font, fill, shadow_color="#000000", offset=(1,1), tags=()):
    sx, sy = offset
    canvas.create_text(x + sx, y + sy, text=text, font=font, fill=shadow_color, tags=tags)
    return canvas.create_text(x, y, text=text, font=font, fill=fill, tags=tags)

# ---------------- Dibujado principal ----------------
def dibujar_ui():
    main_canvas.delete("ui")
    W = main_canvas.winfo_width() or 960
    H = main_canvas.winfo_height() or 640

    x_center = W / 2

    logo_h = 0
    if logo_img:
        logo_h = logo_img.height()

    y_top = max(int(0.18 * H), logo_h + 70)

    if logo_img:
        main_canvas.create_image(x_center, int(logo_h/2) + 12, image=logo_img, tags=("ui",))

    title_font = ("Century Gothic", max(18, int(H*0.03)), "bold")
    subtitle_font = ("Arial", max(11, int(H*0.017)), "normal")
    instruction_font = ("Arial", max(12, int(H*0.018)), "italic")

    create_text_with_shadow(main_canvas, x_center, y_top + 10,
                            "Bienvenidos al desafío ucabista",
                            title_font, TEXT_LIGHT, shadow_color="#000000", offset=(2,2), tags=("ui",))

    create_text_with_shadow(main_canvas, x_center, y_top + 48,
                            "Ingresa tu nombre de usuario para comenzar a jugar",
                            subtitle_font, TEXT_LIGHT, shadow_color="#000000", offset=(1,1), tags=("ui",))

    entrada_w = min(420, int(W * 0.32))
    main_canvas.create_window(
        x_center,
        y_top + 92,
        window=entrada_widget,
        width=entrada_w,
        height=34,
        tags=("ui", "entry_widget")
    )
    entrada_widget.focus_set()

    create_text_with_shadow(main_canvas, x_center, y_top + 132,
                            "Selecciona un juego para comenzar",
                            instruction_font, TEXT_LIGHT, shadow_color="#000000", offset=(1,1), tags=("ui",))

    # ALTURA REDUCIDA: Cambié el máximo de altura a 80 para que sean más chatos y alargados
    total_w = min(0.85 * W, 900)
    pr_w = (total_w - 40) / 3
    pr_h = min(0.35 * (H - (y_top + 260)), 80) 
    gap = 20
    start_x = (W - (3*pr_w + 2*gap)) / 2 + pr_w/2
    y_center = y_top + 320 

    def crear_prisma(xc, yc, w, h, color, texto, text_color, comando):
        # Actualizado para que use la nueva función sin el parámetro "neck_ratio"
        pts = prisma_points(xc, yc, w, h)
        poly = main_canvas.create_polygon(pts, fill=color, outline="", smooth=False, tags=("ui","prism"))
        txt = main_canvas.create_text(xc, yc, text=texto, font=("Arial", max(12, int(pr_w/12)), "bold"), fill=text_color, tags=("ui","prism"))
        
        def on_enter(e, base=color, item=poly):
            main_canvas.itemconfig(item, fill=adjust_brightness(base, HOVER_FACTOR))
        def on_leave(e, base=color, item=poly):
            main_canvas.itemconfig(item, fill=base)
        def on_click(e, cmd=comando):
            cmd()
            
        for item in (poly, txt):
            main_canvas.tag_bind(item, "<Enter>", on_enter)
            main_canvas.tag_bind(item, "<Leave>", on_leave)
            main_canvas.tag_bind(item, "<Button-1>", on_click)

    crear_prisma(start_x, y_center, pr_w, pr_h, UCAB_YELLOW, "Apensar", TEXT_DARK, abrir_ventana_apensar)
    crear_prisma(start_x + pr_w + gap, y_center, pr_w, pr_h, UCAB_BLUE, "Trivia", TEXT_LIGHT, abrir_ventana_trivia)
    crear_prisma(start_x + 2*(pr_w + gap), y_center, pr_w, pr_h, UCAB_GREEN, "Wordle", TEXT_LIGHT, abrir_ventana_wordle)

    btn_w = 160
    btn_h = 40
    bx = W - btn_w/2 - 18
    by = H - btn_h/2 - 18
    rect = main_canvas.create_rectangle(bx - btn_w/2, by - btn_h/2, bx + btn_w/2, by + btn_h/2,
                                        fill="red", outline="", tags=("ui","btn"))
    txt = main_canvas.create_text(bx, by, text="Salir del juego :(", fill="white",
                                  font=("Arial", 11, "bold"), tags=("ui","btn"))
    
    def salir_click(e=None):
        root.destroy()
        
    for item in (rect, txt):
        main_canvas.tag_bind(item, "<Button-1>", lambda e: salir_click())

def reposicionar_widgets():
    actualizar_fondo_cover()
    dibujar_ui()

def on_configure(event):
    global resize_timer
    if resize_timer is not None:
        root.after_cancel(resize_timer)
    resize_timer = root.after(100, reposicionar_widgets)

root.bind("<Configure>", on_configure)

root.after(100, reposicionar_widgets)
root.mainloop()