import matplotlib.pyplot as plt
import random
from beehive import *

def main():
    """
    Main program: simulates the genetic algorithm to optimize
    bees' foraging paths between the hive and flowers.
    """

    # -----------------------------
    # Problem Parameters
    # -----------------------------
    hive = (500, 500)  # fixed hive coordinates

    # Example set of flowers (⚠️ replace with real coordinates provided in dataset)
    flowers = [
        (100, 200), (300, 400), (700, 800),
        (200, 700), (600, 300), (800, 500)
    ]

    POP_SIZE = 101        # 100 bees + 1 queen
    N_GENERATIONS = 200   # number of iterations
    MUTATION_RATE = 0.05  # probability of mutation

    # -----------------------------
    # Initialization
    # -----------------------------
    population = generate_population(POP_SIZE, flowers)
    history_best = []     # stores best fitness per generation
    history_avg = []      # stores average fitness per generation

    # -----------------------------
    # Evolutionary Loop
    # -----------------------------
    for gen in range(N_GENERATIONS):

        # Evaluate population
        for bee in population:
            bee.evaluate(flowers, hive)

        # Sort by fitness (best first)
        population.sort(key=lambda b: b.fitness, reverse=True)

        # Save statistics
        best = population[0]
        avg = sum(b.fitness for b in population) / len(population)
        history_best.append(best.fitness)
        history_avg.append(avg)

        print(f"Generation {gen} | Best distance: {best.distance:.2f}")

        # Selection (elitism)
        selected = selection(population, proportion=0.5)

        # Reproduction + mutation
        offspring = []
        while len(selected) + len(offspring) < POP_SIZE:
            parent1, parent2 = random.sample(selected, 2)
            child = crossover(parent1, parent2)
            child = mutation(child, MUTATION_RATE)
            child.evaluate(flowers, hive)
            offspring.append(child)

        # New population = elites + offspring
        population = selected + offspring

    # -----------------------------
    # Final Results
    # -----------------------------
    best_bee = population[0]
    print("\n=== Final Results ===")
    print(f"Best distance found: {best_bee.distance:.2f}")

    # -----------------------------
    # Visualization: Best Path
    # -----------------------------
    x = [hive[0]] + [flowers[i][0] for i in best_bee.path] + [hive[0]]
    y = [hive[1]] + [flowers[i][1] for i in best_bee.path] + [hive[1]]

    plt.figure(figsize=(9, 7))

    # First plot hive and flowers
    plt.scatter(*hive, color="red", s=120, marker="s", label="Hive")
    plt.scatter([f[0] for f in flowers], [f[1] for f in flowers],
                color="gold", s=100, marker="o", edgecolors="black", label="Flowers")

    # Then plot the path of the best bee
    plt.plot(x, y, color="blue", linewidth=2, linestyle="-", label="Best Path")
    plt.scatter(x, y, color="blue", s=40)  # path nodes in blue

    plt.title("Path of the Best Bee")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()

    # -----------------------------
    # Visualization: Fitness Evolution
    # -----------------------------
    plt.figure()
    plt.plot(history_best, label="Best Fitness")
    plt.plot(history_avg, label="Average Fitness")
    plt.title("Performance Evolution Across Generations")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()