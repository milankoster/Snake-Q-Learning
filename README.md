# Snake Q Learning
This project explores two approaches to training an agent to play the classic game of Snake using Reinforcement Learning techniques. The aim is to develop an agent that can achieve high scores in the game.


## Approaches
The two approaches I explored are:

1. Q-Table: This approach uses a table to store the values of each state-action pair. The Q-Table is updated based on the reward obtained by taking an action in a certain state. The best action to take in each state is determined by selecting the action with the highest value in the Q-Table.


2. Deep Q-Learning: This approach uses a neural network to approximate the Q-Table. The neural network takes the current state as input and outputs the expected values of all possible actions. The network is trained using a variant of the Q-Learning algorithm called Deep Q-Learning.


## Results

I compared various Q-table and Deep Q-Learning approaches. The full results can be found under [Q learning](https://github.com/milankoster/Snake-Q-Learning/tree/master/qlearning) and [Deep Q learning](https://github.com/milankoster/Snake-Q-Learning/tree/master/deepqlearning).

### Q Table

The Q-Table approach achieved the best results. The best model reached an average score of 60. The Q-learning algorithm was able to effectively learn a good policy for playing Snake compared to the other methods.

<img src="https://i.imgur.com/irz0OrQ.gif" width="400" alt="Q Table video">


### Deep Q Learning

The Deep Q-Learning approach achieved worse results, with an average score of 30. Although it was able to learn the game and improve its scores over time, it did not reach the same level of performance as the Q-table approach. This could be due to a number of factors, such as the complexity of the neural network used for training or the hyperparameters selected for the algorithm.

<img src="https://i.imgur.com/q213tjj.gif" width="400" alt="Deep Q video">

### Conclusion 

Overall, it seems that the Q-table approach was the most effective method for playing Snake in this particular implementation, but further experimentation with different algorithms and parameters could lead to improved performance of Deep Q Learning in the future.


## Usage

This project contains 7 runnable files:

1. [manual/manual_snake.py](https://github.com/milankoster/Snake-Q-Learning/blob/master/manual/manual_snake.py): Manually play snake by yourself. See if you can beat the AI's scores!
2. [qlearning/q_trainer.py](https://github.com/milankoster/Snake-Q-Learning/blob/master/qlearning/q_trainer.py): Train your own model using a Q Table. The results are stored in `models/qlearning`. This is required to run the other qlearning scripts. 
3. [qlearning/q_visualiser.py](https://github.com/milankoster/Snake-Q-Learning/blob/master/qlearning/q_visualiser.py): Watch the Q table model play a game of snake. By default, base generation 10000 is shown. 
4. [qlearning/q_replay.py](https://github.com/milankoster/Snake-Q-Learning/blob/master/qlearning/q_replay.py): Watch the Q table model improve over time as it plays multiple games of snake, starting at generation 20.  
5. [deepqlearning/deep_q_trainer.py](https://github.com/milankoster/Snake-Q-Learning/blob/master/deepqlearning/deep_q_trainer.py): Train your own model using deep q learning. By default, the results are stored in `models/deepq_base`. This is required to run the other deep q learning scripts. 
6. [deepqlearning/deep_q_visualiser.py](https://github.com/milankoster/Snake-Q-Learning/blob/master/deepqlearning/deep_q_visualiser.py): Watch the deep neural network play a game of snake. By default, base generation 50 is shown.
7. [deepqlearning/deep_q_environment.py](https://github.com/milankoster/Snake-Q-Learning/blob/master/deepqlearning/deep_q_environment.py): Assess the performance of saved deep q models.

