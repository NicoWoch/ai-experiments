# AI Experiments

## function_maximum

Finds the maximum of a predefined function using a **[genetic algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm)**, with each individual represented by a 30-bit chromosome encoding two integer arguments for the function `f(x, y)`.

## preys_and_predators

Simulates the **predator-prey problem** based on simple, adjustable rules. 

Each entity (prey or predator) has an internal **energy buffer**. Prey gain energy over time, while predators need to "eat" prey to stay alive.

Each entity reproduces after it acquires a defined amount of energy, and after reproduction it loses some of that energy, with some transferred to the offspring and the rest lost in the process.

Includes a **real-time Matplotlib graph** displaying the current population of each entity.
The population graph shows similarities to [Lotka-Volterra](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations) system of differential equations.

https://github.com/user-attachments/assets/7bdf7b5b-8d29-436a-9932-d16c28275526

## snake_rl

Uses **reinforcement learning** with a **Deep Q-Network ([DQN](https://en.wikipedia.org/wiki/Q-learning#Deep_Q-learning))** to train a neural network to play the classic game of Snake.

https://github.com/user-attachments/assets/6766541b-39cb-47df-bf1a-955e03fc4c14
