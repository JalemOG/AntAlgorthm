class Goal:
    """
    Clase que representa la meta final en el laberinto.
    Es un ítem especial que al ser alcanzado por la hormiga marca el final exitoso de la simulación.
    """
    def __init__(self):
        self.symbol = "G"  # Símbolo para representar la meta en la matriz
        self.reached = False
        self.points_reward = 50  # Puntos otorgados por alcanzar la meta

    def interact(self, ant):
        """
        Maneja la interacción cuando la hormiga alcanza la meta
        
        Args:
            ant: Objeto de la clase Ant que interactúa con la meta
        """
        if not self.reached:
            self.reached = True
            ant.points += self.points_reward
            # Podrías agregar más recompensas o efectos aquí
            return True
        return False

    @property
    def is_reached(self):
        """
        Indica si la meta ha sido alcanzada
        
        Returns:
            bool: True si la meta fue alcanzada, False en caso contrario
        """
        return self.reached

    def reset(self):
        """
        Reinicia el estado de la meta para una nueva simulación
        """
        self.reached = False