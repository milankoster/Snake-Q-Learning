﻿import math

from common.constants import *
from common.direction import Direction
from snake.base_trainer import BaseTrainer


def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    # return math.sqrt((self.pos_x - self.food_x) ** 2 + (self.pos_y - self.food_y) ** 2)


class DeepQEnvironment(BaseTrainer):

    def __init__(self):
        super().__init__()
        self.state_space = 23
        self.action_space = 4

    def manhattan_distance(self):
        return abs(self.pos_x - self.food_x) + abs(self.pos_y - self.food_y)

    def step(self, action):
        prev_distance = self.manhattan_distance()
        reward = -1
        done = False

        self.handle_action(action)

        self.move_snake()

        new_distance = self.manhattan_distance()
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
        normalised_food_distance = euclidean_distance(self.pos_x, self.pos_y, self.food_x, self.food_y) / MAX_DISTANCE
        food_angle = math.atan2(self.food_y - self.pos_y, self.food_x - self.pos_x)
        normalised_food_angle = (food_angle + math.pi) / (2 * math.pi)

        normalised_position_x = self.pos_x / DIS_WIDTH
        normalised_position_y = self.pos_y / DIS_HEIGHT
        normalised_food_x = self.food_x / DIS_WIDTH
        normalised_food_y = self.food_y / DIS_HEIGHT

        normalised_snake_length = self.snake_length() * BLOCK_SIZE / DIS_SURFACE

        state = [
            int(self.direction == Direction.LEFT),
            int(self.direction == Direction.RIGHT),
            int(self.direction == Direction.UP),
            int(self.direction == Direction.DOWN),
            int(self.is_safe(self.pos_x + MOVE_SPEED, self.pos_y)),
            int(self.is_safe(self.pos_x - MOVE_SPEED, self.pos_y)),
            int(self.is_safe(self.pos_x, self.pos_y + MOVE_SPEED)),
            int(self.is_safe(self.pos_x, self.pos_y - MOVE_SPEED)),
            normalised_position_x,
            normalised_position_y,
            normalised_food_x,
            normalised_food_y,
            normalised_food_distance,
            normalised_food_angle,
            normalised_snake_length,
            self.ray_cast(0, MOVE_UP),
            self.ray_cast(MOVE_RIGHT, MOVE_UP),
            self.ray_cast(MOVE_RIGHT, 0),
            self.ray_cast(MOVE_RIGHT, MOVE_DOWN),
            self.ray_cast(0, MOVE_DOWN),
            self.ray_cast(MOVE_LEFT, MOVE_DOWN),
            self.ray_cast(MOVE_LEFT, 0),
            self.ray_cast(MOVE_LEFT, MOVE_UP),
        ]

        return state

    def ray_cast(self, x_dir, y_dir):
        ray_x, ray_y = self.pos_x, self.pos_y

        while True:
            ray_x += x_dir
            ray_y += y_dir

            if self.collision(ray_x, ray_y):
                return euclidean_distance(self.pos_x, self.pos_y, ray_x, ray_y) / MAX_DISTANCE
