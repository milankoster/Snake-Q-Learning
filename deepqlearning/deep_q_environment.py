import math

from common.constants import MOVE_SPEED
from common.direction import Direction
from snake.base_trainer import BaseTrainer


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

        # Euclidean distance between the snake's head and the food
        food_distance = math.sqrt((self.pos_x - self.food_x) ** 2 + (self.pos_y - self.food_y) ** 2)
        food_angle = math.atan2(self.food_y - self.pos_y, self.food_x - self.pos_x)

        state = [
            int(self.direction == Direction.LEFT),
            int(self.direction == Direction.RIGHT),
            int(self.direction == Direction.UP),
            int(self.direction == Direction.DOWN),
            int(self.is_safe(snake_head_x + MOVE_SPEED, snake_head_y)),
            int(self.is_safe(snake_head_x - MOVE_SPEED, snake_head_y)),
            int(self.is_safe(snake_head_x, snake_head_y + MOVE_SPEED)),
            int(self.is_safe(snake_head_x, snake_head_y - MOVE_SPEED)),
            food_distance,
            food_angle,
        ]

        return state
