# Press the green button in the gutter to run the script.
from q_learner import QLearner

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
