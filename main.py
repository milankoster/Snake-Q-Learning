# Press the green button in the gutter to run the script.
from manual.manual_snake import ManualSnake
from qlearning.q_trainer import QTrainer
from qlearning.q_visualiser import AutoSnakeVisualiser
from os import listdir

if __name__ == '__main__':
    # # Manual Snake
    # snake = ManualSnake()
    # snake.game_loop()

    # Q learning (no visualisation)
    q_learner = QTrainer()
    q_learner.train()

    # # Q Learning Visualisation
    # visual_snake = AutoSnakeVisualiser()
    # visual_snake.run_game(500, True)

    # # Q Learning Visualisation All Runs
    # files = listdir("pickle/qlearning")
    # 
    # episodes = []
    # for file in files:
    #     episodes.append(int(file.split(".")[0]))
    # episodes.sort()
    # 
    # visual_snake = AutoSnakeVisualiser()
    # for episode in episodes:
    #     visual_snake = AutoSnakeVisualiser()
    #     visual_snake.run_game(episode, False)
