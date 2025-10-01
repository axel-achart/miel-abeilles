import matplotlib.pyplot as plt
import random
import networkx as nx
import csv
import datetime
import os
from beehive import *


def run_simulation(mutation_rate, flowers, hive, pop_size, n_generations, genealogy=False):
    """
    Run one simulation with a given mutation rate.
    Save CSV results and return stats.
    If genealogy=True → returns (best_bee, history_best, history_avg, all_bees, csv_filename).
    Otherwise → returns (history_best, history_avg, csv_filename).
    """

    # --- Create folder for this mutation rate ---
    folder = f"data/mutation_rate_{mutation_rate}"
    os.makedirs(folder, exist_ok=True)

    # --- Create CSV filename ---
    timestamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
    csv_filename = os.path.join(folder, f"results_{timestamp}.csv")

    population = generate_population(pop_size, flowers)
    history_best = []
    history_avg = []
    all_bees = list(population)

    # --- Open CSV file ---
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(["Generation", "Best Distance", "Best Fitness", "Average Fitness"])

        for gen in range(n_generations):
            # Evaluate
            for bee in population:
                bee.evaluate(flowers, hive)

            # Sort by fitness
            population.sort(key=lambda b: b.fitness, reverse=True)

            best = population[0]
            avg = sum(b.fitness for b in population) / len(population)
            history_best.append(best.fitness)
            history_avg.append(avg)

            print(f"[Mutation={mutation_rate}] Gen {gen} | Best distance: {best.distance:.2f}")

            writer.writerow([gen, best.distance, best.fitness, avg])

            # Selection
            selected = selection(population, proportion=0.5)

            # Reproduction + mutation
            offspring = []
            while len(selected) + len(offspring) < pop_size:
                parent1, parent2 = random.sample(selected, 2)
                child = crossover(parent1, parent2)
                child = mutation(child, mutation_rate)
                child.evaluate(flowers, hive)
                offspring.append(child)

            all_bees.extend(offspring)
            population = selected + offspring

    if genealogy:
        return population[0], history_best, history_avg, all_bees, folder, csv_filename
    else:
        return history_best, history_avg, folder, csv_filename


def save_plot(fig, folder, name):
    """Helper to save and close matplotlib figures as PNG"""
    filepath = os.path.join(folder, f"{name}.png")
    fig.savefig(filepath, dpi=300, bbox_inches="tight")
    print(f"[Saved plot] {filepath}")
    plt.close(fig)


def main():
    hive = (500, 500)

    # Fixed set of 20 flowers
    flowers = [(796, 310), (774, 130), (116, 69), (908, 534), (708, 99), (444, 428),
               (220, 307), (501, 287), (345, 560), (628, 311), (901, 639), (436, 619),
               (938, 646), (45, 549), (837, 787), (328, 489), (278, 434), (704, 995),
               (101, 482), (921, 964)]

    POP_SIZE = 101
    N_GENERATIONS = 200

    try:
        taux_mutation = float(input("\nEnter mutation rate (ex : 0.05 for 5%) : "))
        if not (0 <= taux_mutation <= 1):
            raise ValueError
        MAIN_MUTATION = taux_mutation
    except ValueError:
        print("\nInvalid input. Using default mutation rate of 0.05.")
        MAIN_MUTATION = 0.05

    # -----------------------------
    # Main simulation (with genealogy)
    # -----------------------------
    best_bee, history_best, history_avg, all_bees, folder, csv_filename = run_simulation(
        MAIN_MUTATION, flowers, hive, POP_SIZE, N_GENERATIONS, genealogy=True
    )

    print("\n=== Final Results ===")
    print(f"Best distance found: {best_bee.distance:.2f}")
    print(f"Results saved in: {csv_filename}\n")

    # -----------------------------
    # Graph 1: Genealogy Tree
    # -----------------------------
    G = nx.DiGraph()
    bee_dict = {bee.id: bee for bee in all_bees}

    def add_genealogy(bee):
        if bee.id not in G:
            G.add_node(bee.id, label=f"Bee {bee.id} (Gen {bee.generation})")
            for pid in bee.parents:
                G.add_edge(pid, bee.id)
                if pid in bee_dict:
                    add_genealogy(bee_dict[pid])

    add_genealogy(best_bee)

    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')

    fig1 = plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels=labels,
            node_size=600, node_color="lightblue", font_size=8)
    plt.title("Genealogy of the Best Bee")
    save_plot(fig1, folder, "genealogy_tree")
    plt.show()

    # -----------------------------
    # Graph 2: Best Path
    # -----------------------------
    x = [hive[0]] + [flowers[i][0] for i in best_bee.path] + [hive[0]]
    y = [hive[1]] + [flowers[i][1] for i in best_bee.path] + [hive[1]]

    fig2 = plt.figure(figsize=(10, 6))
    plt.scatter(*hive, color="red", s=120, marker="s", label="Hive")
    plt.scatter([f[0] for f in flowers], [f[1] for f in flowers],
                color="gold", s=100, marker="o", edgecolors="black", label="Flowers")
    plt.plot(x, y, color="blue", linewidth=2, linestyle="-", label="Best Path")
    plt.scatter(x, y, color="blue", s=40)
    plt.title("Path of the Best Bee")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    save_plot(fig2, folder, "best_path")
    plt.show()

    # -----------------------------
    # Graph 3: Fitness Evolution
    # -----------------------------
    fig3 = plt.figure(figsize=(10, 6))
    plt.plot(history_best, label="Best Fitness", color="blue")
    plt.plot(history_avg, label="Average Fitness", color="orange")
    plt.title(f"Performance Evolution Across Generations (Mutation {MAIN_MUTATION})")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.legend()
    save_plot(fig3, folder, "fitness_evolution")
    plt.show()

    # -----------------------------
    # Ask for mutation comparison
    # -----------------------------
    choice = input("\nDo you want to visualize mutation rate comparison graphs ? (y/n): ").strip().lower()
    if choice == "y":
        mutation_rates = [0.01, 0.05, 0.1, 0.5, 0.8, 1.0]
        results_best = {}
        results_avg = {}

        for rate in mutation_rates:
            best, avg, folder_rate, csv_file = run_simulation(
                rate, flowers, hive, POP_SIZE, N_GENERATIONS
            )
            results_best[rate] = best
            results_avg[rate] = avg
            print(f"Saved results for mutation {rate} in {csv_file}")

        # Best Fitness comparison
        fig4 = plt.figure(figsize=(10, 6))
        for rate, values in results_best.items():
            plt.plot(values, label=f"Mutation {rate}")
        plt.title("Best Fitness Comparison by Mutation Rate")
        plt.xlabel("Generations")
        plt.ylabel("Best Fitness")
        plt.legend()
        save_plot(fig4, "data", "comparison_best_fitness")
        plt.show()

        # Average Fitness comparison
        fig5 = plt.figure(figsize=(10, 6))
        for rate, values in results_avg.items():
            plt.plot(values, label=f"Mutation {rate}")
        plt.title("Average Fitness Comparison by Mutation Rate")
        plt.xlabel("Generations")
        plt.ylabel("Average Fitness")
        plt.legend()
        save_plot(fig5, "data", "comparison_avg_fitness")
        plt.show()


if __name__ == "__main__":
    main()