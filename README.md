
# Othello AI Project

This repository contains an implementation of the classic board game Othello (also known as Reversi). The script runs in a headless mode, simulating games between two AI players based on a `.txt` file, optimizing gameplay through advanced techniques for move selection and state evaluation.

## Features
- **AI-based Move Decision**: The game is played by two AI players, determining their moves based on a given strategy for each player.
- **Simulation Mode**: Games are played sequentially based on inputs from a `.txt` file, simulating real-time decision-making between AI players.
- **Customizable Game Parameters**: Users can define:
  - Starting token (`x` or `o`).
  - Number of games to simulate.

## How to Run

\`\`\`bash
python3 othello6.py x 4
\`\`\`

- The first argument is the starting token (`x` or `o`).
- The second argument is the number of games to simulate.

The script will read input files containing predefined board configurations and play out the games accordingly.

## Testing with miniMod.py

\`\`\`bash
python3 minMod.py othello6.py x 4
\`\`\`

- Arguments to the script are:
- Othello script file, token to start first game with, # of games
- Defaults are: 'othello6.py, 'x', 1

## Optimization Techniques

### 1. **Minimax Algorithm with Alpha-Beta Pruning**
   The decision-making of each AI player is based on the Minimax algorithm, which is enhanced with Alpha-Beta pruning. This pruning reduces the number of nodes evaluated in the decision tree by eliminating branches that don't need exploration, leading to faster decision-making and reducing computation time.

### 2. **Heuristic Evaluation Function**
   A custom heuristic function is used to evaluate board states. The evaluation is based on:
   - Mobility: The number of possible moves for the current player.
   - Stability: The number of stable discs, which cannot be flipped in subsequent turns.
   - Corner Occupancy: Prioritizes moves that capture corner positions, leading to more stable discs.
   
   These factors ensure that the AI makes smart decisions, balancing short-term gains with long-term strategy.

### 3. **Preprocessing for Efficiency**
   During the game's setup phase, the board positions are preprocessed to identify critical areas (such as edges and corners) that frequently impact the game's outcome. This helps the AI focus on important regions of the board, further speeding up move evaluation.

### 4. **Dynamic Depth Adjustment**
   The search depth of the Minimax algorithm is dynamically adjusted based on the game state. As the game progresses and the number of available moves decreases, the AI deepens its search to make more informed decisions. This allows for deeper analysis in endgames without sacrificing performance in earlier phases.

## Future Improvements
- **Multiplayer Support**: Adding a real-time multiplayer feature where users can play against the AI.
- **Improved Heuristics**: Refining the evaluation function for even more sophisticated move selections.
- **Parallelization**: Implementing parallel processing to further optimize move evaluation and simulation speed.


