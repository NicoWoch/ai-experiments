from abc import ABC, abstractmethod
from dataclasses import dataclass
import random
from typing import Callable, Any, Iterable, Self

from item import Item

NEIGHTBOURS = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1),
)


@dataclass
class EntityConfig:
    energy_per_move: Callable[[int], int]
    reproduction_cost: int
    reproduction_energy: int
    reproduction_threshold: int
    reproduction_chance: float


@dataclass
class EntityQueryCallables:
    kill: Callable[['Entity', int, int], Any]
    spawn: Callable[['Entity'], Any]
    is_on_board: Callable[[int, int], bool]
    get_item_type: Callable[[int, int], Item]
    prey_config: EntityConfig
    predator_config: EntityConfig


class Entity(ABC):
    def __init__(self, x: int, y: int, energy: int, callables: EntityQueryCallables):
        self.x = x
        self.y = y
        self.energy = energy
        self._callables = callables

    @property
    @abstractmethod
    def item_type(self) -> Item: ...

    @abstractmethod
    def can_move(self, move: tuple[int, int]) -> bool: ...

    def _move(self, move: tuple[int, int]):
        assert self._callables.is_on_board(*move) and self.can_move(move), 'Cannot move here'

        self._callables.kill(self, self.x, self.y)
        self._callables.kill(self, *move)

        self.x, self.y = move
        self._callables.spawn(self)

        if self.energy <= 0:
            self._callables.kill(self, self.x, self.y)

    def random_move(self) -> bool:
        moves = list(self._find_possible_moves())

        if len(moves) == 0:
            return False

        self._move(random.choice(moves))
        return True

    def _find_possible_moves(self) -> Iterable[tuple[int, int]]:
        for rel_move_x, rel_move_y in NEIGHTBOURS:
            move = self.x + rel_move_x, self.y + rel_move_y

            if self._callables.is_on_board(*move) and self.can_move(move):
                yield move

    def _reproduct(self, cls: type[Self], energy: int) -> bool:
        possibilities = self._find_possible_moves()
        possibilities = filter(lambda x: self._callables.get_item_type(x[0], x[1]) == Item.Empty, possibilities)
        possibilities = list(possibilities)

        if len(possibilities) == 0:
            return False

        pos = random.choice(possibilities)
        new_entity = cls(pos[0], pos[1], energy, self._callables)
        self._callables.spawn(new_entity)
        return True


class Prey(Entity):
    @property
    def item_type(self) -> Item:
        return Item.Prey

    def can_move(self, move: tuple[int, int]) -> bool:
        item = self._callables.get_item_type(*move)
        return item == Item.Empty

    def _move(self, move: tuple[int, int]):
        config = self._callables.prey_config

        possibilites = len(list(self._find_possible_moves()))
        self.energy += config.energy_per_move(possibilites)

        super()._move(move)

        if self.energy >= config.reproduction_threshold and random.random() < config.reproduction_chance:
            if self._reproduct(type(self), config.reproduction_cost):
                self.energy -= config.reproduction_energy


class Predator(Entity):
    @property
    def item_type(self) -> Item:
        return Item.Predator

    def can_move(self, move: tuple[int, int]) -> bool:
        item = self._callables.get_item_type(*move)
        return item in (Item.Empty, Item.Prey)

    def _move(self, move: tuple[int, int]):
        config = self._callables.predator_config

        possibilites = len(list(self._find_possible_moves()))
        self.energy += config.energy_per_move(possibilites)

        super()._move(move)

        if self.energy >= config.reproduction_threshold and random.random() < config.reproduction_chance:
            if self._reproduct(type(self), config.reproduction_cost):
                self.energy -= config.reproduction_energy
