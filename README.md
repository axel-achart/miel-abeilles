# 🐝 Le Miel et les Abeilles

## 📖 Project Description
The goal is to simulate the evolution of a colony of bees using a **genetic algorithm**, in order to optimize their foraging paths between a hive and a set of flowers.

The project demonstrates how **natural selection** can be modeled computationally as “digital natural selection”.

---

## 🚀 Features
### Maze of Flowers (Problem Setting)
- The hive is fixed.
- Flowers are placed in the field randomly.
- Bees must travel from the hive, visit all flowers, and return to the hive.

### Genetic Algorithm
- **Population**: initialized with random paths (permutations of flowers).
- **Fitness**: inversely proportional to the total distance traveled.
- **Selection**: elitist selection keeps the best bees.
- **Crossover**: Order Crossover (OX).
- **Mutation**: swap mutation with configurable probability.

### Visualization
- Path of the best bee in the final generation.
- Performance curves (best fitness and average fitness across generations).

---

## 📊 Results
- With low mutation, convergence is fast but risks stagnation.
- With higher mutation, diversity is preserved but convergence is slower.
- The **A* fitness evolution graph** shows performance improvement across generations.