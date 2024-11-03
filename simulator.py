import tkinter as tk
from tkinter import messagebox, Toplevel
from maze import Maze
from ant import Ant
import random
import time

class AntSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Hormiga")
        self.root.geometry("600x850")
        self.root.resizable(False, False)

        # Configuración de estilo general
        self.configure_styles()
        
        # Variables de configuración
        self.maze = None
        self.ant = None
        self.simulation_active = False
        self.ant_start_position = (0, 0)
        self.grid_created = False
        self.selected_item = tk.StringVar()
        self.selected_item.set("SUGAR")
        self.simulation_paused = False
        self.simulation_speed = 1
        self.base_speed = 500 
        self.time_multiplier = 1
        self.last_update_time = 0
        self.initial_maze_state = None

        # Cargar las imágenes
        self.ant_image = tk.PhotoImage(file="images/ant.png").subsample(24)
        self.sugar_image = tk.PhotoImage(file="images/sugar.png").subsample(28)
        self.wine_image = tk.PhotoImage(file="images/wine.png").subsample(10)
        self.poison_image = tk.PhotoImage(file="images/poison.png").subsample(10)
        self.rock_image = tk.PhotoImage(file="images/rock.png").subsample(12)
        self.goal_image = tk.PhotoImage(file="images/goal.png").subsample(12)

        # Crear elementos de la interfaz
        self.create_widgets()

    def create_stats_panel(self, simulation_frame):
        """Crea el panel de estadísticas y controles"""
        stats_frame = tk.Frame(simulation_frame, bg=self.bg_color)
        stats_frame.pack(side='right', padx=10, pady=10, fill='y')

        # Variables para las estadísticas
        self.health_var = tk.StringVar(value="Salud: 100")
        self.points_var = tk.StringVar(value="Puntos: 0")
        self.alcohol_var = tk.StringVar(value="Alcohol: 0")
        self.time_var = tk.StringVar(value="Tiempo: 00:00")

        # Estilo para las etiquetas de estadísticas
        label_style = {'bg': self.bg_color, 
                    'fg': self.fg_color, 
                    'font': ('Helvetica', 12), 
                    'pady': 5}

        # Crear las etiquetas de estadísticas
        tk.Label(stats_frame, textvariable=self.health_var, **label_style).pack(anchor='w')
        tk.Label(stats_frame, textvariable=self.points_var, **label_style).pack(anchor='w')
        tk.Label(stats_frame, textvariable=self.alcohol_var, **label_style).pack(anchor='w')
        tk.Label(stats_frame, textvariable=self.time_var, **label_style).pack(anchor='w')

        # Separador
        tk.Frame(stats_frame, height=2, bg=self.accent_color).pack(fill='x', pady=10)

        # Control de pausa
        self.pause_button = tk.Button(
            stats_frame,
            text="Pausar",
            command=self.toggle_pause,
            font=self.button_font,
            bg=self.button_color,
            fg=self.fg_color,
            activebackground=self.hover_color,
            activeforeground=self.fg_color,
            relief='flat',
            width=15
        )
        self.pause_button.pack(pady=10)

        # Control de velocidad
        speed_frame = tk.Frame(stats_frame, bg=self.bg_color)
        speed_frame.pack(pady=10)

        tk.Label(
            speed_frame,
            text="Velocidad:",
            bg=self.bg_color,
            fg=self.fg_color,
            font=self.label_font
        ).pack()

        self.speed_scale = tk.Scale(
            speed_frame,
            from_=1,
            to=20,
            orient='horizontal',
            command=self.update_speed,
            bg=self.bg_color,
            fg=self.fg_color,
            highlightthickness=0,
            troughcolor=self.button_color,
            activebackground=self.hover_color
        )
        self.speed_scale.set(1)
        self.speed_scale.pack()

    def toggle_pause(self):
        """Alterna entre pausa y reproducción"""
        self.simulation_paused = not self.simulation_paused
        self.pause_button.config(text="Reanudar" if self.simulation_paused else "Pausar")
        
        if not self.simulation_paused:
            self.last_update_time = time.time()
            self.run_simulation_step()

    def update_speed(self, value):
        """Actualiza la velocidad de simulación"""
        self.simulation_speed = int(value)
        self.time_multiplier = self.simulation_speed

    def update_stats(self):
        """Actualiza las estadísticas en tiempo real"""
        if hasattr(self, 'ant') and self.ant.is_alive():
            status = self.ant.get_status()
            self.health_var.set(f"Salud: {status['health']}")
            self.points_var.set(f"Puntos: {status['points']}")
            self.alcohol_var.set(f"Alcohol: {status['alcohol_level']}")

    def update_timer(self):
        """Actualiza el cronómetro considerando la velocidad"""
        if hasattr(self, 'ant') and self.ant.is_alive() and not self.simulation_paused:
            current_time = time.time()
            elapsed_real_time = current_time - self.last_update_time
            self.last_update_time = current_time
            
            # Ajustar el tiempo según la velocidad
            self.elapsed_simulation_time += elapsed_real_time * self.time_multiplier
            
            minutes = int(self.elapsed_simulation_time) // 60
            seconds = int(self.elapsed_simulation_time) % 60
            self.time_var.set(f"Tiempo: {minutes:02d}:{seconds:02d}")

    def configure_styles(self):
        # Configuración de colores
        self.bg_color = "#2C3E50"  # Azul oscuro elegante
        self.fg_color = "#ECF0F1"  # Blanco suave
        self.accent_color = "#3498DB"  # Azul claro
        self.button_color = "#2980B9"  # Azul medio
        self.hover_color = "#1ABC9C"  # Verde azulado
        self.grid_bg = "#FFFFFF"  # Blanco puro para el grid
        self.grid_lines = "#BDC3C7"  # Gris claro para las líneas del grid

        # Configuración de la ventana principal
        self.root.configure(bg=self.bg_color)
        
        # Definir estilos de fuente
        self.title_font = ('Helvetica', 14, 'bold')
        self.label_font = ('Helvetica', 11)
        self.button_font = ('Helvetica', 11, 'bold')

    def create_widgets(self):
        # Frame principal para organizar widgets
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=10)
        main_frame.pack(fill='both', expand=True)

        # Título
        title_label = tk.Label(
            main_frame,
            text="Simulación de Hormiga",
            font=('Helvetica', 16, 'bold'),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack(pady=(0, 20))

        # Sección de configuración del laberinto
        tk.Label(
            main_frame,
            text="Tamaño del laberinto (3-10):",
            font=self.label_font,
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(pady=(5, 2))

        self.size_entry = tk.Entry(
            main_frame,
            font=self.label_font,
            justify='center',
            bg=self.fg_color
        )
        self.size_entry.pack(pady=(0, 10))

        self.create_maze_button = tk.Button(
            main_frame,
            text="Crear Laberinto",
            command=self.create_maze,
            font=self.button_font,
            bg=self.button_color,
            fg=self.fg_color,
            activebackground=self.hover_color,
            activeforeground=self.fg_color,
            relief='flat',
            padx=20,
            pady=5
        )
        self.create_maze_button.pack(pady=10)

        # Sección de selección de ítems
        tk.Label(
            main_frame,
            text="Selecciona el tipo de ítem:",
            font=self.label_font,
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(pady=(15, 5))

        item_menu = tk.OptionMenu(
            main_frame,
            self.selected_item,
            "SUGAR",
            "WINE",
            "POISON",
            "ROCK",
            "GOAL"
        )
        item_menu.configure(
            font=self.label_font,
            bg=self.button_color,
            fg=self.fg_color,
            activebackground=self.hover_color,
            activeforeground=self.fg_color,
            relief='flat',
            highlightthickness=0
        )
        item_menu["menu"].configure(
            font=self.label_font,
            bg=self.button_color,
            fg=self.fg_color,
            activebackground=self.hover_color,
            activeforeground=self.fg_color
        )
        item_menu.pack(pady=5)

        # Sección de posición inicial
        tk.Label(
            main_frame,
            text="Posición inicial (fila, columna):",
            font=self.label_font,
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(pady=(15, 5))

        self.start_position_entry = tk.Entry(
            main_frame,
            font=self.label_font,
            justify='center',
            bg=self.fg_color
        )
        self.start_position_entry.pack(pady=(0, 10))

        # Botón de inicio de simulación
        self.start_simulation_button = tk.Button(
            main_frame,
            text="Iniciar Simulación",
            command=self.start_simulation,
            font=self.button_font,
            bg=self.accent_color,
            fg=self.fg_color,
            activebackground=self.hover_color,
            activeforeground=self.fg_color,
            relief='flat',
            padx=20,
            pady=5
        )
        self.start_simulation_button.pack(pady=20)

    def create_maze(self):
        size_text = self.size_entry.get()
        if size_text.isdigit():
            size = int(size_text)
            if 3 <= size <= 10:
                self.maze = Maze(size=size)
                self.maze.initialize_grid()
                self.display_maze_grid()
                messagebox.showinfo("Éxito", f"Laberinto de {size}x{size} creado.")
            else:
                messagebox.showerror("Error", "El tamaño debe estar entre 3 y 10.")
        else:
            messagebox.showerror("Error", "Introduce un tamaño válido entre 3 y 10.")

    def display_maze_grid(self):
        if self.grid_created:
            self.grid_frame.destroy()

        self.grid_frame = tk.Frame(self.root, bg=self.bg_color)
        self.grid_frame.pack(pady=10)
        self.grid_created = True

        cell_size = 40
        canvas_size = self.maze.size * cell_size
        self.maze_canvas = tk.Canvas(
            self.grid_frame,
            width=canvas_size,
            height=canvas_size,
            bg=self.grid_bg,
            highlightthickness=2,
            highlightbackground=self.accent_color
        )
        self.maze_canvas.pack()

        self.cells = []
        for i in range(self.maze.size):
            row = []
            for j in range(self.maze.size):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                cell = self.maze_canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=self.grid_bg,
                    outline=self.grid_lines,
                    width=1
                )
                row.append(cell)
                self.maze_canvas.tag_bind(cell, '<Button-1>', lambda e, x=i, y=j: self.add_item_to_maze(x, y))
            self.cells.append(row)

    def add_item_to_maze(self, x, y):
        if self.maze is None:
            messagebox.showerror("Error", "Primero crea un laberinto.")
            return

        item_type = self.selected_item.get()

        if self.maze.matrix[x][y] == " ":
            try:
                self.maze.add_item(item_type, (x, y))
                self.update_maze_grid()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "La celda ya tiene un ítem.")

    def update_maze_grid(self):
        cell_size = 40
        
        for i in range(self.maze.size):
            for j in range(self.maze.size):
                item = self.maze.matrix[i][j]
                
                x = j * cell_size + cell_size // 2
                y = i * cell_size + cell_size // 2
                
                self.maze_canvas.delete(f"image_{i}_{j}")
                
                if item == "S":
                    self.maze_canvas.create_image(x, y, image=self.sugar_image, tags=(f"image_{i}_{j}"))
                elif item == "W":
                    self.maze_canvas.create_image(x, y, image=self.wine_image, tags=(f"image_{i}_{j}"))
                elif item == "P":
                    self.maze_canvas.create_image(x, y, image=self.poison_image, tags=(f"image_{i}_{j}"))
                elif item == "R":
                    self.maze_canvas.create_image(x, y, image=self.rock_image, tags=(f"image_{i}_{j}"))
                elif item == "G":
                    self.maze_canvas.create_image(x, y, image=self.goal_image, tags=(f"image_{i}_{j}"))

    def reset_simulation(self):
        """Reinicia la simulación manteniendo el laberinto actual"""
        # Reiniciar la hormiga a su posición inicial
        self.ant = Ant(start_position=self.ant_start_position, maze=self.maze)
        
        # Reiniciar el tiempo
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.elapsed_simulation_time = 0
        
        # Reiniciar las estadísticas
        self.health_var.set("Salud: 100")
        self.points_var.set("Puntos: 0")
        self.alcohol_var.set("Alcohol: 0")
        self.time_var.set("Tiempo: 00:00")
        
        # Restaurar los ítems del laberinto original
        self.restore_maze_items()
        
        # Actualizar la visualización
        self.update_simulation_grid()


    def restore_maze_items(self):
        """Restaura los ítems del laberinto a su estado original"""
        if self.initial_maze_state:
            self.maze.matrix = [row[:] for row in self.initial_maze_state]


    def start_simulation(self):
        if not self.maze:
            messagebox.showerror("Error", "Primero crea el laberinto antes de iniciar la simulación.")
            return

        if self.simulation_active:
            messagebox.showwarning("Advertencia", "La simulación ya está en ejecución.")
            return

        start_position_text = self.start_position_entry.get()
        start_position_parts = start_position_text.split(",")
        if len(start_position_parts) == 2 and all(part.strip().isdigit() for part in start_position_parts):
            start_x, start_y = int(start_position_parts[0].strip()), int(start_position_parts[1].strip())
            if 0 <= start_x < self.maze.size and 0 <= start_y < self.maze.size:
                self.ant_start_position = (start_x, start_y)
                self.ant = Ant(start_position=self.ant_start_position, maze=self.maze)
                self.initial_maze_state = [row[:] for row in self.maze.matrix]

            else:
                messagebox.showerror("Error", "Posición fuera del rango del laberinto.")
                return
        else:
            messagebox.showerror("Error", "Posición inicial no válida.")
            return

        self.simulation_window = Toplevel(self.root)
        self.simulation_window.title("Simulación en Progreso")
        self.simulation_active = True

        # Configurar estilo de la ventana de simulación
        self.simulation_window.configure(bg=self.bg_color)

        cell_size = 40
        canvas_size = self.maze.size * cell_size
        stats_panel_width = 200  # Ancho del panel de estadísticas
        window_width = canvas_size + stats_panel_width + 60  # Añadir espacio para el panel
        window_height = canvas_size + 40
        self.simulation_window.geometry(f"{window_width}x{window_height}")

        # Frame principal para la simulación
        simulation_frame = tk.Frame(
            self.simulation_window,
            bg=self.bg_color,
            padx=20,
            pady=20
        )
        simulation_frame.pack(fill='both', expand=True)

        # Crear el canvas de simulación
        canvas_frame = tk.Frame(simulation_frame, bg=self.bg_color)
        canvas_frame.pack(side='left')

        self.simulation_canvas = tk.Canvas(
            canvas_frame,
            width=canvas_size,
            height=canvas_size,
            bg=self.grid_bg,
            highlightthickness=2,
            highlightbackground=self.accent_color
        )
        self.simulation_canvas.pack()

        # Crear el panel de estadísticas
        self.create_stats_panel(simulation_frame)

        # Inicializar el tiempo de inicio
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.elapsed_simulation_time = 0

        # Crear la cuadrícula
        self.simulation_cells = []
        for i in range(self.maze.size):
            row = []
            for j in range(self.maze.size):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                cell = self.simulation_canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=self.grid_bg,
                    outline=self.grid_lines,
                    width=1
                )
                row.append(cell)
            self.simulation_cells.append(row)

        self.update_simulation_grid()
        self.run_simulation_step()

    def update_simulation_grid(self):
        cell_size = 40
        
        self.simulation_canvas.delete("ant")
        
        for i in range(self.maze.size):
            for j in range(self.maze.size):
                item = self.maze.matrix[i][j]
                x = j * cell_size + cell_size // 2
                y = i * cell_size + cell_size // 2
                
                self.simulation_canvas.delete(f"item_{i}_{j}")
                
                if item == "S":
                    self.simulation_canvas.create_image(x, y, image=self.sugar_image, tags=f"item_{i}_{j}")
                elif item == "W":
                    self.simulation_canvas.create_image(x, y, image=self.wine_image, tags=f"item_{i}_{j}")
                elif item == "P":
                    self.simulation_canvas.create_image(x, y, image=self.poison_image, tags=f"item_{i}_{j}")
                elif item == "R":
                    self.simulation_canvas.create_image(x, y, image=self.rock_image, tags=f"item_{i}_{j}")
                elif item == "G":
                    self.simulation_canvas.create_image(x, y, image=self.goal_image, tags=f"item_{i}_{j}")

        ant_x, ant_y = self.ant.position
        x = ant_y * cell_size + cell_size // 2
        y = ant_x * cell_size + cell_size // 2
        self.simulation_canvas.create_image(x, y, image=self.ant_image, tags="ant")

    def run_simulation_step(self):
        if self.ant.is_alive() and not self.simulation_paused:
            direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            self.ant.move(direction)

            ant_x, ant_y = self.ant.position
            item = self.maze.matrix[ant_x][ant_y]

            if item != " ":
                if item == "G":
                    self.ant.interact_with_item(item)
                    messagebox.showinfo(
                        "¡Meta alcanzada!",
                        f"La hormiga ha llegado a la meta con {self.ant.points} puntos.\nReiniciando simulación..."
                    )
                    self.reset_simulation()
                    self.simulation_window.lift()  # Traer la ventana de simulación al frente
                    self.simulation_window.focus_force() 
                else:
                    self.ant.interact_with_item(item)
                    self.maze.matrix[ant_x][ant_y] = " "

            self.update_simulation_grid()
            self.update_stats()
            self.update_timer()
            
            # Calcular el delay ajustado según la velocidad
            adjusted_delay = int(self.base_speed / self.simulation_speed)
            self.simulation_window.after(adjusted_delay, self.run_simulation_step)
        elif self.ant.is_alive() and self.simulation_paused:
            self.simulation_window.after(100, self.run_simulation_step)
        else:
            messagebox.showinfo(
                "Fin de la Simulación",
                "La hormiga ha muerto.\nSimulación finalizada",
                icon="info"
            )
