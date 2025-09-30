import matplotlib.pyplot as plt
import random
import networkx as nx
import csv
import datetime
from beehive import *

def main():
    """
    Main program: simulates a genetic algorithm to optimize
    bees' foraging paths between the hive and flowers.
    """

    # -----------------------------
    # Problem Parameters
    # -----------------------------
    hive = (500, 500)  # fixed hive coordinates (center of the map)

    # Fixed example: 20 random flower positions
    flowers = [(796, 310), (774, 130), (116, 69), (908, 534), (708, 99), (444, 428),
            (220, 307), (501, 287), (345, 560), (628, 311), (901, 639), (436, 619),
            (938, 646), (45, 549), (837, 787), (328, 489), (278, 434), (704, 995),
            (101, 482), (921, 964), (493, 970), (494, 898), (929, 389), (730, 742),
            (528, 794), (371, 429), (98, 711), (724, 631), (573, 903), (964, 726),
            (213, 639), (549, 329), (684, 273), (273, 105), (897, 324), (508, 31),
            (758, 405), (862, 361), (898, 898), (2, 897), (951, 209), (189, 739),
            (602, 68), (437, 601), (330, 410), (3, 517), (643, 404), (875, 407),
            (761, 772), (276, 666)]

    POP_SIZE = 101        # 100 bees + 1 queen
    N_GENERATIONS = 200   # number of iterations
    MUTATION_RATE = 0.05  # probability of mutation

    # -----------------------------
    # Initialization
    # -----------------------------
    population = generate_population(POP_SIZE, flowers)
    history_best = []  # best fitness per generation
    history_avg = []   # average fitness per generation
    all_bees = list(population)  # track every bee created

    # -----------------------------
    # Create a CSV file for this run
    # -----------------------------
    timestamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
    csv_filename = f"data/results_{timestamp}.csv"

    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(["Generation", "Best Distance", "Best Fitness", "Average Fitness"])

        # -----------------------------
        # Evolutionary Loop
        # -----------------------------
        for gen in range(N_GENERATIONS):

            # Evaluate bees
            for bee in population:
                bee.evaluate(flowers, hive)

            # Sort bees by fitness (higher is better)
            population.sort(key=lambda b: b.fitness, reverse=True)

            # Track stats
            best = population[0]
            avg = sum(b.fitness for b in population) / len(population)
            history_best.append(best.fitness)
            history_avg.append(avg)

            print(f"Generation {gen} | Best distance: {best.distance:.2f}")

            # Save stats into CSV
            writer.writerow([gen, best.distance, best.fitness, avg])

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

            # Track all offspring for genealogy
            all_bees.extend(offspring)

            # New population = elites + offspring
            population = selected + offspring

    # -----------------------------
    # Final Results
    # -----------------------------
    best_bee = population[0]
    print("\n=== Final Results ===")
    print(f"Best distance found: {best_bee.distance:.2f}")
    print(f"Results saved in data folder : {csv_filename}")

    # -----------------------------
    # Visualization 1: Genealogy Tree
    # -----------------------------
    G = nx.DiGraph()
    bee_dict = {bee.id: bee for bee in all_bees}

    def add_genealogy(bee):
        """Recursive function to add genealogy links to the graph"""
        if bee.id not in G:
            G.add_node(bee.id, label=f"Bee {bee.id} (Gen {bee.generation})")
            for pid in bee.parents:
                G.add_edge(pid, bee.id)
                if pid in bee_dict:
                    add_genealogy(bee_dict[pid])

    add_genealogy(best_bee)

    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, labels=labels,
            node_size=500, node_color="lightblue", font_size=8)
    plt.title("Genealogy of the Best Bee")
    plt.show()

    # -----------------------------
    # Visualization 2: Best Path
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
    # Visualization 3: Fitness Evolution
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