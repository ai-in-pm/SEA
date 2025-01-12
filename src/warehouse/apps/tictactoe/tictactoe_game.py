import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = WINDOW_SIZE // 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LINE_COLOR = (80, 80, 80)

class TicTacToeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Tic Tac Toe')
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False

    def check_winner(self):
        # Check rows
        for row in self.board:
            if row.count(row[0]) == 3 and row[0] != '':
                return row[0]

        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return self.board[0][col]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]

        # Check for tie
        if all(self.board[i][j] != '' for i in range(3) for j in range(3)):
            return 'Tie'

        return None

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                x, y = event.pos
                row = y // GRID_SIZE
                col = x // GRID_SIZE
                if self.board[row][col] == '':
                    self.board[row][col] = self.current_player
                    self.winner = self.check_winner()
                    if self.winner:
                        self.game_over = True
                    else:
                        self.current_player = 'O' if self.current_player == 'X' else 'X'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
        return True

    def draw(self):
        self.screen.fill(WHITE)

        # Draw grid lines
        for i in range(1, 3):
            pygame.draw.line(self.screen, LINE_COLOR,
                           (i * GRID_SIZE, 0),
                           (i * GRID_SIZE, WINDOW_SIZE), 2)
            pygame.draw.line(self.screen, LINE_COLOR,
                           (0, i * GRID_SIZE),
                           (WINDOW_SIZE, i * GRID_SIZE), 2)

        # Draw X's and O's
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 'X':
                    self.draw_x(row, col)
                elif self.board[row][col] == 'O':
                    self.draw_o(row, col)

        if self.game_over:
            font = pygame.font.Font(None, 72)
            if self.winner == 'Tie':
                text = "It's a Tie!"
            else:
                text = f'Player {self.winner} Wins!'
            text_surface = font.render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2))
            self.screen.blit(text_surface, text_rect)

            font = pygame.font.Font(None, 36)
            restart_text = font.render('Press R to Restart', True, BLACK)
            restart_rect = restart_text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2 + 50))
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def draw_x(self, row, col):
        margin = GRID_SIZE // 4
        start_x = col * GRID_SIZE + margin
        start_y = row * GRID_SIZE + margin
        end_x = (col + 1) * GRID_SIZE - margin
        end_y = (row + 1) * GRID_SIZE - margin
        pygame.draw.line(self.screen, BLACK, (start_x, start_y), (end_x, end_y), 3)
        pygame.draw.line(self.screen, BLACK, (start_x, end_y), (end_x, start_y), 3)

    def draw_o(self, row, col):
        center_x = col * GRID_SIZE + GRID_SIZE // 2
        center_y = row * GRID_SIZE + GRID_SIZE // 2
        radius = GRID_SIZE // 3
        pygame.draw.circle(self.screen, BLACK, (center_x, center_y), radius, 3)

    def run(self):
        while True:
            if not self.handle_input():
                break
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = TicTacToeGame()
    game.run()
