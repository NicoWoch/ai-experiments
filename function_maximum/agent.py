import itertools
from typing import Any, Callable, Iterable
import random

from matplotlib import pyplot as plt

from chromosome import Chromosome

CONFIG: dict[str, Any] = {
    'population': 500,
    'generations': 20,
    'use_elite': True,
    'tournament_group_size': 2,
    'mutation_chance': 0.15,
    'max_mutation_tries': 4,
    'double_mutation_chance': 0.4,
}


class Agent:
    def __init__(self, function: Callable[[float, float], float]):
        self.function = function
        self.population = [Chromosome() for _ in range(CONFIG['population'])]
        self.losses = [0.0 for _ in range(CONFIG['population'])]

    def main(self):
        x1, y1, maximum1 = self.find_maximum(1)
        self.population = [Chromosome() for _ in range(CONFIG['population'])]
        x2, y2, maximum2 = self.find_maximum(2)
        self.population = [Chromosome() for _ in range(CONFIG['population'])]
        x3, y3, maximum3 = self.find_maximum(3)

        print(f'\nx = {x1:.5f}\ny = {y1:.5f}\nf(x, y) = {maximum1:.5f}')
        print(f'\nx = {x2:.5f}\ny = {y2:.5f}\nf(x, y) = {maximum2:.5f}')
        print(f'\nx = {x3:.5f}\ny = {y3:.5f}\nf(x, y) = {maximum3:.5f}')
        
        plt.title('Best value for each generation')
        plt.legend()
        plt.xlabel('Generation')
        plt.xticks(range(0, 21))
        plt.ylabel('best f(x, y)')
        plt.show()

    def find_maximum(self, attempt: int) -> tuple[float, float, float]:
        best_chromosome: Chromosome | None = None
        best_loss: float = float('-inf')
        best_losses: list[float] = []

        for generation in range(CONFIG['generations']):
            self.update_losses()

            if self.losses[0] > best_loss:
                best_chromosome = self.population[0]
                best_loss = self.losses[0]

            print(f' Generation {generation} '.center(20, '-'))
            print(f'Population size:  {len(self.population)}')
            print(f'Best chromosomes:', end='\n\t')
            print(*self.population[:2], sep='\n\t')
            print(f'Best losses:', end='\n\t')
            print(*self.losses[:2], sep='\n\t')
            print()
            best_losses.append(self.losses[0])

            self.population = self.create_new_population()

        plt.plot(best_losses, label=f'Attempt {attempt}')
        
        assert best_chromosome is not None

        return best_chromosome.x, best_chromosome.y, best_loss

    def update_losses(self):
        for i, chromosome in enumerate(self.population):
            self.losses[i] = self.loss_function(chromosome)

        indices = list(range(len(self.population)))
        indices.sort(key=lambda j: self.losses[j], reverse=True)

        self.population = [self.population[j] for j in indices]
        self.losses = [self.losses[j] for j in indices]

    def loss_function(self, chromosome: Chromosome) -> float:
        return self.function(chromosome.x, chromosome.y)

    def create_new_population(self) -> list[Chromosome]:
        selection = self.tournament_selection(CONFIG['tournament_group_size'])
        return self.repopulate(selection)

    def tournament_selection(self, group_size: int) -> set[int]:
        selected: set[int] = set()

        indices = list(range(len(self.population)))
        random.shuffle(indices)

        for rand_index in range(group_size, len(indices), group_size):
            group = indices[rand_index - group_size:rand_index]

            best = max(group, key=lambda i: self.losses[i])
            selected.add(best)

        return selected

    def repopulate(self, parents: set[int]) -> list[Chromosome]:
        new_population_set: set[Chromosome] = set()

        for dad, mom in self.parents_pairer(parents):
            childs = Chromosome.cross(self.population[dad], self.population[mom])
            new_population_set.update(childs)

            if len(new_population_set) >= len(self.population):
                break

        i = 0
        while len(new_population_set) < len(self.population) and i < len(self.population):
            new_population_set.add(self.population[i])
            i += 1

        if len(new_population_set) < len(self.population):
            remaining = len(self.population) - len(new_population_set)
            new_population = list(new_population_set) + self.population[:remaining]
        else:
            new_population = random.sample(list(new_population_set), k=len(self.population))

        for i, chromosome in enumerate(new_population):
            if random.random() <= CONFIG['mutation_chance']:
                new_population[i] = self.mutate_chromosome(chromosome)

        if CONFIG['use_elite']:
            new_population[random.randrange(len(new_population_set))] = self.population[0]

        return new_population

    def parents_pairer(self, parents: set[int]) -> Iterable[tuple[int, int]]:
        # TODO: improve

        parents_lst: list[int] = list(
            sorted(parents, key=lambda i: self.losses[i], reverse=True)
        )

        yield from itertools.combinations(parents_lst, 2)

    @classmethod
    def mutate_chromosome(cls, chromosome: Chromosome) -> Chromosome:
        for _ in range(CONFIG['max_mutation_tries']):
            chromosome = chromosome.mutate()

            if random.random() > CONFIG['double_mutation_chance']:
                break

        return chromosome
