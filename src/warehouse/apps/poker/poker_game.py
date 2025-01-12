import pygame
import random
import sys
from enum import Enum
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (1200, 800)
CARD_SIZE = (100, 140)
CARD_SPACING = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
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

class Player:
    def __init__(self, name: str, chips: int = 1000):
        self.name = name
        self.chips = chips
        self.hand: List[Card] = []
        self.bet = 0
        self.folded = False

class PokerGame:
    def __init__(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('Poker')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.deck = self.create_deck()
        self.shuffle_deck()
        self.players = [
            Player("Player", 1000),
            Player("CPU 1", 1000),
            Player("CPU 2", 1000),
            Player("CPU 3", 1000)
        ]
        self.community_cards: List[Card] = []
        self.pot = 0
        self.current_player = 0
        self.current_bet = 0
        self.game_phase = "pre-flop"  # pre-flop, flop, turn, river, showdown
        self.deal_initial_cards()

    def create_deck(self) -> List[Card]:
        deck = []
        for suit in Suit:
            for value in range(1, 14):
                deck.append(Card(value, suit))
        return deck

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_initial_cards(self):
        for _ in range(2):
            for player in self.players:
                card = self.deck.pop()
                card.face_up = player == self.players[0]  # Only show human player's cards
                player.hand.append(card)

    def deal_community_cards(self, count: int):
        for _ in range(count):
            card = self.deck.pop()
            card.face_up = True
            self.community_cards.append(card)

    def draw_card(self, card: Card, position: Tuple[int, int]):
        x, y = position
        pygame.draw.rect(self.screen, WHITE, (x, y, CARD_SIZE[0], CARD_SIZE[1]))
        pygame.draw.rect(self.screen, BLACK, (x, y, CARD_SIZE[0], CARD_SIZE[1]), 2)

        if card.face_up:
            # Draw rank
            rank_text = self.font.render(card.rank_str, True, card.color)
            self.screen.blit(rank_text, (x + 5, y + 5))
            
            # Draw suit
            suit_text = self.font.render(card.suit.value, True, card.color)
            self.screen.blit(suit_text, (x + 5, y + 25))
        else:
            # Draw card back
            pygame.draw.rect(self.screen, RED, (x + 5, y + 5,
                                              CARD_SIZE[0] - 10, CARD_SIZE[1] - 10))

    def draw_player(self, player: Player, position: Tuple[int, int]):
        x, y = position
        # Draw name and chips
        name_text = self.font.render(f"{player.name}: ${player.chips}", True, WHITE)
        self.screen.blit(name_text, (x, y - 30))

        # Draw cards
        for i, card in enumerate(player.hand):
            self.draw_card(card, (x + i * (CARD_SIZE[0] + CARD_SPACING), y))

        # Draw current bet
        if player.bet > 0:
            bet_text = self.font.render(f"Bet: ${player.bet}", True, WHITE)
            self.screen.blit(bet_text, (x, y + CARD_SIZE[1] + 10))

    def draw_community_cards(self):
        x = (WINDOW_SIZE[0] - (len(self.community_cards) * (CARD_SIZE[0] + CARD_SPACING))) // 2
        y = (WINDOW_SIZE[1] - CARD_SIZE[1]) // 2
        
        for card in self.community_cards:
            self.draw_card(card, (x, y))
            x += CARD_SIZE[0] + CARD_SPACING

    def draw_pot(self):
        pot_text = self.font.render(f"Pot: ${self.pot}", True, WHITE)
        self.screen.blit(pot_text, (WINDOW_SIZE[0] // 2 - 50, 20))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_c and self.current_player == 0:
                    self.handle_player_action("call")
                elif event.key == pygame.K_f and self.current_player == 0:
                    self.handle_player_action("fold")
                elif event.key == pygame.K_b and self.current_player == 0:
                    self.handle_player_action("bet")
        return True

    def handle_player_action(self, action: str):
        player = self.players[self.current_player]
        
        if action == "fold":
            player.folded = True
        elif action == "call":
            amount = self.current_bet - player.bet
            if amount <= player.chips:
                player.chips -= amount
                player.bet += amount
                self.pot += amount
        elif action == "bet":
            # Simple betting for demo
            amount = 50
            if amount <= player.chips:
                player.chips -= amount
                player.bet += amount
                self.pot += amount
                self.current_bet = player.bet

        # Move to next player
        self.current_player = (self.current_player + 1) % len(self.players)
        
        # AI players make simple decisions
        while self.current_player != 0 and not self.players[self.current_player].folded:
            self.handle_ai_action()
            self.current_player = (self.current_player + 1) % len(self.players)

        # Check if round is complete
        if self.all_bets_equal():
            self.advance_game_phase()

    def handle_ai_action(self):
        player = self.players[self.current_player]
        # Simple AI: randomly call or fold
        if random.random() > 0.3:
            self.handle_player_action("call")
        else:
            self.handle_player_action("fold")

    def all_bets_equal(self) -> bool:
        return all(player.bet == self.current_bet or player.folded
                  for player in self.players)

    def advance_game_phase(self):
        if self.game_phase == "pre-flop":
            self.game_phase = "flop"
            self.deal_community_cards(3)
        elif self.game_phase == "flop":
            self.game_phase = "turn"
            self.deal_community_cards(1)
        elif self.game_phase == "turn":
            self.game_phase = "river"
            self.deal_community_cards(1)
        elif self.game_phase == "river":
            self.game_phase = "showdown"
            self.handle_showdown()

    def handle_showdown(self):
        # Simplified showdown for demo
        # In a real implementation, evaluate poker hands
        for player in self.players:
            if not player.folded:
                for card in player.hand:
                    card.face_up = True

    def draw(self):
        self.screen.fill(GREEN)
        
        # Draw community cards
        self.draw_community_cards()
        
        # Draw pot
        self.draw_pot()
        
        # Draw players
        positions = [
            (50, WINDOW_SIZE[1] - 200),  # Bottom (Player)
            (50, 50),                    # Top left (CPU 1)
            (WINDOW_SIZE[0] - 300, 50),  # Top right (CPU 2)
            (WINDOW_SIZE[0] - 300, WINDOW_SIZE[1] - 200)  # Bottom right (CPU 3)
        ]
        
        for player, pos in zip(self.players, positions):
            self.draw_player(player, pos)

        # Draw current phase
        phase_text = self.font.render(f"Phase: {self.game_phase}", True, WHITE)
        self.screen.blit(phase_text, (20, 20))

        # Draw controls for human player
        if self.current_player == 0 and not self.game_phase == "showdown":
            controls_text = self.font.render("Controls: (C)all, (F)old, (B)et", True, WHITE)
            self.screen.blit(controls_text, (20, WINDOW_SIZE[1] - 40))

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
    game = PokerGame()
    game.run()
