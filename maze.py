class Maze:
    def __init__(self, size):
        self.size = size  # Tamaño de la matriz del laberinto en celdas
        self.matrix = []   # Inicializar la matriz como una lista vacía
        self.initialize_grid()  # Crear la matriz vacía al instanciar Maze

    def initialize_grid(self):
        """Crea una matriz vacía con el tamaño especificado."""
        self.matrix = [[" " for _ in range(self.size)] for _ in range(self.size)]

    def add_item(self, item_type, position):
        """Agrega un ítem en la posición especificada."""
        x, y = position
        if 0 <= x < self.size and 0 <= y < self.size:
            if item_type == "SUGAR":
                self.matrix[x][y] = "S"
            elif item_type == "WINE":
                self.matrix[x][y] = "W"
            elif item_type == "POISON":
                self.matrix[x][y] = "P"
            elif item_type == "ROCK":
                self.matrix[x][y] = "R"
            else:
                print("Tipo de ítem desconocido, no se ha agregado al laberinto.")
        else:
            print("Posición fuera de los límites del laberinto.")

    def get_state(self):
        """Devuelve la matriz actual para depuración o revisión de estado."""
        return self.matrix

    def print_maze(self):
        """Imprime el estado actual del laberinto en consola (útil para depuración)."""
        for row in self.matrix:
            print(" ".join(row))
