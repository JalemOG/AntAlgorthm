# ant.py
class Ant:
    """Clase que representa a la hormiga y su comportamiento"""
    
    def __init__(self, start_position=(0, 0), maze=None):
        """
        Inicializa una nueva hormiga
        
        Args:
            start_position (tuple): Posición inicial (x, y)
            maze (Maze): Referencia al laberinto
        """
        self.position = start_position
        self.maze = maze
        self.health = 100
        self.alcohol_level = 0
        self.points = 0
        self.moves = 0
        
        # Efectos de los items
        self.item_effects = {
            'SUGAR': {'points': 10},
            'WINE': {'alcohol': 5},
            'POISON': {'health': -100}
        }
    
    def can_move_to(self, new_position):
        """
        Verifica si la hormiga puede moverse a una nueva posición
        
        Args:
            new_position (tuple): Coordenadas (x, y) de destino
            
        Returns:
            bool: True si el movimiento es válido
        """
        if not self.maze:
            return False
            
        return (self.maze.is_valid_position(new_position) and 
                self.maze.is_walkable(new_position))
    
    def calculate_new_position(self, direction):
        """
        Calcula la nueva posición según la dirección
        
        Args:
            direction (str): Dirección del movimiento ('UP', 'DOWN', 'LEFT', 'RIGHT')
            
        Returns:
            tuple: Nueva posición (x, y) o None si el movimiento no es válido
        """
        x, y = self.position
        movements = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }
        
        if direction not in movements:
            return None
            
        dx, dy = movements[direction]
        return (x + dx, y + dy)
    
    def move(self, direction):
        """
        Mueve la hormiga en la dirección especificada si es posible
        
        Args:
            direction (str): Dirección del movimiento
            
        Returns:
            bool: True si el movimiento fue exitoso
        """
        new_position = self.calculate_new_position(direction)
        
        if new_position and self.can_move_to(new_position):
            self.position = new_position
            self.moves += 1
            
            # Reducir nivel de alcohol gradualmente con el movimiento
            if self.alcohol_level > 0:
                self.adjust_alcohol_level(-1)
                
            return True
        return False
    
    def eat_item(self, item_type):
        """
        Procesa los efectos de consumir un ítem
        
        Args:
            item_type (str): Tipo de ítem consumido
        """
        effects = self.item_effects.get(item_type, {})
        
        if 'points' in effects:
            self.points += effects['points']
        
        if 'alcohol' in effects:
            self.adjust_alcohol_level(effects['alcohol'])
            
        if 'health' in effects:
            self.adjust_health(effects['health'])
    
    def adjust_health(self, amount):
        """Ajusta el nivel de salud de la hormiga"""
        self.health = max(0, min(100, self.health + amount))
        
        # El alcohol excesivo daña la salud
        if self.alcohol_level > 50:
            self.health = max(0, self.health - 5)
    
    def adjust_alcohol_level(self, amount):
        """Ajusta el nivel de alcohol de la hormiga"""
        self.alcohol_level = max(0, min(100, self.alcohol_level + amount))
    
    def get_status(self):
        """
        Obtiene el estado actual de la hormiga
        
        Returns:
            dict: Estado actual de la hormiga
        """
        return {
            'position': self.position,
            'health': self.health,
            'alcohol_level': self.alcohol_level,
            'points': self.points,
            'moves': self.moves,
            'is_alive': self.is_alive()
        }
    
    def is_alive(self):
        """
        Verifica si la hormiga está viva
        
        Returns:
            bool: True si la hormiga está viva
        """
        return self.health > 0