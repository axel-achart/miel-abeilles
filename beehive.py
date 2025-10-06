import math
import random

BEE_COUNTER = 0

class Bee:
    def __init__(self, path, parents=None, generation=0):
        """
        Bee object representing a solution (path through flowers).
        """
        global BEE_COUNTER
        self.path = path
        self.distance = None
        self.fitness = None
        self.parents = parents if parents else []  # genealogy tracking
        self.id = BEE_COUNTER  # unique sequential ID
        BEE_COUNTER += 1
        self.generation = generation  # nouvelle info pour l'affichage


    def evaluate(self, flowers, hive):
        """Compute distance and fitness of a bee"""
        self.distance = calculate_distance(self.path, flowers, hive)
        self.fitness = 1 / self.distance
        return self.fitness



def calculate_distance(path, flowers, hive):
    """
    Compute the total distance of a path starting and ending at the hive.
    """
    distance = 0
    current = hive
    for idx in path:
        next_flower = flowers[idx]
        distance += math.dist(current, next_flower)
        current = next_flower
    distance += math.dist(current, hive)
    return distance


def create_bee(flowers):
    """
    Create a bee with a random path (permutation of flower indices).
    """
    indices = list(range(len(flowers)))
    random.shuffle(indices)
    return Bee(indices)


def generate_population(size, flowers):
    """
    Generate the initial population of bees.
    """
    return [create_bee(flowers) for _ in range(size)]


def selection(population, proportion=0.5):
    """
    Select the best bees according to fitness (elitist selection).
    """
    size = int(len(population) * proportion)
    return population[:size]


def crossover(parent1, parent2):
    n = len(parent1.path)
    start, end = sorted(random.sample(range(n), 2))

    child_path = [None] * n
    child_path[start:end] = parent1.path[start:end]

    pos = end
    for gene in parent2.path:
        if gene not in child_path:
            if pos >= n:
                pos = 0
            child_path[pos] = gene
            pos += 1

    child_gen = max(parent1.generation, parent2.generation) + 1
    return Bee(child_path, parents=[parent1.id, parent2.id], generation=child_gen)


def mutation(bee, rate=0.05):
    path = bee.path[:]
    if random.random() < rate:
        i, j = random.sample(range(len(path)), 2)
        path[i], path[j] = path[j], path[i]
    child_gen = bee.generation + 1
    return Bee(path, parents=[bee.id], generation=child_gen)
