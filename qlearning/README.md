﻿# Q Learning

In the Q Learning folder, we apply classic Q learning with a Q table. The Q table gets updated according to the [Bellman equation](https://en.wikipedia.org/wiki/Bellman_equation). The training is based on a [project](https://github.com/techtribeyt/snake-q-learning) by techtribeyt.

---

## Results

During Q Learning, I attempted several values to observe their affects on the q tables. The dataframes can be found in the `results` folder.

--- 

## Files

The `QEnvironment` makes use of `BaseSnake` to run the game and `BaseTrainer` to handle inputs and check safe spots for the state space.

It gives a reward for 1 per apple gained, and a negative reward of -10 per death, which occurs when the snake runs into a wall or into itself.

The input consists of binary values. These are as follows:
- The snake's direction: Left, Right, Up and Down.
- The direction of the food: Left, Right, Up and Down.
- Safety around the snake's head: Left, Right, Up and Down.

Based on research of other people's attempts, these values seemed the most fitting.

The `q_trainer` uses this environment to create the q table. While the snake is alive it takes actions in the environment. Depending on the epsilon value, these actions may be random. The q table is then updated based on the new state that is created, and the reward that was received based on the actions.

The `QVsualiser` is used to run a game using an existing q table. It uses the `QEnvironment` and `BaseVisualiser` for this purpose. 

The `q_replay` uses the `QVisualiser` to iteratively run and visualise all q tables.

Lastly, `q_loader` is a helper function used to load in existing q tables.