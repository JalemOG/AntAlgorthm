import random
from ant import Ant
from maze import Maze
from ant_genome import AntGenome

class GeneticAlgorithm:
    def __init__(self, population_size, maze_size, generations, mutation_rate):
        self.population_size = population_size
        self.maze = Maze(maze_size)
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = []

    def initialize_population(self):
        start_position = self.maze.get_start_position()
        for _ in range(self.population_size):
            genome = AntGenome()
            ant = Ant(start_position, self.maze, genome)
            self.population.append(ant)

    def fitness(self, ant):
        return ant.points + ant.health + (100 - ant.alcohol_level)

    def select_parents(self):
        # Torneo binario
        parents = []
        for _ in range(2):
            contestant1 = random.choice(self.population)
            contestant2 = random.choice(self.population)
            if self.fitness(contestant1) > self.fitness(contestant2):
                parents.append(contestant1)
            else:
                parents.append(contestant2)
        return parents

    def crossover(self, parent1, parent2):
        child_genome = AntGenome()
        for gene in child_genome.genes:
            if random.random() < 0.5:
                child_genome.genes[gene] = parent1.genome.genes[gene]
            else:
                child_genome.genes[gene] = parent2.genome.genes[gene]
        return child_genome

    def mutate(self, genome):
        for gene in genome.genes:
            if random.random() < self.mutation_rate:
                genome.genes[gene] = (genome.genes[gene][0], random.uniform(0, 1))

    def create_next_generation(self):
        new_population = []
        for _ in range(self.population_size):
            parent1, parent2 = self.select_parents()
            child_genome = self.crossover(parent1, parent2)
            self.mutate(child_genome)
            child = Ant(self.maze.get_start_position(), self.maze, child_genome)
            new_population.append(child)
        self.population = new_population

    def run_simulation(self, steps):
        for ant in self.population:
            for _ in range(steps):
                if ant.is_alive():
                    ant.move()
                    current_item = self.maze.get_item(ant.position)
                    if current_item:
                        ant.interact_with_item(current_item)

    def run(self):
        self.initialize_population()
        for generation in range(self.generations):
            print(f"Generation {generation + 1}")
            self.run_simulation(100)  # Cada hormiga hace 100 movimientos
            
            # Encontrar la mejor hormiga de esta generación
            best_ant = max(self.population, key=self.fitness)
            print(f"Best fitness: {self.fitness(best_ant)}")
            
            self.create_next_generation()

        # Encontrar la mejor hormiga de todas las generaciones
        best_ant = max(self.population, key=self.fitness)
        print("\nBest ant:")
        print(f"Fitness: {self.fitness(best_ant)}")
        print(f"Genome: {best_ant.genome.genes}")
        print(f"Final position: {best_ant.position}")
        print(f"Health: {best_ant.health}")
        print(f"Points: {best_ant.points}")
        print(f"Alcohol level: {best_ant.alcohol_level}")

# Uso del algoritmo
if __name__ == "__main__":
    ga = GeneticAlgorithm(population_size=50, maze_size=10, generations=100, mutation_rate=0.1)
    ga.run()