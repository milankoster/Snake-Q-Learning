# Snake Q Learning
This project explores two approaches to training an agent to play the classic game of Snake using Reinforcement Learning techniques. The aim is to develop an agent that can achieve high scores in the game.

---

## Approaches
The two approaches I explored are:

1. Q-Table: This approach uses a table to store the values of each state-action pair. The Q-Table is updated based on the reward obtained by taking an action in a certain state. The best action to take in each state is determined by selecting the action with the highest value in the Q-Table.


2. Deep Q-Learning: This approach uses a neural network to approximate the Q-Table. The neural network takes the current state as input and outputs the expected values of all possible actions. The network is trained using a variant of the Q-Learning algorithm called Deep Q-Learning.

---

## Results

I compared various Q-table and Deep Q-Learning approaches. The full results can be found under [Q learning] and [Deep Q learning].

### Q Table

The Q-Table approach achieved the best results. The best model reached an average score of 60. The Q-learning algorithm was able to effectively learn a good policy for playing Snake compared to the other methods.

[video1]

### Deep Q Learning

The Deep Q-Learning approach achieved worse results, with an average score of 30. Although it was able to learn the game and improve its scores over time, it did not reach the same level of performance as the Q-table approach. This could be due to a number of factors, such as the complexity of the neural network used for training or the hyperparameters selected for the algorithm.

[video2]

### Conclusion 

Overall, it seems that the Q-table approach was the most effective method for playing Snake in this particular implementation, but further experimentation with different algorithms and parameters could lead to improved performance of Deep Q Learning in the future.

---

## Usage

[manual]


