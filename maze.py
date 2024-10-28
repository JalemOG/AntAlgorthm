# maze.py

class Maze:
    """Clase que representa el laberinto y gestiona su estado"""
    
    def __init__(self, size):
        # Aseguramos que el tamaño esté dentro del rango permitido de 3x3 a 10x10

        if not (3 <= size <= 10):
            raise ValueError("El tamaño del laberinto debe estar entre 3 y 10.")
        self.size = size
        self.matrix = [[" " for _ in range(size)] for _ in range(size)]
        self.items = {'SUGAR': [], 'WINE': [], 'POISON': [], 'ROCK': []}

    def create_maze(self):
        # Permite al usuario crear el laberinto y colocar ítems.
        # Llena el laberinto con espacios vacíos inicialmente

        self.matrix = [[" " for _ in range(self.size)] for _ in range(self.size)]
        print("Laberinto creado con tamaño:", self.size)

    def add_item(self, item_type, position):
        # Agrega un ítem en la posición especificada

        x, y = position
        if item_type not in self.items:
            raise ValueError(f"Tipo de ítem '{item_type}' no válido.")

        if not (0 <= x < self.size and 0 <= y < self.size):
            raise ValueError("Posición fuera del rango del laberinto.")

        # Añadir el ítem en la matriz y registrar la posición

        self.matrix[x][y] = item_type[0]  # Usa la primera letra del ítem como símbolo
        self.items[item_type].append((x, y))
        print(f"{item_type} agregado en la posición ({x}, {y})")

    def update_state(self, ant_position):
        # Actualiza el contenido de la matriz según la posición de la hormiga

        x, y = ant_position
        if self.matrix[x][y] == " ":
            return "No hay ítem"

        item_type = next((k for k, v in self.items.items() if (x, y) in v), None)
        if item_type:
            self.items[item_type].remove((x, y))  # Elimina el ítem si la hormiga lo consume
            print(f"La hormiga consumió {item_type} en la posición ({x}, {y})")
            return item_type
        return None

    def display_maze(self):
        # Imprime la matriz del laberinto en consola

        for row in self.matrix:
            print(" ".join(row))
        print()


if __name__ == "__main__":
    # Crear un laberinto de tamaño 5x5

    laberinto = Maze(size=5)
    laberinto.create_maze()

    # Agregar ítems en el laberinto
    laberinto.add_item("SUGAR", (1, 2))
    laberinto.add_item("WINE", (2, 3))
    laberinto.add_item("POISON", (4, 4))

    # Mostrar el laberinto en consola
    laberinto.display_maze()

    # Actualizar estado al simular la posición de la hormiga
    laberinto.update_state((1, 2))  # La hormiga consume azúcar
    laberinto.update_state((4, 4))  # La hormiga consume veneno

    # Mostrar el laberinto después de que la hormiga ha consumido algunos ítems
    laberinto.display_maze()
