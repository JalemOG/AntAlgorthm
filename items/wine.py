class Wine:
    def __init__(self, alcohol_increase=5, health_penalty=10):
        self.alcohol_increase = alcohol_increase
        self.health_penalty = health_penalty

    def consume(self, ant):
        """Aplica el efecto del vino en la hormiga."""
        ant.alcohol_level += self.alcohol_increase
        print(f"Hormiga consumió vino. Nivel de alcohol actual: {ant.alcohol_level}")
        if ant.alcohol_level > 50:
            ant.health -= self.health_penalty
            print(f"La hormiga está borracha y pierde {self.health_penalty} de salud. Salud actual: {ant.health}")
