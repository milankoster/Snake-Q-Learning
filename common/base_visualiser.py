import pygame

from common.constants import *
from common.base_snake import BaseSnake


class BaseVisualiser(BaseSnake):
    def __init__(self):
        super().__init__()
        pygame.init()

        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
        self.score_font = pygame.font.SysFont("arial", 25)

    def draw_score(self, score, x, y):
        value = self.score_font.render(f"Score: {score}", True, WHITE)
        self.display.blit(value, [x, y])

    def draw_episode(self, epi, x, y):
        value = self.score_font.render(f"Gen: {epi}", True, WHITE)
        self.display.blit(value, [x, y])

    def draw_snake(self, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.display, BLACK, [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])

    def draw_food(self):
        pygame.draw.rect(self.display, RED, [self.food_x, self.food_y, BLOCK_SIZE, BLOCK_SIZE])