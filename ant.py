class Ant:
    def __init__(self, start_position, maze):
        # Posición inicial de la hormiga en el laberinto
        self.position = start_position
        self.health = 100            # Salud inicial
        self.alcohol_level = 0       # Nivel inicial de alcohol
        self.points = 0              # Puntos iniciales
        self.maze = maze             # Referencia al objeto Maze para conocer el estado y tamaño

    def move(self, direction):
        """Mueve la hormiga en la dirección especificada, respetando los límites del laberinto."""
        x, y = self.position
        if direction == "UP" and x > 0:
            x -= 1
        elif direction == "DOWN" and x < self.maze.size - 1:
            x += 1
        elif direction == "LEFT" and y > 0:
            y -= 1
        elif direction == "RIGHT" and y < self.maze.size - 1:
            y += 1
        else:
            return  # Movimiento no válido, permanece en la misma posición

        self.position = (x, y)
        print(f"La hormiga se movió hacia {direction}. Nueva posición: {self.position}")

    def eat_item(self, item_type):
        """Interacción con ítems encontrados en el laberinto."""
        if item_type == "SUGAR":
            self.points += 10
            print("La hormiga consumió azúcar y ganó puntos. Puntos actuales:", self.points)
        elif item_type == "WINE":
            self.alcohol_level += 5
            print("La hormiga consumió vino. Nivel de alcohol actual:", self.alcohol_level)
            if self.alcohol_level > 50:
                self.health -= 10
                print("La hormiga está borracha y pierde salud. Salud actual:", self.health)
        elif item_type == "POISON":
            self.health = 0
            print("La hormiga consumió veneno y ha muerto.")
        else:
            print("Ítem desconocido, no tiene efecto en la hormiga.")

    def is_alive(self):
        """Verifica si la hormiga está viva."""
        return self.health > 0
