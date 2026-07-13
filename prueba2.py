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
BG_APENSAR = "#C1E5F5"
KEY_BLUE = "#2491D8"
KEY_SHADOW = "#145D8F"
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
            "bibliotecaucab.jpg",
            "bibliotecaucab1.png",
            "bibliotecaucab2.jpg",
            "bibliotecaucab3.png"
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


def create_rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    points = (
        x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y1 + r, x2, y2 - r,
        x2, y2 - r, x2, y2, x2 - r, y2, x2 - r, y2, x1 + r, y2, x1 + r, y2, x1, y2, x1, y2 - r,
        x1, y2 - r, x1, y1 + r, x1, y1 + r, x1, y1
    )
    return canvas.create_polygon(points, **kwargs, smooth=True)


class ApensarGame:
    def __init__(self, parent, user_name):
        self.parent = parent
        self.window = Toplevel(parent)
        self.window.title("Apensar UCAB")
        self.window.state("zoomed")
        self.window.configure(bg=BG_APENSAR)
        self.window.bind("<Key>", self.tecla_presionada)

        self.user_name = user_name
        self.vidas = 3
        self.bloqueado = False

        self.progreso_idx = 0
        self.orden_niveles = list(range(len(NIVELES_APENSAR)))
        random.seed()
        random.shuffle(self.orden_niveles)

        self.canvas = Canvas(self.window, bg=BG_APENSAR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.window.update()
        self.cargar_nivel()

    def cargar_nivel(self):
        self.canvas.delete("all")

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

        self.canvas.create_text(W / 2, 50, text=f"APENSAR UCAB - Nivel {self.progreso_idx + 1}", font=("Arial", 28, "bold"), fill=UCAB_BLUE, tags="ui")

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
            except Exception:
                img_blank = Image.new("RGBA", (img_size, img_size), (200, 200, 200, 255))
                self.img_referencias.append(ImageTk.PhotoImage(img_blank))

        coords_imagenes = [
            (x_center - img_size - gap_img / 2, marco_y1 + gap_img / 2),
            (x_center + gap_img / 2, marco_y1 + gap_img / 2),
            (x_center - img_size - gap_img / 2, marco_y1 + img_size + gap_img * 1.5),
            (x_center + gap_img / 2, marco_y1 + img_size + gap_img * 1.5)
        ]

        for idx, (bx, by) in enumerate(coords_imagenes):
            if idx < len(self.img_referencias):
                self.canvas.create_image(bx, by, image=self.img_referencias[idx], anchor="nw", tags="ui")

        tile_w = 40
        gap_slots = 8
        total_w_slots = self.longitud * (tile_w + gap_slots) - gap_slots
        start_x_slots = x_center - total_w_slots / 2 + tile_w / 2
        y_slots = marco_y2 + 60

        for i in range(self.longitud):
            sx = start_x_slots + i * (tile_w + gap_slots)
            create_rounded_rect(self.canvas, sx - tile_w / 2, y_slots - tile_w / 2, sx + tile_w / 2, y_slots + tile_w / 2 + 3, 6, fill="#A5C1D1", tags=("ui", f"slot_bg_{i}"))
            box = create_rounded_rect(self.canvas, sx - tile_w / 2, y_slots - tile_w / 2, sx + tile_w / 2, y_slots + tile_w / 2, 6, fill=TEXT_LIGHT, tags=("ui", f"slot_box_{i}"))
            txt = self.canvas.create_text(sx, y_slots, text="", font=("Arial", 22, "bold"), fill=TEXT_DARK, tags=("ui", f"slot_txt_{i}"))
            for item in (box, txt):
                self.canvas.tag_bind(item, "<Button-1>", lambda e, idx=i: self.remover_letra(idx))

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

            p_shadow = create_rounded_rect(self.canvas, px - key_w, py - key_h, px + key_w, py + key_h + 8, 8, fill=KEY_SHADOW, tags=("ui", f"pal_sh_{idx}"))
            p_box = create_rounded_rect(self.canvas, px - key_w, py - key_h, px + key_w, py + key_h, 8, fill=KEY_BLUE, tags=("ui", f"pal_box_{idx}"))
            p_txt = self.canvas.create_text(px, py, text=letra, font=("Arial", 28, "bold"), fill=TEXT_LIGHT, tags=("ui", f"pal_txt_{idx}"))

            self.palette_items.append((p_shadow, p_box, p_txt))
            for item in (p_shadow, p_box, p_txt):
                self.canvas.tag_bind(item, "<Button-1>", lambda e, l=letra, i=idx: self.presionar_letra(l, i))

    def tecla_presionada(self, event):
        if self.bloqueado:
            return

        if event.keysym == 'BackSpace':
            for i in range(self.longitud - 1, -1, -1):
                if self.slots[i] is not None:
                    self.remover_letra(i)
                    return
        elif event.char and event.char.isalpha():
            letra = event.char.upper()
            for idx, pal_letra in enumerate(self.letras_paleta):
                if pal_letra == letra:
                    estado_actual = self.canvas.itemcget(f"pal_box_{idx}", "state")
                    if estado_actual != "hidden":
                        self.presionar_letra(letra, idx)
                        return

    def presionar_letra(self, letra, idx_paleta):
        if self.bloqueado:
            return

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
        if self.bloqueado:
            return

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
                self.mostrar_mensaje_in_game("fin", "¡Te has quedado sin vidas!\nSuerte para la próxima.", auto_cerrar=False)
            else:
                self.mostrar_mensaje_in_game("error", f"Palabra incorrecta.\nTe quedan {self.vidas} vida(s).", auto_cerrar=True)

    def avanzar_nivel(self):
        self.progreso_idx += 1
        self.cargar_nivel()

    def mostrar_mensaje_in_game(self, tipo, texto, auto_cerrar):
        self.bloqueado = True
        W, H = self.window.winfo_width(), self.window.winfo_height()
        cx, cy = W / 2, H / 2
        w_box, h_box = 420, 240

        create_rounded_rect(self.canvas, cx - w_box / 2 + 6, cy - h_box / 2 + 6, cx + w_box / 2 + 6, cy + h_box / 2 + 6, 16, fill="#7A9CAE", tags="msg_ui")
        create_rounded_rect(self.canvas, cx - w_box / 2, cy - h_box / 2, cx + w_box / 2, cy + h_box / 2, 16, fill=TEXT_LIGHT, tags="msg_ui")

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
            create_rounded_rect(self.canvas, cx - btn_w / 2, btn_y - btn_h / 2, cx + btn_w / 2, btn_y + btn_h / 2, 8, fill=UCAB_BLUE, tags=("msg_ui", "btn_msg_bg"))

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
def clamp(v, a=0, b=255):
    return max(a, min(b, int(v)))


def hex_to_rgb(h):
    return tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def adjust_brightness(hexcol, factor):
    r, g, b = hex_to_rgb(hexcol)
    return rgb_to_hex((clamp(r * factor), clamp(g * factor), clamp(b * factor)))


def prisma_points(xc, yc, w, h):
    tail_w, tail_h, chamfer = w * 0.12, h * 0.12, w * 0.12
    body_w = w - (2 * tail_w)
    return [
        xc - body_w / 2 + chamfer, yc - h / 2, xc + body_w / 2 - chamfer, yc - h / 2,
        xc + body_w / 2, yc - tail_h / 2, xc + w / 2, yc - tail_h / 2,
        xc + w / 2, yc + tail_h / 2, xc + body_w / 2, yc + tail_h / 2,
        xc + body_w / 2 - chamfer, yc + h / 2, xc - body_w / 2 + chamfer, yc + h / 2,
        xc - body_w / 2, yc + tail_h / 2, xc - w / 2, yc + tail_h / 2,
        xc - w / 2, yc - tail_h / 2, xc - body_w / 2, yc - tail_h / 2
    ]

# ====================================================================================
# JUEGO TRIVIA UCAB
#====================================================================================

class TriviaUCABApp:
    def __init__(self, root, player_name):
        self.root = root
        self.player_name = player_name

        self.window = Toplevel(root)
        self.window.title("Trivia UCAB")
        self.window.state("zoomed")
        self.window.configure(bg="black")

        self._configurar_variables()
        self._cargar_fondo()
        self._crear_interfaz()
        self._mostrar_pregunta(0)

    def _configurar_variables(self):
        self.questions_db = [
            {"nivel": 1, "pregunta": "¿Qué bebida es considerada un clásico entre los ucabistas?", "opciones": ["Agua", "Nestea", "Coca-Cola", "Malta"], "respuesta": "Nestea"},
            {"nivel": 2, "pregunta": "¿En qué año se fundó la UCAB?", "opciones": ["1963", "1953", "1952", "1962"], "respuesta": "1953"},
            {"nivel": 3, "pregunta": "¿Quién es el actual rector de la universidad?", "opciones": ["Pedro Peraza", "Arturo Pastrana", "Pedro Pastrana", "Arturo Peraza"], "respuesta": "Arturo Peraza"},
            {"nivel": 4, "pregunta": "¿Qué representa el color amarillo en el logo de la UCAB?", "opciones": ["El amarillo de la bandera de Venezuela", "Las riquezas de Venezuela", "El color de la bandera del Vaticano", "Un nuevo amanecer"], "respuesta": "El color de la bandera del Vaticano"},
            {"nivel": 5, "pregunta": "¿Dónde estaba ubicada la primera sede de la UCAB antes de mudarse a Montalbán?", "opciones": ["El centro de Caracas", "En la Av. Paez", "En San Antonio", "El 23 de enero"], "respuesta": "El centro de Caracas"},
            {"nivel": 6, "pregunta": "La UCAB se llama Andrés Bello, pero ¿quién fue el padre jesuita fundador y primer rector?", "opciones": ["Andrés Guillermo Plaza", "Carlos Guillermo Pérez", "Carlos Guillermo Plaza", "Andrés Guillermo Pérez"], "respuesta": "Carlos Guillermo Plaza"},
            {"nivel": 7, "pregunta": "¿Cuál edificio fue el primero en entrar en funcionamiento en el campus Montalbán?", "opciones": ["Laboratorios", "Aulas", "Postgrado", "Centro Loyola"], "respuesta": "Laboratorios"},
            {"nivel": 8, "pregunta": "¿Cuáles son las sedes principales de la UCAB activas actualmente?", "opciones": ["Montalbán/San Antonio", "Montalbán/Guayana", "Montalbán/Puerto Ordaz", "Montalbán/Mérida"], "respuesta": "Montalbán/Guayana"},
            {"nivel": 9, "pregunta": "¿Qué creencia hay entre los ucabistas sobre pasar por detrás de la estatua de Andrés Bello?", "opciones": ["Que raspan el siguiente parcial", "Que raspan una materia", "Que no se graduan", "Que no consiguen pareja"], "respuesta": "Que no se graduan"},
            {"nivel": 10, "pregunta": "¿En cuál de estas ciudades la UCAB tiene un centro de formación jesuita?", "opciones": ["San Antonio", "Maracaibo", "Valencia", "Barquisimeto"], "respuesta": "San Antonio"},
            {"nivel": 11, "pregunta": "¿Cómo se llama la plataforma digital donde los estudiantes inscriben sus materias, pagan matrícula y revisan su récord académico?", "opciones": ["Módulo 7", "Gestión de Solicitudes", "Planificación e Inscripción", "Secretaría en Línea"], "respuesta": "Secretaría en Línea"},
            {"nivel": 12, "pregunta": "Según QS, ¿qué posición ocupa la UCAB entre las universidades privadas de Venezuela?", "opciones": ["Primer lugar", "Segundo lugar", "Tercer lugar", "Cuarto lugar"], "respuesta": "Primer lugar"},
            {"nivel": 13, "pregunta": "¿Qué idioma extranjero debe aprobar obligatoriamente un estudiante de pregrado para graduarse?", "opciones": ["Italiano", "Alemán", "Portugués", "Inglés"], "respuesta": "Inglés"},
            {"nivel": 14, "pregunta": "El edificio de aulas se divide en bloques; ¿cómo se les llama?", "opciones": ["Pasillos", "Unidades", "Programas", "Módulos"], "respuesta": "Módulos"},
            {"nivel": 15, "pregunta": "¿Cómo se llama el trabajo final de investigación que deben presentar para obtener el título?", "opciones": ["Investigación Final", "Tesis de Grado", "Trabajo Final", "Parcial Final"], "respuesta": "Tesis de Grado"},
        ]

        self.num_questions = 10
        self.num_lives = 3
        self.current_question_index = 0
        self.selected_questions = random.sample(self.questions_db, self.num_questions)
        self.player_lives = self.num_lives
        self.buttons_active = True

        self.color_green = "#004B18"
        self.color_gold = "#CC9900"
        self.color_light_gold = "#FFD700"
        self.color_exit = "#dc3545"
        self.color_exit_hover = "#c82333"

    def _cargar_fondo(self):
        self.window.update_idletasks()
        self.screen_width = self.window.winfo_width()
        self.screen_height = self.window.winfo_height()

        try:
            original_bg = Image.open("images_aulas_trivia.jpeg")
            bg_image = original_bg.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
        except Exception:
            try:
                original_bg = Image.open("image_0.png")
                bg_image = original_bg.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(bg_image)
            except Exception:
                self.bg_photo = None

    def _crear_interfaz(self):
        self.canvas = tk.Canvas(self.window, width=self.screen_width, height=self.screen_height, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        if self.bg_photo:
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        else:
            self.canvas.configure(bg="black")

        self._crear_ui_elements()

    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1, x2, y1,
            x2, y1 + radius, x2, y1 + radius, x2, y2 - radius, x2, y2 - radius, x2, y2,
            x2 - radius, y2, x2 - radius, y2, x1 + radius, y2, x1 + radius, y2, x1, y2,
            x1, y2 - radius, x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1,
        ]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def _crear_ui_elements(self):
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        top_w, top_h = 850, 130
        top_x1, top_y1 = center_x - top_w // 2, 30
        top_x2, top_y2 = center_x + top_w // 2, 30 + top_h

        self.create_rounded_rect(top_x1, top_y1, top_x2, top_y2, radius=20, fill=self.color_gold)
        self.create_rounded_rect(top_x1 + 6, top_y1 + 6, top_x2 - 6, top_y2 - 6, radius=15, fill=self.color_green)
        self.canvas.create_line(top_x1 + 40, top_y1 + 80, top_x2 - 40, top_y1 + 80, fill=self.color_gold, width=2)

        self.canvas.create_text(center_x, top_y1 + 45, text="🐝 TRIVIA UCAB 🎓", font=("Arial", 38, "bold"), fill=self.color_light_gold)
        self.lbl_level_id = self.canvas.create_text(top_x1 + 60, top_y1 + 105, text="", font=("Arial", 22, "bold"), fill="white", anchor="w")
        self.lbl_lives_id = self.canvas.create_text(top_x2 - 60, top_y1 + 105, text="", font=("Arial", 22, "bold"), fill="white", anchor="e")

        panel_w, panel_h = 1000, 500
        self.translucent_image = Image.new("RGBA", (panel_w, panel_h), (0, 0, 0, 160))
        self.translucent_photo = ImageTk.PhotoImage(self.translucent_image)
        self.canvas.create_image(center_x, center_y + 40, image=self.translucent_photo, anchor="center", tags="translucent_panel")

        self.canvas.create_text(center_x, center_y - 180, text="", font=("Arial", 24, "bold"), fill="white", width=900, justify="center", anchor="n", tags="q_text")
        self.canvas.create_text(center_x, center_y - 5, text="", font=("Arial", 22, "bold"), tags="feedback_text")

        self.custom_btns = []
        btn_w, btn_h = 380, 90
        positions = [
            (center_x - 210, center_y + 90), (center_x + 210, center_y + 90),
            (center_x - 210, center_y + 200), (center_x + 210, center_y + 200),
        ]

        for i, pos in enumerate(positions):
            x_c, y_c = pos
            x1, y1 = x_c - btn_w // 2, y_c - btn_h // 2
            x2, y2 = x_c + btn_w // 2, y_c + btn_h // 2

            btn_tag = f"btn_{i}"
            bg_id = self.create_rounded_rect(x1, y1, x2, y2, radius=20, fill=self.color_gold, tags=(btn_tag, "btn_bg"))
            text_id = self.canvas.create_text(x_c, y_c, text="", font=("Arial", 15, "bold"), fill=self.color_green, width=btn_w - 40, justify="center", tags=(btn_tag, "btn_text"))
            self.custom_btns.append({"bg": bg_id, "text": text_id, "tag": btn_tag})
            self.canvas.tag_bind(btn_tag, "<Button-1>", lambda e, idx=i: self._verificar_respuesta(idx))
            self.canvas.tag_bind(btn_tag, "<Enter>", lambda e, idx=i: self._hover(idx, True))
            self.canvas.tag_bind(btn_tag, "<Leave>", lambda e, idx=i: self._hover(idx, False))

        exit_w, exit_h = 220, 50
        exit_x1, exit_y1 = center_x - exit_w // 2, center_y + 320
        exit_x2, exit_y2 = center_x + exit_w // 2, center_y + 320 + exit_h

        exit_tag = "btn_exit"
        self.exit_bg = self.create_rounded_rect(exit_x1, exit_y1, exit_x2, exit_y2, radius=15, fill=self.color_exit, tags=(exit_tag, "exit_bg"))
        self.exit_text = self.canvas.create_text(center_x, center_y + 345, text="Salir del Juego", font=("Arial", 14, "bold"), fill="white", tags=(exit_tag, "exit_text"))

        self.canvas.tag_bind(exit_tag, "<Button-1>", lambda e: self.window.destroy())
        self.canvas.tag_bind(exit_tag, "<Enter>", lambda e: self.canvas.itemconfig(self.exit_bg, fill=self.color_exit_hover))
        self.canvas.tag_bind(exit_tag, "<Leave>", lambda e: self.canvas.itemconfig(self.exit_bg, fill=self.color_exit))

    def _hover(self, idx, entering):
        if not self.buttons_active:
            return
        color = self.color_light_gold if entering else self.color_gold
        self._cambiar_color_boton(idx, color, self.color_green)

    def _cambiar_color_boton(self, idx, bg_color, fg_color):
        btn = self.custom_btns[idx]
        self.canvas.itemconfig(btn["bg"], fill=bg_color)
        self.canvas.itemconfig(btn["text"], fill=fg_color)

    def _mostrar_pregunta(self, index):
        if index < self.num_questions:
            self.buttons_active = True
            for i in range(4):
                self._cambiar_color_boton(i, self.color_gold, self.color_green)
            self.canvas.itemconfigure("feedback_text", text="")
            self.current_question_data = self.selected_questions[index]
            self.canvas.itemconfig(self.lbl_level_id, text=f"Nivel: {index + 1}/{self.num_questions}")
            self.canvas.itemconfig(self.lbl_lives_id, text=f"Vidas: {'❤️ ' * self.player_lives}")

            texto_pregunta = f"Nivel {index + 1}: {self.current_question_data['pregunta']}"
            self.canvas.itemconfigure("q_text", text=texto_pregunta)

            shuffled_options = random.sample(self.current_question_data["opciones"], len(self.current_question_data["opciones"]))
            self.current_shuffled_options = shuffled_options

            for i, text in enumerate(shuffled_options):
                self.canvas.itemconfig(self.custom_btns[i]["text"], text=f"{chr(65 + i)}: {text}")
        else:
            messagebox.showinfo("¡Felicidades!", f"🎓 ¡Felicidades {self.player_name}! Has completado la Trivia UCAB con éxito.")
            self.window.destroy()

    def _verificar_respuesta(self, button_index):
        if not self.buttons_active:
            return
        self.buttons_active = False
        selected_answer = self.current_shuffled_options[button_index]
        correct_answer = self.current_question_data["respuesta"]
        correct_button_index = self.current_shuffled_options.index(correct_answer)

        if selected_answer == correct_answer:
            self._cambiar_color_boton(button_index, "#28a745", "white")
            self.canvas.itemconfigure("feedback_text", text="¡Respuesta Correcta! ✅", fill="#28a745")
            self.current_question_index += 1
            self.window.after(2000, lambda: self._mostrar_pregunta(self.current_question_index))
        else:
            self.player_lives -= 1
            self.canvas.itemconfig(self.lbl_lives_id, text=f"Vidas: {'❤️ ' * self.player_lives}")
            self._cambiar_color_boton(button_index, "#dc3545", "white")
            self.canvas.itemconfigure("feedback_text", text="Respuesta Incorrecta ❌", fill="#dc3545")
            self._cambiar_color_boton(correct_button_index, "#28a745", "white")

            if self.player_lives > 0:
                preguntas_usadas = [q["pregunta"] for q in self.selected_questions]
                preguntas_disponibles = [q for q in self.questions_db if q["pregunta"] not in preguntas_usadas]
                if preguntas_disponibles:
                    nueva_pregunta = random.choice(preguntas_disponibles)
                else:
                    opciones_emergencia = [q for q in self.questions_db if q["pregunta"] != self.current_question_data["pregunta"]]
                    nueva_pregunta = random.choice(opciones_emergencia)
                self.selected_questions[self.current_question_index] = nueva_pregunta
                self.window.after(2000, lambda: self._mostrar_pregunta(self.current_question_index))
            else:
                self.window.after(2000, self._fin_del_juego)

    def _fin_del_juego(self):
        messagebox.showerror("Fin del Juego", f"💀 {self.player_name}, te has quedado sin vidas. ¡Inténtalo de nuevo!")
        self.window.destroy()

#====================================================================================
#JUEGO WORDLE UCAB
#====================================================================================

def iniciar_juego_wordle(v_wordle, player_name):
    v_wordle.title("Wordle UCAB")
    v_wordle.state("zoomed")
    v_wordle.configure(bg=UCAB_GREEN)

    palabras = ["UCAB", "AULAS", "NESTEA", "FERIA", "LOBOS", "ANDRES", "BELLO"]

    game_state = {
        "palabras_restantes": [],
        "palabras_adivinadas": 0,
        "palabra_secreta": "",
        "intento_actual": 0,
        "largo": 0,
        "letras_escritas": [],
        "cuadros_grid": [],
        "enable_input": True,
        "text_feedback_id": None,
        "frame_grid": None,
        "bg_photo": None,
        "overlay_photo": None
    }

    canvas = tk.Canvas(v_wordle, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.focus_set()

    def load_background():
        fondo_wordle = "ucab.jpg"
        try:
            if os.path.exists(fondo_wordle):
                img = Image.open(fondo_wordle).convert("RGBA")
                game_state["bg_photo"] = ImageTk.PhotoImage(img.resize((max(1, v_wordle.winfo_screenwidth()), max(1, v_wordle.winfo_screenheight())), Image.Resampling.LANCZOS))
                canvas.create_image(0, 0, image=game_state["bg_photo"], anchor="nw")
            else:
                canvas.configure(bg="#1a1a1a")
        except Exception:
            canvas.configure(bg="#1a1a1a")

    def inicializar_interfaz_juego():
        canvas.delete("juego")
        v_wordle.update()

        game_state["enable_input"] = True
        canvas.focus_set()

        canvas_w = max(1, canvas.winfo_width())
        canvas_h = max(1, canvas.winfo_height())
        center_x = canvas_w / 2

        if not game_state["palabras_restantes"]:
            game_state["palabras_restantes"] = palabras.copy()
            random.shuffle(game_state["palabras_restantes"])

        game_state["palabra_secreta"] = game_state["palabras_restantes"].pop()
        game_state["intento_actual"] = 0
        game_state["largo"] = len(game_state["palabra_secreta"])
        game_state["letras_escritas"] = []

        header_w = min(canvas_w * 0.78, 760)
        header_h = max(90, int(canvas_h * 0.13))
        header_x0 = int(center_x - header_w / 2)
        header_y0 = int(canvas_h * 0.03)
        header_y1 = header_y0 + header_h

        canvas.create_rectangle(header_x0, header_y0, header_x0 + header_w, header_y1, fill=UCAB_GREEN, outline=UCAB_YELLOW, width=max(2, int(canvas_w * 0.003)), tags=("juego",))
        canvas.create_text(center_x, header_y0 + (header_h * 0.35), text="WORDLE UCAB 🎓", font=("Arial", max(18, int(min(canvas_w, canvas_h) * 0.03)), "bold"), fill=UCAB_YELLOW, tags=("juego",))
        canvas.create_text(center_x, header_y0 + (header_h * 0.75), text=f"Jugador: {player_name}         |         Palabras: {game_state['palabras_adivinadas']}/4", font=("Arial", max(11, int(min(canvas_w, canvas_h) * 0.016)), "bold"), fill=TEXT_LIGHT, tags=("juego",))

        panel_w = min(canvas_w * 0.82, 720)
        panel_h = min(canvas_h * 0.62, 520)
        panel_y0 = header_y1 + max(10, int(canvas_h * 0.02))
        panel_y1 = panel_y0 + panel_h

        overlay = Image.new("RGBA", (max(2, int(panel_w)), max(2, int(panel_h))), (0, 0, 0, 170))
        game_state["overlay_photo"] = ImageTk.PhotoImage(overlay)
        canvas.create_image(center_x, panel_y0 + panel_h / 2, image=game_state["overlay_photo"], anchor="center", tags=("juego",))

        game_state["frame_grid"] = Frame(canvas, bg="#1a1a1a")
        canvas.create_window(center_x, panel_y0 + (panel_h * 0.42), window=game_state["frame_grid"], tags=("juego",))

        game_state["cuadros_grid"] = []
        font_size = max(16, int(min(canvas_w, canvas_h) * 0.025))
        padx_value = max(3, int(min(canvas_w, canvas_h) * 0.007))
        pady_value = max(3, int(min(canvas_w, canvas_h) * 0.007))
        for fila in range(6):
            fila_cuadros = []
            for col in range(game_state["largo"]):
                lbl = Label(game_state["frame_grid"], text="", font=("Comic Sans MS", font_size, "bold"), width=4, height=1, bd=2, relief="solid", bg="white", fg="black")
                lbl.grid(row=fila, column=col, padx=padx_value, pady=pady_value)
                fila_cuadros.append(lbl)
            game_state["cuadros_grid"].append(fila_cuadros)

        instruccion = f"Usa tu teclado para escribir la palabra de {game_state['largo']} letras"
        game_state["text_feedback_id"] = canvas.create_text(center_x, panel_y0 + (panel_h * 0.88), text=instruccion, font=("Arial", max(11, int(min(canvas_w, canvas_h) * 0.018)), "italic", "bold"), fill=TEXT_LIGHT, tags=("juego",))

        btn_salir = Button(canvas, text="Salir del Juego", font=("Arial", max(10, int(min(canvas_w, canvas_h) * 0.014)), "bold"), bg="#D93843", fg=TEXT_LIGHT, activebackground="#A6242B", bd=0, padx=20, pady=6, cursor="hand2", command=v_wordle.destroy)
        canvas.create_window(center_x, panel_y1 + max(20, int(canvas_h * 0.04)), window=btn_salir, tags=("juego",))

    def actualizar_feedback(texto, color):
        if canvas and game_state["text_feedback_id"]:
            canvas.itemconfig(game_state["text_feedback_id"], text=texto, fill=color)

    def mostrar_boton_siguiente(texto_boton):
        game_state["enable_input"] = False
        canvas_w = max(1, canvas.winfo_width())
        canvas_h = max(1, canvas.winfo_height())
        boton_siguiente = Button(canvas, text=texto_boton, font=("Arial", max(10, int(min(canvas_w, canvas_h) * 0.016)), "bold"), bg=UCAB_YELLOW, fg=TEXT_DARK, activebackground="#dca61d", bd=0, padx=15, pady=8, command=inicializar_interfaz_juego)
        if game_state["text_feedback_id"]:
            coords = canvas.coords(game_state["text_feedback_id"])
            pos_y = coords[1] - max(40, int(canvas_h * 0.06))
        else:
            pos_y = int(canvas_h * 0.70)
        canvas.create_window(canvas_w / 2, pos_y, window=boton_siguiente, tags=("juego",))

    def mostrar_felicitaciones_wordle():
        game_state["enable_input"] = False
        canvas.delete("juego")
        canvas.configure(bg="#1a1a1a")

        canvas_w = max(1, canvas.winfo_width())
        canvas_h = max(1, canvas.winfo_height())
        center_x = canvas_w / 2
        center_y = canvas_h / 2

        global trofeo_photo_ref

        try:
            img_pil = Image.open("trofeo.png").convert("RGBA")
            alto_deseado = int(canvas_h * 0.6)
            proporcion = alto_deseado / float(img_pil.size[1])
            ancho_deseado = int(float(img_pil.size[0]) * proporcion)
            img_pil = img_pil.resize((ancho_deseado, alto_deseado), Image.Resampling.LANCZOS)

            trofeo_photo_ref = ImageTk.PhotoImage(img_pil)
            canvas.create_image(ancho_deseado / 3 + 70, center_y, image=trofeo_photo_ref, anchor="center")
            texto_x = center_x + (canvas_w * 0.15)
        except Exception:
            texto_x = center_x

        canvas.create_text(texto_x, center_y - 60, text=f"¡Felicidades {player_name}! 🏆", font=("Comic Sans MS", 38, "bold"), fill="white")
        canvas.create_text(texto_x, center_y + 30, text="¡HAZ COMPLETADO EL DESAFÍO UCABISTA! 🎉", font=("Comic Sans MS", 28, "bold"), fill="white", justify="center")

        btn_finalizar = Button(canvas, text="FINALIZAR", font=("Arial", 12, "bold"), bg="#f04730", fg="black", bd=1, padx=20, pady=10, cursor="hand2", command=v_wordle.destroy)
        canvas.create_window(texto_x, center_y + 130, window=btn_finalizar)

    def on_key(event):
        if not game_state["enable_input"]:
            return
        if game_state["intento_actual"] >= 6:
            return
        if event.char is None:
            return

        tecla = event.char.upper()

        if tecla.isalpha() and len(tecla) == 1:
            if len(game_state["letras_escritas"]) < game_state["largo"]:
                game_state["letras_escritas"].append(tecla)
                columna_actual = len(game_state["letras_escritas"]) - 1
                game_state["cuadros_grid"][game_state["intento_actual"]][columna_actual].config(text=tecla)
        elif event.keysym == "BackSpace":
            if len(game_state["letras_escritas"]) > 0:
                columna_a_borrar = len(game_state["letras_escritas"]) - 1
                game_state["cuadros_grid"][game_state["intento_actual"]][columna_a_borrar].config(text="")
                game_state["letras_escritas"].pop()
        elif event.keysym == "Return":
            if len(game_state["letras_escritas"]) != game_state["largo"]:
                actualizar_feedback(f"¡Te faltan letras! Deben ser {game_state['largo']}", UCAB_YELLOW)
                return

            intento = "".join(game_state["letras_escritas"])
            actualizar_feedback("", TEXT_LIGHT)
            copia_letras = list(game_state["palabra_secreta"])
            colores = ["#787C7E"] * game_state["largo"]

            for i in range(game_state["largo"]):
                if intento[i] == game_state["palabra_secreta"][i]:
                    colores[i] = "#6AAA64"
                    copia_letras[i] = None

            for i in range(game_state["largo"]):
                if colores[i] != "#6AAA64":
                    if intento[i] in copia_letras:
                        colores[i] = "#C9B458"
                        copia_letras[copia_letras.index(intento[i])] = None

            for i in range(game_state["largo"]):
                game_state["cuadros_grid"][game_state["intento_actual"]][i].config(bg=colores[i], fg="white")

            if intento == game_state["palabra_secreta"]:
                game_state["palabras_adivinadas"] += 1
                if game_state["palabras_adivinadas"] >= 4:
                    mostrar_felicitaciones_wordle()
                else:
                    actualizar_feedback(f"¡EXCELENTE! Llevas {game_state['palabras_adivinadas']}/4 🎉", "#6AAA64")
                    mostrar_boton_siguiente("SIGUIENTE PALABRA →")
                return

            game_state["intento_actual"] += 1
            game_state["letras_escritas"] = []
            if game_state["intento_actual"] >= 6:
                actualizar_feedback(f"Se acabaron los intentos. Era: {game_state['palabra_secreta']} 😢", "#D93843")
                mostrar_boton_siguiente("INTENTAR DE NUEVO 🔄")

    v_wordle.bind_all("<Key>", on_key)

    def al_cerrar_ventana():
        v_wordle.unbind_all("<Key>")
        v_wordle.destroy()

    v_wordle.protocol("WM_DELETE_WINDOW", al_cerrar_ventana)

    load_background()
    inicializar_interfaz_juego()


def abrir_ventana_trivia():
    n = nombre_usuario()
    welcome_win = Toplevel(root)
    welcome_win.title("Bienvenida - Trivia UCAB")
    welcome_win.geometry("500x300")
    welcome_win.config(bg=UCAB_BLUE)

    Label(welcome_win, text=f"¡Bienvenido al juego de Trivia,\n{n}!", font=("Arial", 18, "bold"), bg=UCAB_BLUE, fg=TEXT_LIGHT, justify="center").pack(pady=(70, 30))

    def iniciar_juego():
        welcome_win.destroy()
        TriviaUCABApp(root, n)

    Button(welcome_win, text="Empezar el juego", command=iniciar_juego, bg=UCAB_YELLOW, fg=TEXT_DARK, font=("Arial", 14, "bold"), padx=20, pady=10, cursor="hand2").pack()


def abrir_ventana_wordle():
    n = nombre_usuario()
    welcome_win = Toplevel(root)
    welcome_win.title("Bienvenida - Wordle UCAB")
    welcome_win.geometry("500x300")
    welcome_win.config(bg=UCAB_GREEN)

    Label(welcome_win, text=f"¡Bienvenido al juego de Wordle,\n{n}!", font=("Arial", 18, "bold"), bg=UCAB_GREEN, fg=TEXT_LIGHT, justify="center").pack(pady=(70, 30))

    def iniciar_juego():
        welcome_win.destroy()
        iniciar_juego_wordle(Toplevel(root), n)

    Button(welcome_win, text="Empezar el juego", command=iniciar_juego, bg=UCAB_YELLOW, fg=TEXT_DARK, font=("Arial", 14, "bold"), padx=20, pady=10, cursor="hand2").pack()


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
    if resize_timer is not None:
        root.after_cancel(resize_timer)
    resize_timer = root.after(100, reposicionar_widgets)


def reposicionar_widgets():
    actualizar_fondo_cover_menu()
    dibujar_ui_menu()


def cargar_imagen_fondo(ruta):
    if not os.path.exists(ruta):
        return None
    try:
        return Image.open(ruta).convert("RGBA")
    except Exception:
        return None


def aplicar_oscurecimiento(img_pil, factor):
    overlay = Image.new("RGBA", img_pil.size, (0, 0, 0, int(255 * factor)))
    return Image.alpha_composite(img_pil.copy(), overlay)


def actualizar_fondo_cover_menu():
    global bg_photo, fondo_pil
    if fondo_pil is None:
        fondo_pil = cargar_imagen_fondo(FONDO_RUTA)
        if fondo_pil is None:
            return

    W, H = max(1, main_canvas.winfo_width()), max(1, main_canvas.winfo_height())
    img_w, img_h = fondo_pil.size
    scale = max(W / img_w, H / img_h)
    new_w, new_h = int(img_w * scale), int(img_h * scale)
    img_resized = fondo_pil.resize((new_w, new_h), Image.Resampling.LANCZOS)
    img_cropped = img_resized.crop(((new_w - W) // 2, (new_h - H) // 2, (new_w - W) // 2 + W, (new_h - H) // 2 + H))
    bg_photo = ImageTk.PhotoImage(aplicar_oscurecimiento(img_cropped, darkness_factor))

    if getattr(main_canvas, "bg_id", None):
        main_canvas.itemconfig(main_canvas.bg_id, image=bg_photo)
    else:
        main_canvas.bg_id = main_canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        main_canvas.tag_lower(main_canvas.bg_id)


def cargar_logo(ruta, ancho_max):
    if not os.path.exists(ruta):
        return None
    try:
        img = Image.open(ruta)
        ancho = min(ancho_max, img.size[0])
        h_size = int(float(img.size[1]) * (ancho / float(img.size[0])))
        return ImageTk.PhotoImage(img.resize((ancho, h_size), Image.Resampling.LANCZOS))
    except Exception:
        return None


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

    if logo_img is None:
        logo_img = cargar_logo(LOGO_RUTA, 160)
    logo_h = logo_img.height() if logo_img else 0
    y_top = max(int(0.18 * H), logo_h + 70)

    if logo_img:
        main_canvas.create_image(x_center, int(logo_h / 2) + 12, image=logo_img, tags="ui")

    create_text_with_shadow(main_canvas, x_center, y_top + 10, "Bienvenidos al desafío ucabista", ("Century Gothic", max(18, int(H * 0.03)), "bold"), TEXT_LIGHT, "ui")
    create_text_with_shadow(main_canvas, x_center, y_top + 48, "Ingresa tu nombre de usuario para comenzar a jugar", ("Arial", max(11, int(H * 0.017)), "normal"), TEXT_LIGHT, "ui")

    if entrada_widget is None:
        entrada_widget = Entry(root, font=("Arial", 12), justify="center", width=20, bd=0, highlightthickness=1, relief="flat")
        entrada_widget.config(highlightbackground="#cccccc", highlightcolor="#aaaaaa")

    main_canvas.create_window(x_center, y_top + 92, window=entrada_widget, width=min(420, int(W * 0.32)), height=34, tags="ui")
    create_text_with_shadow(main_canvas, x_center, y_top + 132, "Selecciona un juego para comenzar", ("Arial", max(12, int(H * 0.018)), "italic"), TEXT_LIGHT, "ui")

    total_w = min(0.85 * W, 900)
    pr_w = (total_w - 40) / 3
    pr_h = min(0.35 * (H - (y_top + 260)), 80)
    gap = 20
    start_x = (W - (3 * pr_w + 2 * gap)) / 2 + pr_w / 2
    y_center = y_top + 320

    def crear_prisma_menu(xc, yc, w, h, color, texto, text_color, comando):
        pts = prisma_points(xc, yc, w, h)
        poly = main_canvas.create_polygon(pts, fill=color, outline="", smooth=False, tags=("ui", "prism"))
        txt = main_canvas.create_text(xc, yc, text=texto, font=("Arial", max(12, int(pr_w / 12)), "bold"), fill=text_color, tags=("ui", "prism"))
        for item in (poly, txt):
            main_canvas.tag_bind(item, "<Button-1>", lambda e, cmd=comando: cmd())

    crear_prisma_menu(start_x, y_center, pr_w, pr_h, UCAB_YELLOW, "Apensar", TEXT_DARK, abrir_ventana_apensar)
    crear_prisma_menu(start_x + pr_w + gap, y_center, pr_w, pr_h, UCAB_BLUE, "Trivia", TEXT_LIGHT, abrir_ventana_trivia)
    crear_prisma_menu(start_x + 2 * (pr_w + gap), y_center, pr_w, pr_h, UCAB_GREEN, "Wordle", TEXT_LIGHT, abrir_ventana_wordle)

    bx, by = W - 98, H - 38
    main_canvas.create_rectangle(bx - 80, by - 20, bx + 80, by + 20, fill="red", outline="", tags=("ui", "btn_salir"))
    main_canvas.create_text(bx, by, text="Salir de la App :(", fill="white", font=("Arial", 11, "bold"), tags=("ui", "btn_salir"))

    def cerrar_todo(event):
        root.quit()
        root.destroy()

    main_canvas.tag_bind("btn_salir", "<Button-1>", cerrar_todo)


root.bind("<Configure>", on_configure)
root.after(100, reposicionar_widgets)
root.mainloop()
