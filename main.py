# Press the green button in the gutter to run the script.
from Common.direction import Direction
from Manual.manual_snake import ManualSnake
from QLearning.q_learner import QLearner

if __name__ == '__main__':
    q_learner = QLearner()
    q_learner.train()
    
    # snake = ManualSnake()
    # snake.game_loop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
