import logging_config as logging_config
logging_config.configure_logging()

import pygame

from mean_stream import MeanStream
from ai_snake_game import AISnakeGame
from ai_agent import Agent, AgentTrainer
from controls import Controls, ControlsWindow, Info
from snake_game import GraphicalSnakeGame
import graph_score as graph_score


def play_ai():
    game = AISnakeGame((10, 10), apple_count=5, max_unfed_moves=50)
    
    controls = Controls(
        learning_rate=0.01,
        exploration=0.5,
        map_influence=0,
        tps=10,
    )
    
    info = Info()
    ctrl_window = ControlsWindow(controls)

    agent = Agent(controls.learning_rate)
    trainer = AgentTrainer(agent, game, MeanStream(40))
    
    running = True
    clock = pygame.time.Clock()
    accumulator = 1001
    plot_acc = 1001
    while running:
        dt_ms = clock.tick(0)
        accumulator += dt_ms
        plot_acc += dt_ms
        
        if controls.tps != 0 and accumulator > (1000 / controls.tps):
            # trainer.agent.map_influence = controls.map_influence
            trainer.train_step(controls.exploration)
            info.iteration = trainer.iteration
            info.step = trainer.step
            info.best_score = trainer.record
            accumulator = 0
            
        if plot_acc > 1000:
            graph_score.plot(trainer.get_scores())
            plot_acc = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)

        ctrl_window.set_info(info)
        ctrl_window.update()
        trainer.agent.set_learning_rate(controls.learning_rate)
        
        game.render()


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


if __name__ == "__main__":
    play_ai()
