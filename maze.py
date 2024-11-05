class Maze:
    def __init__(self, size):
        self.size = size
        self.matrix = None
        self.has_goal = False  # Atributo para rastrear si ya existe una meta
        self.goal_position = None  
        self.initialize_grid()

    def initialize_grid(self):
        """Inicializa la cuadrícula del laberinto con espacios vacíos"""
        self.matrix = [[" " for _ in range(self.size)] for _ in range(self.size)]
        self.has_goal = False  # Reiniciar el estado de la meta
        self.goal_position = None

    def add_item(self, item_type, position):
        """Añade un ítem en la posición especificada"""
        x, y = position

        if item_type == "GOAL":
            if self.has_goal:
                raise ValueError("Ya existe una meta en el laberinto. Solo puede haber una meta.")
            self.matrix[x][y] = "G"
            self.has_goal = True
            self.goal_position = position
        else:
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
        """
        Verifica si una posición es caminable
        """
        x, y = position
        if not self.is_valid_position(position):
            return False
        return self.matrix[x][y] in [' ', 'S', 'W', 'P', 'G']  # Incluir todos los elementos válidos
    
    def remove_goal(self):
        """Elimina la meta del laberinto si existe"""
        if self.has_goal and self.goal_position is not None:
            x, y = self.goal_position
            self.matrix[x][y] = " "
            self.has_goal = False
            self.goal_position = None