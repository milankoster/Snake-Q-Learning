import numpy as np
import random
import pickle

from direction import Direction
from no_visual_snake import NoVisualSnake


class QLearner:
    def __init__(self):
        self.discount_rate = 0.95
        self.learning_rate = 0.01
        self.eps = 1.0
        self.eps_discount = 0.9992
        self.min_eps = 0.001
        self.num_episodes = 10000

        self.env = NoVisualSnake()
        self.q_table = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4))
        self.score = []
        self.survived = []

    # epsilon-greedy action choice
    def get_action(self, state):
        # select random action (exploration)
        if random.random() < self.eps:
            return random.choice([Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN])

        # select best action (exploitation)
        return np.argmax(self.q_table[state])

    def print_update(self, episode):
        if episode % 25 == 0:
            print(
                f"Episodes: {episode}, score: {np.mean(self.score)}, survived: {np.mean(self.survived)},"
                f" eps: {self.eps}, lr: {self.learning_rate}")
            self.score = []
            self.survived = []

    def save_model(self, episode):
        if episode % 500 == 0:
            with open(f'pickle/{episode}.pickle', 'wb') as file:
                pickle.dump(self.q_table, file)

    def train(self):
        for episode in range(1, self.num_episodes + 1):
            steps_without_food = 0

            self.env = NoVisualSnake()
            self.eps = max(self.eps * self.eps_discount, self.min_eps)

            self.print_update(episode)
            self.save_model(episode)

            snake_length = self.env.snake_length()
            current_state = self.env.get_state()

            done = False
            while not done:
                # choose action and take it
                action = self.get_action(current_state)
                new_state, reward, done = self.env.step(action)

                # Bellman Equation Update
                self.q_table[current_state][action] = (1 - self.learning_rate) \
                                                      * self.q_table[current_state][action] + self.learning_rate \
                                                      * (reward + self.discount_rate * max(self.q_table[new_state]))
                current_state = new_state

                steps_without_food += 1
                if snake_length != self.env.snake_length:
                    snake_length = self.env.snake_length
                    steps_without_food = 0

                if steps_without_food == 1000:
                    break

            # keep track of important metrics
            self.score.append(self.env.snake_length() - 1)
            self.survived.append(self.env.alive)