import tkinter as tk
from tkinter import *
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

# ====================================================================================
# BASE DE DATOS DE NIVELES DE APENSAR
# ====================================================================================
NIVELES_APENSAR = [
    {
        "palabra": "LABORATORIOS",
        "imagenes": [
            "laboratoriosucab1.png",
            "laboratorioucab2.png",
            "laboratorioucab3.png",
            "laboratoriosucab.png"
        ]
    },
    {
        "palabra": "AULAMAGNA",
        "imagenes": [
            "aulamagnaucab.png",
            "aulamagnaucab1.png",
            "aulamagnaucab2.png",
            "aulamagnaucab3.png"
        ]
    },
    {
        "palabra": "BIBLIOTECA",
        "imagenes": [
            "biblioteca.jpg",
            "biblioteca1.png",
            "biblioteca2.jpg",
            "biblioteca3.png"
        ]
    },
    {
        "palabra": "FERIA",
        "imagenes": [
            "feriaucab.png",
            "feriaucab1.png",
            "feriaucab2.jpg",
            "feriaucab3.png"
        ]
    },
    {
        "palabra": "ANDRESBELLO",
        "imagenes": [
            "andresbello.png",
            "andresbello1.jpg",
            "andresbello2.png",
            "andresbello5.png"
        ]
    },
    {
        "palabra": "CINQUENTENARIO",
        "imagenes": [
            "50ucab.png",
            "50ucab1.png",
            "50ucab2.png",
            "50ucab3.jpg"
        ]
    }
]

# Función para dibujar rectángulos redondeados
def create_rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    points = (
        x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, 
        x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, 
        x1, y2-r, x1, y1+r, x1, y1+r, x1, y1
    )
    return canvas.create_polygon(points, **kwargs, smooth=True)

# ====================================================================================
# JUEGO: APENSAR UCAB (PANTALLA COMPLETA)
# ====================================================================================
class ApensarGame:
    def __init__(self, parent, user_name):
        self.parent = parent
        self.window = Toplevel(parent)
        self.window.title("Apensar UCAB")
        
        # PANTALLA COMPLETA
        self.window.state("zoomed") 
        self.window.configure(bg=BG_APENSAR)
        
        # EVENTOS DE TECLADO
        self.window.bind("<Key>", self.tecla_presionada)
        
        self.user_name = user_name
        self.vidas = 3  
        self.bloqueado = False 
        
        # LÓGICA DE MULTINIVEL ALEATORIO
        self.progreso_idx = 0 # Nivel actual (1ro, 2do...)
        # Generar un orden aleatorio de los niveles disponibles
        self.orden_niveles = list(range(len(NIVELES_APENSAR)))
        random.seed()
        random.shuffle(self.orden_niveles)
        
        self.canvas = Canvas(self.window, bg=BG_APENSAR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.window.update()
        
        # Iniciar el primer nivel
        self.cargar_nivel()

    def cargar_nivel(self):
        self.canvas.delete("all")
        
        # Obtener el índice real del nivel mezclado
        indice_real = self.orden_niveles[self.progreso_idx]
        datos_nivel = NIVELES_APENSAR[indice_real]
        
        self.palabra_correcta = datos_nivel["palabra"]
        self.rutas_imagenes = datos_nivel["imagenes"]
        self.longitud = len(self.palabra_correcta)
        
        self.slots = [None] * self.longitud        
        self.slot_sources = [None] * self.longitud 
        self.bloqueado = False
        
        self.iniciar_nivel_ui()

    def dibujar_encabezado_juego(self, W):
        lbl_back = self.canvas.create_text(60, 50, text="< Volver", font=("Arial", 18, "bold"), fill=UCAB_BLUE, tags=("ui", "btn_volver"))
        self.canvas.tag_bind(lbl_back, "<Button-1>", lambda e: self.window.destroy())
        
        self.canvas.create_text(W/2, 50, text=f"APENSAR UCAB - Nivel {self.progreso_idx + 1}", font=("Arial", 28, "bold"), fill=UCAB_BLUE, tags="ui")
        
        # Insignia Vidas
        self.canvas.create_oval(W - 140, 35, W - 105, 70, fill=UCAB_YELLOW, outline=TEXT_LIGHT, width=2, tags="ui")
        self.canvas.create_text(W - 122, 53, text="❤", font=("Arial", 18), fill="red", tags="ui")
        self.canvas.create_text(W - 60, 52, text=str(self.vidas), font=("Arial", 20, "bold"), fill=UCAB_BLUE, tags=("ui", "txt_vidas"))

    def iniciar_nivel_ui(self):
        W = self.window.winfo_width()
        H = self.window.winfo_height()
        
        if W <= 1 or H <= 1:
            W, H = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
            
        x_center = W / 2
        self.dibujar_encabezado_juego(W)

        # IMÁGENES CENTRADAS DINÁMICAMENTE
        img_size = 180 
        gap_img = 6
        marco_y1 = int(H * 0.15) 
        marco_y2 = marco_y1 + (img_size * 2) + (gap_img * 2)
        
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

        # SLOTS (Casillas de letras)
        tile_w = 40
        gap_slots = 8
        total_w_slots = self.longitud * (tile_w + gap_slots) - gap_slots
        start_x_slots = x_center - total_w_slots / 2 + tile_w / 2
        
        y_slots = marco_y2 + 60 

        for i in range(self.longitud):
            sx = start_x_slots + i * (tile_w + gap_slots)
            create_rounded_rect(self.canvas, sx - tile_w/2, y_slots - tile_w/2, sx + tile_w/2, y_slots + tile_w/2 + 3, 6, fill="#A5C1D1", tags=("ui", f"slot_bg_{i}"))
            box = create_rounded_rect(self.canvas, sx - tile_w/2, y_slots - tile_w/2, sx + tile_w/2, y_slots + tile_w/2, 6, fill=TEXT_LIGHT, tags=("ui", f"slot_box_{i}"))
            txt = self.canvas.create_text(sx, y_slots, text="", font=("Arial", 22, "bold"), fill=TEXT_DARK, tags=("ui", f"slot_txt_{i}"))
            
            for item in (box, txt):
                self.canvas.tag_bind(item, "<Button-1>", lambda e, idx=i: self.remover_letra(idx))

        # TECLADO INFERIOR (14 Teclas garantizadas)
        letras_correctas = list(self.palabra_correcta)
        letras_faltantes = 14 - len(letras_correctas)
        abecedario = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        distractores = [random.choice(abecedario) for _ in range(letras_faltantes)]
        self.letras_paleta = letras_correctas + distractores
        
        random.seed() 
        random.shuffle(self.letras_paleta)

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

    def tecla_presionada(self, event):
        if self.bloqueado: return
        
        if event.keysym == 'BackSpace':
            for i in range(self.longitud - 1, -1, -1):
                if self.slots[i] is not None:
                    self.remover_letra(i)
                    return
        elif event.char.isalpha():
            letra = event.char.upper()
            for idx, pal_letra in enumerate(self.letras_paleta):
                if pal_letra == letra:
                    estado_actual = self.canvas.itemcget(f"pal_box_{idx}", "state")
                    if estado_actual != "hidden":
                        self.presionar_letra(letra, idx)
                        return

    def presionar_letra(self, letra, idx_paleta):
        if self.bloqueado: return
        
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
        if self.bloqueado: return
        
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
            if self.progreso_idx + 1 < len(self.orden_niveles):
                self.mostrar_mensaje_in_game("exito", f"¡Excelente {self.user_name}!\nLa respuesta es {self.palabra_correcta}.", auto_cerrar=False)
            else:
                self.mostrar_mensaje_in_game("victoria", f"¡Felicidades {self.user_name}!\nCompletaste todos los niveles.", auto_cerrar=False)
        else:
            self.vidas -= 1
            self.canvas.itemconfig("txt_vidas", text=str(self.vidas))
            
            if self.vidas <= 0:
                self.mostrar_mensaje_in_game("fin", f"¡Te has quedado sin vidas!\nSuerte para la próxima.", auto_cerrar=False)
            else:
                self.mostrar_mensaje_in_game("error", f"Palabra incorrecta.\nTe quedan {self.vidas} vida(s).", auto_cerrar=True)
                
    def avanzar_nivel(self):
        self.progreso_idx += 1
        self.cargar_nivel()
                
    # ================= NUEVO SISTEMA DE MENSAJES IN-GAME =================
    def mostrar_mensaje_in_game(self, tipo, texto, auto_cerrar):
        self.bloqueado = True 
        W, H = self.window.winfo_width(), self.window.winfo_height()
        cx, cy = W/2, H/2
        w_box, h_box = 420, 240
        
        # Sombra y Cartel Principal
        create_rounded_rect(self.canvas, cx - w_box/2 + 6, cy - h_box/2 + 6, cx + w_box/2 + 6, cy + h_box/2 + 6, 16, fill="#7A9CAE", tags="msg_ui")
        create_rounded_rect(self.canvas, cx - w_box/2, cy - h_box/2, cx + w_box/2, cy + h_box/2, 16, fill=TEXT_LIGHT, tags="msg_ui")
        
        if tipo == "exito":
            color_titulo = UCAB_GREEN
            titulo = "¡CORRECTO!"
        elif tipo == "victoria":
            color_titulo = "#D4A000"
            titulo = "¡GANASTE!"
        else:
            color_titulo = "#E74C3C"
            titulo = "¡FALLASTE!" if tipo == "error" else "FIN DEL JUEGO"
        
        self.canvas.create_text(cx, cy - 50, text=titulo, font=("Arial", 28, "bold"), fill=color_titulo, tags="msg_ui")
        self.canvas.create_text(cx, cy + 10, text=texto, font=("Arial", 16), fill=TEXT_DARK, justify="center", tags="msg_ui")
        
        if auto_cerrar:
            self.window.after(1500, self.limpiar_mensaje_y_casillas)
        else:
            btn_w, btn_h = 220, 45
            btn_y = cy + 75
            create_rounded_rect(self.canvas, cx - btn_w/2, btn_y - btn_h/2, cx + btn_w/2, btn_y + btn_h/2, 8, fill=UCAB_BLUE, tags=("msg_ui", "btn_msg_bg"))
            
            if tipo == "exito":
                texto_btn = "Siguiente Nivel"
                cmd = self.avanzar_nivel
            else:
                texto_btn = "Terminar"
                cmd = self.window.destroy
                
            self.canvas.create_text(cx, btn_y, text=texto_btn, font=("Arial", 14, "bold"), fill=TEXT_LIGHT, tags=("msg_ui", "btn_msg_txt"))
            
            self.canvas.tag_bind("btn_msg_bg", "<Button-1>", lambda e: cmd())
            self.canvas.tag_bind("btn_msg_txt", "<Button-1>", lambda e: cmd())

    def limpiar_mensaje_y_casillas(self):
        self.canvas.delete("msg_ui")
        for i in range(self.longitud):
            self.remover_letra(i)
        self.bloqueado = False

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
# VENTANA DE BIENVENIDA PARA APENSAR 
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

    Button(welcome_win, text="Empezar el juego", command=iniciar_juego, bg=UCAB_BLUE, fg=TEXT_LIGHT, font=("Arial", 14, "bold"), padx=20, pady=10, cursor="hand2").pack()

# ====================================================================================
# INTERFAZ PRINCIPAL (MENÚ ORIGINAL INTACTO)
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

    # Botón Salir (Corregido para que el texto y fondo cierren toda la aplicación)
    bx, by = W - 98, H - 38
    main_canvas.create_rectangle(bx - 80, by - 20, bx + 80, by + 20, fill="red", outline="", tags=("ui", "btn_salir"))
    main_canvas.create_text(bx, by, text="Salir de la App :(", fill="white", font=("Arial", 11, "bold"), tags=("ui", "btn_salir"))
    
    def cerrar_todo(event):
        root.quit()
        root.destroy()
        
    main_canvas.tag_bind("btn_salir", "<Button-1>", cerrar_todo)

# Inicializar
root.bind("<Configure>", on_configure)
root.after(100, reposicionar_widgets)
root.mainloop()