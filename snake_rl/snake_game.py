from dataclasses import dataclass
from enum import Enum
from math import sqrt
from random import randint

import logging
from typing import NamedTuple, Self
import pygame


logger = logging.getLogger(__name__)


@dataclass
class Point:
    x: int
    y: int
    
    def distance_to(self, other: Self) -> float:
        return sqrt(abs(self.x - other.x) ** 2 + abs(self.y - other.y) ** 2)

Size = NamedTuple('Size', [('width', int), ('height', int)])


# Style 1
EMPTY_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)
APPLE_COLOR = (255, 0, 0)
SNAKE_HEAD_COLOR = (100, 200, 0)
SNAKE_COLOR = (0, 255, 0)

# Style 2
# SNAKE_HEAD_COLOR = 'green'
# SNAKE_COLOR = 'lightgreen'
# APPLE_COLOR = 'red'
# EMPTY_COLOR = 'white'
# BORDER_COLOR = 'black'


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    def apply_to(self, point: Point):
        return Point(self.value[0] + point.x,
                     self.value[1] + point.y)


class SnakeGame:
    def __init__(self, board_size: tuple[int, int], apple_count: int = 1, max_unfed_moves: int = -1):
        self.board_size = Size(*board_size)
        self.snake = []
        self.snake_dir = Direction.UP
        self.apples = []
        
        self.last_feed_step = 0
        self.max_unfed_moves = max_unfed_moves

        self.snake.append(Point(self.board_size.width//2, self.board_size.height//2))
        self.apples.extend(self.__get_random_empty_point() for _ in range(apple_count))

        self.moves = 0
        self.score = 0

    def reset(self) -> None:
        self.snake = [Point(self.board_size.width//2, self.board_size.height//2)]
        self.apples = [self.__get_random_empty_point() for _ in self.apples]
        self.last_feed_step = 0

        self.moves = 0
        self.score = 0

    @property
    def snake_head(self) -> Point:
        return self.snake[0]

    def __get_random_empty_point(self) -> Point:
        while True:
            point = Point(randint(0, self.board_size.width - 1),
                          randint(0, self.board_size.height - 1))

            if point not in self.snake and point not in self.apples:
                return point

    def _create_new_apple(self) -> None:
        self.apples.append(self.__get_random_empty_point())

    def make_move(self, direction: Direction) -> int:
        new_snake_head = direction.apply_to(self.snake_head)

        if self.is_snake(new_snake_head) or not self.is_inside(new_snake_head):
            logger.debug('You Lose - Hit the wall or yourself')
            return -1
        
        self.snake.insert(0, new_snake_head)
        self.moves += 1

        if (self.max_unfed_moves != -1 and
            self.moves >= self.last_feed_step + self.max_unfed_moves):
            logger.debug('You Lose - Too many moves')
            return -1

        if self.is_apple(new_snake_head):
            self.apples.remove(new_snake_head)
            self._create_new_apple()
            self.score += 1
            self.last_feed_step = self.moves
            return 1
        else:
            self.snake.pop()
            return 0

    def move_relative(self, rel_dir: int) -> int:
        if rel_dir != 0:
            dirs = list(Direction)
            direction_index = (dirs.index(self.snake_dir) + rel_dir) % 4
            self.snake_dir = dirs[direction_index]

        return self.make_move(self.snake_dir)

    def is_collision(self, point: Point) -> bool:
        return self.is_snake(point) or not self.is_inside(point)

    def is_snake(self, point: Point) -> bool:
        return point in self.snake

    def is_apple(self, point: Point) -> bool:
        return point in self.apples

    def is_inside(self, point: Point) -> bool:
        return 0 <= point.x < self.board_size[0] and \
               0 <= point.y < self.board_size[1]


class GraphicalSnakeGame(SnakeGame):
    def __init__(self, board_size: tuple[int, int], apple_count: int = 1, max_unfed_moves: int = -1):
        super().__init__(board_size, apple_count, max_unfed_moves)
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.screen = pygame.display.set_mode((600, 600))

    def update_board(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        self.render()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.make_move(Direction.UP)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.make_move(Direction.DOWN)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.make_move(Direction.RIGHT)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.make_move(Direction.LEFT)
            elif event.key == pygame.K_r:
                self.reset()

    def render(self) -> None:
        self.screen.fill((255, 255, 255))

        cell_size = tuple(map(lambda a, b: round(a / b), self.screen.get_size(), self.board_size))

        for x in range(self.board_size.width):
            for y in range(self.board_size.height):
                rect = pygame.Rect(x * cell_size[0], y * cell_size[1], *cell_size)

                if self.is_snake(Point(x, y)):
                    if self.snake_head == Point(x, y):
                        color = SNAKE_HEAD_COLOR
                    else:
                        color = SNAKE_COLOR
                elif self.is_apple(Point(x, y)):
                    color = APPLE_COLOR
                else:
                    color = EMPTY_COLOR

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BORDER_COLOR, rect, 1)

        pygame.display.update()
