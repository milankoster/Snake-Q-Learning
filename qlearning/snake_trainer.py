import pickle

import numpy as np

from common.constants import *
from common.direction import Direction
from snake.base_snake import BaseSnake


class SnakeTrainer(BaseSnake):
    def __init__(self):
        super().__init__()
        self.alive_duration = 0

    def handle_action(self, action):
        if action == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        elif action == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT
        elif action == Direction.UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        elif action == Direction.DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN

    def get_state(self):
        snake_head_x, snake_head_y = self.pos_x, self.pos_y

        state = [
            int(self.direction == Direction.LEFT),
            int(self.direction == Direction.RIGHT),
            int(self.direction == Direction.UP),
            int(self.direction == Direction.DOWN),
            int(self.is_safe(snake_head_x + 1, snake_head_y)),
            int(self.is_safe(snake_head_x - 1, snake_head_y)),
            int(self.is_safe(snake_head_x, snake_head_y + 1)),
            int(self.is_safe(snake_head_x, snake_head_y - 1)),
            int(self.food_x < snake_head_x),
            int(self.food_y < snake_head_y),
            int(self.food_x > snake_head_x),
            int(self.food_y > snake_head_y),
        ]

        return tuple(state)

    def is_safe(self, x, y):
        if self.collision(x, y):
            return False
        return True

    def step(self, action):
        reward = 0

        self.handle_action(action)

        self.move_snake()
        if self.eat_food():
            reward = 1
        self.handle_tail()

        if self.collision(self.pos_x, self.pos_y):
            self.alive = False
            reward = -10
        else:
            self.alive_duration += 1

        return self.get_state(), reward, self.alive

    def run_game(self, episode):
        filename = f"pickle/qlearning/{episode}.pickle"
        with open(filename, 'rb') as file:
            q_table = pickle.load(file)

        length = self.snake_length()
        steps_without_food = 0

        while self.alive:
            state = self.get_state()

            action = np.argmax(q_table[state])
            action = Direction(action)
            self.step(action)

            if self.snake_length() != length:
                steps_without_food = 0
                length = self.snake_length()
            else:
                steps_without_food += 1

            if steps_without_food == 1000:
                break

        return self.snake_length()
