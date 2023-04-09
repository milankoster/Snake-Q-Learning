# Press the green button in the gutter to run the script.
from deepqlearning.deep_q_trainer import DeepQTrainer
from manual.manual_snake import ManualSnake
from qlearning.q_trainer import QTrainer
from qlearning.q_visualiser import QVisualiser
from os import listdir

if __name__ == '__main__':
    # # Manual Snake
    # snake = ManualSnake()
    # snake.game_loop()

    # # Q learning (no visualisation)
    # q_trainer = QTrainer()
    # q_trainer.train()

    # # Q Learning Visualisation
    # q_visualiser = QVisualiser()
    # q_visualiser.visualise(10000, True)

    # # Q Learning Visualisation All Runs
    # files = listdir("models/qlearning")
    #
    # episodes = []
    # for file in files:
    #     episodes.append(int(file.split(".")[0]))
    # episodes.sort()
    #
    # for episode in episodes:
    #     q_visualiser = QVisualiser()
    #     q_visualiser.visualise(episode, False)

    # Deep Q Learning
    deep_q_trainer = DeepQTrainer()
    deep_q_trainer.train()
