import numpy as np
import random
import pickle

from common.direction import Direction
from qlearning.q_environment import QEnvironment


class QLearner:
    def __init__(self):
        self.discount_rate = 0.95
        self.learning_rate = 0.01
        self.eps = 1.0
        self.eps_discount = 0.9992
        self.min_eps = 0.001
        self.num_episodes = 10000

        self.env = QEnvironment()
        self.q_table = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4))
        self.score = []
        self.survived = []

    # epsilon-greedy action choice
    def get_action(self, state):
        # select random action (exploration)
        if random.random() < self.eps:
            return random.choice([0, 1, 2, 3])

        # select best action (exploitation)
        return np.argmax(self.q_table[state])

    def print_update(self, episode):
        if episode % 100 == 0:
            print(
                f"Episodes: {episode}. Average score: {np.mean(self.score[-100:])}, "
                f"Max Score: {np.max(self.score[-100:])}. Survival duration: {np.mean(self.survived[-100:])}."
                f" eps: {self.eps}")
            self.score = []
            self.survived = []

    def save_model(self, episode):
        should_save = False

        if episode < 100 and episode % 20 == 0:
            should_save = True
        if 100 <= episode < 500 and episode % 50 == 0:
            should_save = True
        elif 500 <= episode < 1000 and episode % 100 == 0:
            should_save = True
        elif episode >= 1000 and episode % 500 == 0:
            should_save = True

        if should_save:
            with open(f'pickle/qlearning/{episode}.pickle', 'wb') as file:
                pickle.dump(self.q_table, file)

    def train(self):
        for episode in range(1, self.num_episodes + 1):
            self.env = QEnvironment()

            self.print_update(episode)
            self.save_model(episode)

            steps_without_food = 0
            snake_length = self.env.snake_length()
            current_state = self.env.get_state()
            self.eps = max(self.eps * self.eps_discount, self.min_eps)

            alive = True
            while alive:
                # choose action and take it
                action = self.get_action(current_state)

                new_state, reward, alive = self.env.step(Direction(action))

                # Bellman Equation Update
                self.q_table[current_state][action] = (1 - self.learning_rate) \
                                                      * self.q_table[current_state][action] + self.learning_rate \
                                                      * (reward + self.discount_rate * max(self.q_table[new_state]))
                current_state = new_state

                steps_without_food += 1
                if snake_length != self.env.snake_length():
                    snake_length = self.env.snake_length()
                    steps_without_food = 0

                if steps_without_food == 1000:
                    break

            # keep track of important metrics
            self.score.append(self.env.snake_length() - 1)
            self.survived.append(self.env.alive_duration)
