# 🐝 Bees and honey

## 📖 Project Description
The goal is to simulate the evolution of a colony of bees using a **genetic algorithm**, in order to optimize their foraging paths between a hive and a set of flowers.

The project demonstrates how **natural selection** can be modeled computationally as “digital natural selection”.

---

## 🚀 Features

### Maze of Flowers (Problem Setting)

| Element          | Description                                                        |
|------------------|--------------------------------------------------------------------|
| Hive             | Fixed position                                                     |
| Flowers          | Fixed randomly in the field                                        |
| Bees             | Must visit all flowers and return to the hive, optimizing the path |

### Genetic Algorithm

| Concept        | Description                                            |
|----------------|--------------------------------------------------------|
| Population     | Random paths (permutations of flowers)                 |
| Fitness        | Inverse of total distance traveled                     |
| Selection      | Elitist (best bees survive and reproduce)              |
| Crossover      | Order Crossover (OX)                                   |
| Mutation       | Swap mutation, probability is configurable             |

### Visualization

| Visualization      | Feature                                                       |
|--------------------|--------------------------------------------------------------|
| Path display       | Shows best bee’s path at last generation                      |
| Performance curves | Graphs for best and average fitness per generation            |

---

## 📊 Results

| Parameter            | Observation                                                      |
|----------------------|------------------------------------------------------------------|
| Mutation rate: Low   | Fast convergence, risk of premature stagnation                  |
| Mutation rate: High  | Greater diversity, slower convergence                           |
| Fitness curves       | A* performance plot shows fitness optimization over generations  |
