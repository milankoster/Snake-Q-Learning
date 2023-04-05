import pickle

import numpy as np
import pygame

from common.constants import *
from common.direction import Direction
from snake.base_trainer import BaseTrainer, load_q_table
from snake.base_visualiser import BaseVisualiser


class AutoSnakeVisualiser(BaseVisualiser, BaseTrainer):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption('Snake with Q Learning')

    def draw_game(self, episode):
        self.display.fill(BLUE)
        self.draw_food()
        self.draw_snake(self.snake_list)
        self.draw_score(self.score, 5, 30)
        self.draw_episode(episode, 5, 5)

        pygame.display.update()
        self.clock.tick(TICK_SPEED)

    def run_game(self, episode):
        q_table = load_q_table(episode)

        length = self.snake_length()
        steps_without_food = 0

        while self.alive:
            state = self.get_state()

            action_index = np.argmax(q_table[state])
            action = Direction(action_index)
            self.handle_action(action)

            self.move_snake()
            self.eat_food()
            self.handle_tail()

            if self.collision(self.pos_x, self.pos_y):
                self.alive = False

            if self.snake_length() != length:
                steps_without_food = 0
                length = self.snake_length()
            else:
                steps_without_food += 1

            if steps_without_food == 1000:
                break

            self.draw_game(episode)

        pygame.quit()

        return self.snake_length()
