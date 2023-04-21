import numpy as np
import pygame
import tensorflow as tf

from common.constants import *
from common.direction import Direction
from deepqlearning.deep_q_environment import DeepQEnvironment
from snake.base_visualiser import BaseVisualiser


class DeepQVisualiser(BaseVisualiser, DeepQEnvironment):
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

    def visualise(self, path, episode, quit_game):
        model = tf.keras.models.load_model(path + f"episode-{episode}.model")

        length = self.snake_length()
        steps_without_food = 0

        while self.alive:
            state = np.reshape(self.get_state(), (1, self.state_space))

            act_values = model.predict(state, verbose=0)
            action_index = np.argmax(act_values[0])
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

        if quit_game:
            pygame.quit()

        return self.snake_length()


if __name__ == '__main__':
    path = "../models/deepq_continuous/"
    deep_q_visualiser = DeepQVisualiser()
    deep_q_visualiser.visualise(path, 290, True)
