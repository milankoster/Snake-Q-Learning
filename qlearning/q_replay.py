from os import listdir

from qlearning.q_visualiser import QVisualiser

if __name__ == '__main__':
    files = listdir("../models/qlearning")

    episodes = []
    for file in files:
        episodes.append(int(file.split(".")[0]))
    episodes.sort()

    for episode in episodes:
        q_visualiser = QVisualiser()
        q_visualiser.visualise(episode, False)
