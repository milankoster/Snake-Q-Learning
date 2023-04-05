﻿import random

import pygame

from common.direction import Direction
from common.constants import *


class ManualSnake:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Manual Snake')

        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
        self.score_font = pygame.font.SysFont("arial", 25)

        # Game State
        self.game_open = True
        self.alive = True
        self.score = 0

        # Snake
        self.snake_list = []
        self.pos_x = DIS_WIDTH / 2
        self.pos_y = DIS_HEIGHT / 2
        self.input_direction = None
        self.direction = None

        # Create first food
        self.food_x = round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
        self.food_y = round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    def handle_input(self, event):
        if event.type == pygame.QUIT:
            self.game_open = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                self.input_direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                self.input_direction = Direction.RIGHT
            elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                self.input_direction = Direction.UP
            elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                self.input_direction = Direction.DOWN

    def move_snake(self):
        self.direction = self.input_direction

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

    def check_collision(self):
        if self.pos_x >= DIS_WIDTH or self.pos_x < 0 or self.pos_y >= DIS_HEIGHT or self.pos_y < 0:
            self.alive = False

        snake_head = [self.pos_x, self.pos_y]
        if snake_head in self.snake_list[:-1]:
            self.alive = False

    def handle_food(self):
        if self.pos_x == self.food_x and self.pos_y == self.food_y:
            self.food_x = round(random.randrange(0, DIS_WIDTH - MOVE_SPEED) / 10.0) * 10.0
            self.food_y = round(random.randrange(0, DIS_HEIGHT - MOVE_SPEED) / 10.0) * 10.0
            self.score += 1

    def handle_tail(self):
        if len(self.snake_list) > self.snake_length():
            del self.snake_list[0]

    def snake_length(self):
        return self.score + 1

    def draw_score(self, score):
        value = self.score_font.render(f"Score: {score}", True, WHITE)
        self.display.blit(value, [5, 5])

    def draw_snake(self, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.display, BLACK, [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])

    def draw_food(self):
        pygame.draw.rect(self.display, RED, [self.food_x, self.food_y, BLOCK_SIZE, BLOCK_SIZE])

    def message(self, msg, color):
        font_style = pygame.font.SysFont(None, 30)

        message = font_style.render(msg, True, color)
        self.display.blit(message, [DIS_WIDTH / 3, DIS_HEIGHT / 3])

    def reset_game(self):
        self.game_open = True
        self.alive = True
        self.score = 0

        self.snake_list = []
        self.pos_x = DIS_WIDTH / 2
        self.pos_y = DIS_HEIGHT / 2
        self.input_direction = None
        self.direction = None

        self.food_x = round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
        self.food_y = round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    def game_loop(self):
        self.reset_game()

        while self.game_open:
            while not self.alive:
                self.display.fill(WHITE)
                self.message("You Lost! Press Q-Quit or C-Play Again", BLACK)
                self.draw_score(self.score)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.game_open = False
                            self.alive = True
                        if event.key == pygame.K_c:
                            self.game_loop()

            for event in pygame.event.get():
                self.handle_input(event)

            self.move_snake()
            self.handle_food()
            self.handle_tail()

            self.check_collision()

            self.display.fill(BLUE)
            self.draw_food()
            self.draw_snake(self.snake_list)
            self.draw_score(self.score)
            pygame.display.update()

            self.clock.tick(TICK_SPEED)

        pygame.quit()
        quit()