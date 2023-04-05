import pickle
import random
import numpy as np

import pygame

from common.constants import *
from common.direction import Direction


class VisualSnake:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake with Q Learning')

        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
        self.score_font = pygame.font.SysFont("arial", 35)

        # Game State
        self.alive = True
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

        snake_head = [self.pos_x, self.pos_y]
        self.snake_list.append(snake_head)

    def eat_food(self):
        if self.pos_x == self.food_x and self.pos_y == self.food_y:
            self.food_x = round(random.randrange(0, DIS_WIDTH - MOVE_SPEED) / 10.0) * 10.0
            self.food_y = round(random.randrange(0, DIS_HEIGHT - MOVE_SPEED) / 10.0) * 10.0
            self.score += 1

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

    def draw_score(self, score):
        value = self.score_font.render(f"Score: {score}", True, WHITE)
        self.display.blit(value, [5, 5])

    def draw_episode(self, epi):
        value = self.score_font.render(f"Episode: {epi}", True, WHITE)
        self.display.blit(value, [5, 30])

    def draw_snake(self, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.display, BLACK, [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])

    def draw_food(self):
        pygame.draw.rect(self.display, RED, [self.food_x, self.food_y, BLOCK_SIZE, BLOCK_SIZE])

    def render_game(self, episode):
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

            self.display.fill(BLUE)
            self.draw_food()
            self.draw_snake(self.snake_list)
            self.draw_score(self.score)
            pygame.display.update()

            self.clock.tick(TICK_SPEED)

        pygame.quit()

        return self.snake_length()
