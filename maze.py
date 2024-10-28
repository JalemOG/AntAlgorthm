# maze.py

class Maze:
    """Clase que representa el laberinto y gestiona su estado"""
    
    def __init__(self, size):
        """
        Inicializa el laberinto con un tamaño específico
        
        Args:
            size (int): Tamaño del laberinto (entre 3 y 10)
        """
        if not (3 <= size <= 10):
            raise ValueError("El tamaño del laberinto debe estar entre 3 y 10.")
        
        self.size = size
        self.matrix = [[" " for _ in range(size)] for _ in range(size)]
        self.items = {
            'SUGAR': [],  # Aumenta puntos
            'WINE': [],   # Aumenta nivel de alcohol
            'POISON': [], # Mata a la hormiga
            'ROCK': []    # Obstáculo
        }
        
        # Diccionario para mapear tipos de items a sus símbolos
        self.item_symbols = {
            'SUGAR': 'S',
            'WINE': 'W',
            'POISON': 'P',
            'ROCK': 'R'
        }

    def is_valid_position(self, position):
        """Verifica si una posición está dentro del laberinto"""
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size
    
    def is_position_empty(self, position):
        """Verifica si una posición está vacía"""
        x, y = position
        return self.matrix[x][y] == " "
    
    def add_item(self, item_type, position):
        """
        Agrega un ítem en la posición especificada
        
        Args:
            item_type (str): Tipo de ítem ('SUGAR', 'WINE', 'POISON', 'ROCK')
            position (tuple): Coordenadas (x, y) donde colocar el ítem
        """
        if item_type not in self.items:
            raise ValueError(f"Tipo de ítem '{item_type}' no válido.")
        
        x, y = position
        if not self.is_valid_position(position):
            raise ValueError("Posición fuera del rango del laberinto.")
            
        if not self.is_position_empty(position):
            raise ValueError("La posición ya está ocupada.")
            
        # Añadir el ítem en la matriz y registrar la posición
        self.matrix[x][y] = self.item_symbols[item_type]
        self.items[item_type].append(position)

    def remove_item(self, position):
        """
        Elimina un ítem de una posición
        
        Args:
            position (tuple): Coordenadas (x, y) del ítem a eliminar
        """
        x, y = position
        item_symbol = self.matrix[x][y]
        
        # Encontrar el tipo de ítem basado en el símbolo
        item_type = next((k for k, v in self.item_symbols.items() 
                         if v == item_symbol), None)
        
        if item_type:
            self.matrix[x][y] = " "
            if position in self.items[item_type]:
                self.items[item_type].remove(position)
    
    def get_item_at(self, position):
        """
        Obtiene el tipo de ítem en una posición específica
        
        Args:
            position (tuple): Coordenadas (x, y) a verificar
            
        Returns:
            str: Tipo de ítem o None si no hay ítem
        """
        x, y = position
        item_symbol = self.matrix[x][y]
        return next((k for k, v in self.item_symbols.items() 
                    if v == item_symbol), None)
    
    def is_walkable(self, position):
        """
        Verifica si una posición es transitable (no tiene una roca)
        
        Args:
            position (tuple): Coordenadas (x, y) a verificar
            
        Returns:
            bool: True si la posición es transitable
        """
        if not self.is_valid_position(position):
            return False
            
        x, y = position
        return self.matrix[x][y] != self.item_symbols['ROCK']

    def is_path(self, row, col):
        """Revisa si una posición en el laberinto es transitable o tiene un ítem."""
        return self.matrix[row][col] == " "
