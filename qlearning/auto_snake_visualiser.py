import pickle

import numpy as np
import pygame

from common.constants import *
from common.direction import Direction
from snake.snake_visualiser import SnakeVisualiser


class AutoSnakeVisualiser(SnakeVisualiser):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption('Snake with Q Learning')

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

    def draw_episode(self, epi, x, y):
        value = self.score_font.render(f"Gen: {epi}", True, WHITE)
        self.display.blit(value, [x, y])

    def draw_game(self, episode):
        self.display.fill(BLUE)
        self.draw_food()
        self.draw_snake(self.snake_list)
        self.draw_score(self.score, 5, 30)
        self.draw_episode(episode, 5, 5)

        pygame.display.update()
        self.clock.tick(TICK_SPEED)

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
