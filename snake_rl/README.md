# Snake Reinforcement Learning

Uses **reinforcement learning** with a **Deep Q-Network ([DQN](https://en.wikipedia.org/wiki/Q-learning#Deep_Q-learning))** to train a neural network to play the classic game of Snake.

## File Structure

### Entry points

- `main.py` - entry point of the AI training program.

- `main_human.py` - entry point of the test program, where you can test the game without AI.

### AI

- `ai_agent.py` - implements *Agent* and *AgentTrainer*. Has more high-level training algorithm related methods.

- `ai_model.py` - implements *LinearQNet* and *QTrainer* using the **[PyTorch](https://github.com/pytorch/pytorch)** API.

- `ai_snake_game.py` - adds usefull methods for AI to *GraphicalSnakeGame* base class and disables user control over the game.

### Utils

- `snake_game.py` - implements *SnakeGame*, board with moving semantics, abstract from any AI-related methods. Contains *GraphicalSnakeGame* using **[pygame](https://github.com/pygame/pygame)** to display and update the grid for the game.

- `controls.py` - small tkinter window containing sliders for easy modification of variables.

- `graph_score.py` - Matplotlib graph for displaying score of AI. Initializes at import time.

- `logging_config.py` - configuration for python logging module.

- `mean_stream.py` - stream of numbers having automatic rolling mean calculation.

### Runtime Data

- `data/app.log` - output from logging module, additional to console.

- `data/model.pth` - backup of the first model that got the current best score.
