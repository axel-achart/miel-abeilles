import matplotlib.pyplot as plt
import random
from beehive import *
import networkx as nx

def main():
    """
    Main program: simulates the genetic algorithm to optimize
    bees' foraging paths between the hive and flowers.
    """

    # -----------------------------
    # Problem Parameters
    # -----------------------------
    hive = (500, 500)  # fixed hive coordinates

    # Generate 20 random flowers around the hive
    random.seed()
    flowers = [(random.randint(50, 950), random.randint(50, 950)) for _ in range(8)]
    """flowers = [(100, 200), (200, 800), (400, 600), (500, 300), (600, 700), (700, 200), (800, 500), (150, 750)]"""

    POP_SIZE = 101        # 100 bees + 1 queen
    N_GENERATIONS = 200   # number of iterations
    MUTATION_RATE = 0.05  # probability of mutation

    # -----------------------------
    # Initialization
    # -----------------------------
    population = generate_population(POP_SIZE, flowers)
    history_best = []
    history_avg = []

    all_bees = []         # store all bees ever created
    all_bees.extend(population)  # add initial population

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

        # Add offspring to all_bees
        all_bees.extend(offspring)

        # New population = elites + offspring
        population = selected + offspring

    # -----------------------------
    # Final Results
    # -----------------------------
    best_bee = population[0]
    print("\n=== Final Results ===")
    print(f"Best distance found: {best_bee.distance:.2f}")

    # -----------------------------
    # Visualization: Genealogy Tree
    # -----------------------------
    G = nx.DiGraph()

    # Dictionary to access any bee by ID (includes all bees ever created)
    bee_dict = {bee.id: bee for bee in all_bees}

    # Recursive function to build genealogy from a bee
    def add_genealogy(bee):
        if bee.id not in G:
            G.add_node(bee.id, label=f"Bee {bee.id} (Gen {bee.generation})")
            for pid in bee.parents:
                G.add_edge(pid, bee.id)
                if pid in bee_dict:
                    add_genealogy(bee_dict[pid])

    add_genealogy(best_bee)

    # Draw genealogy tree
    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=500, node_color="lightblue", font_size=8)
    plt.title("Genealogy of the Best Bee")
    plt.show()

    # -----------------------------
    # Visualization: Best Path
    # -----------------------------
    x = [hive[0]] + [flowers[i][0] for i in best_bee.path] + [hive[0]]
    y = [hive[1]] + [flowers[i][1] for i in best_bee.path] + [hive[1]]

    plt.figure(figsize=(8, 6))
    plt.scatter(*hive, color="red", s=120, marker="s", label="Hive")
    plt.scatter([f[0] for f in flowers], [f[1] for f in flowers],
                color="gold", s=100, marker="o", edgecolors="black", label="Flowers")
    plt.plot(x, y, color="blue", linewidth=2, linestyle="-", label="Best Path")
    plt.scatter(x, y, color="blue", s=40)
    plt.title("Path of the Best Bee")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()

    # -----------------------------
    # Visualization: Fitness Evolution
    # -----------------------------
    plt.figure()
    plt.plot(history_best, label="Best Fitness", color="blue")
    plt.plot(history_avg, label="Average Fitness", color="orange")
    plt.title("Performance Evolution Across Generations")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()