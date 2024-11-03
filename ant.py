import numpy as np
import random
from items.sugar import Sugar
from items.wine import Wine
from items.poison import Poison
from items.rock import Rock
from items.goal import Goal
from ant_genome import AntGenome

class Ant:
    def __init__(self, start_position, maze, genome=None):
        self.position = start_position
        self.maze = maze
        self.health = 100
        self.points = 0
        self.alcohol_level = 0
        self.state_matrix = np.zeros((maze.size, maze.size))
        self.state_matrix[start_position] = 1
        self.last_move = None
        self.previous_moves = []
        self.visited_positions = set()
        self.stuck_counter = 0
        
        # Añadir el genoma
        self.genome = genome if genome else AntGenome()
        
        # Inicializar matrices de movimiento
        self.initialize_movement_matrices(maze.size)

    def initialize_movement_matrices(self, size):
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

        if self.stuck_counter > 5:
            return self.wall_following()

        best_directions = sorted(possible_moves.items(), key=lambda x: x[1], reverse=True)[:2]
        chosen_direction = random.choice(best_directions)[0]

        print(f"Movimientos posibles: {possible_moves}")
        print(f"Dirección elegida: {chosen_direction}")
        return chosen_direction

    def calculate_distance_factor(self, current, goal):
        distance = abs(current[0] - goal[0]) + abs(current[1] - goal[1])
        return 1 / (distance + 1)

    def find_goal(self):
        for i in range(self.maze.size):
            for j in range(self.maze.size):
                if self.maze.matrix[i][j] == 'G':
                    return (i, j)
        return None

    def get_item_weight(self, item):
        weights = {
            ' ': 1,
            'S': self._apply_sugar_preference(2),
            'W': self._apply_wine_resistance(1.5),
            'P': self._apply_risk_tolerance(0.1),
            'G': 3,
            'R': 0
        }
        
        base_weight = weights.get(item, 0)
        
        if self.last_move in ['UP', 'DOWN']:
            if item in ['S', 'W', 'G']:
                base_weight *= 1.2
        
        if len(self.previous_moves) >= 2:
            if self.previous_moves[-1] == self.previous_moves[-2]:
                base_weight *= 0.7
        
        exploration_modifier = self.genome.genes['exploration_rate'][1]
        if item not in self.visited_positions:
            base_weight *= exploration_modifier
        
        return base_weight

    def _apply_sugar_preference(self, base_weight):
        sugar_preference = self.genome.genes['sugar_preference'][1]
        return base_weight * sugar_preference

    def _apply_wine_resistance(self, base_weight):
        wine_resistance = self.genome.genes['wine_resistance'][1]
        if self.alcohol_level < 30:
            return base_weight * wine_resistance
        return base_weight * (1 - wine_resistance)

    def _apply_risk_tolerance(self, base_weight):
        risk_tolerance = self.genome.genes['risk_tolerance'][1]
        return base_weight * (2 - risk_tolerance)

    def validate_move(self, direction, weighted_position):
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

        movement_speed = self.genome.genes['movement_speed'][1]
        if random.random() > movement_speed:
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
            self.previous_moves.append(direction)
            if len(self.previous_moves) > 5:
                self.previous_moves.pop(0)
            self.stuck_counter = 0
            return True

        self.stuck_counter += 1
        return False
    
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

        # Ajustar el valor según el tipo de ítem y los rasgos genéticos
        if item == 'S':
            base_value += 3 * self.genome.genes['sugar_preference'][1]
        elif item == 'W':
            wine_value = 2 if self.alcohol_level < 30 else 0.5
            base_value += wine_value * self.genome.genes['wine_resistance'][1]
        elif item == 'P':
            base_value -= 10 * (2 - self.genome.genes['risk_tolerance'][1])
        elif item == 'G':
            base_value += 10

        # Penalizar posiciones ya visitadas
        if position in self.visited_positions:
            base_value *= (1 - self.genome.genes['exploration_rate'][1])

        # Añadir un elemento de aleatoriedad
        base_value += random.uniform(0, 1)

        return base_value

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
            "is_alive": self.is_alive(),
            "genome": self.genome.genes
        }

    def interact_with_item(self, item):
        if not self.is_alive():
            print("La hormiga está muerta y no puede interactuar con ítems.")
            return

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

        if isinstance(item, Sugar):
            sugar_effect = 10 * self.genome.genes['sugar_preference'][1]
            self.health += sugar_effect
            self.points += sugar_effect
            print(f"Hormiga consumió azúcar. Salud: {self.health}, Puntos: {self.points}")
            
        elif isinstance(item, Wine):
            wine_resistance = self.genome.genes['wine_resistance'][1]
            alcohol_increase = 5 * (1 - wine_resistance)
            health_decrease = 10 * (1 - wine_resistance)
            
            self.alcohol_level += alcohol_increase
            self.health -= health_decrease
            print(f"Hormiga consumió vino. Salud: {self.health}, Nivel de alcohol: {self.alcohol_level}")
            
            if self.alcohol_level > 50:
                self.health -= health_decrease
                print("¡La hormiga está muy borracha y pierde salud extra!")
            
        elif isinstance(item, Poison):
            risk_tolerance = self.genome.genes['risk_tolerance'][1]
            if random.random() > risk_tolerance:
                self.health = 0
                print("¡La hormiga ha consumido veneno y ha muerto!")
            else:
                self.health -= 50
                print("¡La hormiga ha resistido parte del veneno!")
            
        elif isinstance(item, Rock):
            print("La hormiga no puede consumir rocas.")

        elif isinstance(item, Goal):
            item.interact(self)
            print(f"¡La hormiga ha alcanzado la meta! Puntos totales: {self.points}")

        self.update_health(0)