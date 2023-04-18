# Q Learning

In the Q Learning folder, we apply classic Q learning with a Q table. The Q table gets updated according to the [Bellman equation](https://en.wikipedia.org/wiki/Bellman_equation). The training is based on a [project](https://github.com/techtribeyt/snake-q-learning) by techtribeyt.

---

## Results

During Q Learning, I attempted several values to observe their affects on the q tables. The dataframes can be found in the `results` folder.

The scores of the various models are visualised below. The base values are: 
- Learning rate: 0.01
- Epsilon Discount: 0.9992 
- Discount Rate: 0.95

<img src="https://i.imgur.com/Bc0c5fn.png" width="600" alt="Score results">

We can also visualise the survival duration.

<img src="https://i.imgur.com/bLeS3RB.png" width="600" alt="Alive Duration results">

Interestingly, the best performing model was the model with a 0.100 learning rate at around 9000 episodes. It seems to have had a much greater focus on staying alive than reaching the food. However, the model's performance drops severely the last 300 episodes. 

On average, the model with a 0.001 learning rate did the best. The lowered epsilon also improved the performance. Perhaps a change in both learning rate and epsilon discount could perform even better.

--- 

## Files

The `QEnvironment` inherits from `BaseTrainer` to handle inputs and check safe spots for the state space, which in turn inherits from `BaseSnake` to run the game.

It gives a reward for 1 per apple gained, and a negative reward of -10 per death, which occurs when the snake runs into a wall or into itself.

The input consists of binary values. These are as follows:
- The snake's direction: Left, Right, Up and Down.
- The direction of the food: Left, Right, Up and Down.
- Safety around the snake's head: Left, Right, Up and Down.

Based on research of other people's attempts, these values seemed the most fitting.

The `QTrainer` uses the `QEnvironment` to train the q table. While the snake is alive it takes actions in the environment. Depending on the epsilon value, these actions may be random. The q table is then updated based on the new state that is created, and the reward that was received based on the actions.

The `QVisualiser` is used to run a game using an existing q table. It uses the `QEnvironment` and `BaseVisualiser` for this purpose. 

In `q_replay.py`, the `QVisualiser` is used to iteratively run a game for all stored q tables.

Lastly, `q_loader` is a helper function used to load in existing q tables.