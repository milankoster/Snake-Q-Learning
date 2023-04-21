import os

import keras.models
import numpy as np
import pandas as pd

from common.constants import MOVE_SPEED
from common.direction import Direction
from common.base_trainer import BaseTrainer


class DeepQEnvironment(BaseTrainer):

    def __init__(self):
        super().__init__()
        self.state_space = 12
        self.action_space = 4

    def measure_distance(self):
        return abs(self.pos_x - self.food_x) + abs(self.pos_y - self.food_y)

    def step(self, action):
        prev_distance = self.measure_distance()
        reward = -1
        done = False

        self.handle_action(action)

        self.move_snake()

        new_distance = self.measure_distance()
        if new_distance < prev_distance:
            reward = 1

        if self.eat_food():
            reward = 10
        self.handle_tail()

        if self.collision(self.pos_x, self.pos_y):
            self.alive = False
            done = True
            reward = -100

        return self.get_state(), reward, done

    def get_state(self):
        snake_head_x, snake_head_y = self.pos_x, self.pos_y

        state = [
            int(self.direction == Direction.LEFT),
            int(self.direction == Direction.RIGHT),
            int(self.direction == Direction.UP),
            int(self.direction == Direction.DOWN),
            int(self.is_safe(snake_head_x + MOVE_SPEED, snake_head_y)),
            int(self.is_safe(snake_head_x - MOVE_SPEED, snake_head_y)),
            int(self.is_safe(snake_head_x, snake_head_y + MOVE_SPEED)),
            int(self.is_safe(snake_head_x, snake_head_y - MOVE_SPEED)),
            int(self.food_x > snake_head_x),
            int(self.food_x < snake_head_x),
            int(self.food_y < snake_head_y),
            int(self.food_y > snake_head_y),
        ]

        return state

    def run_game(self, model):

        length = self.snake_length()
        steps_without_food = 0

        while self.alive:
            state = self.get_state()
            state = np.reshape(state, (1, self.state_space))

            action_index = np.argmax(model.predict(state, verbose=0)[0])
            action = Direction(action_index)
            self.step(action)

            if self.snake_length() != length:
                steps_without_food = 0
                length = self.snake_length()
            else:
                steps_without_food += 1

            if steps_without_food == 1000:
                break

        return self.snake_length()


if __name__ == '__main__':
    directory = '../models/deepq_base'
    models = os.listdir(directory)

    scores = []

    for model_count in range(1, 101):
        if model_count > 10 and model_count % 10 != 0:
            continue

        model = keras.models.load_model(f"{directory}/episode-{model_count}.model")

        env = DeepQEnvironment()
        score = env.run_game(model)
        scores.append([model_count, score])
        print(f"Score of model {model_count}: {score}")

    df = pd.DataFrame(data=scores)
    df.to_csv("base_deepq_results")
