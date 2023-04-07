from common.constants import MOVE_SPEED
from common.direction import Direction
from snake.base_trainer import BaseTrainer


class DeepQEnvironment(BaseTrainer):

    def step(self, action):
        reward = 0

        self.handle_action(action)

        self.move_snake()
        if self.eat_food():
            reward = 1
        self.handle_tail()

        if self.collision(self.pos_x, self.pos_y):
            self.alive = False
            reward = -10

        done = not self.alive

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
