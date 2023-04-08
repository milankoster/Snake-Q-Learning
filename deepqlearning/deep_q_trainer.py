import random
from collections import deque

import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam

from common.direction import Direction
from deepqlearning.deep_q_environment import DeepQEnvironment


class DeepQTrainer:
    def __init__(self):
        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.tau = .125
        self.batch_size = 512

        self.trials = 1000
        self.trial_len = 500

        self.env = DeepQEnvironment()
        self.memory = deque(maxlen=2000)
        self.model = self.create_model()
        self.target_model = self.create_model()

    # TODO Figure out input size
    def create_model(self):
        model = Sequential()
        input_dim = 12
        model.add(Dense(24, input_dim=input_dim, activation="relu"))
        model.add(Dense(48, activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(4))
        model.compile(loss="mean_squared_error", optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            return random.choice([0, 1, 2, 3])

        prediction = self.model.predict(state, verbose=0)
        return np.argmax(prediction[0])

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        samples = random.sample(self.memory, self.batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state, verbose=0)
            if done:
                target[0][action] = reward
            else:
                prediction = self.target_model.predict(new_state, verbose=0)
                q_future = max(prediction[0])
                target[0][action] = reward + q_future * self.gamma
            self.model.fit(state, target, epochs=1, verbose=0)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def save_model(self, fn):
        self.model.save(fn)

    def train(self):
        for trial in range(self.trials):
            self.env = DeepQEnvironment()

            current_state = np.reshape(self.env.get_state(), (1, 12))
            score = 0

            for step in range(self.trial_len):
                action = self.act(current_state)
                new_state, reward, done = self.env.step(Direction(action))
                new_state = np.reshape(new_state, (1, 12))
                score += reward

                self.remember(current_state, action, reward, new_state, done)

                self.replay()  # internally iterates default (prediction) model
                self.target_train()  # iterates target model

                current_state = new_state
                if done:
                    print(f'episode: {trial + 1}/{self.trials}, score: {score + 10}')
                    break

            print("Failed to complete in trial {}".format(trial))
            if trial % 10 == 0:
                self.save_model("models/trial-{}.model".format(trial))
