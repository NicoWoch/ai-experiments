import logging
import random
from collections import deque
import os.path

import torch
from torch import Tensor

from ai_model import LinearQNet, QTrainer
from mean_stream import MeanStream
from ai_snake_game import AISnakeGame
from snake_game import Direction


type MemoryEntry = tuple[Tensor, Tensor, float, Tensor, int]


logger = logging.getLogger(__name__)


MAX_MEMORY = 100_000
BATCH_SIZE = 1_000


class Agent:
    def __init__(self, learning_rate: float):
        self.n_games = 0
        self.gamma = 0.9
        self.memory: deque[MemoryEntry] = deque(maxlen=MAX_MEMORY)
        self.model = LinearQNet(10, [256], 3)
        self.trainer = QTrainer(self.model, lr=learning_rate, gamma=self.gamma)
        
        # self.map_influence: float = 0

    def set_learning_rate(self, learning_rate: float) -> None:
        self.trainer.optimizer.param_groups[0]["lr"] = learning_rate

    def get_state(self, game: AISnakeGame) -> Tensor:
        apple = game.apples[0]
        head = game.snake_head

        apple_dir = min(max(apple.x - head.x, -1), 1), \
                    min(max(apple.y - head.y, -1), 1)
                    
        # apples_map: list[list[float]] = [[0 for _ in range(10)] for _ in range(10)]
        # snake_map: list[list[float]] = [[0 for _ in range(10)] for _ in range(10)]
        
        # for part in game.apples:
        #     apples_map[part.y][part.x] = 1
        
        # for part in game.snake:
        #     snake_map[part.y][part.x] = 0.5
            
        # snake_map[game.snake_head.y][game.snake_head.x] = 1

        return Tensor(list(map(int, [
            game.snake_dir == Direction.UP,
            game.snake_dir == Direction.DOWN,
            game.snake_dir == Direction.RIGHT,
            game.snake_dir == Direction.LEFT,
            apple_dir[0],
            apple_dir[1],
            game.is_collision(Direction.UP.apply_to(game.snake_head)),
            game.is_collision(Direction.DOWN.apply_to(game.snake_head)),
            game.is_collision(Direction.RIGHT.apply_to(game.snake_head)),
            game.is_collision(Direction.LEFT.apply_to(game.snake_head)),
            # *[v for row in apples_map for v in row],
            # *[v for row in snake_map for v in row],
        ])))

    def remember(self, state: Tensor, action: Tensor, reward: float, next_state: Tensor, done: int):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        self.trainer.train_step(
            torch.stack([v[0] for v in mini_sample]),
            torch.stack([v[1] for v in mini_sample]),
            torch.tensor([v[2] for v in mini_sample]),
            torch.stack([v[3] for v in mini_sample]),
            torch.tensor([v[4] for v in mini_sample]),
        )

    def train_short_memory(self, state: Tensor, action: Tensor, reward: float, next_state: Tensor, done: int):
        self.trainer.train_step(
            state.unsqueeze(0), action.unsqueeze(0),
            torch.tensor([reward]), next_state.unsqueeze(0),
            torch.tensor([done])
        )

    def get_action(self, state: Tensor, exploration: float = 0) -> Tensor:
        if random.random() < exploration:
            move = [0, 0, 0]
            move[random.randint(0, 2)] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            move = self.model(state0)

        return Tensor(move)


class AgentTrainer:
    def __init__(self, agent: Agent, game: AISnakeGame, scores_mean: MeanStream) -> None:
        self.agent = agent
        self.game = game
        
        self.iteration: int = 1
        self.step: int = 1
        
        self.last_apple_step: int = 0
        
        self.record: int = 0
        self.scores: MeanStream = scores_mean
    
    def train_step(self, exploration: float) -> None:
        state_old = self.agent.get_state(self.game)

        final_move = self.agent.get_action(state_old, exploration=exploration)
        reward, done, score = self.game.ai_play_move(int(torch.argmax(final_move).item()))

        logger.debug(f'STEP: {final_move=}\n\t{reward=}  -  {done=}  -  {score=}\n\tstate={state_old}')

        state_new = self.agent.get_state(self.game)

        self.agent.train_short_memory(state_old, final_move, reward, state_new, done)
        self.agent.remember(state_old, final_move, reward, state_new, done)
        
        self.step += 1

        if done:
            self.game.reset()
            self.agent.n_games += 1
            self.agent.train_long_memory()

            self.iteration += 1
            self.step = 1
            
            if score > self.record:
                self.record = score
                path = os.path.join(os.path.dirname(__file__), 'data/model.pth')
                self.agent.model.save(path)
                logger.info(f'Saved model with new record {self.record}')

            logger.info(f'Game {self.agent.n_games} ended with score {score}')

            self.scores.append(score)
            
    def get_scores(self) -> MeanStream:
        return self.scores
