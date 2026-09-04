from typing import Self
import random

X_RANGE = (1, 2)
Y_RANGE = (3, 5)


def map_range(value: float, start: tuple[float, float], end: tuple[float, float]) -> float:
    return (value - start[0]) * (end[1] - end[0]) / (start[1] - start[0]) + end[0]


class Chromosome:
    def __init__(self, gens: int | None = None):
        self._gens = gens if gens is not None else random.getrandbits(30)

    @classmethod
    def cross(cls, ch1: Self, ch2: Self) -> tuple[Self, Self]:
        child_1 = (ch1.gen_x << 15) | ch2.gen_y
        child_2 = (ch2.gen_x << 15) | ch1.gen_y

        return cls(child_1), cls(child_2)

    def mutate(self) -> 'Chromosome':
        new_gens = self._gens
        new_gens ^= 1 << random.randrange(30)
        return Chromosome(new_gens)

    @property
    def gen_x(self) -> int:
        return self._gens >> 15

    @property
    def gen_y(self) -> int:
        return self._gens & (2 ** 15 - 1)

    @property
    def x(self) -> float:
        return map_range(self.gen_x, (0, 2 ** 15 - 1), X_RANGE)

    @property
    def y(self) -> float:
        return map_range(self.gen_y, (0, 2 ** 15 - 1), Y_RANGE)

    @property
    def gens(self) -> int:
        return self._gens

    @property
    def gencode(self) -> str:
        return f'{self._gens:#b}'[2:]

    def __lt__(self, other: Self) -> bool:
        return self.gens < other.gens

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Chromosome):
            return False
        
        return self.gens == other.gens

    def __hash__(self) -> int:
        return hash(self._gens)

    def __str__(self) -> str:
        return f'<Chromosome {self.x:.3f} {self.y:.3f}>'

    __repr__ = __str__
