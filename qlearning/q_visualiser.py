import numpy as np
import pygame

from common.constants import *
from common.direction import Direction
from qlearning.q_environment import QEnvironment
from qlearning.q_loader import load_q_table
from base.base_visualiser import BaseVisualiser


class QVisualiser(BaseVisualiser, QEnvironment):
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

    def visualise(self, episode, quit_game):
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

            if steps_without_food == 200:
                break

            self.draw_game(episode)

        if quit_game:
            pygame.quit()

        return self.snake_length()


if __name__ == '__main__':
    q_visualiser = QVisualiser()
    q_visualiser.visualise(10000, True)
