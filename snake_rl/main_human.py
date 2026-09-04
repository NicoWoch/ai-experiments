import pygame

from snake_game import GraphicalSnakeGame


def play_human():
    game = GraphicalSnakeGame((10, 10))

    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)

        game.render()
        
        
if __name__ == '__main__':
    play_human()
