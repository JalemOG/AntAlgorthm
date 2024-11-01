import tkinter as tk
from tkinter import messagebox, Toplevel
from maze import Maze
from ant import Ant
import random

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

        # Cargar las imágenes
        self.ant_image = tk.PhotoImage(file="images/ant.png").subsample(24)
        self.sugar_image = tk.PhotoImage(file="images/sugar.png").subsample(28)
        self.wine_image = tk.PhotoImage(file="images/wine.png").subsample(10)
        self.poison_image = tk.PhotoImage(file="images/poison.png").subsample(10)
        self.rock_image = tk.PhotoImage(file="images/rock.png").subsample(12)

        # Crear elementos de la interfaz
        self.create_widgets()

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
            "ROCK"
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
            self.maze.add_item(item_type, (x, y))
            self.update_maze_grid()
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
        self.simulation_window.geometry(f"{canvas_size + 40}x{canvas_size + 40}")  # Añadir padding

        # Frame para el canvas con padding
        simulation_frame = tk.Frame(
            self.simulation_window,
            bg=self.bg_color,
            padx=20,
            pady=20
        )
        simulation_frame.pack(fill='both', expand=True)

        self.simulation_canvas = tk.Canvas(
            simulation_frame,
            width=canvas_size,
            height=canvas_size,
            bg=self.grid_bg,
            highlightthickness=2,
            highlightbackground=self.accent_color
        )
        self.simulation_canvas.pack()

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

        ant_x, ant_y = self.ant.position
        x = ant_y * cell_size + cell_size // 2
        y = ant_x * cell_size + cell_size // 2
        self.simulation_canvas.create_image(x, y, image=self.ant_image, tags="ant")

    def run_simulation_step(self):
        if self.ant.is_alive():
            direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            self.ant.move(direction)

            ant_x, ant_y = self.ant.position
            item = self.maze.matrix[ant_x][ant_y]
            if item != " ":
                self.ant.eat_item(item)
                self.maze.matrix[ant_x][ant_y] = " "

            self.update_simulation_grid()
            self.simulation_window.after(500, self.run_simulation_step)
        else:
            messagebox.showinfo(
                "Fin de la Simulación",
                "La hormiga ha muerto.\nSimulación finalizada",
                icon="info"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = AntSimulationApp(root)
    root.mainloop()