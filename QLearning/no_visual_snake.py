import numpy as np
import random
import pickle

from Common.constants import *
from Common.direction import Direction


class NoVisualSnake:
    def __init__(self):
        # Game State
        self.alive = True
        self.alive_duration = 0
        self.score = 0

        # Snake
        self.snake_list = []
        self.pos_x = DIS_WIDTH / 2
        self.pos_y = DIS_HEIGHT / 2
        self.direction = None

        # Create first food
        self.food_x = round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
        self.food_y = round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    def handle_action(self, action):
        if action == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        elif action == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT
        elif action == Direction.UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        elif action == Direction.DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN

    def move_snake(self):
        if self.direction == Direction.LEFT:
            self.pos_x += MOVE_LEFT
        elif self.direction == Direction.RIGHT:
            self.pos_x += MOVE_RIGHT
        elif self.direction == Direction.UP:
            self.pos_y += MOVE_UP
        elif self.direction == Direction.DOWN:
            self.pos_y += MOVE_DOWN

        self.snake_list.append(self.snake_head())

    def eat_food(self):
        if self.pos_x == self.food_x and self.pos_y == self.food_y:
            self.food_x = round(random.randrange(0, DIS_WIDTH - MOVE_SPEED) / 10.0) * 10.0
            self.food_y = round(random.randrange(0, DIS_HEIGHT - MOVE_SPEED) / 10.0) * 10.0
            self.score += 1
            return True
        return False

    def handle_tail(self):
        if len(self.snake_list) > self.snake_length():
            del self.snake_list[0]

    def collision(self, x, y):
        if x >= DIS_WIDTH or x < 0 or y >= DIS_HEIGHT or y < 0:
            return True

        if [x, y] in self.snake_list[:-1]:
            return True

    def get_state(self):
        snake_head = self.snake_head()
        snake_head_x, snake_head_y = snake_head[0], snake_head[1]

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

    def snake_head(self):
        return [self.pos_x, self.pos_y]

    def snake_length(self):
        return self.score + 1

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
