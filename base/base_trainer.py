from common.direction import Direction
from base.base_snake import BaseSnake


class BaseTrainer(BaseSnake):
    def __init__(self):
        super().__init__()

    def handle_action(self, action):
        if action != Direction.LEFT and action != Direction.RIGHT and action != Direction.UP and action != Direction.DOWN:
            raise Exception('Invalid action')
        if action == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        elif action == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT
        elif action == Direction.UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        elif action == Direction.DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN

    def is_safe(self, x, y):
        if self.collision(x, y):
            return False
        return True
