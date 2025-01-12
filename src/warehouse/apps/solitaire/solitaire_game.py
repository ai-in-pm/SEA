import pygame
import random
import sys
from enum import Enum
from typing import List, Optional, Tuple

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (1200, 800)
CARD_SIZE = (100, 140)
CARD_SPACING = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

class Card:
    def __init__(self, value: int, suit: Suit):
        self.value = value
        self.suit = suit
        self.face_up = False
        self.rect = pygame.Rect(0, 0, CARD_SIZE[0], CARD_SIZE[1])

    @property
    def color(self):
        return RED if self.suit in [Suit.HEARTS, Suit.DIAMONDS] else BLACK

    @property
    def rank_str(self):
        if self.value == 1:
            return 'A'
        elif self.value == 11:
            return 'J'
        elif self.value == 12:
            return 'Q'
        elif self.value == 13:
            return 'K'
        return str(self.value)

class Pile:
    def __init__(self, x: int, y: int):
        self.cards: List[Card] = []
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, CARD_SIZE[0], CARD_SIZE[1])

    def add_card(self, card: Card):
        self.cards.append(card)
        self.update_card_positions()

    def remove_card(self) -> Optional[Card]:
        if self.cards:
            card = self.cards.pop()
            self.update_card_positions()
            return card
        return None

    def update_card_positions(self):
        for i, card in enumerate(self.cards):
            card.rect.x = self.x
            card.rect.y = self.y + i * 30

class SolitaireGame:
    def __init__(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('Solitaire')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.deck = self.create_deck()
        self.shuffle_deck()
        
        # Initialize foundation piles (for completed suits)
        self.foundations = [Pile(250 + i * (CARD_SIZE[0] + 20), 50) for i in range(4)]
        
        # Initialize tableau piles
        self.tableau = [Pile(50 + i * (CARD_SIZE[0] + 20), 250) for i in range(7)]
        self.deal_initial_cards()
        
        # Initialize stock and waste piles
        self.stock = Pile(50, 50)
        self.waste = Pile(150, 50)
        
        # Add remaining cards to stock
        for card in self.deck:
            self.stock.add_card(card)

        self.selected_cards = []
        self.selected_pile = None

    def create_deck(self) -> List[Card]:
        deck = []
        for suit in Suit:
            for value in range(1, 14):
                deck.append(Card(value, suit))
        return deck

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_initial_cards(self):
        for i, pile in enumerate(self.tableau):
            for j in range(i + 1):
                card = self.deck.pop()
                card.face_up = j == i  # Only flip the top card
                pile.add_card(card)

    def draw_card(self, card: Card, position: Tuple[int, int]):
        x, y = position
        card.rect.x = x
        card.rect.y = y
        
        pygame.draw.rect(self.screen, WHITE, card.rect)
        pygame.draw.rect(self.screen, BLACK, card.rect, 2)

        if card.face_up:
            # Draw rank
            rank_text = self.font.render(card.rank_str, True, card.color)
            self.screen.blit(rank_text, (x + 5, y + 5))
            
            # Draw suit
            suit_text = self.font.render(card.suit.value, True, card.color)
            self.screen.blit(suit_text, (x + 5, y + 25))
        else:
            # Draw card back
            pygame.draw.rect(self.screen, RED,
                           (x + 5, y + 5, CARD_SIZE[0] - 10, CARD_SIZE[1] - 10))

    def draw_pile(self, pile: Pile):
        if not pile.cards:
            pygame.draw.rect(self.screen, BLACK, pile.rect, 2)
        else:
            for i, card in enumerate(pile.cards):
                self.draw_card(card, (pile.x, pile.y + i * 30))

    def can_place_on_foundation(self, card: Card, foundation: Pile) -> bool:
        if not foundation.cards:
            return card.value == 1
        top_card = foundation.cards[-1]
        return (card.suit == top_card.suit and
                card.value == top_card.value + 1)

    def can_place_on_tableau(self, card: Card, tableau: Pile) -> bool:
        if not tableau.cards:
            return card.value == 13  # King
        top_card = tableau.cards[-1]
        return (card.color != top_card.color and
                card.value == top_card.value - 1)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_SPACE:
                    self.draw_from_stock()
        return True

    def handle_click(self, pos):
        # Check stock pile
        if self.stock.rect.collidepoint(pos):
            self.draw_from_stock()
            return

        # Check tableau piles
        for pile in self.tableau + self.foundations + [self.waste]:
            if pile.cards:
                for i, card in enumerate(pile.cards):
                    if card.rect.collidepoint(pos) and card.face_up:
                        if self.selected_cards:
                            # Try to place selected cards
                            if pile in self.foundations:
                                if (len(self.selected_cards) == 1 and
                                    self.can_place_on_foundation(self.selected_cards[0], pile)):
                                    pile.add_card(self.selected_pile.remove_card())
                            elif pile in self.tableau:
                                if self.can_place_on_tableau(self.selected_cards[0], pile):
                                    for card in self.selected_cards:
                                        pile.add_card(self.selected_pile.remove_card())
                            self.selected_cards = []
                            self.selected_pile = None
                        else:
                            # Select cards
                            self.selected_cards = pile.cards[i:]
                            self.selected_pile = pile
                        return

    def draw_from_stock(self):
        if not self.stock.cards:
            # Reset stock from waste
            while self.waste.cards:
                card = self.waste.remove_card()
                card.face_up = False
                self.stock.add_card(card)
        elif self.stock.cards:
            card = self.stock.remove_card()
            card.face_up = True
            self.waste.add_card(card)

    def draw(self):
        self.screen.fill(GREEN)

        # Draw stock and waste piles
        self.draw_pile(self.stock)
        self.draw_pile(self.waste)

        # Draw foundation piles
        for pile in self.foundations:
            self.draw_pile(pile)

        # Draw tableau piles
        for pile in self.tableau:
            self.draw_pile(pile)

        # Draw selected cards with highlight
        if self.selected_cards:
            pygame.draw.rect(self.screen, (255, 255, 0),
                           self.selected_cards[0].rect, 3)

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
    game = SolitaireGame()
    game.run()
