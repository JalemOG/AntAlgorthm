import tkinter as tk
from tkinter import messagebox
from maze import Maze  # Asegúrate de que la clase Maze esté en el archivo correcto
from items.sugar import Sugar
from items.wine import Wine
from items.poison import Poison
from items.rock import Rock
from ant import Ant

class AntSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Hormiga")

        # Configura el tamaño de la ventana
        self.root.geometry("800x600")

        # Variables de configuración
        self.maze = None  # Inicializa la instancia de Maze como None
        self.grid_created = False  # Indica si la cuadrícula ya fue creada
        self.selected_item = tk.StringVar()
        self.selected_item.set("SUGAR")  # Tipo de ítem predeterminado

        # Crear elementos de la interfaz
        self.create_widgets()

    def create_widgets(self):
        # Entrada para el tamaño del laberinto
        tk.Label(self.root, text="Tamaño del laberinto (3-10):").pack(pady=5)
        self.size_entry = tk.Entry(self.root)
        self.size_entry.pack(pady=5)

        # Botón para crear el laberinto
        self.create_maze_button = tk.Button(
            self.root, text="Crear Laberinto", command=self.create_maze
        )
        self.create_maze_button.pack(pady=10)

        # Selector de tipo de ítem a colocar
        tk.Label(self.root, text="Selecciona el tipo de ítem a colocar:").pack(pady=5)
        item_menu = tk.OptionMenu(self.root, self.selected_item, "SUGAR", "WINE", "POISON", "ROCK")
        item_menu.pack(pady=5)

        # Botón para iniciar la simulación (Placeholder)
        self.start_simulation_button = tk.Button(
            self.root, text="Iniciar Simulación", command=self.start_simulation
        )
        self.start_simulation_button.pack(pady=10)

    def create_maze(self):
        """Inicializa el laberinto con el tamaño proporcionado por el usuario."""
        size_text = self.size_entry.get()
        if size_text.isdigit():
            size = int(size_text)
            if 3 <= size <= 10:
                self.maze = Maze(size=size)
                self.display_maze_grid()  # Muestra la cuadrícula en la interfaz
                messagebox.showinfo("Éxito", f"Laberinto de {size}x{size} creado.")
            else:
                messagebox.showerror("Error", "El tamaño debe estar entre 3 y 10.")
        else:
            messagebox.showerror("Error", "Introduce un tamaño válido entre 3 y 10.")

    def display_maze_grid(self):
        """Crea una cuadrícula en la interfaz para visualizar el laberinto."""
        # Eliminar cuadrícula existente si ya fue creada
        if self.grid_created:
            self.grid_frame.destroy()

        # Crear un nuevo Frame para la cuadrícula
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=10)
        self.grid_created = True  # Marcar la cuadrícula como creada

        # Crear la cuadrícula de celdas
        self.cells = []
        for i in range(self.maze.size):
            row = []
            for j in range(self.maze.size):
                cell = tk.Label(self.grid_frame, text=" ", borderwidth=1, relief="solid", width=4, height=2)
                cell.grid(row=i, column=j)
                cell.bind("<Button-1>", lambda e, x=i, y=j: self.add_item_to_maze(x, y))  # Vincula clic a cada celda
                row.append(cell)
            self.cells.append(row)

    def add_item_to_maze(self, x, y):
        """Agrega el ítem seleccionado al laberinto en la posición (x, y) si es válida."""
        if self.maze is None:
            messagebox.showerror("Error", "Primero crea un laberinto.")
            return

        item_type = self.selected_item.get()

        # Verificar que la celda esté vacía antes de colocar un ítem
        if self.maze.matrix[x][y] == " ":
            self.maze.add_item(item_type, (x, y))
            self.update_maze_grid()
        else:
            messagebox.showerror("Error", "La celda ya tiene un ítem. Elige otra posición.")

    def update_maze_grid(self):
        """Actualiza la cuadrícula visual en la interfaz para reflejar el estado actual del laberinto."""
        for i in range(self.maze.size):
            for j in range(self.maze.size):
                item = self.maze.matrix[i][j]
                self.cells[i][j].config(text=item if item != " " else "")

    def start_simulation(self):
        messagebox.showinfo("Iniciar Simulación", "Función para iniciar la simulación.")


# Ejecutar la aplicación
if __name__ == "__main__":
    # Crear una hormiga
    ant = Ant(start_position=(0, 0), maze_size=(5, 5))

    # Crear ítems
    sugar = Sugar()
    wine = Wine()
    poison = Poison()
    rock = Rock()

    # Consumir los ítems
    sugar.consume(ant)  # La hormiga gana puntos
    wine.consume(ant)  # La hormiga incrementa su nivel de alcohol
    poison.consume(ant)  # La hormiga consume veneno y muere
    rock.consume(ant)  # La hormiga intenta consumir la roca sin efecto

    root = tk.Tk()
    app = AntSimulationApp(root)
    root.mainloop()
