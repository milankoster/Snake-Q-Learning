# Press the green button in the gutter to run the script.
from manual.manual_snake import ManualSnake
from qlearning.q_learner import QLearner
from qlearning.q_visualiser import AutoSnakeVisualiser

if __name__ == '__main__':
    # # Manual Snake
    # snake = ManualSnake()
    # snake.game_loop()

    # # Q learning (no visualisation)
    # q_learner = QLearner()
    # q_learner.train()

    # Q Learning Visualisation
    visual_snake = AutoSnakeVisualiser()
    visual_snake.run_game(10000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
