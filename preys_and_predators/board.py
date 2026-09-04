import random
from dataclasses import dataclass

from item import Item
from entity import EntityQueryCallables, Entity, Prey, Predator, EntityConfig


@dataclass
class BoardConfig:
    initial_preys: int
    initial_predators: int
    initial_prey_energy: int
    initial_predator_energy: int
    predator_kill_energy: int
    prey_config: EntityConfig
    predator_config: EntityConfig


class Board:
    def __init__(self, board_size: int, config: BoardConfig):
        self.board_size = board_size
        self.config = config
        self.step_count = 0

        self.board = [[Item.Empty for _ in range(board_size)] for _ in range(board_size)]

        self._callables = EntityQueryCallables(
            self._kill, self._spawn,
            self._is_on_board, self._get_item_type,
            self.config.prey_config, self.config.predator_config
        )
        self._preys: dict[tuple[int, int], Entity] = {}
        self._predators: dict[tuple[int, int], Entity] = {}

        self.init_board()

    @property
    def population(self) -> int:
        return self.preys + self.predators

    @property
    def preys(self) -> int:
        return len(self._preys)

    @property
    def predators(self) -> int:
        return len(self._predators)

    def init_board(self):
        population = self.config.initial_preys + self.config.initial_predators
        assert population <= self.board_size ** 2, 'Initial population is greater than board'

        self._initial_spawn(count=self.config.initial_preys, is_prey=True)
        self._initial_spawn(count=self.config.initial_predators, is_prey=False)
        self.step_count = 0

    def _initial_spawn(self, *, count: int, is_prey: bool):
        spawned = 0

        while spawned < count:
            pos = tuple(random.randrange(self.board_size) for _ in range(2))

            if self.board[pos[0]][pos[1]] != Item.Empty:
                continue

            if is_prey:
                entity = Prey(pos[0], pos[1], self.config.initial_prey_energy, self._callables)
            else:
                entity = Predator(pos[0], pos[1], self.config.initial_predator_energy, self._callables)

            self._spawn(entity)
            spawned += 1

    def step(self):
        for prey in list(self._preys.values()):
            prey.random_move()

        for predator in list(self._predators.values()):
            predator.random_move()

        self.step_count += 1

    def _kill(self, who: Entity, x: int, y: int):
        killed = self.board[x][y]
        if who.item_type == Item.Predator and killed == Item.Prey:
            who.energy += self.config.predator_kill_energy

        if killed == Item.Prey:
            del self._preys[x, y]
        elif killed == Item.Predator:
            del self._predators[x, y]

        self.board[x][y] = Item.Empty

    def _spawn(self, entity: Entity):
        assert self.board[entity.x][entity.y] == Item.Empty, 'spawing cell is not empty'

        if entity.item_type == Item.Prey:
            self._preys[entity.x, entity.y] = entity
        elif entity.item_type == Item.Predator:
            self._predators[entity.x, entity.y] = entity

        self.board[entity.x][entity.y] = entity.item_type

    def _get_item_type(self, x: int, y: int) -> Item:
        return self.board[x][y]

    def _is_on_board(self, x: int, y: int) -> bool:
        return 0 <= x < self.board_size and 0 <= y < self.board_size
