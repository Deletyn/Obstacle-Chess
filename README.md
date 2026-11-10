# Obstacle Chess

A Python command-line chess project that extends a traditional chess board with additional board elements and movement challenges.

## Project files

- `obstacleChess.py` - main program; reads a board file, validates it, processes moves when a move file is supplied, and writes the resulting board.
- `move_piece.py` - handles piece movement.
- `piece_check.py` - contains movement and check-related logic.
- `validate.py` - checks board setup and game-state rules.
- `002665_random.board` - sample board file.

## Requirements

- Python 3
- No third-party Python packages are required by the source files in this project.

## Running the project

Open a terminal in this folder.

To validate a board and write the result to an output file:

```bash
python obstacleChess.py 002665_random.board output.board
```

To process moves, provide a move file as the third argument:

```bash
python obstacleChess.py 002665_random.board output.board moves.txt
```

The move file should follow the move notation expected by the program.

## Notes

This is a command-line project. The sample `.board` file is included so the project has an input file to start testing with. The original Python source files have been retained as supplied.
