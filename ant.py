class Ant:
    def __init__(self, start_position=(0, 0)):
        # Posición inicial de la hormiga en el laberinto
        self.position = start_position
        self.health = 100            # Salud inicial
        self.alcohol_level = 0       # Nivel inicial de alcohol
        self.points = 0              # Puntos iniciales

    def move(self, direction):
        """Mueve la hormiga en la dirección especificada."""
        x, y = self.position
        if direction == "UP":
            self.position = (x - 1, y)
        elif direction == "DOWN":
            self.position = (x + 1, y)
        elif direction == "LEFT":
            self.position = (x, y - 1)
        elif direction == "RIGHT":
            self.position = (x, y + 1)
        else:
            raise ValueError("Dirección no válida.")
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

    def adjust_health(self, amount):
        """Ajusta el nivel de salud de la hormiga."""
        self.health += amount
        self.health = max(0, min(self.health, 100))  # Limita la salud entre 0 y 100
        print(f"Salud ajustada: {self.health}")

    def adjust_alcohol_level(self, amount):
        """Ajusta el nivel de alcohol de la hormiga."""
        self.alcohol_level += amount
        self.alcohol_level = max(0, min(self.alcohol_level, 50))  # Limita el nivel de alcohol entre 0 y 50
        print(f"Nivel de alcohol ajustado: {self.alcohol_level}")

    def is_alive(self):
        """Verifica si la hormiga está viva."""
        return self.health > 0


if __name__ == "__main__":
    ant = Ant((0, 0))
    print("Posición inicial:", ant.position)

    # Mover la hormiga en varias direcciones
    ant.move("DOWN")
    ant.move("RIGHT")

    # Consumir diferentes ítems
    ant.eat_item("SUGAR")
    ant.eat_item("WINE")
    ant.eat_item("POISON")

    # Ajustar salud y nivel de alcohol
    ant.adjust_health(-20)
    ant.adjust_alcohol_level(10)

    # Comprobar si la hormiga sigue viva
    if ant.is_alive():
        print("La hormiga sigue viva.")
    else:
        print("La hormiga ha muerto.")
