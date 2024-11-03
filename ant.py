import numpy as np
from items.sugar import Sugar
from items.wine import Wine
from items.poison import Poison
from items.rock import Rock
from items.goal import Goal
import random

class Ant:
    def __init__(self, start_position, maze):
        self.position = start_position
        self.maze = maze
        self.health = 100
        self.points = 0
        self.alcohol_level = 0
        self.state_matrix = np.zeros((maze.size, maze.size))
        self.state_matrix[start_position] = 1
        self.last_move = None  # Añadir esta línea
        self.previous_moves = []  # Añadir esta línea
        self.visited_positions = set()  # Nuevo: conjunto para rastrear posiciones visitadas
        self.stuck_counter = 0
        
        # Crear matrices de transformación dinámicas según el tamaño del laberinto
        self.initialize_movement_matrices(maze.size)

    def initialize_movement_matrices(self, size):
        """
        Inicializa las matrices de transformación según el tamaño del laberinto
        """
        # Crear matrices base para cada dirección
        self.movement_matrices = {}
        
        # Matriz para movimiento hacia arriba
        up_matrix = np.zeros((size, size))
        for i in range(size-1):
            up_matrix[i][i+1] = 1
            
        # Matriz para movimiento hacia abajo
        down_matrix = np.zeros((size, size))
        for i in range(size-1):
            down_matrix[i+1][i] = 1
            
        # Matriz para movimiento hacia la izquierda
        left_matrix = np.zeros((size, size))
        for i in range(size-1):
            left_matrix[i][i+1] = 1
            
        # Matriz para movimiento hacia la derecha
        right_matrix = np.zeros((size, size))
        for i in range(size-1):
            right_matrix[i+1][i] = 1

        self.movement_matrices = {

        'UP': np.eye(size, k=-1),

        'DOWN': np.eye(size, k=1),

        'LEFT': np.eye(size, k=-1),

        'RIGHT': np.eye(size, k=1)

        }
    def is_alive(self):
        return self.health > 0
    
    def calculate_next_position(self):
        possible_moves = self.get_possible_moves()
        if not possible_moves:
            print("No hay movimientos posibles")
            return None

        # Si la hormiga está atascada, usar "wall following"
        if self.stuck_counter > 5:
            return self.wall_following()

        # Elegir la mejor dirección con un poco de aleatoriedad
        best_directions = sorted(possible_moves.items(), key=lambda x: x[1], reverse=True)[:2]
        chosen_direction = random.choice(best_directions)[0]

        print(f"Movimientos posibles: {possible_moves}")
        print(f"Dirección elegida: {chosen_direction}")
        return chosen_direction

    def calculate_distance_factor(self, current, goal):
        """Calcula un factor basado en la distancia Manhattan al objetivo"""
        distance = abs(current[0] - goal[0]) + abs(current[1] - goal[1])
        return 1 / (distance + 1)  # Evitar división por cero

    def find_goal(self):
        """Encuentra la posición de la meta en el laberinto"""
        for i in range(self.maze.size):
            for j in range(self.maze.size):
                if self.maze.matrix[i][j] == 'G':
                    return (i, j)
        return None
    
    def get_item_weight(self, item):
        weights = {
            ' ': 1,
            'S': 2,
            'W': 1.5 if self.alcohol_level < 30 else 0.5,
            'P': 0.1,
            'G': 3,
            'R': 0
        }
        
        base_weight = weights.get(item, 0)
        
        # Añadir preferencia por movimientos horizontales si el último movimiento fue vertical
        if self.last_move in ['UP', 'DOWN']:
            if item in ['S', 'W', 'G']:  # Si hay objetivos en movimientos laterales
                base_weight *= 1.2  # Aumentar el peso de movimientos horizontales
        
        # Penalizar movimientos repetitivos
        if len(self.previous_moves) >= 2:
            if self.previous_moves[-1] == self.previous_moves[-2]:  # Si los últimos dos movimientos son iguales
                base_weight *= 0.7  # Reducir el peso para evitar repeticiones
        
        return base_weight

    def validate_move(self, direction, weighted_position):
        """
        Valida si un movimiento es posible y calcula su valor
        """
        x, y = self.position
        size = self.maze.size
        
        if direction == "UP" and x > 0:
            return weighted_position[x-1][y] if self.maze.is_walkable((x-1, y)) else 0
        elif direction == "DOWN" and x < size - 1:
            return weighted_position[x+1][y] if self.maze.is_walkable((x+1, y)) else 0
        elif direction == "LEFT" and y > 0:
            return weighted_position[x][y-1] if self.maze.is_walkable((x, y-1)) else 0
        elif direction == "RIGHT" and y < size - 1:
            return weighted_position[x][y+1] if self.maze.is_walkable((x, y+1)) else 0
        return 0
    
    def wall_following(self):
        # Implementar una estrategia simple de "wall following"
        directions = ["UP", "RIGHT", "DOWN", "LEFT"]
        current_index = directions.index(self.last_move) if self.last_move else 0
        for _ in range(4):
            next_index = (current_index + 1) % 4
            next_direction = directions[next_index]
            if next_direction in self.get_possible_moves():
                return next_direction
            current_index = next_index
        return None

    def move(self):
        if not self.is_alive():
            return False

        direction = self.calculate_next_position()
        if direction is None:
            self.stuck_counter += 1
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
            self.visited_positions.add(new_position)
            self.last_move = direction
            self.stuck_counter = 0  # Reiniciar el contador de atasco
            return True

        self.stuck_counter += 1
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
    
    def get_possible_moves(self):
        possible_moves = {}
        x, y = self.position
        size = self.maze.size

        directions = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)
        }
        for direction, (dx, dy) in directions.items():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < size and 0 <= new_y < size:
                new_position = (new_x, new_y)
                if self.maze.is_walkable(new_position):
                    move_value = self.calculate_move_value(new_position)
                    possible_moves[direction] = move_value
        return possible_moves

    def calculate_move_value(self, position):
        x, y = position
        item = self.maze.matrix[x][y]
        base_value = 1

        # Ajustar el valor según el tipo de ítem
        if item == 'S':
            base_value += 3
        elif item == 'W':
            base_value += 2 if self.alcohol_level < 30 else 0.5
        elif item == 'P':
            base_value -= 10
        elif item == 'G':
            base_value += 10

        # Penalizar posiciones ya visitadas
        if position in self.visited_positions:
            base_value -= 2

        # Añadir un elemento de aleatoriedad
        base_value += random.uniform(0, 1)

        return base_value