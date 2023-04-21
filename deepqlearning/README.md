# Deep Q Learning

In the Deep Q Learning folder, we apply deep Q learning with a Neural Network. The training is based on a [project](https://towardsdatascience.com/snake-played-by-a-deep-reinforcement-learning-agent-53f2c4331d36) by Hennie de Harder.

---

## Results

During Deep Q Learning, I attempted two tests to observe their affects on the q tables. The dataframes can be found in the `results` folder.

Both attempt used a neural network that was shaped as follows:

- Input shape according to state space.
- 3 hidden layers shaped: [128, 128, 128]
- Output of 4 neurons 

### Base Model

The 'base' model uses the same 12 states as the normal q learning version. The inputs are all binary and indicate the snake's direction, direction of the food and whether the spaces surrounding the snake's head are safe.

The scores are very erratic, which means the model is very inconsistent.

<img src="https://i.imgur.com/vCwSjRb.png" width="400" alt="DeepQ Base results">

We should keep in mind that this includes a minimum epsilon value of 0.01. This means 1 out of every 100 steps are random, which can be the cause of some lower results.

When we rerun the models without any epsilon value, we get the following result. Note that this data contains models divisible by 10 up to 100.

<img src="https://i.imgur.com/En3VF2M.png" width="400" alt="DeepQ Base results">

At episode 8, the model had a very good run with a score of 80. However, most other runs the score hovers around 40. The randomness originates from the apples spawning in different locations. The snake has a hard time learning to avoid its own body. While it can check its immediate surroundings, it can't look further than block from its head and traps itself as a result. 

With this being said, the model performs worse than the q table version. While the models are given the same information, it is much more difficult for the neural network to find the correct values base on its rewards.

### Continuous Model

To give the model more insight into its surroundings, the continuous model extends to 23 different states. From these states 8 are binary and 15 of are continuous. All continuous states were normalised to a range of 0 to 1.

The binary states include the snake's direction and whether the spaces surrounding the snake are safe.

The continuous states are the position of the head, the position of the food, the distance and angle to the food, the length of the snake and distance of the closest object in all 8 directions starting from the snake's head.

<img src="https://i.imgur.com/3QYbi48.png" width="400" alt="DeepQ Continuous results">

The model is off to a rough start, because it is no longer given binary indications to where the food is. Rather than an 'Up', 'Down', 'Left' and 'Right' approach, it is given the distance and angle. After a while, the model does figure it out. However, when visualised, it often goes a block too up or down, then corrects itself when it gets close to the food.

Over time there is a gradual improvement. The model reaches has an average score of around 30, but hovers between 0 and 60. 

In this case, the model does not learn how to avoid its own body very well at all. This may be, because it takes a long time before the snake is of sufficient size to struggle with its tail. As such, the snake does not reach this situation very often. When it does reach the situation, the epsilon has already reached its minimum, meaning there's very little room for exploration. This is also visible when we rerun the models without any exploration.

<img src="https://i.imgur.com/EXOTH1X.png" width="400" alt="DeepQ Continuous results">
    
Based on these results the average is even a little lower than expected, around 25.

A future version may benefit from a different training method, such as starting off with a longer body or approaching exploration versus exploitation differently.