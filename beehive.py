import math
import random

class Bee:
    def __init__(self, path):
        """
        Initialize a bee with a given path (permutation of flower indices).
        """
        self.path = path
        self.distance = None
        self.fitness = None

    def evaluate(self, flowers, hive):
        """
        Evaluate the bee by calculating the distance of its path
        and its fitness (inverse of distance).
        """
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
    """
    Perform Order Crossover (OX) between two parents.
    """
    n = len(parent1.path)
    start, end = sorted(random.sample(range(n), 2))

    child = [None] * n
    child[start:end] = parent1.path[start:end]

    pos = end
    for gene in parent2.path:
        if gene not in child:
            if pos >= n:
                pos = 0
            child[pos] = gene
            pos += 1
    return Bee(child)


def mutation(bee, rate=0.05):
    """
    Mutate a bee by swapping two genes with a given probability.
    """
    path = bee.path[:]
    if random.random() < rate:
        i, j = random.sample(range(len(path)), 2)
        path[i], path[j] = path[j], path[i]
    return Bee(path)
