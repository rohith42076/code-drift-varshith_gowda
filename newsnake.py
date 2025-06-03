# snake.py
import pygame

class Snake:
    def __init__(self, block_size, screen_width, screen_height):
        self.block_size = block_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.direction = "RIGHT"
        self.body = [(screen_width // 2, screen_height // 2)]
        self.color = (0, 255, 0)
        self.change_to = self.direction
        self.grow_pending = False
        self.speed = 1

    def set_direction(self, direction):
        """Avoid reversing direction"""
        opposites = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }
        if direction != opposites.get(self.direction):
            self.change_to = direction

    def move(self):
        """Move the snake based on direction"""
        self.direction = self.change_to
        head_x, head_y = self.body[0]

        if self.direction == "UP":
            head_y -= self.block_size
        elif self.direction == "DOWN":
            head_y += self.block_size
        elif self.direction == "LEFT":
            head_x -= self.block_size
        elif self.direction == "RIGHT":
            head_x += self.block_size

        new_head = (head_x, head_y)
        self.body.insert(0, new_head)

        if self.grow_pending:
            self.grow_pending = False
        else:
            self.body.pop()

    def grow(self):
        self.grow_pending = True

    def draw(self, screen):
        for i, segment in enumerate(self.body):
            color = (0, 200, 0) if i == 0 else self.color
            pygame.draw.rect(screen, color, pygame.Rect(segment[0], segment[1], self.block_size, self.block_size))

    def reset(self):
        self.body = [(self.screen_width // 2, self.screen_height // 2)]
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.grow_pending = False

    def get_head_position(self):
        return self.body[0]

        def get_body(self):
        return self.body

    def length(self):
        return len(self.body)

    def increase_speed(self, factor=0.2):
        self.speed += factor

    def get_speed(self):
        return self.speed

    def hit_wall(self):
        head_x, head_y = self.body[0]
        return (
            head_x < 0 or head_x >= self.screen_width or
            head_y < 0 or head_y >= self.screen_height
        )

    def hit_self(self):
        return self.body[0] in self.body[1:]
# food.py
import pygame
import random

class Food:
    def __init__(self, block_size, screen_width, screen_height):
        self.block_size = block_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.types = {
            "normal": (255, 0, 0),     # red
            "special": (255, 255, 0),  # yellow
        }
        self.position = self.generate_position()
        self.type = "normal"
        self.spawn_timer = 0
        self.special_food_duration = 100  # frames

    def generate_position(self):
        """Generate a grid-aligned position within bounds"""
        x = random.randint(0, (self.screen_width - self.block_size) // self.block_size) * self.block_size
        y = random.randint(0, (self.screen_height - self.block_size) // self.block_size) * self.block_size
        return (x, y)

    def spawn(self, is_special=False):
        self.position = self.generate_position()
        self.type = "special" if is_special else "normal"
        self.spawn_timer = 0

    def draw(self, screen):
        color = self.types.get(self.type, (255, 0, 0))
        pygame.draw.rect(screen, color, pygame.Rect(self.position[0], self.position[1], self.block_size, self.block_size))

    def update(self):
        if self.type == "special":
            self.spawn_timer += 1
            if self.spawn_timer > self.special_food_duration:
                self.spawn(False)

    def check_collision(self, snake_head):
        return snake_head == self.position

    def get_type(self):
        return self.type

    def get_position(self):
        return self.position

    def get_color(self):
        return self.types.get(self.type, (255, 0, 0))

    def is_special(self):
        return self.type == "special"

    def set_special_timer(self, duration):
        self.special_food_duration = duration

    def despawn(self):
        """For example, if special food expires without being eaten"""
        self.type = "normal"
        self.spawn()

# Example usage:
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    clock = pygame.time.Clock()
    food = Food(20, 400, 300)

    running = True
    while running:
        screen.fill((0, 0, 0))
        food.update()
        food.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(10)

    pygame.quit()
# collision.py

class CollisionHandler:
    def _init_(self, screen_width, screen_height, block_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size
        self.boundary_mode = "solid"  # can be "solid" or "wrap"
        self.obstacles = []

    def check_wall_collision(self, snake):
        """Detect if snake hits wall (if solid wall enabled)"""
        head_x, head_y = snake.get_head_position()
        if self.boundary_mode == "solid":
            return (
                head_x < 0 or
                head_x >= self.screen_width or
                head_y < 0 or
                head_y >= self.screen_height
            )
        return False

    def handle_wall_wrap(self, snake):
        """Wrap around screen edges (for wrap mode)"""
        head_x, head_y = snake.get_head_position()
        if head_x < 0:
            head_x = self.screen_width - self.block_size
        elif head_x >= self.screen_width:
            head_x = 0
        if head_y < 0:
            head_y = self.screen_height - self.block_size
        elif head_y >= self.screen_height:
            head_y = 0

        # Set wrapped head position
        body = snake.get_body()
        body[0] = (head_x, head_y)
        snake.body = body

    def check_self_collision(self, snake):
        """Detect if the head collides with its own body"""
        head = snake.get_head_position()
        return head in snake.get_body()[1:]

    def toggle_boundary_mode(self):
        """Toggle between wrap and solid wall"""
        self.boundary_mode = "wrap" if self.boundary_mode == "solid" else "solid"

    def add_obstacle(self, position):
        """Add a static obstacle"""
        self.obstacles.append(position)

    def clear_obstacles(self):
        self.obstacles = []

    def draw_obstacles(self, screen, color=(100, 100, 100)):
        import pygame
        for pos in self.obstacles:
            pygame.draw.rect(screen, color, (*pos, self.block_size, self.block_size))

    def check_obstacle_collision(self, snake):
        return snake.get_head_position() in self.obstacles

    def is_game_over(self, snake):
        """Combined check for wall, self, and obstacles"""
        return (
            self.check_wall_collision(snake)
            or self.check_self_collision(snake)
            or self.check_obstacle_collision(snake)
        )

    def get_boundary_mode(self):
        return self.boundary_mode

# Sample test
if _name_ == "_main_":
    from snake import Snake
    snake = Snake(20, 400, 300)
    collision = CollisionHandler(400, 300, 20)

    # Simulate self-collision
    snake.body = [(100, 100), (80, 100), (60, 100), (100, 100)]  # intentional collision
    print("Self collision?", collision.check_self_collision(snake))  # True

    # Simulate wall collision
    snake.body = [(-20, 100)]
    print("Wall collision?", collision.check_wall_collision(snake))  # True
