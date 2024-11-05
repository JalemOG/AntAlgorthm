class Sugar:
    def __init__(self, points=10):
        self.points = points  # Puntos que la hormiga gana al consumir azúcar

    def consume(self, ant):
        """Aplica el efecto del azúcar en la hormiga."""
        ant.points += self.points
        print(f"Hormiga consumió azúcar y ganó {self.points} puntos. Puntos actuales: {ant.points}")
