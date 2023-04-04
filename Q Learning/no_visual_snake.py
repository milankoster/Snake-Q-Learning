import random

from Common.constants import *
from Common.direction import Direction


class NoVisualSnake:
    def __init__(self):

        # Game State
        self.input_direction = None
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

    def move_snake(self):
        if self.direction == Direction.LEFT:
            self.pos_x += MOVE_LEFT
        elif self.direction == Direction.RIGHT:
            self.pos_x += MOVE_RIGHT
        elif self.direction == Direction.UP:
            self.pos_y += MOVE_UP
        elif self.direction == Direction.DOWN:
            self.pos_y += MOVE_DOWN

        self.snake_list.append(self.snake_head())

    def collision(self, x, y):
        if x >= DIS_WIDTH or x < 0 or y >= DIS_HEIGHT or y < 0:
            return True

        if [x, y] in self.snake_list[:-1]:
            return True

    def eat_food(self):
        if self.pos_x == self.food_x and self.pos_y == self.food_y:
            self.food_x = round(random.randrange(0, DIS_WIDTH - MOVE_SPEED) / 10.0) * 10.0
            self.food_y = round(random.randrange(0, DIS_HEIGHT - MOVE_SPEED) / 10.0) * 10.0
            self.score += 1
            return True
        return False

    def handle_tail(self):
        if len(self.snake_list) > self.snake_length():
            del self.snake_list[0]

    def snake_head(self):
        return [self.pos_x, self.pos_y]

    def snake_length(self):
        return self.score + 1

    def get_state(self):
        snake_head = self.snake_head()
        snake_head_x, snake_head_y = snake_head[0], snake_head[1]

        state = [
            int(self.direction == Direction.LEFT),
            int(self.direction == Direction.RIGHT),
            int(self.direction == Direction.UP),
            int(self.direction == Direction.DOWN),
            self.is_safe(snake_head_x + 1, snake_head_y),
            self.is_safe(snake_head_x - 1, snake_head_y),
            self.is_safe(snake_head_x, snake_head_y + 1),
            self.is_safe(snake_head_x, snake_head_y - 1),
            int(self.food_x < snake_head_x),
            int(self.food_y < snake_head_y),
            # int(self.food_x > snake_head[0]),
            # int(self.food_y > snake_head[1]),
        ]

        return state

    def is_safe(self, x, y):
        if self.collision(x, y):
            return 0
        return 1

    def step(self, action):
        reward = 0

        if action == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        elif action == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT
        elif action == Direction.UP and self.direction != Direction.DOWN:
            self.input_direction = Direction.UP
        elif action == Direction.DOWN and self.direction != Direction.UP:
            self.input_direction = Direction.DOWN

        self.move_snake()

        if self.collision(self.pos_x, self.pos_y):
            self.alive = False

        if self.eat_food():
            reward = 1

        self.handle_tail()

        if not self.alive:
            reward = -10

        return self.get_state(), reward, self.alive

    # TODO new game run that loops and gets final length
    # def game_loop(self):
    #     while self.alive:
    #         self.step()
    #
    #         self.move_snake()
    #         self.check_collision()
    #
    #         self.eat_food()
    #         self.handle_tail()
    #
    #     quit()

    # TODO: :Load model
    def load_model(self):
        return
