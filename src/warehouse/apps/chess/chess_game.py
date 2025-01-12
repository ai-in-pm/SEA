import pygame
import sys
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

class PieceType(Enum):
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6

class Piece:
    def __init__(self, piece_type: PieceType, is_white: bool):
        self.piece_type = piece_type
        self.is_white = is_white
        self.has_moved = False

class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Chess')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.selected_piece = None
        self.selected_pos = None
        self.current_player = True  # True for white, False for black
        self.game_over = False
        self.initialize_board()

    def initialize_board(self):
        # Initialize pawns
        for col in range(BOARD_SIZE):
            self.board[1][col] = Piece(PieceType.PAWN, False)
            self.board[6][col] = Piece(PieceType.PAWN, True)

        # Initialize other pieces
        piece_order = [
            PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
            PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK
        ]

        for col in range(BOARD_SIZE):
            self.board[0][col] = Piece(piece_order[col], False)
            self.board[7][col] = Piece(piece_order[col], True)

    def get_piece_symbol(self, piece: Piece) -> str:
        symbols = {
            PieceType.PAWN: '♟',
            PieceType.ROOK: '♜',
            PieceType.KNIGHT: '♞',
            PieceType.BISHOP: '♝',
            PieceType.QUEEN: '♛',
            PieceType.KING: '♚'
        }
        return symbols[piece.piece_type]

    def is_valid_move(self, start_pos, end_pos) -> bool:
        # Basic move validation (to be expanded)
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        piece = self.board[start_row][start_col]

        if not piece or piece.is_white != self.current_player:
            return False

        # Check if destination has friendly piece
        if self.board[end_row][end_col] and self.board[end_row][end_col].is_white == piece.is_white:
            return False

        # Implement basic movement rules for each piece type
        if piece.piece_type == PieceType.PAWN:
            direction = -1 if piece.is_white else 1
            if start_col == end_col:  # Moving forward
                if end_row == start_row + direction:
                    return not self.board[end_row][end_col]
                if not piece.has_moved and end_row == start_row + 2 * direction:
                    return not self.board[end_row][end_col] and not self.board[start_row + direction][start_col]
            elif abs(start_col - end_col) == 1 and end_row == start_row + direction:
                return self.board[end_row][end_col] and self.board[end_row][end_col].is_white != piece.is_white

        return True  # Simplified for demo purposes

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                x, y = event.pos
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE

                if self.selected_piece:
                    if self.is_valid_move(self.selected_pos, (row, col)):
                        # Make the move
                        self.board[row][col] = self.selected_piece
                        self.board[self.selected_pos[0]][self.selected_pos[1]] = None
                        self.selected_piece.has_moved = True
                        self.current_player = not self.current_player
                    self.selected_piece = None
                    self.selected_pos = None
                else:
                    piece = self.board[row][col]
                    if piece and piece.is_white == self.current_player:
                        self.selected_piece = piece
                        self.selected_pos = (row, col)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
        return True

    def draw(self):
        self.screen.fill(WHITE)

        # Draw board
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = WHITE if (row + col) % 2 == 0 else GRAY
                if self.selected_pos == (row, col):
                    color = YELLOW
                pygame.draw.rect(self.screen, color,
                               (col * SQUARE_SIZE, row * SQUARE_SIZE,
                                SQUARE_SIZE, SQUARE_SIZE))

                piece = self.board[row][col]
                if piece:
                    color = WHITE if piece.is_white else BLACK
                    text = self.font.render(self.get_piece_symbol(piece), True, color)
                    text_rect = text.get_rect(center=(
                        col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2
                    ))
                    self.screen.blit(text, text_rect)

        pygame.display.flip()

    def run(self):
        while True:
            if not self.handle_input():
                break
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = ChessGame()
    game.run()
