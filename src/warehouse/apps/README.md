# Game Warehouse

A collection of classic games implemented in Python using Pygame.

## Games Available

1. **Snake Game**
   - Classic snake game with score tracking
   - Controls: Arrow keys to move, R to restart
   - Features: Growing snake, food collection, collision detection

2. **Tic Tac Toe**
   - Two-player tic tac toe game
   - Controls: Mouse click to place X/O, R to restart
   - Features: Win detection, turn tracking

3. **Chess**
   - Two-player chess game
   - Controls: Mouse click to select and move pieces, R to restart
   - Features: Basic piece movement, turn system

4. **Checkers**
   - Two-player checkers game
   - Controls: Mouse click to select and move pieces, R to restart
   - Features: Piece capture, king promotion

5. **Poker**
   - Multiplayer poker game with AI opponents
   - Controls: C to call, F to fold, B to bet, R to restart
   - Features: Card dealing, betting system, AI opponents

6. **Solitaire**
   - Single-player solitaire card game
   - Controls: Mouse click to move cards, Space to draw from deck, R to restart
   - Features: Card stacking, suit foundations, multiple tableau piles

## Requirements

```bash
pip install pygame
```

## Running the Games

Each game can be run independently. Navigate to the game directory and run the Python file:

```bash
# For Snake Game
python snake/snake_game.py

# For Tic Tac Toe
python tictactoe/tictactoe_game.py

# For Chess
python chess/chess_game.py

# For Checkers
python checkers/checkers_game.py

# For Poker
python poker/poker_game.py

# For Solitaire
python solitaire/solitaire_game.py
```

## Common Features

- All games use Pygame for graphics
- Consistent control scheme (R to restart)
- Score tracking where applicable
- Clean, modular code structure
- Error handling and game state management

## Game Customization

Each game can be customized by modifying constants at the top of their respective files:

- Window size
- Colors
- Game speed
- Difficulty levels (where applicable)

## Contributing

Feel free to contribute by:
1. Adding new games
2. Improving existing games
3. Adding features
4. Fixing bugs

## License

MIT License - See LICENSE file for details
