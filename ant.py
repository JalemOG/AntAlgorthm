from items.sugar import Sugar
from items.wine import Wine
from items.poison import Poison
from items.rock import Rock
from items.goal import Goal

class Ant:
    def __init__(self, start_position, maze):
        self.position = start_position
        self.maze = maze
        self.health = 100
        self.points = 0
        self.alcohol_level = 0

    def is_alive(self):
        return self.health > 0

    def move(self, direction):
        if not self.is_alive():
            return False

        x, y = self.position
        new_position = self.position

        if direction == "UP" and x > 0:
            new_position = (x - 1, y)
        elif direction == "DOWN" and x < self.maze.size - 1:
            new_position = (x + 1, y)
        elif direction == "LEFT" and y > 0:
            new_position = (x, y - 1)
        elif direction == "RIGHT" and y < self.maze.size - 1:
            new_position = (x, y + 1)

        if self.maze.is_valid_position(new_position) and self.maze.is_walkable(new_position):
            self.position = new_position
            return True
        return False

    def interact_with_item(self, item):
        """
        Maneja la interacción con ítems, ya sean objetos o strings
        """
        if not self.is_alive():
            print("La hormiga está muerta y no puede interactuar con ítems.")
            return

        # Si el ítem es un string, convertirlo al objeto correspondiente
        if isinstance(item, str):
            if item == 'S':
                item = Sugar()
            elif item == 'W':
                item = Wine()
            elif item == 'P':
                item = Poison()
            elif item == 'R':
                item = Rock()
            elif item == 'G':
                item = Goal()

        # Procesar el ítem según su tipo
        if isinstance(item, Sugar):
            self.health += 10
            self.points += 10
            print(f"Hormiga consumió azúcar. Salud: {self.health}, Puntos: {self.points}")
            
        elif isinstance(item, Wine):
            self.alcohol_level += 5
            self.health -= 10
            print(f"Hormiga consumió vino. Salud: {self.health}, Nivel de alcohol: {self.alcohol_level}")
            
            if self.alcohol_level > 50:
                self.health -= 10
                print("¡La hormiga está muy borracha y pierde salud extra!")
            
        elif isinstance(item, Poison):
            self.health = 0
            print("¡La hormiga ha consumido veneno y ha muerto!")
            
        elif isinstance(item, Rock):
            print("La hormiga no puede consumir rocas.")

        elif isinstance(item, Goal):
            item.interact(self)
            print(f"¡La hormiga ha alcanzado la meta! Puntos totales: {self.points}")

        # Actualizar estado de salud
        self.update_health(0)  # Solo para verificar límites            

    def update_health(self, change):
        """
        Actualiza y verifica los límites de salud
        """
        self.health += change
        if self.health <= 0:
            self.health = 0
            print("La hormiga ha muerto.")
        elif self.health > 100:
            self.health = 100
            print("La hormiga ha alcanzado su máxima salud.")

    def get_status(self):
        """
        Retorna el estado actual de la hormiga
        """
        return {
            "position": self.position,
            "health": self.health,
            "points": self.points,
            "alcohol_level": self.alcohol_level,
            "is_alive": self.is_alive()
        }