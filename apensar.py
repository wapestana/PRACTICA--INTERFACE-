import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

# ====================================================================================
# CONFIGURACIÓN GENERAL Y ESTILOS
# ====================================================================================
BG = "#3DA5dc"
UCAB_YELLOW = "#FFCC00"
UCAB_BLUE = "#00599C"  
UCAB_GREEN = "#008343"
TEXT_DARK = "#131514"
TEXT_LIGHT = "#ffffff"
BG_APENSAR = "#C1E5F5" # Azul celeste de la nueva referencia
KEY_BLUE = "#2491D8"   # Azul de las teclas
KEY_SHADOW = "#145D8F" # Sombra de las teclas
HOVER_FACTOR = 0.92

FONDO_RUTA = "fondo.ucab.png"
LOGO_RUTA = "Logo_UCAB.png"

# Función para dibujar rectángulos redondeados
def create_rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    points = (
        x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, 
        x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, 
        x1, y2-r, x1, y1+r, x1, y1+r, x1, y1
    )
    return canvas.create_polygon(points, **kwargs, smooth=True)

# ====================================================================================
# JUEGO: APENSAR UCAB (NIVEL 1)
# ====================================================================================
class ApensarGame:
    def __init__(self, parent, user_name):
        self.parent = parent
        self.window = Toplevel(parent)
        self.window.title(f"Apensar - {user_name} (Nivel 1)")
        
        self.window.geometry("540x850")
        self.window.resizable(False, False) 
        
        self.user_name = user_name
        self.palabra_correcta = "LABORATORIOS"
        self.longitud = len(self.palabra_correcta)
        
        self.slots = [None] * self.longitud        
        self.slot_sources = [None] * self.longitud 
        self.monedas = 185 # Monedas de la referencia
        self.nivel = 12    # Nivel de la referencia
        
        self.rutas_imagenes = [
            "laboratoriosucab1.jpg",
            "laboratorioucab2.jpg",
            "laboratorioucab3.jpg",
            "laboratoriosucab.jpg"
        ]
        self.img_referencias = []
        
        self.canvas = Canvas(self.window, bg=BG_APENSAR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Iniciar el nivel directamente (saltando la pantalla inicial interna)
        self.iniciar_nivel()

    def dibujar_encabezado_juego(self):
        W = 540
        # Botón volver (<)
        lbl_back = self.canvas.create_text(30, 45, text="<", font=("Arial", 28, "bold"), fill=TEXT_LIGHT, tags=("ui", "btn_volver"))
        self.canvas.tag_bind(lbl_back, "<Button-1>", lambda e: self.window.destroy())
        
        # Título APENSAR
        self.canvas.create_text(115, 45, text="APENSAR", font=("Arial", 18, "bold"), fill=TEXT_LIGHT, tags="ui", anchor="w")
        
        # Insignia de Nivel (Estrella simulada con círculo amarillo)
        self.canvas.create_oval(W/2 + 20, 25, W/2 + 65, 70, fill=UCAB_YELLOW, outline=TEXT_LIGHT, width=2, tags="ui")
        self.canvas.create_text(W/2 + 42, 47, text=str(self.nivel), font=("Arial", 18, "bold"), fill=TEXT_LIGHT, tags="ui")

        # Insignia de Monedas
        self.canvas.create_oval(W - 130, 30, W - 95, 65, fill=UCAB_YELLOW, outline=TEXT_LIGHT, width=2, tags="ui")
        self.canvas.create_text(W - 112, 47, text="$", font=("Arial", 16, "bold"), fill="#D4A000", tags="ui")
        self.canvas.create_text(W - 60, 47, text=str(self.monedas), font=("Arial", 18, "bold"), fill=TEXT_LIGHT, tags="ui")

    # ---------------- Pantalla Principal del Nivel ----------------
    def iniciar_nivel(self):
        self.canvas.delete("ui")
        W, H = 540, 850
        x_center = W / 2

        self.dibujar_encabezado_juego()

        # ---------------- IMÁGENES (Estilo 4 fotos 1 bloque) ----------------
        img_size = 160
        gap_img = 4
        # Marco blanco de fondo que agrupa las 4 imágenes
        marco_x1 = x_center - img_size - gap_img
        marco_y1 = 120
        marco_x2 = x_center + img_size + gap_img
        marco_y2 = 120 + (img_size * 2) + (gap_img * 2)
        create_rounded_rect(self.canvas, marco_x1, marco_y1, marco_x2, marco_y2, 12, fill=TEXT_LIGHT, tags="ui")

        self.img_referencias = []
        for ruta in self.rutas_imagenes:
            try:
                if os.path.exists(ruta):
                    img = Image.open(ruta).convert("RGBA").resize((img_size, img_size), Image.Resampling.LANCZOS)
                    self.img_referencias.append(ImageTk.PhotoImage(img))
                else:
                    img_blank = Image.new("RGBA", (img_size, img_size), (200, 200, 200, 255))
                    self.img_referencias.append(ImageTk.PhotoImage(img_blank))
            except:
                pass

        coords_imagenes = [
            (x_center - img_size - gap_img/2, 120 + gap_img/2), 
            (x_center + gap_img/2, 120 + gap_img/2),
            (x_center - img_size - gap_img/2, 120 + img_size + gap_img * 1.5), 
            (x_center + gap_img/2, 120 + img_size + gap_img * 1.5)
        ]
        
        for idx, (bx, by) in enumerate(coords_imagenes):
            if idx < len(self.img_referencias):
                self.canvas.create_image(bx, by, image=self.img_referencias[idx], anchor="nw", tags="ui")

        # ---------------- SLOTS (Casillas de letras) ----------------
        tile_w = 34
        gap_slots = 6
        total_w_slots = self.longitud * (tile_w + gap_slots) - gap_slots
        start_x_slots = x_center - total_w_slots / 2 + tile_w / 2
        y_slots = 520

        for i in range(self.longitud):
            sx = start_x_slots + i * (tile_w + gap_slots)
            
            # Sombra gris sutil y cuadro blanco
            create_rounded_rect(self.canvas, sx - tile_w/2, y_slots - tile_w/2, sx + tile_w/2, y_slots + tile_w/2 + 2, 4, fill="#A5C1D1", tags=("ui", f"slot_bg_{i}"))
            box = create_rounded_rect(self.canvas, sx - tile_w/2, y_slots - tile_w/2, sx + tile_w/2, y_slots + tile_w/2, 4, fill=TEXT_LIGHT, tags=("ui", f"slot_box_{i}"))
            txt = self.canvas.create_text(sx, y_slots, text="", font=("Arial", 18, "bold"), fill=TEXT_DARK, tags=("ui", f"slot_txt_{i}"))
            
            for item in (box, txt):
                self.canvas.tag_bind(item, "<Button-1>", lambda e, idx=i: self.remover_letra(idx))

        # ---------------- TECLADO INFERIOR ----------------
        letras_correctas = list(self.palabra_correcta)
        distractores = ["M", "U"]
        self.letras_paleta = letras_correctas + distractores
        random.seed(42)
        random.shuffle(self.letras_paleta)

        y_palette_start = 620
        key_w = 26
        key_h = 28
        self.palette_items = []
        
        for idx, letra in enumerate(self.letras_paleta):
            row = idx // 7
            col = idx % 7
            # Centrado de las 7 teclas
            px = x_center - 195 + col * 65
            py = y_palette_start + row * 70
            
            # Sombra oscura (Efecto 3D)
            p_shadow = create_rounded_rect(self.canvas, px-key_w, py-key_h, px+key_w, py+key_h+6, 8, fill=KEY_SHADOW, tags=("ui", f"pal_sh_{idx}"))
            # Botón azul principal
            p_box = create_rounded_rect(self.canvas, px-key_w, py-key_h, px+key_w, py+key_h, 8, fill=KEY_BLUE, tags=("ui", f"pal_box_{idx}"))
            p_txt = self.canvas.create_text(px, py, text=letra, font=("Arial", 26, "bold"), fill=TEXT_LIGHT, tags=("ui", f"pal_txt_{idx}"))
            
            self.palette_items.append((p_shadow, p_box, p_txt))
            
            for item in (p_shadow, p_box, p_txt):
                self.canvas.tag_bind(item, "<Button-1>", lambda e, l=letra, i=idx: self.presionar_letra(l, i))

    def presionar_letra(self, letra, idx_paleta):
        for i in range(self.longitud):
            if self.slots[i] is None:
                self.slots[i] = letra
                self.slot_sources[i] = idx_paleta
                self.canvas.itemconfig(f"slot_txt_{i}", text=letra)
                
                p_shadow, p_box, p_txt = self.palette_items[idx_paleta]
                self.canvas.itemconfig(p_shadow, state="hidden")
                self.canvas.itemconfig(p_box, state="hidden")
                self.canvas.itemconfig(p_txt, state="hidden")
                
                if None not in self.slots:
                    self.window.after(300, self.verificar_resultado)
                break

    def remover_letra(self, idx_slot):
        if self.slots[idx_slot] is not None:
            idx_paleta = self.slot_sources[idx_slot]
            self.slots[idx_slot] = None
            self.slot_sources[idx_slot] = None
            self.canvas.itemconfig(f"slot_txt_{idx_slot}", text="")
            
            p_shadow, p_box, p_txt = self.palette_items[idx_paleta]
            self.canvas.itemconfig(p_shadow, state="normal")
            self.canvas.itemconfig(p_box, state="normal")
            self.canvas.itemconfig(p_txt, state="normal")

    def verificar_resultado(self):
        intento = "".join(self.slots)
        if intento == self.palabra_correcta:
            messagebox.showinfo("¡CORRECTO!", f"¡Excelente {self.user_name}!\nLa respuesta es LABORATORIOS.")
            self.window.destroy()
        else:
            messagebox.showerror("Fallaste", "Palabra incorrecta. Intenta de nuevo.")

# ----------------- Funciones Auxiliares del Menú Original -----------------
def clamp(v, a=0, b=255): return max(a, min(b, int(v)))
def hex_to_rgb(h): return tuple(int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
def rgb_to_hex(rgb): return '#{:02x}{:02x}{:02x}'.format(*rgb)
def adjust_brightness(hexcol, factor):
    r, g, b = hex_to_rgb(hexcol)
    return rgb_to_hex((clamp(r * factor), clamp(g * factor), clamp(b * factor)))

def prisma_points(xc, yc, w, h):
    tail_w, tail_h, chamfer = w * 0.12, h * 0.12, w * 0.12
    body_w = w - (2 * tail_w)
    return [
        xc - body_w/2 + chamfer, yc - h/2, xc + body_w/2 - chamfer, yc - h/2,
        xc + body_w/2, yc - tail_h/2, xc + w/2, yc - tail_h/2,
        xc + w/2, yc + tail_h/2, xc + body_w/2, yc + tail_h/2,
        xc + body_w/2 - chamfer, yc + h/2, xc - body_w/2 + chamfer, yc + h/2,
        xc - body_w/2, yc + tail_h/2, xc - w/2, yc + tail_h/2,
        xc - w/2, yc - tail_h/2, xc - body_w/2, yc - tail_h/2
    ]

# ====================================================================================
# CLASES ORIGINALES REUTILIZADAS (TRIVIA Y WORDLE)
# ====================================================================================
class TriviaUCABApp:
    def __init__(self, root, player_name):
        self.root = root
        self.player_name = player_name
        self.window = Toplevel(root)
        self.window.title("Trivia UCAB")
        self.window.geometry("500x400")
        self.window.config(bg=UCAB_BLUE)
        Label(self.window, text=f"¡Bienvenido a Trivia, {player_name}!", font=("Arial", 16, "bold"), bg=UCAB_BLUE, fg=TEXT_LIGHT).pack(pady=50)
        Button(self.window, text="Cerrar", command=self.window.destroy, bg=TEXT_DARK, fg=TEXT_LIGHT, font=("Arial", 11, "bold")).pack()

def abrir_ventana_trivia():
    TriviaUCABApp(root, nombre_usuario())

def abrir_ventana_wordle():
    n = nombre_usuario()
    welcome_win = Toplevel(root)
    welcome_win.title("Bienvenida - Wordle UCAB")
    welcome_win.geometry("500x300")
    welcome_win.config(bg=UCAB_GREEN)

    Label(welcome_win, text=f"¡Bienvenido al juego de Wordle,\n{n}!", font=("Arial", 18, "bold"), bg=UCAB_GREEN, fg=TEXT_LIGHT, justify="center").pack(pady=(70, 30))

    def iniciar_juego():
        welcome_win.destroy()
        # Placeholder para la lógica real de Wordle
        v = Toplevel(root)
        v.title("Wordle - UCAB")
        v.geometry("480x360")
        v.config(bg=UCAB_GREEN)
        Label(v, text=f"Juego de Wordle iniciado", font=("Arial", 16, "bold"), bg=UCAB_GREEN, fg=TEXT_LIGHT).pack(pady=40)
        Button(v, text="Cerrar", command=v.destroy, bg=TEXT_LIGHT, fg=UCAB_GREEN, font=("Arial", 11, "bold"), padx=12, pady=6).pack()

    Button(welcome_win, text="Empezar el juego", command=iniciar_juego, bg=UCAB_YELLOW, fg=TEXT_DARK, font=("Arial", 14, "bold"), padx=20, pady=10, cursor="hand2").pack()

# ====================================================================================
# NUEVA VENTANA DE BIENVENIDA PARA APENSAR
# ====================================================================================
def abrir_ventana_apensar():
    n = nombre_usuario()
    welcome_win = Toplevel(root)
    welcome_win.title("Apensar UCAB")
    welcome_win.geometry("500x300")
    welcome_win.config(bg=UCAB_YELLOW)

    Label(welcome_win, text=f"¡Bienvenido al juego de Apensar,\n{n}!", font=("Arial", 18, "bold"), bg=UCAB_YELLOW, fg=TEXT_DARK, justify="center").pack(pady=(70, 30))

    def iniciar_juego():
        welcome_win.destroy()
        ApensarGame(root, n)

    Button(welcome_win, text="Empezar el juego", command=iniciar_juego, bg="#131514", fg="#ffffff", font=("Arial", 14, "bold"), padx=20, pady=10, cursor="hand2").pack()


# ====================================================================================
# INTERFAZ PRINCIPAL (MENÚ ORIGINAL)
# ====================================================================================
root = Tk()
root.title("El Ucabista - Desafío Digital")
root.geometry("960x640")
root.minsize(640, 420)

main_canvas = Canvas(root, highlightthickness=0)
main_canvas.pack(fill="both", expand=True)

fondo_pil = None
bg_photo = None
darkness_factor = 0.45
resize_timer = None
logo_img = None
entrada_widget = None

def on_configure(event):
    global resize_timer
    if resize_timer is not None: root.after_cancel(resize_timer)
    resize_timer = root.after(100, reposicionar_widgets)

def reposicionar_widgets():
    actualizar_fondo_cover_menu()
    dibujar_ui_menu()

def cargar_imagen_fondo(ruta):
    if not os.path.exists(ruta): return None
    try: return Image.open(ruta).convert("RGBA")
    except: return None

def aplicar_oscurecimiento(img_pil, factor):
    overlay = Image.new("RGBA", img_pil.size, (0, 0, 0, int(255 * factor)))
    return Image.alpha_composite(img_pil.copy(), overlay)

def actualizar_fondo_cover_menu():
    global bg_photo, fondo_pil
    if fondo_pil is None:
        fondo_pil = cargar_imagen_fondo(FONDO_RUTA)
        if fondo_pil is None:
            main_canvas.config(bg=BG)
            return
    W, H = max(1, main_canvas.winfo_width()), max(1, main_canvas.winfo_height())
    img_w, img_h = fondo_pil.size
    scale = max(W / img_w, H / img_h)
    new_w, new_h = int(img_w * scale), int(img_h * scale)
    img_resized = fondo_pil.resize((new_w, new_h), Image.Resampling.LANCZOS)
    img_cropped = img_resized.crop(((new_w - W) // 2, (new_h - H) // 2, (new_w - W) // 2 + W, (new_h - H) // 2 + H))
    bg_photo = ImageTk.PhotoImage(aplicar_oscurecimiento(img_cropped, darkness_factor))
    
    if getattr(main_canvas, "bg_id", None): main_canvas.itemconfig(main_canvas.bg_id, image=bg_photo)
    else: main_canvas.bg_id = main_canvas.create_image(0, 0, image=bg_photo, anchor="nw"); main_canvas.tag_lower(main_canvas.bg_id)

def cargar_logo(ruta, ancho_max):
    if not os.path.exists(ruta): return None
    try:
        img = Image.open(ruta)
        ancho = min(ancho_max, img.size[0])
        h_size = int(float(img.size[1]) * (ancho / float(img.size[0])))
        return ImageTk.PhotoImage(img.resize((ancho, h_size), Image.Resampling.LANCZOS))
    except: return None

def nombre_usuario():
    return entrada_widget.get().strip() if entrada_widget and entrada_widget.get().strip() else "VISITANTE UCABISTA"

def create_text_with_shadow(canvas, x, y, text, font, fill, tags=()):
    canvas.create_text(x + 1, y + 1, text=text, font=font, fill="#000000", tags=tags)
    canvas.create_text(x, y, text=text, font=font, fill=fill, tags=tags)

def dibujar_ui_menu():
    global logo_img, entrada_widget
    main_canvas.delete("ui")
    W, H = main_canvas.winfo_width() or 960, main_canvas.winfo_height() or 640
    x_center = W / 2

    if logo_img is None: logo_img = cargar_logo(LOGO_RUTA, 160)
    logo_h = logo_img.height() if logo_img else 0
    y_top = max(int(0.18 * H), logo_h + 70)

    if logo_img: main_canvas.create_image(x_center, int(logo_h/2) + 12, image=logo_img, tags="ui")

    create_text_with_shadow(main_canvas, x_center, y_top + 10, "Bienvenidos al desafío ucabista", ("Century Gothic", max(18, int(H*0.03)), "bold"), TEXT_LIGHT, "ui")
    create_text_with_shadow(main_canvas, x_center, y_top + 48, "Ingresa tu nombre de usuario para comenzar a jugar", ("Arial", max(11, int(H*0.017)), "normal"), TEXT_LIGHT, "ui")

    if entrada_widget is None:
        entrada_widget = Entry(root, font=("Arial", 12), justify="center", width=20, bd=0, highlightthickness=1, relief="flat")
        entrada_widget.config(highlightbackground="#cccccc", highlightcolor="#aaaaaa")
        
    main_canvas.create_window(x_center, y_top + 92, window=entrada_widget, width=min(420, int(W * 0.32)), height=34, tags="ui")
    create_text_with_shadow(main_canvas, x_center, y_top + 132, "Selecciona un juego para comenzar", ("Arial", max(12, int(H*0.018)), "italic"), TEXT_LIGHT, "ui")

    total_w = min(0.85 * W, 900)
    pr_w = (total_w - 40) / 3
    pr_h = min(0.35 * (H - (y_top + 260)), 80)
    gap = 20
    start_x = (W - (3*pr_w + 2*gap)) / 2 + pr_w/2
    y_center = y_top + 320

    def crear_prisma_menu(xc, yc, w, h, color, texto, text_color, comando):
        pts = prisma_points(xc, yc, w, h)
        poly = main_canvas.create_polygon(pts, fill=color, outline="", smooth=False, tags=("ui","prism"))
        txt = main_canvas.create_text(xc, yc, text=texto, font=("Arial", max(12, int(pr_w/12)), "bold"), fill=text_color, tags=("ui","prism"))
        for item in (poly, txt):
            main_canvas.tag_bind(item, "<Enter>", lambda e: main_canvas.itemconfig(poly, fill=adjust_brightness(color, HOVER_FACTOR)))
            main_canvas.tag_bind(item, "<Leave>", lambda e: main_canvas.itemconfig(poly, fill=color))
            main_canvas.tag_bind(item, "<Button-1>", lambda e: comando())

    crear_prisma_menu(start_x, y_center, pr_w, pr_h, UCAB_YELLOW, "Apensar", TEXT_DARK, abrir_ventana_apensar)
    crear_prisma_menu(start_x + pr_w + gap, y_center, pr_w, pr_h, UCAB_BLUE, "Trivia", TEXT_LIGHT, abrir_ventana_trivia)
    crear_prisma_menu(start_x + 2*(pr_w + gap), y_center, pr_w, pr_h, UCAB_GREEN, "Wordle", TEXT_LIGHT, abrir_ventana_wordle)

    # Botón Salir
    bx, by = W - 98, H - 38
    rect = main_canvas.create_rectangle(bx - 80, by - 20, bx + 80, by + 20, fill="red", outline="", tags="ui")
    main_canvas.create_text(bx, by, text="Salir de la App :(", fill="white", font=("Arial", 11, "bold"), tags="ui")
    main_canvas.tag_bind(rect, "<Button-1>", lambda e: root.destroy())

# Inicializar
root.bind("<Configure>", on_configure)
root.after(100, reposicionar_widgets)
root.mainloop()