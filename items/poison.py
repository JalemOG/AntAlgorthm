class Poison:
    def consume(self, ant):
        """Aplica el efecto del veneno en la hormiga."""
        ant.health = 0
        print("Hormiga consumió veneno y ha muerto.")
