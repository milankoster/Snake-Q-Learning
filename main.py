# Press the green button in the gutter to run the script.
from common.direction import Direction
from manual.manual_snake import ManualSnake
from qlearning.snake_trainer import SnakeTrainer
from qlearning.q_learner import QLearner
from qlearning.auto_snake_visualiser import AutoSnakeVisualiser

if __name__ == '__main__':

    q_learner = QLearner()
    q_learner.train()

    # # Manual Snake
    # snake = ManualSnake()
    # snake.game_loop()

    # # Snake Visualisation
    # visual_snake = AutoSnakeVisualiser()
    # visual_snake.run_game(10000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
