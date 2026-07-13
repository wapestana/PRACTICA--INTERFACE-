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
BG_APENSAR = "#C1E5F5" # Azul celeste
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
        self.window.title("Apensar UCAB")
        
        # Activar Pantalla Completa (Maximizada)
        self.window.state("zoomed") 
        self.window.configure(bg=BG_APENSAR)
        
        self.user_name = user_name
        self.palabra_correcta = "LABORATORIOS"
        self.longitud = len(self.palabra_correcta)
        
        self.slots = [None] * self.longitud        
        self.slot_sources = [None] * self.longitud 
        self.monedas = 185 
        self.nivel = 12    
        
        self.rutas_imagenes = [
            "laboratoriosucab1.jpg",
            "laboratorioucab2.jpg",
            "laboratorioucab3.jpg",
            "laboratoriosucab.jpg"
        ]
        self.img_referencias = []
        
        self.canvas = Canvas(self.window, bg=BG_APENSAR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Esperar un instante para que la ventana tome el tamaño de la pantalla
        self.window.update()
        self.iniciar_nivel()

    def dibujar_encabezado_juego(self, W):
        # Botón volver (<)
        lbl_back = self.canvas.create_text(60, 50, text="< Volver", font=("Arial", 18, "bold"), fill=UCAB_BLUE, tags=("ui", "btn_volver"))
        self.canvas.tag_bind(lbl_back, "<Button-1>", lambda e: self.window.destroy())
        
        # Título APENSAR UCAB
        self.canvas.create_text(W/2, 50, text="APENSAR UCAB", font=("Arial", 28, "bold"), fill=UCAB_BLUE, tags="ui")
        
        # Insignia de Nivel
        self.canvas.create_oval(W - 250, 30, W - 205, 75, fill=UCAB_YELLOW, outline=TEXT_LIGHT, width=2, tags="ui")
        self.canvas.create_text(W - 227, 52, text=str(self.nivel), font=("Arial", 18, "bold"), fill=TEXT_LIGHT, tags="ui")

        # Insignia de Monedas
        self.canvas.create_oval(W - 160, 35, W - 125, 70, fill=UCAB_YELLOW, outline=TEXT_LIGHT, width=2, tags="ui")
        self.canvas.create_text(W - 142, 52, text="$", font=("Arial", 16, "bold"), fill="#D4A000", tags="ui")
        self.canvas.create_text(W - 80, 52, text=str(self.monedas), font=("Arial", 20, "bold"), fill=UCAB_BLUE, tags="ui")

    # ---------------- Pantalla Principal del Nivel ----------------
    def iniciar_nivel(self):
        self.canvas.delete("ui")
        
        # Obtener dimensiones reales de la pantalla
        W = self.window.winfo_width()
        H = self.window.winfo_height()
        
        # Si por alguna razón la ventana no se actualizó, usamos los de la pantalla principal
        if W <= 1 or H <= 1:
            W, H = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
            
        x_center = W / 2

        self.dibujar_encabezado_juego(W)

        # ---------------- IMÁGENES CENTRADAS DINÁMICAMENTE ----------------
        img_size = 180 # Tamaño de cada cuadrito
        gap_img = 6
        
        # Altura inicial basada en el porcentaje de la pantalla
        marco_y1 = int(H * 0.15) 
        marco_y2 = marco_y1 + (img_size * 2) + (gap_img * 2)
        
        # Marco blanco de fondo que agrupa las 4 imágenes
        marco_x1 = x_center - img_size - gap_img
        marco_x2 = x_center + img_size + gap_img
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
                img_blank = Image.new("RGBA", (img_size, img_size), (200, 200, 200, 255))
                self.img_referencias.append(ImageTk.PhotoImage(img_blank))

        coords_imagenes = [
            (x_center - img_size - gap_img/2, marco_y1 + gap_img/2), 
            (x_center + gap_img/2, marco_y1 + gap_img/2),
            (x_center - img_size - gap_img/2, marco_y1 + img_size + gap_img * 1.5), 
            (x_center + gap_img/2, marco_y1 + img_size + gap_img * 1.5)
        ]
        
        for idx, (bx, by) in enumerate(coords_imagenes):
            if idx < len(self.img_referencias):
                self.canvas.create_image(bx, by, image=self.img_referencias[idx], anchor="nw", tags="ui")

        # ---------------- SLOTS (Casillas de letras) ----------------
        tile_w = 40
        gap_slots = 8
        total_w_slots = self.longitud * (tile_w + gap_slots) - gap_slots
        start_x_slots = x_center - total_w_slots / 2 + tile_w / 2
        
        # Ubicados justo debajo del marco de imágenes
        y_slots = marco_y2 + 60 

        for i in range(self.longitud):
            sx = start_x_slots + i * (tile_w + gap_slots)
            
            create_rounded_rect(self.canvas, sx - tile_w/2, y_slots - tile_w/2, sx + tile_w/2, y_slots + tile_w/2 + 3, 6, fill="#A5C1D1", tags=("ui", f"slot_bg_{i}"))
            box = create_rounded_rect(self.canvas, sx - tile_w/2, y_slots - tile_w/2, sx + tile_w/2, y_slots + tile_w/2, 6, fill=TEXT_LIGHT, tags=("ui", f"slot_box_{i}"))
            txt = self.canvas.create_text(sx, y_slots, text="", font=("Arial", 22, "bold"), fill=TEXT_DARK, tags=("ui", f"slot_txt_{i}"))
            
            for item in (box, txt):
                self.canvas.tag_bind(item, "<Button-1>", lambda e, idx=i: self.remover_letra(idx))

        # ---------------- TECLADO INFERIOR ----------------
        letras_correctas = list(self.palabra_correcta)
        distractores = ["M", "U"]
        self.letras_paleta = letras_correctas + distractores
        random.seed(42)
        random.shuffle(self.letras_paleta)

        # Ubicado justo debajo de las casillas
        y_palette_start = y_slots + 90
        key_w = 30
        key_h = 32
        self.palette_items = []
        
        for idx, letra in enumerate(self.letras_paleta):
            row = idx // 7
            col = idx % 7
            
            px = x_center - 225 + col * 75
            py = y_palette_start + row * 80
            
            p_shadow = create_rounded_rect(self.canvas, px-key_w, py-key_h, px+key_w, py+key_h+8, 8, fill=KEY_SHADOW, tags=("ui", f"pal_sh_{idx}"))
            p_box = create_rounded_rect(self.canvas, px-key_w, py-key_h, px+key_w, py+key_h, 8, fill=KEY_BLUE, tags=("ui", f"pal_box_{idx}"))
            p_txt = self.canvas.create_text(px, py, text=letra, font=("Arial", 28, "bold"), fill=TEXT_LIGHT, tags=("ui", f"pal_txt_{idx}"))
            
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
        v = Toplevel(root)
        v.title("Wordle - UCAB")
        v.geometry("480x360")
        v.config(bg=UCAB_GREEN)
        Label(v, text=f"Juego de Wordle iniciado", font=("Arial", 16, "bold"), bg=UCAB_GREEN, fg=TEXT_LIGHT).pack(pady=40)
        Button(v, text="Cerrar", command=v.destroy, bg=TEXT_LIGHT, fg=UCAB_GREEN, font=("Arial", 11, "bold"), padx=12, pady=6).pack()

    Button(welcome_win, text="Empezar el juego", command=iniciar_juego, bg=UCAB_YELLOW, fg=TEXT_DARK, font=("Arial", 14, "bold"), padx=20, pady=10, cursor="hand2").pack()

# ====================================================================================
# VENTANA DE BIENVENIDA MAXIMIZADA PARA APENSAR
# ====================================================================================
def abrir_ventana_apensar():
    n = nombre_usuario()
    welcome_win = Toplevel(root)
    welcome_win.title("Apensar UCAB")
    
    # Activar pantalla completa para la bienvenida
    welcome_win.state("zoomed")
    welcome_win.config(bg=UCAB_YELLOW)

    # Contenedor central para alinear todo en medio
    frame_central = Frame(welcome_win, bg=UCAB_YELLOW)
    frame_central.pack(expand=True)

    Label(frame_central, text="APENSAR UCAB", font=("Arial", 50, "bold"), bg=UCAB_YELLOW, fg=UCAB_BLUE).pack(pady=(0, 20))
    Label(frame_central, text=f"¡Bienvenido al desafío,\n{n}!", font=("Arial", 24, "bold"), bg=UCAB_YELLOW, fg=TEXT_DARK, justify="center").pack(pady=(0, 50))

    def iniciar_juego():
        welcome_win.destroy()
        ApensarGame(root, n)

    Button(frame_central, text="▶ JUGAR", command=iniciar_juego, bg=UCAB_BLUE, fg=TEXT_LIGHT, font=("Arial", 20, "bold"), padx=40, pady=15, cursor="hand2").pack(pady=10)
    Button(frame_central, text="Volver al Menú", command=welcome_win.destroy, bg="red", fg=TEXT_LIGHT, font=("Arial", 14, "bold"), padx=20, pady=5, cursor="hand2").pack(pady=20)


# ====================================================================================
# INTERFAZ PRINCIPAL (MENÚ ORIGINAL)
# ====================================================================================
root = Tk()
root.title("El Ucabista - Desafío Digital")
root.state("zoomed") # Asegura que el menú inicial también inicie maximizado si lo deseas
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
    canvas.create_text(x + 2, y + 2, text=text, font=font, fill="#000000", tags=tags)
    canvas.create_text(x, y, text=text, font=font, fill=fill, tags=tags)

def dibujar_ui_menu():
    global logo_img, entrada_widget
    main_canvas.delete("ui")
    W, H = main_canvas.winfo_width() or 960, main_canvas.winfo_height() or 640
    x_center = W / 2

    if logo_img is None: logo_img = cargar_logo(LOGO_RUTA, 220)
    logo_h = logo_img.height() if logo_img else 0
    y_top = max(int(0.18 * H), logo_h + 90)

    if logo_img: main_canvas.create_image(x_center, int(logo_h/2) + 20, image=logo_img, tags="ui")

    create_text_with_shadow(main_canvas, x_center, y_top + 10, "Bienvenidos al desafío ucabista", ("Century Gothic", max(24, int(H*0.04)), "bold"), TEXT_LIGHT, "ui")
    create_text_with_shadow(main_canvas, x_center, y_top + 60, "Ingresa tu nombre de usuario para comenzar a jugar", ("Arial", max(14, int(H*0.02)), "normal"), TEXT_LIGHT, "ui")

    if entrada_widget is None:
        entrada_widget = Entry(root, font=("Arial", 16), justify="center", width=25, bd=0, highlightthickness=1, relief="flat")
        entrada_widget.config(highlightbackground="#cccccc", highlightcolor="#aaaaaa")
        
    main_canvas.create_window(x_center, y_top + 120, window=entrada_widget, width=min(500, int(W * 0.4)), height=40, tags="ui")
    create_text_with_shadow(main_canvas, x_center, y_top + 180, "Selecciona un juego para comenzar", ("Arial", max(16, int(H*0.025)), "italic"), TEXT_LIGHT, "ui")

    total_w = min(0.85 * W, 1000)
    pr_w = (total_w - 60) / 3
    pr_h = min(0.35 * (H - (y_top + 300)), 90)
    gap = 30
    start_x = (W - (3*pr_w + 2*gap)) / 2 + pr_w/2
    y_center = y_top + 380

    def crear_prisma_menu(xc, yc, w, h, color, texto, text_color, comando):
        pts = prisma_points(xc, yc, w, h)
        poly = main_canvas.create_polygon(pts, fill=color, outline="", smooth=False, tags=("ui","prism"))
        txt = main_canvas.create_text(xc, yc, text=texto, font=("Arial", max(16, int(pr_w/10)), "bold"), fill=text_color, tags=("ui","prism"))
        for item in (poly, txt):
            main_canvas.tag_bind(item, "<Enter>", lambda e: main_canvas.itemconfig(poly, fill=adjust_brightness(color, HOVER_FACTOR)))
            main_canvas.tag_bind(item, "<Leave>", lambda e: main_canvas.itemconfig(poly, fill=color))
            main_canvas.tag_bind(item, "<Button-1>", lambda e: comando())

    crear_prisma_menu(start_x, y_center, pr_w, pr_h, UCAB_YELLOW, "Apensar", TEXT_DARK, abrir_ventana_apensar)
    crear_prisma_menu(start_x + pr_w + gap, y_center, pr_w, pr_h, UCAB_BLUE, "Trivia", TEXT_LIGHT, abrir_ventana_trivia)
    crear_prisma_menu(start_x + 2*(pr_w + gap), y_center, pr_w, pr_h, UCAB_GREEN, "Wordle", TEXT_LIGHT, abrir_ventana_wordle)

    # Botón Salir
    bx, by = W - 120, H - 50
    rect = main_canvas.create_rectangle(bx - 100, by - 25, bx + 100, by + 25, fill="red", outline="", tags="ui")
    main_canvas.create_text(bx, by, text="Salir de la App :(", fill="white", font=("Arial", 14, "bold"), tags="ui")
    main_canvas.tag_bind(rect, "<Button-1>", lambda e: root.destroy())

# Inicializar
root.bind("<Configure>", on_configure)
root.after(100, reposicionar_widgets)
root.mainloop()