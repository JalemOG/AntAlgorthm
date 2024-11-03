import random

class AntGenome:
    def __init__(self):
        """
        Inicializa el genoma de la hormiga con genes que afectan su comportamiento
        Cada gen es una tupla (nombre, valor) donde valor está entre 0 y 1
        """
        self.genes = {
            'sugar_preference': ('Preferencia por azúcar', random.uniform(0, 1)),
            'wine_resistance': ('Resistencia al alcohol', random.uniform(0, 1)),
            'risk_tolerance': ('Tolerancia al riesgo', random.uniform(0, 1)),
            'exploration_rate': ('Tasa de exploración', random.uniform(0, 1)),
            'movement_speed': ('Velocidad de movimiento', random.uniform(0, 1))
        }

    def mutate(self, mutation_rate):
        """
        Aplica mutaciones aleatorias a los genes con una probabilidad dada
        """
        for gene in self.genes:
            if random.random() < mutation_rate:
                self.genes[gene] = (self.genes[gene][0], random.uniform(0, 1))

    def crossover(self, other_genome):
        """
        Realiza un cruce entre dos genomas para crear uno nuevo
        """
        new_genome = AntGenome()
        for gene in self.genes:
            if random.random() < 0.5:
                new_genome.genes[gene] = self.genes[gene]
            else:
                new_genome.genes[gene] = other_genome.genes[gene]
        return new_genome

    def get_gene_value(self, gene_name):
        """
        Retorna el valor numérico de un gen específico
        """
        return self.genes[gene_name][1]

    def __str__(self):
        """
        Representación en string del genoma
        """
        return "\n".join([f"{name}: {value[1]:.2f}" for name, value in self.genes.items()])