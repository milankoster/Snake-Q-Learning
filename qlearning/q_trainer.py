import numpy as np

from common.direction import Direction
from snake.base_trainer import BaseTrainer, load_q_table


class QTrainer(BaseTrainer):
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
