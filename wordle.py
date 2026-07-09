import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

# ====================================================================================
# VARIABLES GLOBALES PARA EL WORDLE
# ====================================================================================
palabras = ['UCAB', 'AULAS', 'NESTEA', 'FERIA', 'LOBOS', 'ANDRES', 'BELLO']
palabras_adivinadas = 0
palabra_secreta = ""
intento_actual = 0
largo = 0
letras_escritas = []
cuadros_grid = []

# Variables de ventanas y widgets para el Wordle
v_wordle = None
frame_grid = None
canvas_wordle = None
bg_wordle_photo = None  # Almacenar la referencia de imagen de fondo del juego
text_feedback_id = None  # ID para el texto dinámico del canvas

# Variables de paleta e interfaz
BG = "#3DA5dc"
UCAB_YELLOW = "#f9c32b"
UCAB_BLUE = "#0072CE"
UCAB_GREEN = "#008343"
TEXT_DARK = "#131514"
TEXT_LIGHT = "#ffffff"
HOVER_FACTOR = 0.92

FONDO_RUTA = "fondo.ucab.png"

# ====================================================================================
# LÓGICA E INTERFAZ DE JUEGO DE WORDLE (ESTILO TRIVIA PERFECTO)
# ====================================================================================
def inicializar_interfaz_juego():
    global palabra_secreta, intento_actual, cuadros_grid, letras_escritas, largo, frame_grid, canvas_wordle, text_feedback_id
    
    if not canvas_wordle or not v_wordle:
        return

    # CORRECCIÓN: Forzar actualización real para leer las dimensiones del monitor en pantalla completa
    v_wordle.update()
    canvas_w = max(1, canvas_wordle.winfo_width())
    canvas_h = max(1, canvas_wordle.winfo_height())
    center_x = canvas_w / 2

    # Limpiar elementos previos del canvas
    canvas_wordle.delete("juego")
    
    palabra_secreta = random.choice(palabras)
    intento_actual = 0
    largo = len(palabra_secreta)
    letras_escritas = []

    header_w = min(canvas_w * 0.78, 760)
    header_h = max(70, int(canvas_h * 0.13))
    header_x0 = int(center_x - header_w / 2)
    header_y0 = int(canvas_h * 0.03)
    header_y1 = header_y0 + header_h

    # 1. ENCABEZADO INSTITUCIONAL DE JUEGO
    canvas_wordle.create_rectangle(header_x0, header_y0, header_x0 + header_w, header_y1, fill=UCAB_GREEN, outline=UCAB_YELLOW, width=max(2, int(canvas_w * 0.003)), tags=("juego",))
    canvas_wordle.create_text(center_x, int((header_y0 + header_y1) / 2) - 4, text="WORDLE UCAB 🎓", font=('Arial', max(18, int(min(canvas_w, canvas_h) * 0.03)), 'bold'), fill=UCAB_YELLOW, tags=("juego",))
    
    nombre_jugador = nombre_usuario()
    info_text = f"Jugador: {nombre_jugador}         |         Palabras: {palabras_adivinadas}/4"
    canvas_wordle.create_text(center_x, int(canvas_h * 0.11), text=info_text, font=('Arial', max(11, int(min(canvas_w, canvas_h) * 0.016)), 'bold'), fill=TEXT_LIGHT, tags=("juego",))

    # 2. CONTENEDOR CENTRAL SEMITRANSPARENTE OSCURO
    panel_w = min(canvas_w * 0.82, 720)
    panel_h = min(canvas_h * 0.62, 520)
    panel_x0 = int(center_x - panel_w / 2)
    panel_y0 = int(canvas_h * 0.16)
    panel_x1 = panel_x0 + panel_w
    panel_y1 = panel_y0 + panel_h
    overlay_blur = Image.new("RGBA", (max(2, int(panel_w)), max(2, int(panel_h))), (0, 0, 0, 170))
    canvas_wordle.overlay_blur_tk = ImageTk.PhotoImage(overlay_blur)
    canvas_wordle.create_image(center_x, panel_y0 + panel_h / 2, image=canvas_wordle.overlay_blur_tk, anchor="center", tags=("juego",))

    # 3. MARCO DE LA CUADRÍCULA
    frame_grid = Frame(canvas_wordle, bg='#1a1a1a')
    canvas_wordle.create_window(center_x, int(canvas_h * 0.44), window=frame_grid, tags=("juego",))
    
    cuadros_grid = []
    font_size = max(16, int(min(canvas_w, canvas_h) * 0.025))
    padx_value = max(3, int(min(canvas_w, canvas_h) * 0.007))
    pady_value = max(3, int(min(canvas_w, canvas_h) * 0.007))
    for fila in range(6):
        fila_cuadros = []
        for col in range(largo):
            lbl = Label(frame_grid, text="", font=('Comic Sans MS', font_size, 'bold'), width=4, height=1, 
                        bd=2, relief="solid", bg="white", fg="black")
            lbl.grid(row=fila, column=col, padx=padx_value, pady=pady_value)
            fila_cuadros.append(lbl)
        cuadros_grid.append(fila_cuadros)

    # 4. FEEDBACK EN TEXTO NATIVO DEL CANVAS
    instrucciones = f"Usa tu teclado para escribir la palabra de {largo} letras"
    text_feedback_id = canvas_wordle.create_text(center_x, int(canvas_h * 0.77), text=instrucciones, font=('Arial', max(11, int(min(canvas_w, canvas_h) * 0.018)), 'italic', 'bold'), fill=TEXT_LIGHT, tags=("juego",))

    # 5. BOTÓN SALIR DEL JUEGO
    btn_salir = Button(canvas_wordle, text="Salir del Juego", font=('Arial', max(10, int(min(canvas_w, canvas_h) * 0.014)), 'bold'), 
                       bg='#D93843', fg=TEXT_LIGHT, activebackground='#A6242B', bd=0,
                       padx=20, pady=6, cursor="hand2", command=v_wordle.destroy)
    canvas_wordle.create_window(center_x, int(canvas_h * 0.90), window=btn_salir, tags=("juego",))

    v_wordle.bind("<Key>", presionar_tecla)

def actualizar_feedback(texto, color):
    global text_feedback_id
    if canvas_wordle and text_feedback_id:
        canvas_wordle.itemconfig(text_feedback_id, text=texto, fill=color)

def mostrar_boton_siguiente(texto_boton):
    v_wordle.unbind("<Key>")
    canvas_w = max(1, canvas_wordle.winfo_width())
    canvas_h = max(1, canvas_wordle.winfo_height())
    boton_siguiente = Button(canvas_wordle, text=texto_boton, font=('Arial', max(10, int(min(canvas_w, canvas_h) * 0.016)), 'bold'), 
                             bg=UCAB_YELLOW, fg=TEXT_DARK, activebackground='#dca61d', bd=0,
                             padx=15, pady=8, command=inicializar_interfaz_juego)
    canvas_wordle.create_window(canvas_w / 2, int(canvas_h * 0.70), window=boton_siguiente, tags=("juego",))

def mostrar_felicitaciones_wordle():
    canvas_wordle.delete("juego")
    v_wordle.unbind("<Key>")

    canvas_w = max(1, canvas_wordle.winfo_width())
    canvas_h = max(1, canvas_wordle.winfo_height())
    center_x = canvas_w / 2
    
    overlay_win = Image.new("RGBA", (max(2, int(canvas_w * 0.70)), max(2, int(canvas_h * 0.55))), (0, 0, 0, 190))
    canvas_wordle.overlay_win_tk = ImageTk.PhotoImage(overlay_win)
    canvas_wordle.create_image(center_x, canvas_h / 2, image=canvas_wordle.overlay_win_tk, anchor="center", tags=("juego",))
    
    nombre_jugador = nombre_usuario()
    canvas_wordle.create_text(center_x, int(canvas_h * 0.35), text=f"¡Felicidades {nombre_jugador}! 🎉", font=('Arial', max(18, int(min(canvas_w, canvas_h) * 0.03)), 'bold'), fill=UCAB_YELLOW, tags=("juego",))
    canvas_wordle.create_text(center_x, int(canvas_h * 0.48), text="¡Adivinaste 4 palabras!\n¡Has completado el desafío! 🦇", font=('Arial', max(13, int(min(canvas_w, canvas_h) * 0.02)), 'bold'), fill=TEXT_LIGHT, justify="center", tags=("juego",))
    
    boton_cerrar = Button(canvas_wordle, text="CERRAR JUEGO 🚀", font=('Arial', max(11, int(min(canvas_w, canvas_h) * 0.016)), 'bold'), bg=UCAB_GREEN, fg=TEXT_LIGHT, bd=0, padx=15, pady=8, command=v_wordle.destroy)
    canvas_wordle.create_window(center_x, int(canvas_h * 0.67), window=boton_cerrar, tags=("juego",))

def presionar_tecla(event):
    global intento_actual, letras_escritas, palabras_adivinadas
    
    if intento_actual >= 6:
        return

    tecla = event.char.upper()
    
    if tecla.isalpha() and len(tecla) == 1:
        if len(letras_escritas) < largo:
            letras_escritas.append(tecla)
            columna_actual = len(letras_escritas) - 1
            cuadros_grid[intento_actual][columna_actual].config(text=tecla)
            
    elif event.keysym == "BackSpace":
        if len(letras_escritas) > 0:
            columna_a_borrar = len(letras_escritas) - 1
            cuadros_grid[intento_actual][columna_a_borrar].config(text="")
            letras_escritas.pop()

    elif event.keysym == "Return":
        if len(letras_escritas) != largo:
            actualizar_feedback(f"¡Te faltan letras! Deben ser {largo}", UCAB_YELLOW)
            return
            
        intento = "".join(letras_escritas)
        actualizar_feedback("", TEXT_LIGHT)
        
        copia_letras = list(palabra_secreta)
        colores = ["#787C7E"] * largo

        for i in range(largo):
            if intento[i] == palabra_secreta[i]:
                colores[i] = "#6AAA64"
                copia_letras[i] = None

        for i in range(largo):
            if colores[i] != "#6AAA64":
                if intento[i] in copia_letras:
                    colores[i] = "#C9B458"
                    copia_letras[copia_letras.index(intento[i])] = None

        for i in range(largo):
            cuadros_grid[intento_actual][i].config(bg=colores[i], fg="white")
        
        if intento == palabra_secreta:
            palabras_adivinadas += 1
            
            if palabras_adivinadas >= 4:
                mostrar_felicitaciones_wordle() 
            else:
                actualizar_feedback(f"¡EXCELENTE! Llevas {palabras_adivinadas}/4 🎉", "#6AAA64")
                mostrar_boton_siguiente("SIGUIENTE PALABRA →")
            return

        intento_actual += 1
        letras_escritas = []

        if intento_actual >= 6:
            actualizar_feedback(f"Se acabaron los intentos. Era: {palabra_secreta} 😢", "#D93843")
            mostrar_boton_siguiente("INTENTAR DE NUEVO 🔄")
            return


# ====================================================================================
# INTERFAZ PRINCIPAL Y PROCESAMIENTO DE IMÁGENES
# ====================================================================================

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
    if img_pil is None or factor <= 0:
        return img_pil
    overlay = Image.new("RGBA", img_pil.size, (0, 0, 0, int(255 * factor)))
    base = img_pil.copy()
    return Image.alpha_composite(base, overlay)

# ----------------- FLUJO DE BIENVENIDA Y JUEGO DE WORDLE -----------------
def abrir_ventana_wordle():
    global v_wordle, palabras_adivinadas, canvas_wordle, bg_wordle_photo
    n = nombre_usuario()
    palabras_adivinadas = 0  
    
    welcome_win = Toplevel(root)
    welcome_win.title("Bienvenida - Wordle UCAB")
    welcome_win.geometry("500x300")
    welcome_win.config(bg=UCAB_GREEN) 
    welcome_win.resizable(False, False)
    
    Label(welcome_win, text=f"¡Bienvenido al juego de Wordle,\n{n}!",
          font=("Arial", 18, "bold"), bg=UCAB_GREEN, fg=TEXT_LIGHT, justify="center").pack(pady=(70, 30))
    
    def lanzar_wordle_real():
        global v_wordle, canvas_wordle, bg_wordle_photo
        welcome_win.destroy()       
        
        v_wordle = Toplevel(root)   
        v_wordle.title("Wordle UCAB v1.0")
        
        # CORRECCIÓN CLAVE: Pasamos al frente la ventana y activamos pantalla completa
        # Se elimina por completo la línea de resizable que causaba el conflicto en Windows.
        v_wordle.focus_force()
        v_wordle.attributes("-fullscreen", True)
        v_wordle.bind("<Escape>", lambda event: v_wordle.attributes("-fullscreen", False))
        
        canvas_wordle = Canvas(v_wordle, highlightthickness=0)
        canvas_wordle.pack(fill="both", expand=True)
        
        # Sincronizamos la ventana para heredar las propiedades del monitor completo
        v_wordle.update()
        
        if fondo_pil:
            canvas_w = max(1, canvas_wordle.winfo_width())
            canvas_h = max(1, canvas_wordle.winfo_height())
            img_resized = fondo_pil.resize((canvas_w, canvas_h), Image.Resampling.LANCZOS)
            img_dark = aplicar_oscurecimiento(img_resized, 0.45)
            bg_wordle_photo = ImageTk.PhotoImage(img_dark)
            canvas_wordle.create_image(0, 0, image=bg_wordle_photo, anchor="nw")
        else:
            canvas_wordle.config(bg="#1a1a1a")
        
        inicializar_interfaz_juego() 
        
    Button(welcome_win, text="Empezar el juego", command=lanzar_wordle_real, 
           bg=UCAB_YELLOW, fg=TEXT_DARK, font=("Arial", 14, "bold"), 
           padx=20, pady=10, cursor="hand2", bd=0, activebackground="#dca61d").pack()
# --------------------------------------------------------------------------------

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

# ---------------- Configuración Ventana Principal ----------------
root = Tk()
root.title("El Ucabista - Desafío Digital")
root.geometry("960x640")
root.minsize(640, 420)
root.resizable(True, True)

main_canvas = Canvas(root, highlightthickness=0)
main_canvas.pack(fill="both", expand=True)

entrada_widget = Entry(root, font=("Arial", 12), justify="center", width=20, bd=0, highlightthickness=1, relief="flat")
entrada_widget.config(highlightbackground="#cccccc", highlightcolor="#aaaaaa")

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

def prisma_points(xc, yc, w, h):
    tail_w = w * 0.12      
    tail_h = h * 0.12      
    chamfer = w * 0.12     
    body_w = w - (2 * tail_w)
    half_body = body_w / 2
    half_h = h / 2
    half_tail_h = tail_h / 2
    half_w = w / 2
    return [
        xc - half_body + chamfer, yc - half_h,          
        xc + half_body - chamfer, yc - half_h,          
        xc + half_body, yc - half_tail_h,               
        xc + half_w, yc - half_tail_h,                  
        xc + half_w, yc + half_tail_h,                  
        xc + half_body, yc + half_tail_h,               
        xc + half_body - chamfer, yc + half_h,          
        xc - half_body + chamfer, yc + half_h,          
        xc - half_body, yc + half_tail_h,               
        xc - half_w, yc + half_tail_h,                  
        xc - half_w, yc - half_tail_h,                  
        xc - half_body, yc - half_tail_h                
    ]

def nombre_usuario():
    n = entrada_widget.get().strip()
    return n if n else "VISITANTE UCABISTA"

def abrir_ventana_apensar():
    n = nombre_usuario()
    v = Toplevel(root)
    v.title("Apensar - UCAB")
    v.geometry("480x360")
    v.config(bg=UCAB_YELLOW)
    Label(v, text="¡Bienvenido al juego de Apensar,", font=("Arial", 16, "bold"), bg=UCAB_YELLOW, fg=TEXT_DARK).pack(pady=(40,4))
    Label(v, text=n, font=("Arial", 16, "bold"), bg=UCAB_YELLOW, fg=TEXT_DARK).pack(pady=(0,20))
    Button(v, text="Cerrar", command=v.destroy, bg=TEXT_DARK, fg=TEXT_LIGHT, font=("Arial", 11, "bold"), padx=12, pady=6).pack(pady=8)

def create_text_with_shadow(canvas, x, y, text, font, fill, shadow_color="#000000", offset=(1,1), tags=()):
    sx, sy = offset
    canvas.create_text(x + sx, y + sy, text=text, font=font, fill=shadow_color, tags=tags)
    return canvas.create_text(x, y, text=text, font=font, fill=fill, tags=tags)

def dibujar_ui():
    main_canvas.delete("ui")
    W = main_canvas.winfo_width() or 960
    H = main_canvas.winfo_height() or 640
    x_center = W / 2
    logo_h = logo_img.height() if logo_img else 0
    y_top = max(int(0.18 * H), logo_h + 70)

    if logo_img:
        main_canvas.create_image(x_center, int(logo_h/2) + 12, image=logo_img, tags=("ui",))

    title_font = ("Century Gothic", max(18, int(H*0.03)), "bold")
    subtitle_font = ("Arial", max(11, int(H*0.017)), "normal")
    instruction_font = ("Arial", max(12, int(H*0.018)), "italic")

    create_text_with_shadow(main_canvas, x_center, y_top + 10, "Bienvenidos al desafío ucabista", title_font, TEXT_LIGHT, shadow_color="#000000", offset=(2,2), tags=("ui",))
    create_text_with_shadow(main_canvas, x_center, y_top + 48, "Ingresa tu nombre de usuario para comenzar a jugar", subtitle_font, TEXT_LIGHT, shadow_color="#000000", offset=(1,1), tags=("ui",))

    entrada_w = min(420, int(W * 0.32))
    main_canvas.create_window(x_center, y_top + 92, window=entrada_widget, width=entrada_w, height=34, tags=("ui",))

    create_text_with_shadow(main_canvas, x_center, y_top + 132, "Selecciona un juego para comenzar", instruction_font, TEXT_LIGHT, shadow_color="#000000", offset=(1,1), tags=("ui",))

    total_w = min(0.60 * W, 600)
    pr_w = (total_w - 20) / 2
    pr_h = min(0.35 * (H - (y_top + 260)), 80)
    gap = 40
    start_x = (W - (2*pr_w + gap)) / 2 + pr_w/2
    y_center = y_top + 320

    def crear_prisma(xc, yc, w, h, color, texto, text_color, comando):
        pts = prisma_points(xc, yc, w, h)
        poly = main_canvas.create_polygon(pts, fill=color, outline="", smooth=False, tags=("ui","prism"))
        txt = main_canvas.create_text(xc, yc, text=texto, font=("Arial", max(12, int(pr_w/10)), "bold"), fill=text_color, tags=("ui","prism"))
        
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
    crear_prisma(start_x + pr_w + gap, y_center, pr_w, pr_h, UCAB_GREEN, "Wordle", TEXT_LIGHT, abrir_ventana_wordle)

    btn_w, btn_h = 160, 40
    bx, by = W - btn_w/2 - 18, H - btn_h/2 - 18
    rect = main_canvas.create_rectangle(bx - btn_w/2, by - btn_h/2, bx + btn_w/2, by + btn_h/2, fill="red", outline="", tags=("ui","btn"))
    txt = main_canvas.create_text(bx, by, text="Salir de la App :(", fill="white", font=("Arial", 11, "bold"), tags=("ui","btn"))
    
    main_canvas.tag_bind(rect, "<Button-1>", lambda e: root.destroy())
    main_canvas.tag_bind(txt, "<Button-1>", lambda e: root.destroy())

def reposicionar_widgets():
    actualizar_fondo_cover()
    dibujar_ui()

darkness_factor = 0.45
resize_timer = None
def on_configure(event):
    global resize_timer
    if resize_timer is not None:
        root.after_cancel(resize_timer)
    resize_timer = root.after(100, reposicionar_widgets)

root.bind("<Configure>", on_configure)
root.after(100, reposicionar_widgets)
root.mainloop()