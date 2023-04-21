import random

import pygame

from common.constants import *
from common.direction import Direction
from common.base_visualiser import BaseVisualiser


class ManualSnake(BaseVisualiser):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption('Manual Snake')

        self.game_open = True
        self.input_direction = None

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

    def show_death_screen(self):
        self.display.fill(BLUE)
        self.message("You Lost! Press Q to Quit or C to Play Again", BLACK)
        self.draw_score(self.score, 5, 5)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game_open = False
                    self.alive = True
                if event.key == pygame.K_c:
                    self.game_loop()

    def message(self, msg, color):
        font_style = pygame.font.SysFont("arial", 30)

        message = font_style.render(msg, True, color)
        self.display.blit(message, [60, DIS_HEIGHT / 3])

    def draw_game(self):
        self.display.fill(BLUE)
        self.draw_food()
        self.draw_snake(self.snake_list)
        self.draw_score(self.score, 5, 5)

        pygame.display.update()
        self.clock.tick(TICK_SPEED)

    def game_loop(self):
        self.reset_game()

        while self.game_open:
            while not self.alive:
                self.show_death_screen()

            for event in pygame.event.get():
                self.handle_input(event)

            self.direction = self.input_direction
            self.move_snake()
            self.eat_food()
            self.handle_tail()

            if self.collision(self.pos_x, self.pos_y):
                self.alive = False

            self.draw_game()

        pygame.quit()
        quit()


if __name__ == '__main__':
    snake = ManualSnake()
    snake.game_loop()
