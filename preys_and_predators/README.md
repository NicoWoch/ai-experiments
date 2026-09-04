# Preys and Predators

Simulates the **predator-prey problem** based on simple, adjustable rules. 

Each entity (prey or predator) has an internal **energy buffer**. Prey gain energy over time, while predators need to "eat" prey to stay alive.

Each entity reproduces after it acquires a defined amount of energy, and after reproduction it loses some of that energy, with some transferred to the offspring and the rest lost in the process.

Includes a **real-time Matplotlib graph** displaying the current population of each entity.
The population graph shows similarities to [Lotka-Volterra](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations) system of differential equations.

## File Structure

- `board_window.py` - tkinter window for displaying a *Board* object

- `board.py` - defines a grid of entities and orchestrates rules in *step()*. Delegates work to separate entities classes.

- `entity.py` - declares base *Entity* class and **rules for prey and predator** in appropriate classes.

- `item.py` - has just one enum *Item* specifying three different type of cells in *Board* grid

- `main.py` - entry point of the program. Contains **configuration** for rules of silumation.
