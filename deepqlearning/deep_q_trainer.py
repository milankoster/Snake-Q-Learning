import gc
import os
import random
from collections import deque

import numpy as np
import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam

from common.direction import Direction
from deepqlearning.deep_q_environment import DeepQEnvironment


class DeepQTrainer:
    def __init__(self):
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.00025
        self.batch_size = 512

        self.episodes = 200
        self.episode_length = 10000

        self.env = DeepQEnvironment()
        self.memory = deque(maxlen=2000)
        self.model = self.create_model()
        self.target_model = self.create_model()

        self.scores = []
        self.rewards = []

    def create_model(self):
        model = Sequential()
        model.add(Dense(128, input_dim=self.env.state_space, activation="relu"))
        model.add(Dense(128, activation="relu"))
        model.add(Dense(128, activation="relu"))
        model.add(Dense(self.env.action_space, activation='softmax'))
        model.compile(loss="mse", optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.env.action_space)
        act_values = self.model.predict(state, verbose=0)
        return np.argmax(act_values[0])

    def remember(self, state, action, reward, new_state, done):
        self.memory.append((state, action, reward, new_state, done))

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma * (np.amax(self.model.predict_on_batch(next_states), axis=1)) * (1 - dones)
        targets_full = self.model.predict_on_batch(states)

        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save_model(self, model_name, episode):
        should_save = False

        if episode < 10:
            should_save = True
        elif 10 <= episode < 200 and episode % 10 == 0:
            should_save = True
        elif episode % 50 == 0:
            should_save = True

        if should_save:
            file_name = f'../models/{model_name}/episode-{episode}.model'
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            self.model.save(f"../models/{model_name}/episode-{episode}.model")

    def save_results(self, model_name):
        df = pd.DataFrame()
        df['Scores'] = self.scores
        df['Reward'] = self.rewards

        df.to_csv(f'results/{model_name}.csv')

    def train(self, model_name):
        for episode in range(1, self.episodes + 1):
            gc.collect()
            self.env = DeepQEnvironment()

            current_state = self.env.get_state()
            current_state = np.reshape(current_state, (1, self.env.state_space))
            epi_reward = 0

            for i in range(self.episode_length):
                action = self.act(current_state)
                new_state, reward, done = self.env.step(Direction(action))
                new_state = np.reshape(new_state, (1, self.env.state_space))
                epi_reward += reward

                self.remember(current_state, action, reward, new_state, done)

                current_state = new_state

                self.replay()

                if done:
                    print(f'episode: {episode}/{self.episodes}, score: {self.env.score}, '
                          f'reward: {epi_reward}, epsilon: {self.epsilon}')
                    self.scores.append(self.env.score)
                    self.rewards.append(epi_reward)

                    self.save_model(model_name, episode)
                    self.save_results(model_name)
                    break


if __name__ == '__main__':
    name = "deepq_base"

    deep_q_trainer = DeepQTrainer()
    deep_q_trainer.train(name)
    deep_q_trainer.save_results(name)
