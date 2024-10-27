import tkinter as tk
from tkinter import messagebox


class AntSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Hormiga")

        # Configura el tamaño de la ventana
        self.root.geometry("800x600")

        # Crear elementos de la interfaz
        self.create_widgets()

    def create_widgets(self):
        # Botón para crear el laberinto
        self.create_maze_button = tk.Button(
            self.root, text="Crear Laberinto", command=self.create_maze
        )
        self.create_maze_button.pack(pady=10)

        # Botón para iniciar la simulación
        self.start_simulation_button = tk.Button(
            self.root, text="Iniciar Simulación", command=self.start_simulation
        )
        self.start_simulation_button.pack(pady=10)

        # Botón para ver estadísticas
        self.view_stats_button = tk.Button(
            self.root, text="Ver Estadísticas", command=self.view_stats
        )
        self.view_stats_button.pack(pady=10)

    def create_maze(self):
        messagebox.showinfo("Crear Laberinto", "Función para crear el laberinto.")

    def start_simulation(self):
        messagebox.showinfo("Iniciar Simulación", "Función para iniciar la simulación.")

    def view_stats(self):
        messagebox.showinfo("Estadísticas", "Función para ver estadísticas de la simulación.")


# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AntSimulationApp(root)
    root.mainloop()
