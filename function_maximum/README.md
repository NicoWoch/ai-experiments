# Function Maximum

Finds the maximum of a predefined function using a **[genetic algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm)**, with each individual represented by a 30-bit chromosome encoding two integer arguments for the function `f(x, y)`.

## File Structure

- `agent.py` - matches chromosomes and merges them using underlying *Chromosome* class

- `chromosome.py` - has cross breed and mutation algorithms for chromosome

- `main.py` - defines `f(x, y)` and is the entry point of the program
