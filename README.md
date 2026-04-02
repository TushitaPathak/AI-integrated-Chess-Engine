# Chess Engine with Alpha-Beta Pruning

A chess engine implementation using Flask and python-chess, featuring minimax search with alpha-beta pruning, quiescence search, and piece-square table evaluation. Built as a college project demonstrating AI game-playing algorithms.

## Features

- **AI Opponent**: Computer opponent using minimax algorithm with alpha-beta pruning (depth 2)
- **Quiescence Search**: Evaluates capture sequences to avoid the horizon effect
- **Position Evaluation**: 
  - Material balance with standard piece values (pawn=100, knight=320, bishop=330, rook=500, queen=900)
  - Piece-square tables for positional play
  - Endgame-specific king evaluation
  - MVV-LVA (Most Valuable Victim - Least Valuable Aggressor) move ordering
- **Dual Interface**:
  - Web interface (Flask-based)
  - Command-line interface for terminal play

## Technical Details

### Search Algorithms
- **Minimax**: Decision rule for minimizing potential loss
- **Alpha-Beta Pruning**: Optimizes search by eliminating branches that cannot influence the final decision
- **Quiescence Search**: Prevents the horizon effect by searching capture sequences until a "quiet" position is reached

### Evaluation Function
The evaluation considers:
- Material balance
- Piece positions via piece-square tables
- Endgame detection for specialized king evaluation
- Checkmate/stalemate detection

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup
```bash

pip install flask python-chess
```

## Usage

### Web Interface (Default)
```bash
python chess_engine.py
 Open http://localhost:5000 in your browser
```

### Command-Line Interface
```bash
python chess_engine.py cli
```

In CLI mode:
- You play as White (enter moves in algebraic notation)
- Engine plays as Black
- Examples: `e4`, `Nf3`, `O-O`, `exd5`

## Project Structure

```
chess_engine/
├── chess_engine.py     # Main application file
├── README.md           # This file
└── requirements.txt    # Dependencies (flask, python-chess)
```

## Algorithm Highlights

### 1. **Move Ordering with MVV-LVA**
   - Captures are prioritized to improve alpha-beta pruning efficiency
   - Check moves are given bonus to search promising lines first

### 2. **Piece-Square Tables**
   - Pre-computed positional values for each piece type
   - Adapts to endgame phase (king becomes more active)

### 3. **Endgame Detection**
   - Detects positions with few major pieces
   - Switches to endgame-specific king evaluation

## Performance Notes

- **Depth 2**: Fast response (~0.1-0.5 seconds per move)
- **Depth 3**: Stronger play but may take 2-5 seconds
- **Depth 4+**: Not recommended without further optimizations

## Future Improvements

- Iterative deepening
- Transposition table
- Opening book implementation
- Parallel search
- Increased search depth with better pruning
- Zobrist hashing

## Acknowledgments

- Built with [python-chess](https://python-chess.readthedocs.io/) library
- Flask framework for web interface
- Chess piece icons via Unicode chess symbols


