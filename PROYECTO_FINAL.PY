import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

# =========================
# CONFIGURACIÓN GENERAL
# =========================
BG = "#3DA5dc"
UCAB_YELLOW = "#f9c32b"
UCAB_BLUE = "#0072CE"
UCAB_GREEN = "#008343"
TEXT_DARK = "#131514"
TEXT_LIGHT = "#ffffff"
HOVER_FACTOR = 0.92
FONDO_RUTA = "fondo.ucab.png"
LOGO_RUTA = "Logo_UCAB.png"

# =========================
# CLASE: TRIVIA UCAB
# =========================
class TriviaUCABApp:
    def __init__(self, root, player_name):
        self.root = root
        self.player_name = player_name
        self.root.title("Trivia UCAB v1.0")
        self.root.state("zoomed")
        self.root.configure(bg="black")

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

        self.root.update_idletasks()
        self.screen_width = self.root.winfo_width()
        self.screen_height = self.root.winfo_height()

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

        self.canvas = tk.Canvas(root, width=self.screen_width, height=self.screen_height, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        if self.bg_photo:
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        else:
            self.canvas.configure(bg="black")

        self.create_ui_elements()
        self.load_question(0)

    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def create_ui_elements(self):
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
            (center_x - 210, center_y + 90),
            (center_x + 210, center_y + 90),
            (center_x - 210, center_y + 200),
            (center_x + 210, center_y + 200),
        ]

        for i, pos in enumerate(positions):
            x_c, y_c = pos
            x1, y1 = x_c - btn_w // 2, y_c - btn_h // 2
            x2, y2 = x_c + btn_w // 2, y_c + btn_h // 2

            btn_tag = f"btn_{i}"
            bg_id = self.create_rounded_rect(x1, y1, x2, y2, radius=20, fill=self.color_gold, tags=(btn_tag, "btn_bg"))
            text_id = self.canvas.create_text(x_c, y_c, text="", font=("Arial", 15, "bold"), fill=self.color_green, width=btn_w - 40, justify="center", tags=(btn_tag, "btn_text"))
            self.custom_btns.append({"bg": bg_id, "text": text_id, "tag": btn_tag})
            self.canvas.tag_bind(btn_tag, "<Button-1>", lambda e, idx=i: self.check_answer(idx))
            self.canvas.tag_bind(btn_tag, "<Enter>", lambda e, idx=i: self.on_hover(idx, True))
            self.canvas.tag_bind(btn_tag, "<Leave>", lambda e, idx=i: self.on_hover(idx, False))

        exit_w, exit_h = 220, 50
        exit_x1, exit_y1 = center_x - exit_w // 2, center_y + 320
        exit_x2, exit_y2 = center_x + exit_w // 2, center_y + 320 + exit_h

        exit_tag = "btn_exit"
        self.exit_bg = self.create_rounded_rect(exit_x1, exit_y1, exit_x2, exit_y2, radius=15, fill=self.color_exit, tags=(exit_tag, "exit_bg"))
        self.exit_text = self.canvas.create_text(center_x, center_y + 345, text="Salir del Juego", font=("Arial", 14, "bold"), fill="white", tags=(exit_tag, "exit_text"))

        self.canvas.tag_bind(exit_tag, "<Button-1>", lambda e: self.root.destroy())
        self.canvas.tag_bind(exit_tag, "<Enter>", lambda e: self.canvas.itemconfig(self.exit_bg, fill=self.color_exit_hover))
        self.canvas.tag_bind(exit_tag, "<Leave>", lambda e: self.canvas.itemconfig(self.exit_bg, fill=self.color_exit))

    def on_hover(self, idx, entering):
        if not self.buttons_active:
            return
        color = self.color_light_gold if entering else self.color_gold
        self.set_button_color(idx, color, self.color_green)

    def set_button_color(self, idx, bg_color, fg_color):
        btn = self.custom_btns[idx]
        self.canvas.itemconfig(btn["bg"], fill=bg_color)
        self.canvas.itemconfig(btn["text"], fill=fg_color)

    def load_question(self, index):
        if index < self.num_questions:
            self.buttons_active = True
            for i in range(4):
                self.set_button_color(i, self.color_gold, self.color_green)
            self.canvas.itemconfigure("feedback_text", text="")
            self.current_question_data = self.selected_questions[index]
            self.canvas.itemconfig(self.lbl_level_id, text=f"Nivel: {index + 1}/{self.num_questions}")
            self.canvas.itemconfig(self.lbl_lives_id, text=f"Vidas: {'❤️ ' * self.player_lives}")

            texto_pregunta = f"Nivel {index + 1}: {self.current_question_data['pregunta']}"
            self.canvas.itemconfigure("q_text", text=texto_pregunta)

            options = self.current_question_data["opciones"]
            shuffled_options = random.sample(options, len(options))
            self.current_shuffled_options = shuffled_options

            for i, text in enumerate(shuffled_options):
                self.canvas.itemconfig(self.custom_btns[i]["text"], text=f"{chr(65 + i)}: {text}")
        else:
            messagebox.showinfo("¡Felicidades!", f"🎓 ¡Felicidades {self.player_name}! Has completado la Trivia UCAB con éxito.")
            self.root.destroy()

    def check_answer(self, button_index):
        if not self.buttons_active:
            return
        self.buttons_active = False
        selected_answer = self.current_shuffled_options[button_index]
        correct_answer = self.current_question_data["respuesta"]
        correct_button_index = self.current_shuffled_options.index(correct_answer)

        if selected_answer == correct_answer:
            self.set_button_color(button_index, "#28a745", "white")
            self.canvas.itemconfigure("feedback_text", text="¡Respuesta Correcta! ✅", fill="#28a745")
            self.current_question_index += 1
            self.root.after(2000, lambda: self.load_question(self.current_question_index))
        else:
            self.player_lives -= 1
            self.canvas.itemconfig(self.lbl_lives_id, text=f"Vidas: {'❤️ ' * self.player_lives}")
            self.set_button_color(button_index, "#dc3545", "white")
            self.canvas.itemconfigure("feedback_text", text="Respuesta Incorrecta ❌", fill="#dc3545")
            self.set_button_color(correct_button_index, "#28a745", "white")

            if self.player_lives > 0:
                preguntas_usadas = [q["pregunta"] for q in self.selected_questions]
                preguntas_disponibles = [q for q in self.questions_db if q["pregunta"] not in preguntas_usadas]
                if preguntas_disponibles:
                    nueva_pregunta = random.choice(preguntas_disponibles)
                else:
                    opciones_emergencia = [q for q in self.questions_db if q["pregunta"] != self.current_question_data["pregunta"]]
                    nueva_pregunta = random.choice(opciones_emergencia)
                self.selected_questions[self.current_question_index] = nueva_pregunta
                self.root.after(2000, lambda: self.load_question(self.current_question_index))
            else:
                self.root.after(2000, self.game_over)

    def game_over(self):
        messagebox.showerror("Fin del Juego", f"💀 {self.player_name}, te has quedado sin vidas. ¡Inténtalo de nuevo!")
        self.root.destroy()


# =========================
# CLASE: WORDLE UCAB
# =========================
class WordleUCABApp:
    def __init__(self, root, player_name):
        self.root = root
        self.player_name = player_name
        self.root.title("Wordle UCAB v1.0")
        self.root.state("zoomed")
        self.root.configure(bg=UCAB_GREEN)

        self.palabras = ["UCAB", "AULAS", "NESTEA", "FERIA", "LOBOS", "ANDRES", "BELLO"]
        self.palabras_restantes = []
        self.palabras_adivinadas = 0
        self.palabra_secreta = ""
        self.intento_actual = 0
        self.largo = 0
        self.letras_escritas = []
        self.cuadros_grid = []

        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.frame_grid = None
        self.text_feedback_id = None
        self.bg_photo = None
        self.enable_input = True

        self.root.bind_all("<Key>", self.on_key)
        self.canvas.focus_set()

        self.load_background()
        self.inicializar_interfaz_juego()

    def load_background(self):
        try:
            if os.path.exists(FONDO_RUTA):
                img = Image.open(FONDO_RUTA).convert("RGBA")
                self.bg_photo = ImageTk.PhotoImage(img.resize((max(1, self.root.winfo_screenwidth()), max(1, self.root.winfo_screenheight())), Image.Resampling.LANCZOS))
                self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
            else:
                self.canvas.configure(bg="#1a1a1a")
        except Exception:
            self.canvas.configure(bg="#1a1a1a")

    def inicializar_interfaz_juego(self):
        self.enable_input = True  # ¡SOLUCIÓN AQUÍ! Reactivamos el teclado para la nueva palabra
        self.canvas.delete("juego")
        self.root.update()
        canvas_w = max(1, self.canvas.winfo_width())
        canvas_h = max(1, self.canvas.winfo_height())
        center_x = canvas_w / 2

        if not self.palabras_restantes:
            self.palabras_restantes = self.palabras.copy()
            random.shuffle(self.palabras_restantes)

        self.palabra_secreta = self.palabras_restantes.pop()
        self.intento_actual = 0
        self.largo = len(self.palabra_secreta)
        self.letras_escritas = []

        header_w = min(canvas_w * 0.78, 760)
        header_h = max(90, int(canvas_h * 0.13))
        header_x0 = int(center_x - header_w / 2)
        header_y0 = int(canvas_h * 0.03)
        header_y1 = header_y0 + header_h

        self.canvas.create_rectangle(header_x0, header_y0, header_x0 + header_w, header_y1, fill=UCAB_GREEN, outline=UCAB_YELLOW, width=max(2, int(canvas_w * 0.003)), tags=("juego",))
        self.canvas.create_text(center_x, header_y0 + (header_h * 0.35), text="WORDLE UCAB 🎓", font=("Arial", max(18, int(min(canvas_w, canvas_h) * 0.03)), "bold"), fill=UCAB_YELLOW, tags=("juego",))
        self.canvas.create_text(center_x, header_y0 + (header_h * 0.75), text=f"Jugador: {self.player_name}         |         Palabras: {self.palabras_adivinadas}/4", font=("Arial", max(11, int(min(canvas_w, canvas_h) * 0.016)), "bold"), fill=TEXT_LIGHT, tags=("juego",))

        panel_w = min(canvas_w * 0.82, 720)
        panel_h = min(canvas_h * 0.62, 520)
        panel_x0 = int(center_x - panel_w / 2)
        panel_y0 = header_y1 + max(10, int(canvas_h * 0.02))
        panel_y1 = panel_y0 + panel_h

        overlay = Image.new("RGBA", (max(2, int(panel_w)), max(2, int(panel_h))), (0, 0, 0, 170))
        self.overlay_photo = ImageTk.PhotoImage(overlay)
        self.canvas.create_image(center_x, panel_y0 + panel_h / 2, image=self.overlay_photo, anchor="center", tags=("juego",))

        self.frame_grid = Frame(self.canvas, bg="#1a1a1a")
        self.canvas.create_window(center_x, panel_y0 + (panel_h * 0.42), window=self.frame_grid, tags=("juego",))

        self.cuadros_grid = []
        font_size = max(16, int(min(canvas_w, canvas_h) * 0.025))
        padx_value = max(3, int(min(canvas_w, canvas_h) * 0.007))
        pady_value = max(3, int(min(canvas_w, canvas_h) * 0.007))
        for fila in range(6):
            fila_cuadros = []
            for col in range(self.largo):
                lbl = Label(self.frame_grid, text="", font=("Comic Sans MS", font_size, "bold"), width=4, height=1, bd=2, relief="solid", bg="white", fg="black")
                lbl.grid(row=fila, column=col, padx=padx_value, pady=pady_value)
                fila_cuadros.append(lbl)
            self.cuadros_grid.append(fila_cuadros)

        instruccion = f"Usa tu teclado para escribir la palabra de {self.largo} letras"
        self.text_feedback_id = self.canvas.create_text(center_x, panel_y0 + (panel_h * 0.88), text=instruccion, font=("Arial", max(11, int(min(canvas_w, canvas_h) * 0.018)), "italic", "bold"), fill=TEXT_LIGHT, tags=("juego",))

        btn_salir = Button(self.canvas, text="Salir del Juego", font=("Arial", max(10, int(min(canvas_w, canvas_h) * 0.014)), "bold"), bg="#D93843", fg=TEXT_LIGHT, activebackground="#A6242B", bd=0, padx=20, pady=6, cursor="hand2", command=self.root.destroy)
        self.canvas.create_window(center_x, panel_y1 + max(20, int(canvas_h * 0.04)), window=btn_salir, tags=("juego",))
        
        self.canvas.focus_set()  # Mantenemos el foco en el canvas principal para capturar los eventos de teclado

    def actualizar_feedback(self, texto, color):
        if self.canvas and self.text_feedback_id:
            self.canvas.itemconfig(self.text_feedback_id, text=texto, fill=color)

    def mostrar_boton_siguiente(self, texto_boton):
        self.enable_input = False
        canvas_w = max(1, self.canvas.winfo_width())
        canvas_h = max(1, self.canvas.winfo_height())
        boton_siguiente = Button(self.canvas, text=texto_boton, font=("Arial", max(10, int(min(canvas_w, canvas_h) * 0.016)), "bold"), bg=UCAB_YELLOW, fg=TEXT_DARK, activebackground="#dca61d", bd=0, padx=15, pady=8, command=self.inicializar_interfaz_juego)
        if self.text_feedback_id:
            coords = self.canvas.coords(self.text_feedback_id)
            pos_y = coords[1] - max(40, int(canvas_h * 0.06))
        else:
            pos_y = int(canvas_h * 0.70)
        self.canvas.create_window(canvas_w / 2, pos_y, window=boton_siguiente, tags=("juego",))

    def mostrar_felicitaciones_wordle(self):
        self.enable_input = False
        mensaje = f"🎓 ¡Felicidades {self.player_name}! Has completado el Wordle UCAB con éxito."
        messagebox.showinfo("¡Felicidades!", mensaje, parent=self.root)
        self.root.destroy()

    def on_key(self, event):
        if not self.enable_input:
            return
        if self.intento_actual >= 6:
            return
        if event.char is None:
            return

        tecla = event.char.upper()

        if tecla.isalpha() and len(tecla) == 1:
            if len(self.letras_escritas) < self.largo:
                self.letras_escritas.append(tecla)
                columna_actual = len(self.letras_escritas) - 1
                self.cuadros_grid[self.intento_actual][columna_actual].config(text=tecla)
        elif event.keysym == "BackSpace":
            if len(self.letras_escritas) > 0:
                columna_a_borrar = len(self.letras_escritas) - 1
                self.cuadros_grid[self.intento_actual][columna_a_borrar].config(text="")
                self.letras_escritas.pop()
        elif event.keysym == "Return":
            if len(self.letras_escritas) != self.largo:
                self.actualizar_feedback(f"¡Te faltan letras! Deben ser {self.largo}", UCAB_YELLOW)
                return

            intento = "".join(self.letras_escritas)
            self.actualizar_feedback("", TEXT_LIGHT)
            copia_letras = list(self.palabra_secreta)
            colores = ["#787C7E"] * self.largo

            for i in range(self.largo):
                if intento[i] == self.palabra_secreta[i]:
                    colores[i] = "#6AAA64"
                    copia_letras[i] = None

            for i in range(self.largo):
                if colores[i] != "#6AAA64":
                    if intento[i] in copia_letras:
                        colores[i] = "#C9B458"
                        copia_letras[copia_letras.index(intento[i])] = None

            for i in range(self.largo):
                self.cuadros_grid[self.intento_actual][i].config(bg=colores[i], fg="white")

            if intento == self.palabra_secreta:
                self.palabras_adivinadas += 1
                if self.palabras_adivinadas >= 4:
                    self.mostrar_felicitaciones_wordle()
                else:
                    self.actualizar_feedback(f"¡EXCELENTE! Llevas {self.palabras_adivinadas}/4 🎉", "#6AAA64")
                    self.mostrar_boton_siguiente("SIGUIENTE PALABRA →")
                return

            self.intento_actual += 1
            self.letras_escritas = []
            if self.intento_actual >= 6:
                self.actualizar_feedback(f"Se acabaron los intentos. Era: {self.palabra_secreta} 😢", "#D93843")
                self.mostrar_boton_siguiente("INTENTAR DE NUEVO 🔄")


# =========================
# INTERFAZ PRINCIPAL
# =========================
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


logo_img = cargar_logo(LOGO_RUTA, 160)


def clamp(v, a=0, b=255):
    return max(a, min(b, int(v)))


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def adjust_brightness(hexcol, factor):
    r, g, b = hex_to_rgb(hexcol)
    r = clamp(r * factor)
    g = clamp(g * factor)
    b = clamp(b * factor)
    return rgb_to_hex((r, g, b))


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
        xc - half_body, yc - half_tail_h,
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
    Label(v, text="¡Bienvenido al juego de Apensar,", font=("Arial", 16, "bold"), bg=UCAB_YELLOW, fg=TEXT_DARK).pack(pady=(40, 4))
    Label(v, text=n, font=("Arial", 16, "bold"), bg=UCAB_YELLOW, fg=TEXT_DARK).pack(pady=(0, 20))
    Button(v, text="Cerrar", command=v.destroy, bg=TEXT_DARK, fg=TEXT_LIGHT, font=("Arial", 11, "bold"), padx=12, pady=6).pack(pady=8)


def abrir_ventana_trivia():
    n = nombre_usuario()
    welcome_win = Toplevel(root)
    welcome_win.title("Bienvenida - Trivia UCAB")
    welcome_win.geometry("500x300")
    welcome_win.config(bg=UCAB_BLUE)

    Label(welcome_win, text=f"¡Bienvenido al juego de trivia,\n{n}!", font=("Arial", 18, "bold"), bg=UCAB_BLUE, fg=TEXT_LIGHT, justify="center").pack(pady=(70, 30))

    def iniciar_juego():
        welcome_win.destroy()
        v = Toplevel(root)
        TriviaUCABApp(v, n)

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
        v = Toplevel(root)
        WordleUCABApp(v, n)

    Button(welcome_win, text="Empezar el juego", command=iniciar_juego, bg=UCAB_YELLOW, fg=TEXT_DARK, font=("Arial", 14, "bold"), padx=20, pady=10, cursor="hand2").pack()


def create_text_with_shadow(canvas, x, y, text, font, fill, shadow_color="#000000", offset=(1, 1), tags=()):
    sx, sy = offset
    canvas.create_text(x + sx, y + sy, text=text, font=font, fill=shadow_color, tags=tags)
    return canvas.create_text(x, y, text=text, font=font, fill=fill, tags=tags)


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
    img_dark = aplicar_oscurecimiento(img_cropped, 0.45)
    bg_photo = ImageTk.PhotoImage(img_dark)
    if getattr(main_canvas, "bg_id", None):
        main_canvas.itemconfig(main_canvas.bg_id, image=bg_photo)
    else:
        main_canvas.bg_id = main_canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        main_canvas.tag_lower(main_canvas.bg_id)


def dibujar_ui():
    main_canvas.delete("ui")
    W = main_canvas.winfo_width() or 960
    H = main_canvas.winfo_height() or 640
    x_center = W / 2

    logo_h = logo_img.height() if logo_img else 0
    y_top = max(int(0.18 * H), logo_h + 70)

    if logo_img:
        main_canvas.create_image(x_center, int(logo_h / 2) + 12, image=logo_img, tags=("ui",))

    title_font = ("Century Gothic", max(18, int(H * 0.03)), "bold")
    subtitle_font = ("Arial", max(11, int(H * 0.017)), "normal")
    instruction_font = ("Arial", max(12, int(H * 0.018)), "italic")

    create_text_with_shadow(main_canvas, x_center, y_top + 10, "Bienvenidos al desafío ucabista", title_font, TEXT_LIGHT, shadow_color="#000000", offset=(2, 2), tags=("ui",))
    create_text_with_shadow(main_canvas, x_center, y_top + 48, "Ingresa tu nombre de usuario para comenzar a jugar", subtitle_font, TEXT_LIGHT, shadow_color="#000000", offset=(1, 1), tags=("ui",))

    entrada_w = min(420, int(W * 0.32))
    main_canvas.create_window(x_center, y_top + 92, window=entrada_widget, width=entrada_w, height=34, tags=("ui",))

    create_text_with_shadow(main_canvas, x_center, y_top + 132, "Selecciona un juego para comenzar", instruction_font, TEXT_LIGHT, shadow_color="#000000", offset=(1, 1), tags=("ui",))

    total_w = min(0.85 * W, 900)
    pr_w = (total_w - 40) / 3
    pr_h = min(0.35 * (H - (y_top + 260)), 80)
    gap = 20
    start_x = (W - (3 * pr_w + 2 * gap)) / 2 + pr_w / 2
    y_center = y_top + 320

    def crear_prisma(xc, yc, w, h, color, texto, text_color, comando):
        pts = prisma_points(xc, yc, w, h)
        poly = main_canvas.create_polygon(pts, fill=color, outline="", smooth=False, tags=("ui", "prism"))
        txt = main_canvas.create_text(xc, yc, text=texto, font=("Arial", max(12, int(pr_w / 12)), "bold"), fill=text_color, tags=("ui", "prism"))

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
    crear_prisma(start_x + 2 * (pr_w + gap), y_center, pr_w, pr_h, UCAB_GREEN, "Wordle", TEXT_LIGHT, abrir_ventana_wordle)

    btn_w = 160
    btn_h = 40
    bx = W - btn_w / 2 - 18
    by = H - btn_h / 2 - 18
    rect = main_canvas.create_rectangle(bx - btn_w / 2, by - btn_h / 2, bx + btn_w / 2, by + btn_h / 2, fill="red", outline="", tags=("ui", "btn"))
    txt = main_canvas.create_text(bx, by, text="Salir de la App :(", fill="white", font=("Arial", 11, "bold"), tags=("ui", "btn"))

    def salir_click(e=None):
        root.destroy()

    for item in (rect, txt):
        main_canvas.tag_bind(item, "<Button-1>", lambda e: salir_click())


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