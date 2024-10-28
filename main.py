# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from maze import Maze
from ant import Ant
import random

class AntSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Hormiga")
        
        # Configuración inicial de la ventana
        self.window_width = 1024
        self.window_height = 768
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        
        # Variables de control
        self.maze = None
        self.ant = None
        self.simulation_running = False
        self.cell_size = 40
        
        # Variables de la interfaz
        self.selected_item = tk.StringVar(value="SUGAR")
        self.maze_size = tk.IntVar(value=5)
        self.simulation_speed = tk.IntVar(value=500)
        
        # Inicializar interfaz
        self.setup_ui()
        self.load_images()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal con dos paneles
        self.main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel de control (izquierda)
        self.control_panel = self.create_control_panel()
        
        # Panel de juego (derecha)
        self.game_panel = self.create_game_panel()
        
        # Añadir paneles al PanedWindow
        self.main_frame.add(self.control_panel, weight=1)
        self.main_frame.add(self.game_panel, weight=3)
    
    def create_control_panel(self):
        """Crea el panel de control"""
        control_frame = ttk.Frame(self.main_frame)
        
        # Configuración del laberinto
        maze_config = ttk.LabelFrame(control_frame, text="Configuración del Laberinto")
        maze_config.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(maze_config, text="Tamaño:").pack()
        size_scale = ttk.Scale(maze_config, from_=3, to=10, 
                             variable=self.maze_size, orient=tk.HORIZONTAL)
        size_scale.pack(fill=tk.X, padx=5)
        
        # Selector de items
        items_frame = ttk.LabelFrame(control_frame, text="Tipos de Ítems")
        items_frame.pack(fill=tk.X, padx=5, pady=5)
        
        for item in ["SUGAR", "WINE", "POISON", "ROCK"]:
            ttk.Radiobutton(items_frame, text=item, 
                           variable=self.selected_item, value=item).pack(anchor=tk.W)
        
        # Control de simulación
        sim_control = ttk.LabelFrame(control_frame, text="Control de Simulación")
        sim_control.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(sim_control, text="Velocidad:").pack()
        speed_scale = ttk.Scale(sim_control, from_=100, to=1000, 
                              variable=self.simulation_speed, orient=tk.HORIZONTAL)
        speed_scale.pack(fill=tk.X, padx=5)
        
        # Estado de la hormiga
        self.status_frame = ttk.LabelFrame(control_frame, text="Estado de la Hormiga")
        self.status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_labels = {}
        for stat in ['health', 'alcohol_level', 'points', 'moves']:
            self.status_labels[stat] = ttk.Label(self.status_frame, text=f"{stat}: 0")
            self.status_labels[stat].pack(anchor=tk.W)
        
        # Botones de control
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(buttons_frame, text="Nuevo Laberinto", 
                  command=self.create_maze).pack(fill=tk.X, pady=2)
        self.start_button = ttk.Button(buttons_frame, text="Iniciar Simulación", 
                                     command=self.toggle_simulation)
        self.start_button.pack(fill=tk.X, pady=2)
        ttk.Button(buttons_frame, text="Reiniciar", 
                  command=self.reset_simulation).pack(fill=tk.X, pady=2)
        
        return control_frame
    
    def create_game_panel(self):
        """Crea el panel de juego"""
        game_frame = ttk.Frame(self.main_frame)
        
        # Canvas para el laberinto
        self.canvas = tk.Canvas(game_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configurar evento de redimensionamiento
        self.canvas.bind('<Configure>', self.on_canvas_resize)
        
        return game_frame
    
    def load_images(self):
        """Carga las imágenes del juego"""
        # Similar al código anterior de carga de imágenes
        # [Se mantiene igual que en la versión anterior]
        pass
    
    def create_maze(self):
        """Crea un nuevo laberinto"""
        size = self.maze_size.get()
        self.maze = Maze(size=size)
        self.ant = Ant(start_position=(0, 0), maze=self.maze)
        self.draw_maze()
        self.simulation_running = False
        self.start_button.config(text="Iniciar Simulación")
        self.update_status_display()
    
    def draw_maze(self):
        """Dibuja el laberinto y la hormiga en el canvas con celdas de tamaño constante."""
        self.canvas.delete("all")  # Limpia el canvas

        if not self.maze:
            return

        # Tamaño constante de las celdas (por ejemplo, 40x40 píxeles)
        cell_size = 40

        for row in range(self.maze.size):
            for col in range(self.maze.size):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                # Verifica si la posición está vacía
                fill_color = "white" if self.maze.is_position_empty((row, col)) else "black"
                
                # Dibuja el rectángulo de la celda
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="gray")

                # Dibuja el símbolo del ítem si existe en esa posición
                item_type = self.maze.get_item_at((row, col))
                if item_type:
                    item_symbol = self.maze.item_symbols[item_type]
                    self.canvas.create_text(x1 + cell_size // 2, y1 + cell_size // 2, 
                                            text=item_symbol, font=("Arial", 16))

        # Dibuja la hormiga
        if self.ant:
            ant_x, ant_y = self.ant.position
            x1 = ant_x * cell_size
            y1 = ant_y * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            self.canvas.create_oval(x1, y1, x2, y2, fill="red")


    def update_status_display(self):
        """Actualiza el estado de la hormiga en el panel de estado"""
        if self.ant:
            self.status_labels['health'].config(text=f"Health: {self.ant.health}")
            self.status_labels['alcohol_level'].config(text=f"Alcohol Level: {self.ant.alcohol_level}")
            self.status_labels['points'].config(text=f"Points: {self.ant.points}")
            self.status_labels['moves'].config(text=f"Moves: {self.ant.moves}")

    def toggle_simulation(self):
        """Inicia o pausa la simulación"""
        if self.simulation_running:
            self.simulation_running = False
            self.start_button.config(text="Iniciar Simulación")
        else:
            self.simulation_running = True
            self.start_button.config(text="Pausar Simulación")
            self.run_simulation_step()

    def run_simulation_step(self):
        """Ejecuta un paso de la simulación"""
        if self.simulation_running and self.ant and self.maze:
            self.ant.move()
            self.update_status_display()
            self.draw_maze()
            self.root.after(self.simulation_speed.get(), self.run_simulation_step)

    def reset_simulation(self):
        """Reinicia la simulación"""
        if self.ant:
            self.ant.reset()
            self.update_status_display()
            self.draw_maze()

    def on_canvas_resize(self, event):
        """Redibuja el laberinto cuando se redimensiona el canvas"""
        self.draw_maze()

if __name__ == "__main__":
    root = tk.Tk()
    app = AntSimulationApp(root)
    root.mainloop()
