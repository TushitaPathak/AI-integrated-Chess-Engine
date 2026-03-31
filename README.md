# Chess Engine - Minimax AI with Flask Interface

A sophisticated chess engine that combines classical AI search algorithms with an interactive web interface. This engine features a Minimax-based AI with Alpha-Beta pruning, quiescence search, and a comprehensive positional evaluation system.

##  Features

- **Full Chess Rules**: Complete implementation of chess rules using `python-chess` library
- **AI Opponent**: Intelligent computer opponent with adjustable difficulty through search depth
- **Interactive Web Interface**: Clean, responsive chessboard with move input and game history
- **Advanced Search Algorithms**:
  - Minimax decision tree search
  - Alpha-Beta pruning for efficiency
  - Quiescence search to prevent horizon effect
- **Sophisticated Evaluation**:
  - Material valuation (centipawn-based)
  - Piece-Square Tables for positional understanding
  - Dynamic endgame evaluation
- **Performance Optimizations**: MVV-LVA move ordering for improved search efficiency

##  Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/chess-engine.git
cd chess-engine
```

2. **Install dependencies**
```bash
pip install flask python-chess
```

3. **Run the application**
```bash
python chess_engine.py
```

4. **Open your browser**
Navigate to `http://localhost:5000`

##  How to Play

1. **Make a Move**: Enter moves in algebraic notation (e.g., `e4`, `Nf3`, `O-O`) in the input box and click "Play"
2. **View AI Moves**: The engine will respond with its move, displayed in the Engine panel
3. **Track History**: All moves are recorded in the Moves panel
4. **New Game**: Click "↺ new game" to reset the board

### Move Notation Examples
- **Pawn moves**: `e4`, `d5`
- **Piece moves**: `Nf3` (knight), `Bc4` (bishop)
- **Captures**: `Nxe5`, `dxc6`
- **Castling**: `O-O` (kingside), `O-O-O` (queenside)

##  System Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   Frontend      │         │    Backend      │
│   (Browser)     │◄───────►│   (Flask)       │
│                 │  HTTP   │                 │
│ • Chessboard    │  JSON   │ • Game State    │
│ • Move Input    │         │ • AI Engine     │
│ • Game History  │         │ • Move Logic    │
└─────────────────┘         └─────────────────┘
```

- **Backend**: Flask server maintaining game state and executing AI computations
- **Frontend**: JavaScript client with dynamic board rendering and move validation
- **API**: REST endpoints for moves, resets, and state synchronization

##  AI Technical Deep Dive

### Search Algorithms

#### Minimax with Alpha-Beta Pruning
The engine explores the game tree using the Minimax algorithm, assuming optimal play from both sides. Alpha-Beta pruning dramatically reduces search space by eliminating branches that cannot influence the final decision.

```python
# Simplified example of alpha-beta pruning
def minimax(board, depth, alpha, beta, is_maximizing):
    if depth == 0:
        return evaluate(board)
    
    if is_maximizing:
        for move in ordered_moves:
            board.push(move)
            value = minimax(board, depth-1, alpha, beta, False)
            board.pop()
            alpha = max(alpha, value)
            if beta <= alpha: break  # Beta cutoff
        return alpha
    # ... minimizing logic
```

#### Quiescence Search
Prevents the horizon effect by continuing to search capture sequences until a quiet position is reached.

### Evaluation Function

The engine evaluates positions using a combination of:
- **Material Balance**: Traditional piece values (Pawn=100, Knight=320, etc.)
- **Positional Tables**: Pre-computed 8×8 grids rewarding piece placement
- **Dynamic King Safety**: Different evaluation for middlegame vs. endgame

### Performance Optimizations

**MVV-LVA Move Ordering**: Prioritizes promising moves (captures, checks) to maximize pruning efficiency.

##  Technical Specifications

|     Component   | Technology              |
| Backend         | Python 3, Flask         | 
| Chess Logic     | python-chess library    |
| Frontend        | HTML5, CSS3, JavaScript |
| Board Rendering | Custom CSS Grid         |
| API Protocol    | RESTful JSON            | 

##  Configuration

Adjust AI strength by modifying the search depth in `best()` function:
```python
# In move() endpoint
m = best(b, depth=2)  # Faster, less accurate
m = best(b, depth=3)  # Stronger, slower
```

##  Future Enhancements

### Machine Learning Integration
- **Neural Network Evaluation**: Replace heuristic evaluation with CNN-based position evaluation
- **Policy Networks**: Train move probability distributions to improve move ordering
- **Self-Play Training**: Implement reinforcement learning similar to AlphaZero






