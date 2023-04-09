from common.constants import MOVE_SPEED
from common.direction import Direction
from snake.base_trainer import BaseTrainer


class DeepQEnvironment(BaseTrainer):

    def __init__(self):
        super().__init__()
        self.state_space = 12
        self.action_space = 4

        self.steps_without_food = 0

    def step(self, action):
        reward = 0
        done = False
        snake_length = self.snake_length()
        self.steps_without_food += 1

        self.handle_action(action)

        self.move_snake()
        if self.eat_food():
            reward = 1
        self.handle_tail()

        if snake_length != self.snake_length():
            self.steps_without_food = 0

        if self.collision(self.pos_x, self.pos_y) or self.steps_without_food == 1000:
            self.alive = False
            done = True
            reward = -10

        return self.get_state(), reward, done

    def get_state(self):
        snake_head_x, snake_head_y = self.pos_x, self.pos_y

        state = [
            int(self.direction == Direction.LEFT),
            int(self.direction == Direction.RIGHT),
            int(self.direction == Direction.UP),
            int(self.direction == Direction.DOWN),
            int(self.is_safe(snake_head_x + MOVE_SPEED, snake_head_y)),
            int(self.is_safe(snake_head_x - MOVE_SPEED, snake_head_y)),
            int(self.is_safe(snake_head_x, snake_head_y + MOVE_SPEED)),
            int(self.is_safe(snake_head_x, snake_head_y - MOVE_SPEED)),
            int(self.food_x > snake_head_x),
            int(self.food_x < snake_head_x),
            int(self.food_y < snake_head_y),
            int(self.food_y > snake_head_y),
        ]

        return state
