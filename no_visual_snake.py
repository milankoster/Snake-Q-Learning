import random

from constants import *
from direction import Direction


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

        self.snake_list.append(self.snake_head)

    def check_collision(self):
        if self.pos_x >= DIS_WIDTH or self.pos_x < 0 or self.pos_y >= DIS_HEIGHT or self.pos_y < 0:
            self.alive = False

        if self.snake_head in self.snake_list[:-1]:
            self.alive = False

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
        return

    # def _GetState(self, snake, food):
    #     snake_head = snake[-1]
    #     dist_x = food[0] - snake_head[0]
    #     dist_y = food[1] - snake_head[1]
    #
    #     if dist_x > 0:
    #         pos_x = '1'  # Food is to the right of the snake
    #     elif dist_x < 0:
    #         pos_x = '0'  # Food is to the left of the snake
    #     else:
    #         pos_x = 'NA'  # Food and snake are on the same X file
    #
    #     if dist_y > 0:
    #         pos_y = '3'  # Food is below snake
    #     elif dist_y < 0:
    #         pos_y = '2'  # Food is above snake
    #     else:
    #         pos_y = 'NA'  # Food and snake are on the same Y file
    #
    #     sqs = [
    #         (snake_head[0] - self.block_size, snake_head[1]),
    #         (snake_head[0] + self.block_size, snake_head[1]),
    #         (snake_head[0], snake_head[1] - self.block_size),
    #         (snake_head[0], snake_head[1] + self.block_size),
    #     ]
    #
    #     surrounding_list = []
    #     for sq in sqs:
    #         if sq[0] < 0 or sq[1] < 0:  # off screen left or top
    #             surrounding_list.append('1')
    #         elif sq[0] >= self.display_width or sq[1] >= self.display_height:  # off screen right or bottom
    #             surrounding_list.append('1')
    #         elif sq in snake[:-1]:  # part of tail
    #             surrounding_list.append('1')
    #         else:
    #             surrounding_list.append('0')
    #     surroundings = ''.join(surrounding_list)
    #
    #     return GameState((dist_x, dist_y), (pos_x, pos_y), surroundings, food)
    #
    # def _GetStateStr(self, state):
    #     return str((state.position[0], state.position[1], state.surroundings))

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
        self.check_collision()

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