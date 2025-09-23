import random
import numpy as np

class Bee():
    def __init__(self,path,flower_positions,hive_position,parents=None):
        self.path = path
        self.hive_position = hive_position
        self.parents = parents
        self.total_distance = self.compute_total_distance()
        self.flower_positions = flower_positions
    
    def compute_total_distance(self):
        distance = 0
        current = self.hive_position
        for flower_index in self.path:
            next_flower = self.flower_positions[flower_index]
            distance += euclidean_distance(current,next_flower)
            current = next_flower
        distance += euclidean_distance(current, self.hive_position)
        return distance

def euclidean_distance(a,b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2) ** 0.5

def generate_random_path(num_flowers):
    path = list(range(len(num_flowers)))
    random.shuffle(path)
    return path


def  generate_population(num_bees,flower_positions,hive_position):
    population = []
    for _ in range(num_bees):
        path = generate_random_path(flower_positions)
        bee = Bee(path,flower_positions,hive_position)
        population.append(bee)
    return population