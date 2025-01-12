import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.snake = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = (1, 0)
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False

    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
            if food not in self.snake:
                return food

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != (0, 1):
                    self.direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                    self.direction = (0, 1)
                elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                    self.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                    self.direction = (1, 0)
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
        return True

    def update(self):
        if self.game_over:
            return

        # Move snake
        new_head = (
            (self.snake[0][0] + self.direction[0]) % GRID_COUNT,
            (self.snake[0][1] + self.direction[1]) % GRID_COUNT
        )

        # Check collision with self
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Check if food eaten
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill(BLACK)

        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN,
                           (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE,
                            GRID_SIZE - 2, GRID_SIZE - 2))

        # Draw food
        pygame.draw.rect(self.screen, RED,
                        (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE,
                         GRID_SIZE - 2, GRID_SIZE - 2))

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = font.render('Game Over! Press R to Restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        while True:
            if not self.handle_input():
                break
            self.update()
            self.draw()
            self.clock.tick(10)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = SnakeGame()
    game.run()
