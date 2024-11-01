class Maze:
    def __init__(self, size):
        self.size = size
        self.matrix = None
        self.initialize_grid()

    def initialize_grid(self):
        """Inicializa la cuadrícula del laberinto con espacios vacíos"""
        self.matrix = [[" " for _ in range(self.size)] for _ in range(self.size)]

    def add_item(self, item_type, position):
        """Añade un ítem en la posición especificada"""
        x, y = position
        if item_type == "SUGAR":
            self.matrix[x][y] = "S"
        elif item_type == "WINE":
            self.matrix[x][y] = "W"
        elif item_type == "POISON":
            self.matrix[x][y] = "P"
        elif item_type == "ROCK":
            self.matrix[x][y] = "R"

    def get_item(self, position):
        """Obtiene el ítem en la posición especificada"""
        x, y = position
        return self.matrix[x][y]

    def is_valid_position(self, position):
        """Verifica si una posición está dentro de los límites del laberinto"""
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size

    def is_walkable(self, position):
        """Verifica si una posición es transitable (no hay roca)"""
        x, y = position
        return self.matrix[x][y] != "R"