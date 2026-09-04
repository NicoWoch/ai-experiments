import pygame

from snake_game import GraphicalSnakeGame, Point


class AISnakeGame(GraphicalSnakeGame):
    def get_nearest_apple(self) -> Point:
        return min(self.apples, key=lambda x: self.snake_head.distance_to(x))

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def ai_play_move(self, state: int) -> tuple[int, int, int]:
        old_dist = self.get_apple_dist(self.snake_head)
        
        move_result = self.move_relative(state - 1)

        self.update_board()
        
        new_dist = self.get_apple_dist(self.snake_head)
        is_closer_to_apple = new_dist < old_dist

        if move_result == -1:
            return -4, 1, self.score
        elif move_result == 0 and is_closer_to_apple:
            return 0, 0, self.score
        elif move_result == 0:
            return -1, 0, self.score
        else:
            return 8, 0, self.score
        
    def get_apple_dist(self, point: Point) -> float:
        return min(
            self.snake_head.distance_to(apple)
            for apple in self.apples
        )
