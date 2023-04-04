import random

from constants import *
from direction import Direction


class Snake:
    def __init__(self):

        # Game State
        self.alive = True
        self.cause_of_death = None
        self.score = 0

        # Snake
        self.snake_list = []
        self.pos_x = DIS_WIDTH / 2
        self.pos_y = DIS_HEIGHT / 2
        self.direction = None

        # Create first food
        self.food_x = round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
        self.food_y = round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    # TODO: Q Learning Action
    def handle_action(self):
        return

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

    def check_collision(self):
        if self.pos_x >= DIS_WIDTH or self.pos_x < 0 or self.pos_y >= DIS_HEIGHT or self.pos_y < 0:
            self.alive = False
            self.cause_of_death = 'Out of bounds'

        snake_head = [self.pos_x, self.pos_y]
        if snake_head in self.snake_list[:-1]:
            self.alive = False
            self.cause_of_death = 'Hit Tail'

    def handle_food(self):
        if self.pos_x == self.food_x and self.pos_y == self.food_y:
            self.food_x = round(random.randrange(0, DIS_WIDTH - MOVE_SPEED) / 10.0) * 10.0
            self.food_y = round(random.randrange(0, DIS_HEIGHT - MOVE_SPEED) / 10.0) * 10.0
            self.score += 1

    def handle_tail(self):
        snake_length = self.score + 1
        if len(self.snake_list) > snake_length:
            del self.snake_list[0]

    def game_loop(self):
        while self.alive:
            self.handle_action()

            self.move_snake()
            self.check_collision()

            self.handle_food()
            self.handle_tail()

        quit()
