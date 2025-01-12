import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

class CheckersGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Checkers')
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.selected_piece = None
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.turn = RED
        self.valid_moves = {}
        self.initialize_board()

    def initialize_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row][col] = Piece(row, col, WHITE)
                    elif row > 4:
                        self.board[row][col] = Piece(row, col, RED)

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, BOARD_SIZE), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, BOARD_SIZE), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current is None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, BOARD_SIZE)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= BOARD_SIZE:
                break

            current = self.board[r][right]
            if current is None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, BOARD_SIZE)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

                if self.selected_piece:
                    move = None
                    if (row, col) in self.valid_moves:
                        self.move(self.selected_piece, row, col)
                    self.selected_piece = None
                    self.valid_moves = {}
                else:
                    piece = self.board[row][col]
                    if piece is not None and piece.color == self.turn:
                        self.selected_piece = piece
                        self.valid_moves = self.get_valid_moves(piece)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
        return True

    def move(self, piece, row, col):
        self.board[piece.row][piece.col] = None
        self.board[row][col] = piece
        piece.row = row
        piece.col = col
        piece.calculate_position()

        if row == BOARD_SIZE - 1 or row == 0:
            piece.make_king()

        # Remove captured pieces
        if (row, col) in self.valid_moves:
            for captured in self.valid_moves[(row, col)]:
                self.board[captured.row][captured.col] = None

        self.turn = WHITE if self.turn == RED else RED

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_board()
        self.draw_pieces()
        pygame.display.flip()

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color,
                               (col * SQUARE_SIZE, row * SQUARE_SIZE,
                                SQUARE_SIZE, SQUARE_SIZE))

                if self.selected_piece and (row, col) in self.valid_moves:
                    pygame.draw.circle(self.screen, YELLOW,
                                    (col * SQUARE_SIZE + SQUARE_SIZE//2,
                                     row * SQUARE_SIZE + SQUARE_SIZE//2),
                                    15)

    def draw_pieces(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece is not None:
                    radius = SQUARE_SIZE//2 - 10
                    pygame.draw.circle(self.screen, piece.color,
                                    (piece.x, piece.y), radius)
                    if piece.king:
                        pygame.draw.circle(self.screen, YELLOW,
                                        (piece.x, piece.y), radius//2)

    def run(self):
        while True:
            if not self.handle_input():
                break
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = CheckersGame()
    game.run()
