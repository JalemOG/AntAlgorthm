import tkinter as tk
from tkinter import messagebox
from maze import Maze
from ant import Ant
import random


class AntSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Hormiga")

        # Configura el tamaño de la ventana
        self.root.geometry("800x600")

        # Variables de configuración
        self.maze = None  # Inicializa el laberinto como None hasta que se elija el tamaño
        self.ant = None  # Inicializa la hormiga como None
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

        # Botón para iniciar la simulación
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
                # Crear el laberinto con el tamaño elegido por el usuario
                self.maze = Maze(size=size)

                # Crear la hormiga y pasar la referencia del laberinto
                self.ant = Ant(start_position=(0, 0), maze=self.maze)

                # Mostrar la cuadrícula en la interfaz
                self.display_maze_grid()

                messagebox.showinfo("Éxito", f"Laberinto de {size}x{size} creado.")
            else:
                messagebox.showerror("Error", "El tamaño debe estar entre 3 y 10.")
        else:
            messagebox.showerror("Error", "Introduce un tamaño válido entre 3 y 10.")

    def display_maze_grid(self):
        """Crea una cuadrícula en la interfaz para visualizar el laberinto con imágenes."""
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
                cell = tk.Label(self.grid_frame, image=None, borderwidth=1, relief="solid", width=50, height=50)
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
        """Actualiza la cuadrícula visual en la interfaz para reflejar el estado actual del laberinto con imágenes."""
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

        # Mostrar la posición de la hormiga
        ant_x, ant_y = self.ant.position
        self.cells[ant_x][ant_y].config(image=self.ant_image)

    def start_simulation(self):
        """Inicia la simulación de movimiento automático de la hormiga."""
        self.run_simulation_step()

    def run_simulation_step(self):
        """Ejecuta un paso de la simulación."""
        if self.ant.is_alive():
            # Selecciona una dirección aleatoria de movimiento
            direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            self.ant.move(direction)

            # Verificar si hay un ítem en la nueva posición de la hormiga
            ant_x, ant_y = self.ant.position
            item = self.maze.matrix[ant_x][ant_y]
            if item != " ":
                self.ant.eat_item(item)
                # Elimina el ítem del laberinto después de consumirlo
                self.maze.matrix[ant_x][ant_y] = " "

            # Actualiza la cuadrícula para reflejar el estado actual del laberinto y la posición de la hormiga
            self.update_maze_grid()

            # Repite la simulación después de un breve retraso
            self.root.after(500, self.run_simulation_step)  # 500 ms de retraso para la simulación
        else:
            messagebox.showinfo("Simulación", "La hormiga ha muerto. Fin de la simulación.")


# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AntSimulationApp(root)
    root.mainloop()
