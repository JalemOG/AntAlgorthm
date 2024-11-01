class Ant:
    def __init__(self, start_position, maze):
        self.position = start_position
        self.maze = maze
        self.health = 100
        self.sugar_collected = 0
        self.wine_collected = 0

    def is_alive(self):
        return self.health > 0

    def move(self, direction):
        if not self.is_alive():
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
            return True
        return False

    def eat_item(self, item):
        if item == "S":
            self.sugar_collected += 1
            self.health += 10
        elif item == "W":
            self.wine_collected += 1
            self.health += 5
        elif item == "P":
            self.health -= 50