import numpy as np

from common.constants import MOVE_SPEED
from common.direction import Direction
from snake.base_trainer import BaseTrainer, load_q_table


class QEnvironment(BaseTrainer):
    def __init__(self):
        super().__init__()
        self.alive_duration = 0

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

        return tuple(state)

    def run_game(self, episode):
        q_table = load_q_table(episode)

        length = self.snake_length()
        steps_without_food = 0

        while self.alive:
            state = self.get_state()

            action_index = np.argmax(q_table[state])
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
