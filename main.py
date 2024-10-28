import tkinter as tk
from tkinter import messagebox, Toplevel
from maze import Maze
from ant import Ant
import random


class AntSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Hormiga")

        # Configura el tamaño de la ventana principal
        self.root.geometry("400x300")

        # Variables de configuración
        self.maze = None  # Inicializa el laberinto como None hasta que se elija el tamaño
        self.ant = None  # Inicializa la hormiga como None
        self.simulation_active = False
        self.ant_start_position = (0, 0)  # Posición inicial predeterminada de la hormiga
        self.grid_created = False  # Variable de control para verificar si la cuadrícula fue creada
        self.selected_item = tk.StringVar()
        self.selected_item.set("SUGAR")  # Tipo de ítem predeterminado

        # Cargar las imágenes (aquí puedes poner la ruta a tus imágenes)
        self.ant_image = tk.PhotoImage(file="images/ant.png")
        self.sugar_image = tk.PhotoImage(file="images/sugar.png")
        self.wine_image = tk.PhotoImage(file="images/wine.png")
        self.poison_image = tk.PhotoImage(file="images/poison.png")
        self.rock_image = tk.PhotoImage(file="images/rock.png")

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

        # Entrada para la posición inicial de la hormiga
        tk.Label(self.root, text="Posición inicial de la hormiga (fila, columna):").pack(pady=5)
        self.start_position_entry = tk.Entry(self.root)
        self.start_position_entry.pack(pady=5)

        # Botón para iniciar la simulación
        self.start_simulation_button = tk.Button(
            self.root, text="Iniciar Simulación", command=self.start_simulation
        )
        self.start_simulation_button.pack(pady=10)

    def create_maze(self):
        """Inicializa el laberinto con el tamaño proporcionado por el usuario y permite colocar ítems."""
        size_text = self.size_entry.get()
        if size_text.isdigit():
            size = int(size_text)
            if 3 <= size <= 10:
                # Crear el laberinto y llamar al método para inicializar la matriz
                self.maze = Maze(size=size)
                self.maze.initialize_grid()  # Llama al método para crear la matriz
                # Mostrar la cuadrícula en la interfaz
                self.display_maze_grid()
                messagebox.showinfo("Éxito", f"Laberinto de {size}x{size} creado.")
            else:
                messagebox.showerror("Error", "El tamaño debe estar entre 3 y 10.")
        else:
            messagebox.showerror("Error", "Introduce un tamaño válido entre 3 y 10.")

    def display_maze_grid(self):
        """Crea una cuadrícula en la interfaz principal para definir el laberinto y colocar ítems."""
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
                cell = tk.Label(self.grid_frame, image=None, borderwidth=1, relief="solid", width=30, height=30)
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
        """Actualiza la cuadrícula visual en la interfaz principal para reflejar el estado actual del laberinto con imágenes."""
        for i in range(self.maze.size):
            for j in range(self.maze.size):
                item = self.maze.matrix[i][j]

                # Actualizar la imagen en función del ítem
                if item == "S":
                    self.cells[i][j].config(image=self.sugar_image)
                elif item == "W":
                    self.cells[i][j].config(image=self.wine_image)
                elif item == "P":
                    self.cells[i][j].config(image=self.poison_image)
                elif item == "R":
                    self.cells[i][j].config(image=self.rock_image)
                else:
                    self.cells[i][j].config(image="")  # Celda vacía

    def start_simulation(self):
        """Abre una ventana de simulación y ejecuta el movimiento de la hormiga."""
        if not self.maze:
            messagebox.showerror("Error", "Primero crea el laberinto antes de iniciar la simulación.")
            return

        # Comprobar si ya hay una simulación activa
        if self.simulation_active:
            messagebox.showwarning("Advertencia", "La simulación ya está en ejecución.")
            return

        # Validación de la posición inicial de la hormiga
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

        # Crear la ventana de simulación
        self.simulation_window = Toplevel(self.root)
        self.simulation_window.title("Ventana de Simulación")
        self.simulation_active = True  # Marcar la simulación como activa

        # Configurar la ventana de simulación
        cell_size = 10
        window_size = self.maze.size * cell_size
        self.simulation_window.geometry(f"{window_size}x{window_size}")

        # Crear la cuadrícula en la ventana de simulación
        self.simulation_cells = []
        for i in range(self.maze.size):
            row = []
            for j in range(self.maze.size):
                cell = tk.Label(self.simulation_window, image=None, borderwidth=1, relief="solid", width=cell_size,
                                height=cell_size)
                cell.grid(row=i, column=j)
                row.append(cell)
            self.simulation_cells.append(row)

        # Iniciar la cuadrícula de simulación
        self.update_simulation_grid()
        self.run_simulation_step()

    def update_simulation_grid(self):
        """Actualiza la cuadrícula de la ventana de simulación para mostrar la posición actual de la hormiga y los ítems."""
        for i in range(self.maze.size):
            for j in range(self.maze.size):
                item = self.maze.matrix[i][j]

                # Actualizar la imagen en función del ítem en la celda correspondiente
                if item == "S":
                    self.simulation_cells[i][j].config(image=self.sugar_image)
                elif item == "W":
                    self.simulation_cells[i][j].config(image=self.wine_image)
                elif item == "P":
                    self.simulation_cells[i][j].config(image=self.poison_image)
                elif item == "R":
                    self.simulation_cells[i][j].config(image=self.rock_image)
                else:
                    self.simulation_cells[i][j].config(image="")  # Celda vacía

        # Mostrar la hormiga en su posición actual
        ant_x, ant_y = self.ant.position
        self.simulation_cells[ant_x][ant_y].config(image=self.ant_image)

    def run_simulation_step(self):
        """Ejecuta un paso de la simulación en la ventana de simulación."""
        if self.ant.is_alive():
            # Seleccionar una dirección aleatoria
            direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            self.ant.move(direction)

            # Verificar si hay un ítem en la nueva posición de la hormiga
            ant_x, ant_y = self.ant.position
            item = self.maze.matrix[ant_x][ant_y]
            if item != " ":
                self.ant.eat_item(item)
                # Elimina el ítem del laberinto después de consumirlo
                self.maze.matrix[ant_x][ant_y] = " "

            # Actualizar la cuadrícula para reflejar el estado actual del laberinto y la posición de la hormiga
            self.update_simulation_grid()

            # Repite la simulación después de un breve retraso
            self.simulation_window.after(500, self.run_simulation_step)  # 500 ms de retraso para la simulación
        else:
            messagebox.showinfo("Simulación", "La hormiga ha muerto. Fin de la simulación.")


if __name__ == "__main__":
    root = tk.Tk()  # Crear la ventana principal de Tkinter
    app = AntSimulationApp(root)  # Instanciar la aplicación con la ventana principal
    root.mainloop()  # Ejecutar el bucle principal de Tkinter para mostrar la ventana

